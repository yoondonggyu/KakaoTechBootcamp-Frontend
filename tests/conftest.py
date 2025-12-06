"""
pytest configuration and fixtures for FASTAPI_Project_front

프론트엔드 테스트 설정
- JavaScript 로직 검증 (Python으로 동일 로직 테스트)
- E2E 테스트 지원 (백엔드 연동 시)
- Mock 기반 API 테스트

테스트 전략:
1. 클라이언트 사이드 유효성 검사 로직 테스트
2. API 요청/응답 구조 테스트
3. 에러 처리 및 메시지 테스트
"""
import pytest
import re
from typing import Dict, Any


# ============================================================================
# 테스트 설정 상수
# ============================================================================

BACKEND_URL = "http://localhost:8000"
API_BASE_URL = f"{BACKEND_URL}/api"
MODEL_API_URL = "http://localhost:8001/api"
FRONTEND_URL = "http://localhost:3000"


# ============================================================================
# 기본 데이터 Fixture
# ============================================================================

@pytest.fixture
def test_user_credentials():
    """
    테스트용 사용자 인증 정보

    Returns:
        dict: 유효한 사용자 인증 데이터
    """
    return {
        "email": "testuser@example.com",
        "password": "TestPassword123!@#",
        "nickname": "테스트유저"
    }


@pytest.fixture
def test_user_credentials_2():
    """두 번째 테스트 사용자"""
    return {
        "email": "testuser2@example.com",
        "password": "AnotherPass456!@#",
        "nickname": "유저2"
    }


@pytest.fixture
def test_post_data():
    """테스트용 게시글 데이터"""
    return {
        "title": "테스트 게시글 제목",
        "content": "테스트 게시글 내용입니다. 이것은 E2E 테스트용 게시글입니다."
    }


@pytest.fixture
def test_comment_data():
    """테스트용 댓글 데이터"""
    return {
        "content": "테스트 댓글 내용입니다."
    }


# ============================================================================
# 유효성 검사 테스트 데이터
# ============================================================================

@pytest.fixture
def valid_email_formats():
    """유효한 이메일 형식 목록"""
    return [
        "test@example.com",
        "user.name@domain.co.kr",
        "user123@test.org",
        "test_user@sub.domain.com",
        "test+tag@example.com"
    ]


@pytest.fixture
def invalid_email_formats():
    """잘못된 이메일 형식 목록"""
    return [
        "plainaddress",          # @ 없음
        "@no-local-part.com",    # 로컬 파트 없음
        "missing-at-sign.com",   # @ 없음
        "missing@domain",        # TLD 없음
        "spaces in@email.com",   # 공백 포함
        "double@@at.com",        # 중복 @
        ""                       # 빈 문자열
    ]


@pytest.fixture
def valid_password_formats():
    """유효한 비밀번호 형식 목록"""
    return [
        "Password1!",            # 최소 조건 충족
        "MySecure@123",          # 일반적인 비밀번호
        "Test1234!@#$",          # 특수문자 다수
        "AbCdEf1!AbCdEf1!"      # 긴 비밀번호
    ]


@pytest.fixture
def invalid_password_formats():
    """
    잘못된 비밀번호 형식 목록

    비밀번호 규칙:
    - 8자 이상 20자 이하
    - 대문자 포함
    - 소문자 포함
    - 특수문자 포함
    """
    return [
        "short",                 # 너무 짧음 (8자 미만)
        "nouppercase1!",         # 대문자 없음
        "NOLOWERCASE1!",         # 소문자 없음
        "NoSpecialChar1",        # 특수문자 없음
        "NoNumber!Aa",           # 숫자 없음
        "",                      # 빈 문자열
        "a" * 21 + "A1!"         # 너무 긴 비밀번호
    ]


@pytest.fixture
def valid_nicknames():
    """유효한 닉네임 목록"""
    return [
        "유저",
        "user123",
        "테스트유저",
        "닉네임1234"              # 최대 10자
    ]


