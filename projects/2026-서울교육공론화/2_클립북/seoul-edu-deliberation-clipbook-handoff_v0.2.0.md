# HANDOFF — 서울교육 공론화 클립북

- doc_type: clipbook (자료맵 아님. 실제 발신·보도 클립 모음)
- doc_version: v0.2.0
- status: draft (수집 진행 중)
- generated: 2026-06-04
- owner: Korea Speaks
- key_fact: "서울교육 공론화"는 단일 전용 사이트 없음. 다채널 분산.
- structure: 매체(channel) 1차축 → 연도순 클립(clip). 출처는 official_edu / press / research.
- v0.2.0 변경: 채널 F (브랜드 자산·홍보 머티어리얼 소스) 신설 — 4단계 PR 콘텐츠 제작 시 필수

## 봇 작업 지시 (next actions)
1. status=`verified` 클립의 URL은 신뢰. 게시판 번호(bbsSn)는 변동 가능 → 200 응답만 확인.
2. gaps 항목을 채우는 것이 봇의 핵심 임무. 특히 영상·카드뉴스 개별 URL.
3. 영상 탐색: SEN TV 채널 내 "공론화" "원탁토론" "시민참여단" 검색 → 개별 영상 URL을 channel id=4 entries에 append.
4. 신규 클립 추가 시 source(official_edu/press/research)와 year 필수 기입, doc_version 패치 상승.

## 데이터 (machine-readable)

