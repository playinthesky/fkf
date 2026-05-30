"""fKF 회원 저장소.

회원 인증(이름 + 회원번호)과 마이페이지 대시보드에 필요한 회원 데이터를
공급합니다. 데이터 출처는 교체 가능합니다.

- ``SheetsRepository``: Google Sheets 마스터 시트(서비스 계정)에서 회원 명단과
  실적을 읽습니다. ``FKF_MASTER_SHEET_ID`` 환경 변수와 ``GOOGLE_CREDENTIALS``
  (또는 credentials.json)가 있으면 사용됩니다.
- ``SampleRepository``: 시트가 설정되지 않은 환경(로컬/데모)에서 쓰는 내장 샘플.

회원 식별 키는 ``member_no``(회원번호)이며, 로그인 시 ``name``(이름)을 2차
확인 요소로 대조합니다.

회원 레코드 스키마(dict)::

    {
      "member_no", "name", "phone", "email", "region",
      "fkf_grade", "private_grade", "specialties",
      "cpr", "sensitivity_edu", "youth_debate",
      "performance": { "2026": {"seminar_hours","probono_hours","project_count"}, ... },
      "records": [ {"date","type","name","seminar_hours","probono_hours","role"}, ... ],
    }
"""

import os

PERFORMANCE_YEARS = ["2026", "2025", "2024"]

# 마스터 시트 회원 명단 탭의 헤더 → 레코드 필드 매핑.
# 실제 마스터 시트의 헤더에 맞춰 환경에 따라 조정할 수 있습니다.
ROSTER_HEADER_MAP = {
    "회원번호": "member_no",
    "이름": "name",
    "성명": "name",
    "연락처": "phone",
    "이메일": "email",
    "이 메 일": "email",
    "활동지역": "region",
    "fKF 자격등급": "fkf_grade",
    "fkf자격등급": "fkf_grade",
    "민간자격 등급": "private_grade",
    "민간자격등급": "private_grade",
    "Specialties": "specialties",
    "전문분야": "specialties",
    "CPR교육 수료 여부": "cpr",
    "CPR": "cpr",
    "성인지&아동감수성교육": "sensitivity_edu",
    "청소년토론지도사 자격": "youth_debate",
}


def _norm(value):
    return (value or "").strip()


def _empty_performance():
    return {y: {"seminar_hours": 0, "probono_hours": 0, "project_count": 0} for y in PERFORMANCE_YEARS}


class MemberRepository:
    """저장소 공통 인터페이스."""

    def get_member(self, member_no):
        raise NotImplementedError

    def authenticate(self, name, member_no):
        """이름 + 회원번호로 본인 확인. 성공 시 회원 dict, 실패 시 None."""
        member_no = _norm(member_no)
        name = _norm(name)
        if not member_no or not name:
            return None
        member = self.get_member(member_no)
        if not member:
            return None
        if _norm(member.get("name")) != name:
            return None
        return member


# ── 샘플 저장소 ───────────────────────────────────────────────────────────────
_SAMPLE_MEMBERS = {
    "F2021-0007": {
        "member_no": "F2021-0007",
        "name": "홍길동",
        "phone": "010-1234-5678",
        "email": "gildong@example.com",
        "region": "제주",
        "fkf_grade": "1급 / 2023-05-01",
        "private_grade": "전문퍼실리테이터 / 2022-11-10",
        "specialties": "공론화, 청소년토론, 도시계획",
        "cpr": "수료 (2024-03)",
        "sensitivity_edu": "이수 (2024-02)",
        "youth_debate": "보유",
        "performance": {
            "2026": {"seminar_hours": 6, "probono_hours": 4, "project_count": 2},
            "2025": {"seminar_hours": 18, "probono_hours": 12, "project_count": 5},
            "2024": {"seminar_hours": 22, "probono_hours": 8, "project_count": 4},
        },
        "records": [
            {"date": "2025-03-12", "type": "세미나", "name": "공론화 설계 워크숍",
             "seminar_hours": 3, "probono_hours": 0, "role": ""},
            {"date": "2025-05-20", "type": "프로젝트", "name": "제주 숙의형 데이터 분석",
             "seminar_hours": 0, "probono_hours": 4, "role": "퍼실리테이터"},
            {"date": "2025-09-02", "type": "세미나", "name": "청소년 토론지도 심화",
             "seminar_hours": 4, "probono_hours": 0, "role": ""},
        ],
    },
}