@pytest.fixture
def invalid_nicknames():
    """잘못된 닉네임 목록"""
    return [
        "",                       # 빈 문자열
        "닉 네 임",               # 공백 포함
        "이것은너무긴닉네임입니다",  # 10자 초과
        "   "                     # 공백만
    ]


# ============================================================================
# API 응답 Mock Fixture
# ============================================================================

@pytest.fixture
def mock_login_success_response():
    """로그인 성공 응답"""
    return {
        "message": "login_success",
        "data": {
            "user_id": 1,
            "nickname": "테스트유저",
            "profile_image_url": "https://example.com/image.jpg"
        }
    }


@pytest.fixture
def mock_login_failure_response():
    """로그인 실패 응답"""
    return {
        "message": "invalid_credentials",
        "data": None
    }


@pytest.fixture
def mock_signup_success_response():
    """회원가입 성공 응답"""
    return {
        "message": "register_success",
        "data": {
            "user_id": 1
        }
    }


@pytest.fixture
def mock_signup_failure_response():
    """회원가입 실패 응답 (중복 이메일)"""
    return {
        "message": "duplicate_email",
        "data": None
    }


@pytest.fixture
def mock_posts_list_response():
    """게시글 목록 응답"""
    return {
        "message": "get_posts_success",
        "data": {
            "posts": [
                {
                    "id": 1,
                    "title": "첫 번째 게시글",
                    "content": "내용입니다.",
                    "user_id": 1,
                    "nickname": "작성자",
                    "like_count": 5,
                    "view_count": 100,
                    "created_at": "2024-01-01T12:00:00"
                },
                {
                    "id": 2,
                    "title": "두 번째 게시글",
                    "content": "두 번째 내용입니다.",
                    "user_id": 2,
                    "nickname": "작성자2",
                    "like_count": 3,
                    "view_count": 50,
                    "created_at": "2024-01-02T12:00:00"
                }
            ],
            "total": 2,
            "page": 1,
            "limit": 10
        }
    }


@pytest.fixture
def mock_create_post_success_response():
    """게시글 생성 성공 응답"""
    return {
        "message": "create_post_success",
        "data": {
            "post_id": 1
        }
    }


# ============================================================================
# 유효성 검사 헬퍼 Fixture
# ============================================================================

@pytest.fixture
def email_validator():
    """
    이메일 유효성 검사 함수

    JavaScript의 이메일 검증 로직과 동일
    """
    def validate(email: str) -> bool:
        if not email or not isinstance(email, str):
            return False
        # JavaScript 정규식과 동일
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    return validate


@pytest.fixture
def password_validator():
    """
    비밀번호 유효성 검사 함수

    규칙:
    - 8자 이상 20자 이하
    - 대문자 1개 이상
    - 소문자 1개 이상
    - 특수문자 1개 이상
    """
    def validate(password: str) -> Dict[str, Any]:
        errors = []

        if not password:
            return {"valid": False, "errors": ["비밀번호를 입력해주세요"]}

        if len(password) < 8:
            errors.append("8자 이상이어야 합니다")
        if len(password) > 20:
            errors.append("20자 이하여야 합니다")
        if not re.search(r'[A-Z]', password):
            errors.append("대문자가 필요합니다")
        if not re.search(r'[a-z]', password):
            errors.append("소문자가 필요합니다")
        if not re.search(r'[0-9]', password):
            errors.append("숫자가 필요합니다")
        if not re.search(r'[!@#$%^&*()\-_=+\[\]{}|;:\'",.<>/?`~]', password):
            errors.append("특수문자가 필요합니다")

        return {"valid": len(errors) == 0, "errors": errors}
    return validate


