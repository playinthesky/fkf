# 아키텍처

> Version 0.1.0 | 2026-06-04

---

## 1. 시스템 구성도

```
                    ┌─────────────────────┐
                    │      Slack Workspace │
                    │  ┌────────────────┐  │
                    │  │ /실행계획서      │  │
                    │  │ + 스레드 대화    │  │
                    │  │ + 파일 첨부      │  │
                    │  └────────┬───────┘  │
                    └───────────┼──────────┘
                                │ Events API + Slash Commands
                                ▼
┌──────────────────────────────────────────────────────────┐
│              실행계획서 봇 (Render 호스팅)                  │
│              ─────────────────────────                    │
│                                                          │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Slack Bolt App (app.py)                           │  │
│  │  ─────────────────────                              │  │
│  │  • /실행계획서 핸들러                                  │  │
│  │  • file_shared 이벤트 핸들러                          │  │
│  │  • message 이벤트 핸들러 (스레드 멀티턴)               │  │
│  │  • interactive components (Block Kit 버튼)           │  │
│  └────────────────┬───────────────────────────────────┘  │
│                   │                                       │
│       ┌───────────┼───────────┐                          │
│       ▼           ▼           ▼                          │
│  ┌─────────┐ ┌──────────┐ ┌───────────────────┐          │
│  │ Session │ │  File    │ │  Consultation     │          │
│  │ Store   │ │ Extract  │ │  Engine           │          │
│  │ (Redis) │ │  Worker  │ │  (Claude API)     │          │
│  │         │ │          │ │                   │          │
│  │ thread_ │ │ PDF/HWP/ │ │  • 시스템 프롬프트  │          │
│  │ ts ──▶  │ │ HWPX/    │ │  • 프롬프트 캐싱   │          │
│  │ 상태    │ │ DOCX/    │ │  • Tool use       │          │
│  │         │ │ 이미지    │ │                   │          │
│  └─────────┘ └──────────┘ └─────────┬─────────┘          │
│                                     │                     │
│                                     │ tools               │
│            ┌────────────────────────┼────────────────┐   │
│            ▼                        ▼                ▼   │
│    ┌──────────────┐         ┌─────────────┐  ┌──────────┐│
│    │ GitHub Reader│         │ Drive       │  │Doc Builder││
│    │ (fkf 표준 자료)│         │ Connector   │  │           ││
│    │              │         │             │  │ PPT      ││
│    │ • 숙의마스터  │         │ • 최근 파일  │  │ HWPX     ││
│    │ • 템플릿      │         │ • 파일 추출  │  │           ││
│    │ • CLAUDE.md  │         │             │  │           ││
│    └──────────────┘         └─────────────┘  └─────┬────┘│
│                                                    │     │
└────────────────────────────────────────────────────┼─────┘
                                                    │
                ┌───────────────────────────────────┤
                ▼                                   ▼
        ┌──────────────┐                 ┌──────────────────┐
        │  Slack       │                 │  GitHub          │
        │  files.upload│                 │  fkf/projects/   │
        │  (PPT/HWPX)  │                 │  자동 커밋·푸시   │
        └──────────────┘                 └──────────────────┘
```

---

## 2. 데이터 흐름

### 2.1 신규 상담 시작
```
1. 직원: /실행계획서 입력
2. Slack → 봇: command 이벤트
3. 봇: 스레드 생성 (thread_ts 발급)
4. 봇: Session Store에 빈 세션 생성 {thread_ts: {state: "awaiting_files", materials: []}}
5. 봇 → Slack: 안내 메시지 게시 (파일 요청 + Drive 픽업 옵션)
```

### 2.2 파일 인입
```
1. 직원: 파일 업로드 (스레드 내)
2. Slack → 봇: file_shared 이벤트
3. 봇: File Extract Worker 호출 → 텍스트 추출
4. 봇: Session Store 업데이트 {materials: [...추출된 텍스트]}
5. 봇 → Claude API: 자료 분석 + 부족한 정보 질문 생성
6. 봇 → Slack: 분석 요약 + 질문 게시
```

### 2.3 멀티턴 상담
```
1. 직원: 스레드에 답변 메시지
2. Slack → 봇: message 이벤트 (thread_ts 포함)
3. 봇: Session Store에서 이전 상태 로드
4. 봇 → Claude API: 전체 대화 + 자료 컨텍스트 (프롬프트 캐싱)
5. 봇 → Slack: 다음 응답 게시
6. 반복 — 사용자가 "확정"·"진행" 등 트리거 발화까지
```

