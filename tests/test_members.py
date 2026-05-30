"""fKF 회원 저장소 및 로그인 흐름 테스트 (네트워크 불필요)."""

import os
import unittest
from unittest import mock

from members import SampleRepository, SheetsRepository, _to_int


class SampleRepositoryTest(unittest.TestCase):
    def setUp(self):
        self.repo = SampleRepository()

    def test_authenticate_success(self):
        m = self.repo.authenticate("홍길동", "F2021-0007")
        self.assertIsNotNone(m)
        self.assertEqual(m["name"], "홍길동")
        self.assertIn("2025", m["performance"])

    def test_authenticate_trims_whitespace(self):
        self.assertIsNotNone(self.repo.authenticate("  홍길동 ", " F2021-0007 "))

    def test_authenticate_name_mismatch(self):
        self.assertIsNone(self.repo.authenticate("김철수", "F2021-0007"))

    def test_authenticate_unknown_member(self):
        self.assertIsNone(self.repo.authenticate("홍길동", "F9999-0000"))

    def test_authenticate_empty(self):
        self.assertIsNone(self.repo.authenticate("", "F2021-0007"))
        self.assertIsNone(self.repo.authenticate("홍길동", ""))


class SheetsRowParsingTest(unittest.TestCase):
    def test_row_to_member_maps_headers_and_performance(self):
        repo = SheetsRepository("sheet-id")
        headers = [
            "회원번호", "이름", "활동지역", "fKF 자격등급", "CPR교육 수료 여부",
            "2025_세미나", "2025_프로보노", "2025_프로젝트",
        ]
        row = ["F2024-0001", "이몽룡", "서울", "2급 / 2024-01-01", "수료", "10", "4", "3"]
        m = repo._row_to_member(headers, row)
        self.assertEqual(m["member_no"], "F2024-0001")
        self.assertEqual(m["name"], "이몽룡")
        self.assertEqual(m["region"], "서울")
        self.assertEqual(m["fkf_grade"], "2급 / 2024-01-01")
        self.assertEqual(m["cpr"], "수료")
        self.assertEqual(m["performance"]["2025"]["seminar_hours"], 10)
        self.assertEqual(m["performance"]["2025"]["probono_hours"], 4)
        self.assertEqual(m["performance"]["2025"]["project_count"], 3)

    def test_locate_header_skips_title_row(self):
        from members import _locate_header
        values = [
            ["fKF 정회원 명단", "", ""],            # 제목 행
            ["회원번호", "성명", "fKF등급"],          # 실제 헤더 행 (index 1)
            ["fKF-25-0001", "윤혜영", "3급"],
        ]
        hdr_idx, no_idx = _locate_header(values)
        self.assertEqual(hdr_idx, 1)
        self.assertEqual(no_idx, 0)

    def test_locate_header_none_when_missing(self):
        from members import _locate_header
        self.assertEqual(_locate_header([["a", "b"], ["c", "d"]]), (None, None))

    def test_to_int(self):
        self.assertEqual(_to_int("5"), 5)
        self.assertEqual(_to_int("3.0"), 3)
        self.assertEqual(_to_int(""), 0)
        self.assertEqual(_to_int("abc"), 0)
        self.assertEqual(_to_int(None), 0)


class LoginFlowTest(unittest.TestCase):
    def setUp(self):
        os.environ["SECRET_KEY"] = "test"
        import importlib
        import members
        members._repo = SampleRepository()  # 시트 대신 샘플 강제
        import app as appmod
        importlib.reload(appmod)
        appmod.app.config["TESTING"] = True
        self.app = appmod.app
        self.c = appmod.app.test_client()

    def test_dashboard_requires_login(self):
        r = self.c.get("/", follow_redirects=False)
        self.assertEqual(r.status_code, 302)
        self.assertIn("/login", r.headers["Location"])

    def test_login_then_dashboard(self):
        r = self.c.post("/login", data={"name": "홍길동", "member_no": "F2021-0007"})
        self.assertEqual(r.status_code, 302)
        r = self.c.get("/")
        self.assertEqual(r.status_code, 200)
        html = r.get_data(as_text=True)
        self.assertIn("홍길동", html)
        self.assertIn("연도별 실적", html)

    def test_login_failure_shows_error(self):
        r = self.c.post("/login", data={"name": "없는사람", "member_no": "F0000-0000"})
        self.assertEqual(r.status_code, 200)
        self.assertIn("일치하지 않습니다", r.get_data(as_text=True))

    def test_logout_clears_session(self):
        self.c.post("/login", data={"name": "홍길동", "member_no": "F2021-0007"})
        self.c.get("/logout")
        r = self.c.get("/", follow_redirects=False)
        self.assertEqual(r.status_code, 302)


if __name__ == "__main__":
    unittest.main()