@pytest.fixture
def nickname_validator():
    """
    닉네임 유효성 검사 함수

    규칙:
    - 필수 입력
    - 공백 불가
    - 최대 10자
    """
    def validate(nickname: str) -> Dict[str, Any]:
        errors = []

        if not nickname or not nickname.strip():
            return {"valid": False, "errors": ["닉네임을 입력해주세요"]}

        if " " in nickname:
            errors.append("공백을 포함할 수 없습니다")
        if len(nickname) > 10:
            errors.append("10자 이하여야 합니다")

        return {"valid": len(errors) == 0, "errors": errors}
    return validate


# ============================================================================
# 에러 메시지 Fixture
# ============================================================================

@pytest.fixture
def error_messages():
    """
    프론트엔드 에러 메시지 매핑

    JavaScript의 에러 메시지와 동기화
    """
    return {
        # 로그인 에러
        "email_required": "이메일을 입력해주세요",
        "invalid_email_format": "올바른 이메일 주소 형식을 입력해주세요",
        "password_required": "비밀번호를 입력해주세요",
        "invalid_credentials": "아이디 또는 비밀번호를 확인해주세요",

        # 회원가입 에러
        "invalid_email_character": "이메일은 영문과 @, .만 사용이 가능합니다",
        "duplicate_email": "중복된 이메일입니다",
        "invalid_password_format": "비밀번호는 8자 이상, 20자 이하이며 대문자, 소문자, 특수문자를 각각 1개 포함해야 합니다",
        "password_check_required": "비밀번호를 한번 더 입력해주세요",
        "password_mismatch": "비밀번호가 다릅니다",
        "nickname_required": "닉네임을 입력해주세요",
        "nickname_contains_space": "띄어쓰기를 없애주세요",
        "nickname_too_long": "닉네임은 최대 10자까지 작성 가능합니다",
        "duplicate_nickname": "중복된 닉네임입니다",
        "profile_image_url_required": "프로필 사진을 추가해주세요",

        # 게시글 에러
        "title_required": "제목을 입력해주세요",
        "content_required": "내용을 입력해주세요",
        "post_not_found": "게시글을 찾을 수 없습니다",

        # 일반 에러
        "network_error": "네트워크 오류가 발생했습니다",
        "server_error": "서버 오류가 발생했습니다"
    }


# ============================================================================
# API URL 생성 헬퍼 Fixture
# ============================================================================

@pytest.fixture
def api_endpoints():
    """
    API 엔드포인트 생성 헬퍼

    JavaScript api.js의 엔드포인트와 동기화
    """
    class APIEndpoints:
        base_url = API_BASE_URL
        model_url = MODEL_API_URL

        # Auth
        @staticmethod
        def login():
            return f"{API_BASE_URL}/auth/login"

        @staticmethod
        def signup():
            return f"{API_BASE_URL}/auth/signup"

        # Posts
        @staticmethod
        def posts(page=1, limit=10):
            return f"{API_BASE_URL}/posts?page={page}&limit={limit}"

        @staticmethod
        def post(post_id: int):
            return f"{API_BASE_URL}/posts/{post_id}"

        @staticmethod
        def post_like(post_id: int):
            return f"{API_BASE_URL}/posts/{post_id}/like"

        @staticmethod
        def post_view(post_id: int):
            return f"{API_BASE_URL}/posts/{post_id}/view"

        @staticmethod
        def post_upload():
            return f"{API_BASE_URL}/posts/upload"

        # Comments
        @staticmethod
        def comments(post_id: int):
            return f"{API_BASE_URL}/posts/{post_id}/comments"

        @staticmethod
        def comment(post_id: int, comment_id: int):
            return f"{API_BASE_URL}/posts/{post_id}/comments/{comment_id}"

        # Users
        @staticmethod
        def profile_upload():
            return f"{API_BASE_URL}/users/profile/upload"

        # Model API
        @staticmethod
        def sentiment():
            return f"{MODEL_API_URL}/sentiment"

        @staticmethod
        def sentiment_gemini():
            return f"{MODEL_API_URL}/sentiment/gemini"

    return APIEndpoints()