class SampleRepository(MemberRepository):
    """내장 샘플 데이터(시트 미설정 시 폴백). 데모/로컬 개발용."""

    def get_member(self, member_no):
        member = _SAMPLE_MEMBERS.get(_norm(member_no))
        return dict(member) if member else None


# ── Google Sheets 저장소 ──────────────────────────────────────────────────────
_SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]


class SheetsRepository(MemberRepository):
    """Google Sheets 마스터 시트 기반 저장소.

    ``roster_tab`` 워크시트(기본 '회원명단')의 헤더 행을 ROSTER_HEADER_MAP 으로
    해석합니다. 연도별 실적은 ``2026_세미나`` 같은 컬럼이 있으면 읽고, 없으면
    0으로 둡니다. 상세 실적 탭은 선택 사항입니다.
    """

    def __init__(self, spreadsheet_id, roster_tab=None):
        self.spreadsheet_id = spreadsheet_id
        self.roster_tab = roster_tab or os.environ.get("FKF_ROSTER_TAB", "회원명단")
        self._ws = None

    def _worksheet(self):
        if self._ws is not None:
            return self._ws
        import gspread
        from google.oauth2.service_account import Credentials

        credentials_json = os.environ.get("GOOGLE_CREDENTIALS")
        if credentials_json:
            import json

            info = json.loads(credentials_json)
            creds = Credentials.from_service_account_info(info, scopes=_SCOPES)
        else:
            cred_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "credentials.json")
            if not os.path.exists(cred_file):
                raise FileNotFoundError("자격증명 없음")
            creds = Credentials.from_service_account_file(cred_file, scopes=_SCOPES)

        client = gspread.authorize(creds)
        sh = client.open_by_key(self.spreadsheet_id)
        self._ws = sh.worksheet(self.roster_tab)
        return self._ws

    def _row_to_member(self, headers, row):
        member = {
            "member_no": "", "name": "", "phone": "", "email": "", "region": "",
            "fkf_grade": "", "private_grade": "", "specialties": "",
            "cpr": "", "sensitivity_edu": "", "youth_debate": "",
            "performance": _empty_performance(), "records": [],
        }
        for idx, head in enumerate(headers):
            value = row[idx] if idx < len(row) else ""
            head_norm = _norm(head)
            field = ROSTER_HEADER_MAP.get(head_norm)
            if field:
                member[field] = _norm(value)
                continue
            # "2026_세미나" / "2026_프로보노" / "2026_프로젝트" 형태 실적 컬럼
            for year in PERFORMANCE_YEARS:
                if head_norm.startswith(year):
                    if "세미나" in head_norm:
                        member["performance"][year]["seminar_hours"] = _to_int(value)
                    elif "프로보노" in head_norm:
                        member["performance"][year]["probono_hours"] = _to_int(value)
                    elif "프로젝트" in head_norm:
                        member["performance"][year]["project_count"] = _to_int(value)
        return member

    def get_member(self, member_no):
        member_no = _norm(member_no)
        if not member_no:
            return None
        ws = self._worksheet()
        values = ws.get_all_values()
        if not values:
            return None
        headers = values[0]
        try:
            no_idx = next(
                i for i, h in enumerate(headers) if ROSTER_HEADER_MAP.get(_norm(h)) == "member_no"
            )
        except StopIteration:
            return None
        for row in values[1:]:
            if no_idx < len(row) and _norm(row[no_idx]) == member_no:
                return self._row_to_member(headers, row)
        return None


def _to_int(value):
    try:
        return int(float(str(value).strip() or 0))
    except (ValueError, TypeError):
        return 0


# ── 팩토리 ────────────────────────────────────────────────────────────────────
_repo = None


def get_repository():
    """환경에 맞는 회원 저장소 싱글톤을 돌려준다."""
    global _repo
    if _repo is not None:
        return _repo
    sheet_id = os.environ.get("FKF_MASTER_SHEET_ID", "").strip()
    if sheet_id:
        try:
            repo = SheetsRepository(sheet_id)
            repo._worksheet()  # 연결 확인
            _repo = repo
            return _repo
        except Exception as exc:  # noqa: BLE001 - 실패 시 샘플로 폴백
            print(f"[fkf.members] 시트 저장소 사용 불가, 샘플 폴백: {exc}")
    _repo = SampleRepository()
    return _repo
