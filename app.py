#!/usr/bin/env python3
"""fKF(한국퍼실리테이터연합회) 정회원 포털.

이름 + 회원번호로 로그인하면 본인의 자격등급 · 교육 이수 현황 · 연도별 실적을
조회할 수 있는 마이페이지 대시보드를 제공합니다.
"""

import os
from functools import wraps

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    jsonify,
)

from members import get_repository

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = os.environ.get("SECRET_KEY", "fkf-fallback-secret-change-me")


# ── 로그인 게이트 ─────────────────────────────────────────────────────────────
def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("member_no"):
            session["next_url"] = request.path
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapped


def _safe_next(target):
    if target and target.startswith("/") and not target.startswith("//"):
        return target
    return None


# ── 라우트 ────────────────────────────────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("member_no"):
        return redirect(url_for("dashboard"))

    error = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        member_no = request.form.get("member_no", "").strip()
        if not name or not member_no:
            error = "이름과 회원번호를 모두 입력해주세요."
        else:
            member = get_repository().authenticate(name, member_no)
            if member:
                session["member_no"] = member["member_no"]
                session["name"] = member["name"]
                nxt = _safe_next(session.pop("next_url", None))
                return redirect(nxt or url_for("dashboard"))
            error = "이름 또는 회원번호가 일치하지 않습니다."

    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def dashboard():
    # 세션 정보로 최신 회원 데이터를 다시 조회한다.
    member = get_repository().authenticate(session.get("name"), session.get("member_no"))
    if not member:
        session.clear()
        return redirect(url_for("login"))
    return render_template("dashboard.html", m=member, years=_present_years(member))


@app.route("/api/me")
@login_required
def api_me():
    member = get_repository().get_member(session.get("member_no"))
    if not member:
        return jsonify({"authenticated": False}), 401
    return jsonify({"authenticated": True, "member": member})


def _present_years(member):
    """실적 표에 표시할 연도 목록(데이터가 있는 순서대로)."""
    perf = member.get("performance", {})
    return sorted(perf.keys(), reverse=True)


@app.route("/healthz")
def healthz():
    return "ok", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=True)