```json
{
  "doc_type": "clipbook",
  "doc_version": "v0.2.0",
  "status": "draft",
  "generated": "2026-06-04",
  "subject": "서울교육 공론화",
  "channels": [
    {
      "id": "A", "media": "교육청 공식 보도 (enews)",
      "clips": [
        {"year": 2018, "title": "서울학생 두발 자유화 선언 및 편안한 교복 공론화", "source": "official_edu", "url": "https://enews.sen.go.kr/news/view.do?bbsSn=157013&step1=3&step2=1", "status": "verified"},
        {"year": 2024, "title": "서울교육 10년 성찰 미래교육 포럼·현장토론", "source": "official_edu", "url": "https://enews.sen.go.kr/news/view.do?bbsSn=186820&step1=3&step2=1", "status": "verified"},
        {"year": null, "title": "보도자료 전체 목록(공론화 키워드 검색)", "source": "official_edu", "url": "https://enews.sen.go.kr/news/list.do?step1=3&step2=1", "status": "index"}
      ]
    },
    {
      "id": "B", "media": "외부 언론 보도 (미디어 클립)",
      "clips": [
        {"year": 2018, "title": "서울 중·고교 내년 2학기부터 두발 자유화", "source": "press", "outlet": "서울신문", "url": "https://www.seoul.co.kr/news/newsView.php?id=20180928009026", "status": "verified"},
        {"year": 2019, "title": "중고교 교복·두발 자유화…편한 교복 vs 학생다움", "source": "press", "outlet": "아시아경제", "url": "https://www.asiae.co.kr/article/2019011809500068538", "status": "verified"},
        {"year": 2019, "title": "서울 407개교 공론화 거쳐 두발자유화", "source": "press", "outlet": "뉴시스", "url": "https://www.newsis.com/view/NISX20191001_0000785955", "status": "verified"},
        {"year": 2019, "title": "내년부터 서울 중·고생 대부분 생활복 입는다", "source": "press", "outlet": "인사이트", "url": "https://www.insight.co.kr/news/249014", "status": "verified"}
      ]
    },
    {
      "id": "C", "media": "교육청 누리집 참여·의제 채널",
      "clips": [
        {"year": null, "title": "시민참여단 정책 제안(공론화 의제 제안)", "source": "official_edu", "url": "https://www.sen.go.kr/user/bbs/BD_selectBbsList.do?q_bbsSn=1020", "status": "verified"},
        {"year": null, "title": "시민참여단 공지사항(자문·모니터링)", "source": "official_edu", "url": "https://www.sen.go.kr/user/bbs/BD_selectBbsList.do?q_bbsSn=1017", "status": "verified"},
        {"year": null, "title": "정책설문(서울교육 소통광장)", "source": "official_edu", "url": "https://edu-policy.sen.go.kr/", "status": "verified"}
      ]
    },
    {
      "id": "D", "media": "영상·카드뉴스·SNS",
      "clips": [
        {"year": null, "title": "서울특별시교육청TV(SEN) 채널", "source": "official_edu", "url": "https://www.youtube.com/channel/UCq4jckvIGYbC9fD73KPp6tw", "status": "channel_only"},
        {"year": null, "title": "교육연구정보원 채널", "source": "official_edu", "url": "https://www.youtube.com/channel/UCvLh1MdEbn6T15PEYlYRnwA", "status": "channel_only"},
        {"year": null, "title": "공식 인스타그램 @now_seouledu", "source": "official_edu", "url": "https://www.instagram.com/now_seouledu/", "status": "channel_only"},
        {"year": null, "title": "공식 네이버 블로그(누리집 하단 경유)", "source": "official_edu", "url": "https://www.sen.go.kr/sen/index.do", "status": "channel_only"},
        {"year": null, "title": "공론화 전용 영상 재생목록", "url": null, "status": "gap"},
        {"year": null, "title": "공론화 전용 카드뉴스 게시물", "url": null, "status": "gap"}
      ]
    },
    {
      "id": "E", "media": "보고서·연구·웹진",
      "clips": [
        {"year": 2022, "title": "서울미래교육 2030 중기발전계획위원회 최종보고서", "source": "research", "url": "https://www.sen.go.kr/resources/www/data/proposal_5.pdf", "status": "verified"},
        {"year": 2022, "title": "함께 만들어가는 서울미래교육(계간 서울교육 웹진)", "source": "research", "url": "https://webzine-serii.re.kr/%ED%95%A8%EA%BB%98-%EB%A7%8C%EB%93%A4%EC%96%B4%EA%B0%80%EB%8A%94-%EC%84%9C%EC%9A%B8%EB%AF%B8%EB%9E%98%EA%B5%90%EC%9C%A1/", "status": "verified"},
        {"year": null, "title": "교육정책연구소(위탁·이슈페이퍼)", "source": "research", "url": "https://www.serii.re.kr/", "status": "index"},
        {"year": null, "title": "9시 등교 인접정책 학술분석", "source": "research", "url": "https://www.kci.go.kr/kciportal/ci/sereArticleSearch/ciSereArtiView.kci?sereArticleSearchBean.artiId=ART002278502", "status": "verified"},
        {"year": null, "title": "9시 등교제 효과분석", "source": "research", "url": "https://www.dbpia.co.kr/journal/articleDetail?nodeId=NODE11506773", "status": "verified"}
      ]
    },
    {
      "id": "F", "media": "브랜드 자산·홍보 머티어리얼 소스",
      "purpose": "4단계 PR 콘텐츠(인포그래픽·쇼츠·카드뉴스) 제작 시 클라이언트 브랜드 가이드 준수용. 클라이언트가 직접 제공하거나 공식 사이트에서 확보.",
      "clips": [
        {"year": null, "title": "서울시교육청 CI 가이드라인 (로고·서체·컬러)", "source": "official_edu", "url": null, "status": "gap"},
        {"year": null, "title": "서울시교육청 공식 로고 (AI·SVG·PNG)", "source": "official_edu", "url": null, "status": "gap"},
        {"year": null, "title": "서울시교육청 지정 서체 (한글·영문)", "source": "official_edu", "url": null, "status": "gap"},
        {"year": null, "title": "서울교육 소통광장 디자인 가이드", "source": "official_edu", "url": "https://edu-policy.sen.go.kr/", "status": "channel_only"},
        {"year": null, "title": "서울교육+플러스 브랜드 자산 (있다면)", "source": "official_edu", "url": null, "status": "gap"},
        {"year": null, "title": "공론화 사업 전용 BI·심볼 (있다면)", "source": "official_edu", "url": null, "status": "gap"},
        {"year": null, "title": "이전 연도 홍보물 소스 파일 (작년 PR-1~4 카드뉴스·인포그래픽 원본)", "source": "official_edu", "url": null, "status": "gap"}
      ]
    }
  ],
  "gaps": [
    "SEN TV 내 공론화 행사·원탁토론 영상 개별 URL",
    "공론화 전용 카드뉴스(인스타 개별 게시물)",
    "공론화 현장 사진 모음 / 블로그 현장 스케치",
    "연도별 추진사항 통합 타임라인(2018~현재)",
    "공론화 운영 백서 단독본 / 제3자 외부 평가보고서",
    "[F채널] 서울시교육청 CI 가이드라인 PDF 또는 공식 페이지",
    "[F채널] 로고 원본 파일 (AI/SVG/PNG)",
    "[F채널] 지정 서체 (한글·영문) 파일 또는 라이선스 안내",
    "[F채널] 이전 연도 홍보물 소스 (PSD/AI) — 작년 PR 카드뉴스·인포그래픽"
  ]
}
```

## 상태 코드
- `verified`: URL·존재 확인된 실제 클립.
- `channel_only`: 채널 진입점만 확인. 전용 클립 미특정.
- `index`: 목록/검색 페이지(개별 클립 아님).
- `gap`: URL 없음. 봇이 채울 대상.
