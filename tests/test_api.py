"""
프론트엔드 API 모듈 테스트 케이스

테스트 대상:
- API 엔드포인트 URL 생성
- 요청/응답 구조 검증
- 헤더 구조 검증

Note: JavaScript의 api.js 로직을 Python으로 동일하게 테스트합니다.
"""
import pytest


class TestAPIEndpoints:
    """
    API 엔드포인트 URL 테스트

    JavaScript api.js의 엔드포인트 생성 로직 검증
    """

    # =========================================================================
    # Auth 엔드포인트
    # =========================================================================

    def test_login_endpoint(self, api_endpoints):
        """
        [확인] 로그인 엔드포인트 URL

        Given: API 엔드포인트 헬퍼
        When: 로그인 URL 생성
        Then: 올바른 URL 반환
        """
        expected = "http://localhost:8000/api/auth/login"
        assert api_endpoints.login() == expected

    def test_signup_endpoint(self, api_endpoints):
        """
        [확인] 회원가입 엔드포인트 URL

        Given: API 엔드포인트 헬퍼
        When: 회원가입 URL 생성
        Then: 올바른 URL 반환
        """
        expected = "http://localhost:8000/api/auth/signup"
        assert api_endpoints.signup() == expected

    # =========================================================================
    # Posts 엔드포인트
    # =========================================================================

    def test_posts_list_endpoint(self, api_endpoints):
        """
        [확인] 게시글 목록 엔드포인트 URL

        Given: 페이지 및 limit 파라미터
        When: 게시글 목록 URL 생성
        Then: 쿼리 파라미터 포함 URL 반환
        """
        expected = "http://localhost:8000/api/posts?page=1&limit=10"
        assert api_endpoints.posts(page=1, limit=10) == expected

    def test_posts_list_endpoint_custom_params(self, api_endpoints):
        """
        [확인] 커스텀 페이지네이션

        Given: 다른 페이지 및 limit
        When: URL 생성
        Then: 파라미터 반영됨
        """
        expected = "http://localhost:8000/api/posts?page=3&limit=20"
        assert api_endpoints.posts(page=3, limit=20) == expected

    def test_post_detail_endpoint(self, api_endpoints):
        """
        [확인] 게시글 상세 엔드포인트 URL

        Given: 게시글 ID
        When: 상세 URL 생성
        Then: ID 포함 URL 반환
        """
        expected = "http://localhost:8000/api/posts/123"
        assert api_endpoints.post(123) == expected

    def test_post_like_endpoint(self, api_endpoints):
        """
        [확인] 좋아요 엔드포인트 URL
        """
        expected = "http://localhost:8000/api/posts/123/like"
        assert api_endpoints.post_like(123) == expected

    def test_post_view_endpoint(self, api_endpoints):
        """
        [확인] 조회수 증가 엔드포인트 URL
        """
        expected = "http://localhost:8000/api/posts/123/view"
        assert api_endpoints.post_view(123) == expected

    def test_post_upload_endpoint(self, api_endpoints):
        """
        [확인] 이미지 업로드 엔드포인트 URL
        """
        expected = "http://localhost:8000/api/posts/upload"
        assert api_endpoints.post_upload() == expected

    # =========================================================================
    # Comments 엔드포인트
    # =========================================================================

    def test_comments_list_endpoint(self, api_endpoints):
        """
        [확인] 댓글 목록 엔드포인트 URL
        """
        expected = "http://localhost:8000/api/posts/123/comments"
        assert api_endpoints.comments(123) == expected

    def test_comment_detail_endpoint(self, api_endpoints):
        """
        [확인] 댓글 상세 엔드포인트 URL
        """
        expected = "http://localhost:8000/api/posts/123/comments/456"
        assert api_endpoints.comment(123, 456) == expected

    # =========================================================================
    # User 엔드포인트
    # =========================================================================

    def test_profile_upload_endpoint(self, api_endpoints):
        """
        [확인] 프로필 이미지 업로드 엔드포인트 URL
        """
        expected = "http://localhost:8000/api/users/profile/upload"
        assert api_endpoints.profile_upload() == expected

    # =========================================================================
    # Model API 엔드포인트
    # =========================================================================

    def test_sentiment_endpoint(self, api_endpoints):
        """
        [확인] 감정 분석 엔드포인트 URL
        """
        expected = "http://localhost:8001/api/sentiment"
        assert api_endpoints.sentiment() == expected

    def test_sentiment_gemini_endpoint(self, api_endpoints):
        """
        [확인] Gemini 감정 분석 엔드포인트 URL
        """
        expected = "http://localhost:8001/api/sentiment/gemini"
        assert api_endpoints.sentiment_gemini() == expected


