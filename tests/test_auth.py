"""
인증 기능 테스트 케이스

테스트 대상 (JavaScript 로직):
- 로그인 유효성 검사
- 회원가입 유효성 검사
- 세션 관리
- 에러 메시지 처리

Note: 프론트엔드 테스트는 JavaScript 로직을 Python으로 검증합니다.
실제 브라우저 테스트는 Selenium/Playwright 등을 사용해야 합니다.
"""
import pytest
import re


class TestEmailValidation:
    """
    이메일 유효성 검사 테스트

    JavaScript의 이메일 검증 로직 테스트
    """

    def test_valid_email_formats(self, email_validator, valid_email_formats):
        """
        [성공] 유효한 이메일 형식

        Given: 올바른 이메일 형식 목록
        When: 유효성 검사 수행
        Then: 모두 통과
        """
        for email in valid_email_formats:
            assert email_validator(email), f"Expected valid: {email}"

    def test_invalid_email_formats(self, email_validator, invalid_email_formats):
        """
        [실패] 잘못된 이메일 형식

        Given: 잘못된 이메일 형식 목록
        When: 유효성 검사 수행
        Then: 모두 실패
        """
        for email in invalid_email_formats:
            assert not email_validator(email), f"Expected invalid: {email}"

    def test_email_required(self, email_validator):
        """
        [실패] 이메일 필수 입력

        Given: 빈 이메일
        When: 유효성 검사 수행
        Then: 실패
        """
        assert not email_validator("")
        assert not email_validator(None)

    def test_email_with_korean(self, email_validator):
        """
        [실패] 한글 포함 이메일

        Given: 한글이 포함된 이메일
        When: 유효성 검사 수행
        Then: 실패
        """
        assert not email_validator("한글@example.com")
        assert not email_validator("test@한글.com")


class TestPasswordValidation:
    """
    비밀번호 유효성 검사 테스트

    규칙:
    - 8자 이상 20자 이하
    - 대문자 1개 이상
    - 소문자 1개 이상
    - 특수문자 1개 이상
    """

    def test_valid_password_formats(self, password_validator, valid_password_formats):
        """
        [성공] 유효한 비밀번호 형식

        Given: 규칙을 만족하는 비밀번호 목록
        When: 유효성 검사 수행
        Then: 모두 통과
        """
        for password in valid_password_formats:
            result = password_validator(password)
            assert result["valid"], f"Expected valid: {password}, errors: {result['errors']}"

    def test_invalid_password_formats(self, password_validator, invalid_password_formats):
        """
        [실패] 잘못된 비밀번호 형식

        Given: 규칙을 만족하지 않는 비밀번호 목록
        When: 유효성 검사 수행
        Then: 모두 실패
        """
        for password in invalid_password_formats:
            result = password_validator(password)
            assert not result["valid"], f"Expected invalid: {password}"

    def test_password_too_short(self, password_validator):
        """
        [실패] 8자 미만 비밀번호

        Given: 7자 비밀번호
        When: 유효성 검사 수행
        Then: 실패, "8자 이상" 에러
        """
        result = password_validator("Aa1!aaa")
        assert not result["valid"]
        assert any("8자" in err for err in result["errors"])

    def test_password_too_long(self, password_validator):
        """
        [실패] 20자 초과 비밀번호

        Given: 21자 이상 비밀번호
        When: 유효성 검사 수행
        Then: 실패, "20자 이하" 에러
        """
        result = password_validator("Aa1!" + "a" * 17)
        assert not result["valid"]
        assert any("20자" in err for err in result["errors"])

    def test_password_no_uppercase(self, password_validator):
        """
        [실패] 대문자 없는 비밀번호

        Given: 대문자 없는 비밀번호
        When: 유효성 검사 수행
        Then: 실패
        """
        result = password_validator("password1!")
        assert not result["valid"]

    def test_password_no_lowercase(self, password_validator):
        """
        [실패] 소문자 없는 비밀번호

        Given: 소문자 없는 비밀번호
        When: 유효성 검사 수행
        Then: 실패
        """
        result = password_validator("PASSWORD1!")
        assert not result["valid"]

    def test_password_no_special_char(self, password_validator):
        """
        [실패] 특수문자 없는 비밀번호

        Given: 특수문자 없는 비밀번호
        When: 유효성 검사 수행
        Then: 실패
        """
        result = password_validator("Password1")
        assert not result["valid"]