### 2.4 산출물 생성
```
1. 봇: 확정 트리거 감지
2. 봇 → Claude API: 최종 계획 JSON 생성 (트랙별 + 일정표)
3. 봇 → Doc Builder:
   3a. python-pptx로 스픽스형 PPT 생성
   3b. Pandoc → 한컴 변환으로 HWPX 생성
4. 봇 → Slack files.upload: PPT/HWPX 게시
5. 봇 → GitHub: projects/[이름]/ 폴더에 자동 커밋·푸시
6. 봇 → Slack: 완료 메시지 + 레포 링크
```

---

## 3. 세션 상태 모델

```python
{
  "thread_ts": "1717481234.123456",
  "channel": "C012345",
  "user": "U012345",
  "state": "drafting",  # awaiting_files | analyzing | clarifying | drafting | confirmed | done
  "project_name": "2026-서울교육공론화",
  "materials": [
    {
      "source": "slack",  # slack | drive
      "filename": "제안서.pdf",
      "file_id": "F012345",
      "extracted_text": "...",
      "metadata": {...}
    }
  ],
  "extracted_info": {
    "project_name": "...",
    "period": "...",
    "budget": "...",
    "issues": [...]  # 기술협상 등에서 추출
  },
  "clarifications": {
    "kickoff_date": "2026-06-08",
    "deliberation_rounds": 1,
    "counterparts": ["재은", "본인"]
  },
  "draft_version": 1,
  "conversation_history": [...],
  "created_at": "...",
  "updated_at": "..."
}
```

---

## 4. 표준 컨텍스트 (Claude 프롬프트 캐싱)

매 요청마다 다음을 캐시 가능한 청크로 prepend:

```
<system>
[CLAUDE.md 전체]
</system>

<context_cache>
[숙의프로젝트_마스터_v0.1.0.md]
[templates/숙의프로젝트_템플릿_v1.0.0.md]
[templates/슬라이드_디자인_지침서_v0.1.0.md]
[templates/산출내역서_템플릿_v1.0.0.md]
[automation/실행계획서-봇/SPEC.md]
[automation/실행계획서-봇/docs/워크플로우-매핑.md]
</context_cache>

<conversation>
[직원-봇 멀티턴 대화]
</conversation>

<materials>
[추출된 입력 자료 텍스트]
</materials>
```

이 구조로 두면 같은 세션 내 반복 호출 시 캐시 히트가 잘 나서 비용·지연 모두 절감.

---

## 5. 보안·권한

| 항목 | 정책 |
|------|------|
| Slack 봇 권한 스코프 | `commands`, `chat:write`, `files:read`, `files:write`, `channels:history`, `groups:history` |
| Drive 권한 | Service Account → 특정 폴더만 위임 또는 OAuth (`drive.readonly`, 결과 저장 시 `drive.file`) |
| GitHub 권한 | Fine-grained PAT → `fkf` 레포 contents:write만 |
| Anthropic 키 | Render 환경변수로만 (코드에 직접 노출 ❌) |
| 입력 자료 보존 | Redis는 30일 후 자동 삭제, GitHub 커밋은 영구 |

---

## 6. 실패 처리

| 실패 | 처리 |
|------|------|
| PDF 텍스트 추출 0자 (이미지 PDF) | OCR 폴백 → 그래도 실패 시 사용자에게 HWP 원본 요청 |
| Drive 파일 권한 없음 | 권한 부여 안내 메시지 |
| Claude API 오류 | 재시도 3회 (지수 백오프) → 실패 시 사용자에게 알림 |
| PPT 생성 오류 | 마크다운 결과로 폴백 |
| GitHub 푸시 실패 | 로컬 임시 보관 후 재시도 |

---

## 7. 향후 확장

- **다른 산출물 자동화**: `/산출내역서`, `/홍보계획`, `/안전점검` 등 동일 패턴으로 확장
- **세션 공유**: 동료가 같은 스레드에 참여해 협업 상담
- **버전 비교**: 같은 프로젝트 v1 ↔ v2 자동 diff
- **Dashboard**: Render 외 별도 웹 UI로 모든 상담 세션 조회
