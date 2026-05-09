# FKF 프로젝트 설정

## ⚠️ 세션 시작 시 필수 확인

1. **Google Drive MCP 연결 확인** - `mcp__gdrive__*` 도구 사용 가능한지 확인
2. 안 되면 → `.mcp.json` 설정 확인 및 MCP 서버 활성화

---

## 현재 진행 중인 작업: 2026 제주DA 파트너스 원탁회의

### 사업 개요
- **사업명**: 2026 제주DA 파트너스 원탁회의 (메인 타이틀)
- **부제**: 제주DA 앱 사용환경 개선 *(정확한 문구 → Google Drive 회의록/보도자료 확인)*
- **사업기간**: *(Google Drive 회의록 확인 필요 - 60일 아님!)*
- **사업비**: 50,000,000원 (부가세 포함, 수의계약)
- **발주처**: 제주특별자치도 농업기술원 / 농업디지털센터
- **카운터파트**: 농업디지털센터 담당자 *(성함 확정 필요)*

### 🔴 즉시 해야 할 일
1. **Google Drive에서 회의록/보도자료 검색**
2. 부제, 사업기간 등 **정확한 문구 확인**
3. 아래 문서에 반영:
   - `산출내역서_초초안_제주DA원탁회의_50M.md`
   - `과업지시서_제주DA원탁회의_50M.md`
   - `이메일_초안_제주DA원탁회의.md`

### ⚠️ 주의사항
- **프로젝트 개요는 반드시 근거 문서 참조** (임의로 숫자/기간 넣지 말 것)
- 선행 커뮤니케이션: 5/6 사전 협의 미팅 있었음

---

## 작업 히스토리 (2026-05-09)

### 완료된 작업
- [x] 산출내역서 초초안 작성 (50M, 6개 대분류)
- [x] 과업지시서 초안 작성 (5개 장)
- [x] 이메일 초안 작성
- [x] 사업명 수정: "2026 제주DA 파트너스 원탁회의"
- [x] Google Drive MCP 설정 (credentials, .mcp.json)
- [x] 문서 GitHub 커밋/푸시

### 미완료 (다음 세션에서)
- [ ] Google Drive에서 회의록/보도자료 찾기
- [ ] 부제, 사업기간 정확한 문구 반영
- [ ] 종합 견적서 양식 파일 찾기
- [ ] 리멤버 앱 → CSV → 구글시트 자동화

---

## Google Drive MCP 설정

### 인증 정보
- **Client ID**: `263821764650-l286sqqndvftnl9sqeleqklscdcmlll7.apps.googleusercontent.com`
- **Project ID**: `gen-lang-client-0712788641`
- **Credentials 파일**: `~/.config/google-drive-mcp/credentials.json`

### MCP 서버 설정
```json
{
  "mcpServers": {
    "gdrive": {
      "command": "npx",
      "args": ["-y", "@anthropic-ai/mcp-server-gdrive"],
      "env": {
        "GOOGLE_CREDENTIALS_PATH": "~/.config/google-drive-mcp/credentials.json"
      }
    }
  }
}
```

---

## 프로젝트 문서

| 파일명 | 상태 |
|--------|------|
| `산출내역서_초초안_제주DA원탁회의_50M.md` | 초안 완료, 개요 확인 필요 |
| `과업지시서_제주DA원탁회의_50M.md` | 초안 완료, 기간 확인 필요 |
| `이메일_초안_제주DA원탁회의.md` | 초안 완료, 수신자 확정 필요 |

---

## 연락처 정보
- **제주농업기술원 / 농업디지털센터** 담당자 (확정 필요)

---

## 작업 환경 참고

- **메인 작업 환경**: 회사 데스크탑 (비서실장)
- **보조**: 노트북/모바일 → Slack 연동
- GitHub 저장소: `playinthesky/fkf`
- 브랜치: `claude/slack-session-fhGkI`