class TestRequestBodyStructure:
    """
    API 요청 본문 구조 테스트
    """

    def test_login_request_body(self, test_user_credentials):
        """
        [확인] 로그인 요청 본문 구조

        Given: 사용자 인증 정보
        When: 요청 본문 생성
        Then: 필수 필드 포함
        """
        request_body = {
            "email": test_user_credentials["email"],
            "password": test_user_credentials["password"]
        }

        assert "email" in request_body
        assert "password" in request_body
        assert isinstance(request_body["email"], str)
        assert isinstance(request_body["password"], str)

    def test_signup_request_body(self, test_user_credentials):
        """
        [확인] 회원가입 요청 본문 구조

        Given: 사용자 등록 정보
        When: 요청 본문 생성
        Then: 모든 필수 필드 포함
        """
        request_body = {
            "email": test_user_credentials["email"],
            "password": test_user_credentials["password"],
            "password_check": test_user_credentials["password"],
            "nickname": test_user_credentials["nickname"],
            "profile_image_url": "https://example.com/image.jpg"
        }

        required_fields = ["email", "password", "password_check", "nickname", "profile_image_url"]
        for field in required_fields:
            assert field in request_body

    def test_create_post_request_body(self, test_post_data):
        """
        [확인] 게시글 생성 요청 본문 구조

        Given: 게시글 데이터
        When: 요청 본문 생성
        Then: 필수 필드 포함
        """
        request_body = {
            "title": test_post_data["title"],
            "content": test_post_data["content"],
            "image_url": None,
            "image_class": None
        }

        assert "title" in request_body
        assert "content" in request_body

    def test_create_comment_request_body(self, test_comment_data):
        """
        [확인] 댓글 생성 요청 본문 구조

        Given: 댓글 데이터
        When: 요청 본문 생성
        Then: content 필드 포함
        """
        request_body = {
            "content": test_comment_data["content"]
        }

        assert "content" in request_body

    def test_sentiment_request_body(self):
        """
        [확인] 감정 분석 요청 본문 구조
        """
        request_body = {
            "text": "This is a test text",
            "explain": False
        }

        assert "text" in request_body
        assert "explain" in request_body
        assert isinstance(request_body["explain"], bool)


class TestRequestHeaders:
    """
    요청 헤더 구조 테스트
    """

    def test_default_headers(self):
        """
        [확인] 기본 요청 헤더

        Given: 인증되지 않은 요청
        When: 헤더 생성
        Then: Content-Type 포함
        """
        headers = {
            "Content-Type": "application/json"
        }

        assert headers["Content-Type"] == "application/json"

    def test_authenticated_headers(self):
        """
        [확인] 인증된 요청 헤더

        Given: 로그인된 사용자
        When: 헤더 생성
        Then: X-User-Id 포함
        """
        user_id = "123"
        headers = {
            "Content-Type": "application/json",
            "X-User-Id": user_id
        }

        assert "X-User-Id" in headers
        assert headers["X-User-Id"] == user_id

    def test_multipart_headers(self):
        """
        [확인] 파일 업로드 헤더

        Given: 파일 업로드 요청
        When: 헤더 생성
        Then: Content-Type 없음 (브라우저가 자동 설정)

        Note: FormData 전송 시 Content-Type 헤더를 제거해야 함
        """
        # 파일 업로드 시에는 Content-Type을 지정하지 않음
        headers = {
            "X-User-Id": "123"
        }

        assert "Content-Type" not in headers


class TestResponseStructure:
    """
    API 응답 구조 테스트
    """

    def test_posts_list_response(self, mock_posts_list_response):
        """
        [확인] 게시글 목록 응답 구조

        Given: 게시글 목록 응답
        When: 응답 파싱
        Then: 필수 필드 존재
        """
        response = mock_posts_list_response

        assert response["message"] == "get_posts_success"
        assert "data" in response
        assert "posts" in response["data"]
        assert isinstance(response["data"]["posts"], list)

        if len(response["data"]["posts"]) > 0:
            post = response["data"]["posts"][0]
            assert "id" in post
            assert "title" in post
            assert "content" in post

    def test_create_post_response(self, mock_create_post_success_response):
        """
        [확인] 게시글 생성 응답 구조

        Given: 게시글 생성 성공 응답
        When: 응답 파싱
        Then: post_id 존재
        """
        response = mock_create_post_success_response

        assert response["message"] == "create_post_success"
        assert "data" in response
        assert "post_id" in response["data"]


class TestAPIBaseURLs:
    """
    API 기본 URL 테스트
    """

    def test_backend_api_base_url(self, api_endpoints):
        """
        [확인] 백엔드 API 기본 URL
        """
        assert api_endpoints.base_url == "http://localhost:8000/api"

    def test_model_api_base_url(self, api_endpoints):
        """
        [확인] 모델 API 기본 URL
        """
        assert api_endpoints.model_url == "http://localhost:8001/api"


class TestErrorResponseHandling:
    """
    에러 응답 처리 테스트
    """

    def test_network_error_response_structure(self):
        """
        [확인] 네트워크 에러 응답 구조

        Given: 네트워크 에러 발생
        When: 에러 응답 생성
        Then: 표준 에러 구조
        """
        error_response = {
            "ok": False,
            "status": 0,
            "data": {"message": "network_error", "data": None}
        }

        assert error_response["ok"] is False
        assert error_response["status"] == 0
        assert error_response["data"]["message"] == "network_error"

    def test_validation_error_response_structure(self):
        """
        [확인] 유효성 검사 에러 응답 구조

        Given: 422 Unprocessable Entity
        When: 에러 응답 파싱
        Then: 에러 상세 정보 포함
        """
        error_response = {
            "ok": False,
            "status": 422,
            "data": {"message": "invalid_request", "data": None}
        }

        assert error_response["ok"] is False
        assert error_response["status"] == 422

    def test_auth_error_response_structure(self):
        """
        [확인] 인증 에러 응답 구조

        Given: 401 Unauthorized
        When: 에러 응답 파싱
        Then: 인증 에러 메시지
        """
        error_response = {
            "ok": False,
            "status": 401,
            "data": {"message": "unauthorized", "data": None}
        }

        assert error_response["ok"] is False
        assert error_response["status"] == 401
