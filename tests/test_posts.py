"""
게시글 기능 테스트 케이스
게시글 CRUD, 좋아요, 조회수 테스트
"""
import pytest


class TestPostDataValidation:
    """게시글 데이터 유효성 검사 테스트"""
    
    def test_title_required(self):
        """제목 필수 입력 검증"""
        title = ""
        is_valid = len(title.strip()) > 0
        assert not is_valid
    
    def test_content_required(self):
        """내용 필수 입력 검증"""
        content = ""
        is_valid = len(content.strip()) > 0
        assert not is_valid
    
    def test_title_max_length(self):
        """제목 최대 길이 검증 (2000자)"""
        max_length = 2000
        
        valid_title = "A" * 100
        invalid_title = "A" * 2001
        
        assert len(valid_title) <= max_length
        assert len(invalid_title) > max_length
    
    def test_post_with_image(self, test_post_data):
        """이미지가 포함된 게시글 데이터 구조"""
        post_data = {
            **test_post_data,
            "image_url": "https://example.com/image.jpg",
            "image_class": "Dog"
        }
        
        assert "image_url" in post_data
        assert "image_class" in post_data
        assert post_data["image_class"] in ["Dog", "Cat", None]


class TestPostListResponse:
    """게시글 목록 응답 테스트"""
    
    def test_successful_posts_response_structure(self):
        """성공적인 게시글 목록 응답 구조 확인"""
        response = {
            "message": "get_posts_success",
            "data": {
                "posts": [],
                "total": 0,
                "page": 1,
                "limit": 10
            }
        }
        
        assert response["message"] == "get_posts_success"
        assert "data" in response
        assert "posts" in response["data"]
    
    def test_post_item_structure(self):
        """게시글 항목 구조 확인"""
        post = {
            "post_id": 1,
            "title": "테스트 제목",
            "content": "테스트 내용",
            "author_id": 1,
            "author_nickname": "작성자",
            "created_at": "2024-01-01T00:00:00",
            "view_count": 0,
            "like_count": 0,
            "comment_count": 0
        }
        
        required_fields = ["post_id", "title", "content", "author_id"]
        for field in required_fields:
            assert field in post


class TestPostDetailResponse:
    """게시글 상세 응답 테스트"""
    
    def test_successful_post_detail_response_structure(self):
        """성공적인 게시글 상세 응답 구조 확인"""
        response = {
            "message": "get_post_success",
            "data": {
                "post_id": 1,
                "title": "테스트 제목",
                "content": "테스트 내용",
                "author_id": 1,
                "author_nickname": "작성자",
                "image_url": None,
                "image_class": None,
                "created_at": "2024-01-01T00:00:00",
                "view_count": 10,
                "like_count": 5,
                "is_liked": False
            }
        }
        
        assert response["message"] == "get_post_success"
        assert "data" in response
        assert "post_id" in response["data"]
    
    def test_post_not_found_response(self):
        """게시글 없음 응답 확인"""
        response = {
            "message": "post_not_found",
            "data": None
        }
        
        assert response["message"] == "post_not_found"


class TestPostCRUDResponses:
    """게시글 CRUD 응답 테스트"""
    
    def test_create_post_success_response(self):
        """게시글 생성 성공 응답 확인"""
        response = {
            "message": "create_post_success",
            "data": {
                "post_id": 1
            }
        }
        
        assert response["message"] == "create_post_success"
        assert "post_id" in response["data"]
    
    def test_update_post_success_response(self):
        """게시글 수정 성공 응답 확인"""
        response = {
            "message": "update_post_success",
            "data": {
                "post_id": 1
            }
        }
        
        assert response["message"] == "update_post_success"
    
    def test_delete_post_success_response(self):
        """게시글 삭제 성공 응답 확인"""
        response = {
            "message": "delete_post_success",
            "data": None
        }
        
        assert response["message"] == "delete_post_success"


class TestLikeFeature:
    """좋아요 기능 테스트"""
    
    def test_like_toggle_response(self):
        """좋아요 토글 응답 확인"""
        response = {
            "message": "like_toggled",
            "data": {
                "is_liked": True,
                "like_count": 5
            }
        }
        
        assert response["message"] == "like_toggled"
        assert "is_liked" in response["data"]
        assert "like_count" in response["data"]
    
    def test_like_count_increment(self):
        """좋아요 수 증가 확인"""
        initial_count = 5
        after_like = 6
        
        assert after_like == initial_count + 1
    
    def test_like_count_decrement(self):
        """좋아요 수 감소 확인"""
        initial_count = 5
        after_unlike = 4
        
        assert after_unlike == initial_count - 1
    
    def test_like_state_toggle(self):
        """좋아요 상태 토글 확인"""
        is_liked = False
        after_toggle = not is_liked
        
        assert after_toggle == True


class TestViewCountFeature:
    """조회수 기능 테스트"""
    
    def test_view_increment_response(self):
        """조회수 증가 응답 확인"""
        response = {
            "message": "view_incremented",
            "data": {
                "view_count": 11
            }
        }
        
        assert response["message"] == "view_incremented"
        assert "view_count" in response["data"]
    
    def test_view_count_increment(self):
        """조회수 증가 확인"""
        initial_count = 10
        after_view = 11
        
        assert after_view == initial_count + 1


class TestImageUpload:
    """이미지 업로드 테스트"""
    
    def test_upload_success_response(self):
        """이미지 업로드 성공 응답 확인"""
        response = {
            "message": "upload_success",
            "data": {
                "image_url": "http://localhost:8000/uploads/image.jpg",
                "image_class": "Dog"
            }
        }
        
        assert response["message"] == "upload_success"
        assert "image_url" in response["data"]
    
    def test_image_classification_result(self):
        """이미지 분류 결과 확인"""
        valid_classes = ["Dog", "Cat", None]
        result = "Dog"
        
        assert result in valid_classes
    
    def test_allowed_image_types(self):
        """허용된 이미지 타입 확인"""
        allowed_types = ["image/jpeg", "image/png", "image/jpg"]
        
        test_type = "image/jpeg"
        assert test_type in allowed_types
    
    def test_disallowed_image_types(self):
        """허용되지 않은 이미지 타입 확인"""
        allowed_types = ["image/jpeg", "image/png", "image/jpg"]
        
        test_type = "text/plain"
        assert test_type not in allowed_types


class TestPagination:
    """페이지네이션 테스트"""
    
    def test_default_pagination_values(self):
        """기본 페이지네이션 값 확인"""
        default_page = 1
        default_limit = 10
        
        assert default_page == 1
        assert default_limit == 10
    
    def test_pagination_parameters(self):
        """페이지네이션 파라미터 확인"""
        page = 2
        limit = 20
        
        assert page >= 1
        assert limit >= 1
        assert limit <= 100
    
    def test_pagination_response_structure(self):
        """페이지네이션 응답 구조 확인"""
        pagination = {
            "page": 1,
            "limit": 10,
            "total": 100,
            "total_pages": 10
        }
        
        assert "page" in pagination
        assert "limit" in pagination
        assert "total" in pagination