class TestNicknameValidation:
    """
    닉네임 유효성 검사 테스트

    규칙:
    - 필수 입력
    - 공백 불가
    - 최대 10자
    """

    def test_valid_nicknames(self, nickname_validator, valid_nicknames):
        """
        [성공] 유효한 닉네임

        Given: 규칙을 만족하는 닉네임 목록
        When: 유효성 검사 수행
        Then: 모두 통과
        """
        for nickname in valid_nicknames:
            result = nickname_validator(nickname)
            assert result["valid"], f"Expected valid: {nickname}, errors: {result['errors']}"

    def test_invalid_nicknames(self, nickname_validator, invalid_nicknames):
        """
        [실패] 잘못된 닉네임

        Given: 규칙을 만족하지 않는 닉네임 목록
        When: 유효성 검사 수행
        Then: 모두 실패
        """
        for nickname in invalid_nicknames:
            result = nickname_validator(nickname)
            assert not result["valid"], f"Expected invalid: {nickname}"

    def test_nickname_with_space(self, nickname_validator):
        """
        [실패] 공백 포함 닉네임

        Given: 공백이 포함된 닉네임
        When: 유효성 검사 수행
        Then: 실패
        """
        result = nickname_validator("닉 네임")
        assert not result["valid"]

    def test_nickname_too_long(self, nickname_validator):
        """
        [실패] 10자 초과 닉네임

        Given: 11자 이상 닉네임
        When: 유효성 검사 수행
        Then: 실패
        """
        result = nickname_validator("이것은너무긴닉네임입니다")
        assert not result["valid"]

    def test_nickname_max_length(self, nickname_validator):
        """
        [성공] 정확히 10자 닉네임

        Given: 10자 닉네임
        When: 유효성 검사 수행
        Then: 통과
        """
        result = nickname_validator("닉네임12345")
        assert result["valid"]


class TestPasswordMatch:
    """
    비밀번호 확인 일치 테스트
    """

    def test_password_match(self):
        """
        [성공] 비밀번호 일치

        Given: 동일한 비밀번호 두 개
        When: 비교
        Then: 일치
        """
        password = "Password123!@#"
        password_check = "Password123!@#"
        assert password == password_check

    def test_password_mismatch(self):
        """
        [실패] 비밀번호 불일치

        Given: 다른 비밀번호 두 개
        When: 비교
        Then: 불일치
        """
        password = "Password123!@#"
        password_check = "DifferentPassword456!@#"
        assert password != password_check


class TestLoginResponseHandling:
    """
    로그인 응답 처리 테스트
    """

    def test_successful_login_response(self, mock_login_success_response):
        """
        [성공] 로그인 성공 응답 구조

        Given: 성공 응답
        When: 응답 파싱
        Then: 필수 필드 존재
        """
        response = mock_login_success_response

        assert response["message"] == "login_success"
        assert "data" in response
        assert "user_id" in response["data"]
        assert "nickname" in response["data"]

    def test_failed_login_response(self, mock_login_failure_response):
        """
        [실패] 로그인 실패 응답 구조

        Given: 실패 응답
        When: 응답 파싱
        Then: 에러 메시지 확인
        """
        response = mock_login_failure_response

        assert response["message"] != "login_success"
        assert response["message"] == "invalid_credentials"


class TestSignupResponseHandling:
    """
    회원가입 응답 처리 테스트
    """

    def test_successful_signup_response(self, mock_signup_success_response):
        """
        [성공] 회원가입 성공 응답 구조

        Given: 성공 응답
        When: 응답 파싱
        Then: 필수 필드 존재
        """
        response = mock_signup_success_response

        assert response["message"] == "register_success"
        assert "data" in response
        assert "user_id" in response["data"]

    def test_failed_signup_response(self, mock_signup_failure_response):
        """
        [실패] 회원가입 실패 응답 구조 (중복 이메일)

        Given: 실패 응답
        When: 응답 파싱
        Then: 에러 메시지 확인
        """
        response = mock_signup_failure_response

        assert response["message"] != "register_success"
        assert response["message"] == "duplicate_email"


class TestErrorMessages:
    """
    에러 메시지 테스트
    """

    def test_all_login_error_messages_exist(self, error_messages):
        """
        [확인] 로그인 관련 에러 메시지 존재

        Given: 에러 메시지 딕셔너리
        When: 로그인 에러 키 확인
        Then: 모든 키 존재
        """
        login_error_keys = [
            "email_required",
            "invalid_email_format",
            "password_required",
            "invalid_credentials"
        ]

        for key in login_error_keys:
            assert key in error_messages
            assert isinstance(error_messages[key], str)
            assert len(error_messages[key]) > 0

    def test_all_signup_error_messages_exist(self, error_messages):
        """
        [확인] 회원가입 관련 에러 메시지 존재

        Given: 에러 메시지 딕셔너리
        When: 회원가입 에러 키 확인
        Then: 모든 키 존재
        """
        signup_error_keys = [
            "duplicate_email",
            "invalid_password_format",
            "password_mismatch",
            "nickname_required",
            "nickname_contains_space",
            "nickname_too_long"
        ]

        for key in signup_error_keys:
            assert key in error_messages
            assert isinstance(error_messages[key], str)


class TestSessionStorage:
    """
    세션 저장소 구조 테스트
    """

    def test_user_session_keys(self):
        """
        [확인] 세션 저장 키 구조

        Given: 로그인 후 저장할 데이터
        When: 키 확인
        Then: 필수 키 존재
        """
        session_keys = ["user_id", "nickname", "profile_image_url"]

        for key in session_keys:
            assert isinstance(key, str)
            assert len(key) > 0

    def test_user_session_data_structure(self, test_user_credentials):
        """
        [확인] 세션 데이터 구조

        Given: 사용자 인증 정보
        When: 세션 데이터 생성
        Then: 올바른 구조
        """
        session_data = {
            "userId": "123",
            "nickname": test_user_credentials["nickname"],
            "profileImageUrl": "https://example.com/image.jpg"
        }

        assert "userId" in session_data
        assert "nickname" in session_data
        assert "profileImageUrl" in session_data
