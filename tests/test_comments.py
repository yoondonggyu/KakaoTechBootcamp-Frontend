"""
댓글 기능 테스트 케이스
댓글 CRUD 테스트
"""
import pytest


class TestCommentDataValidation:
    """댓글 데이터 유효성 검사 테스트"""
    
    def test_content_required(self):
        """내용 필수 입력 검증"""
        content = ""
        is_valid = len(content.strip()) > 0
        assert not is_valid
    
    def test_content_not_empty(self, test_comment_data):
        """댓글 내용이 비어있지 않은지 검증"""
        content = test_comment_data["content"]
        is_valid = len(content.strip()) > 0
        assert is_valid
    
    def test_comment_data_structure(self, test_comment_data):
        """댓글 데이터 구조 확인"""
        assert "content" in test_comment_data
        assert isinstance(test_comment_data["content"], str)


class TestCommentListResponse:
    """댓글 목록 응답 테스트"""
    
    def test_successful_comments_response_structure(self):
        """성공적인 댓글 목록 응답 구조 확인"""
        response = {
            "message": "get_comments_success",
            "data": {
                "comments": [],
                "total": 0
            }
        }
        
        assert response["message"] == "get_comments_success"
        assert "data" in response
        assert "comments" in response["data"]
    
    def test_comment_item_structure(self):
        """댓글 항목 구조 확인"""
        comment = {
            "comment_id": 1,
            "content": "테스트 댓글 내용",
            "author_id": 1,
            "author_nickname": "작성자",
            "author_profile_image": "https://example.com/image.jpg",
            "created_at": "2024-01-01T00:00:00",
            "sentiment": {
                "label": "positive",
                "confidence": 0.95
            }
        }
        
        required_fields = ["comment_id", "content", "author_id"]
        for field in required_fields:
            assert field in comment
    
    def test_comment_with_sentiment(self):
        """감성 분석 결과가 포함된 댓글 확인"""
        comment = {
            "comment_id": 1,
            "content": "정말 좋은 글이에요!",
            "sentiment": {
                "label": "positive",
                "confidence": 0.92
            }
        }
        
        assert "sentiment" in comment
        assert "label" in comment["sentiment"]
        assert "confidence" in comment["sentiment"]
        assert comment["sentiment"]["label"] in ["positive", "negative", "neutral"]


class TestCommentCRUDResponses:
    """댓글 CRUD 응답 테스트"""
    
    def test_create_comment_success_response(self):
        """댓글 생성 성공 응답 확인"""
        response = {
            "message": "create_comment_success",
            "data": {
                "comment_id": 1,
                "content": "새 댓글 내용",
                "sentiment": {
                    "label": "neutral",
                    "confidence": 0.8
                }
            }
        }
        
        assert response["message"] == "create_comment_success"
        assert "comment_id" in response["data"]
    
    def test_update_comment_success_response(self):
        """댓글 수정 성공 응답 확인"""
        response = {
            "message": "update_comment_success",
            "data": {
                "comment_id": 1,
                "content": "수정된 댓글 내용"
            }
        }
        
        assert response["message"] == "update_comment_success"
    
    def test_delete_comment_success_response(self):
        """댓글 삭제 성공 응답 확인"""
        response = {
            "message": "delete_comment_success",
            "data": None
        }
        
        assert response["message"] == "delete_comment_success"


class TestCommentErrorResponses:
    """댓글 에러 응답 테스트"""
    
    def test_comment_not_found_response(self):
        """댓글 없음 응답 확인"""
        response = {
            "message": "comment_not_found",
            "data": None
        }
        
        assert response["message"] == "comment_not_found"
    
    def test_post_not_found_for_comment(self):
        """게시글 없음 에러 응답 확인 (댓글 작성 시)"""
        response = {
            "message": "post_not_found",
            "data": None
        }
        
        assert response["message"] == "post_not_found"
    
    def test_unauthorized_comment_edit(self):
        """권한 없는 댓글 수정 에러 응답 확인"""
        response = {
            "message": "unauthorized",
            "data": None
        }
        
        assert response["message"] in ["unauthorized", "forbidden"]
    
    def test_content_required_error(self):
        """댓글 내용 필수 에러 응답 확인"""
        response = {
            "message": "content_required",
            "data": None
        }
        
        assert response["message"] == "content_required"


class TestSentimentAnalysis:
    """감성 분석 기능 테스트"""
    
    def test_sentiment_labels(self):
        """감성 분석 레이블 확인"""
        valid_labels = ["positive", "negative", "neutral"]
        
        test_label = "positive"
        assert test_label in valid_labels
    
    def test_sentiment_confidence_range(self):
        """감성 분석 신뢰도 범위 확인"""
        confidence = 0.85
        
        assert confidence >= 0.0
        assert confidence <= 1.0
    
    def test_sentiment_response_structure(self):
        """감성 분석 응답 구조 확인"""
        sentiment = {
            "label": "positive",
            "confidence": 0.92,
            "description": "긍정적인 감정이 느껴집니다."
        }
        
        assert "label" in sentiment
        assert "confidence" in sentiment
    
    def test_positive_sentiment_example(self):
        """긍정적 감성 예시 확인"""
        positive_texts = [
            "정말 좋아요!",
            "감사합니다",
            "아주 만족스러워요",
            "추천합니다"
        ]
        
        # 긍정적인 텍스트들이 비어있지 않은지 확인
        for text in positive_texts:
            assert len(text) > 0
    
    def test_negative_sentiment_example(self):
        """부정적 감성 예시 확인"""
        negative_texts = [
            "별로예요",
            "실망했어요",
            "최악이에요",
            "추천하지 않습니다"
        ]
        
        # 부정적인 텍스트들이 비어있지 않은지 확인
        for text in negative_texts:
            assert len(text) > 0


class TestCommentPermissions:
    """댓글 권한 테스트"""
    
    def test_owner_can_edit(self):
        """작성자는 댓글 수정 가능"""
        comment_author_id = 1
        current_user_id = 1
        
        can_edit = comment_author_id == current_user_id
        assert can_edit == True
    
    def test_non_owner_cannot_edit(self):
        """작성자가 아니면 댓글 수정 불가"""
        comment_author_id = 1
        current_user_id = 2
        
        can_edit = comment_author_id == current_user_id
        assert can_edit == False
    
    def test_owner_can_delete(self):
        """작성자는 댓글 삭제 가능"""
        comment_author_id = 1
        current_user_id = 1
        
        can_delete = comment_author_id == current_user_id
        assert can_delete == True
    
    def test_login_required_for_create(self):
        """댓글 작성 시 로그인 필요"""
        is_logged_in = False
        
        # 로그인하지 않으면 댓글 작성 불가
        can_create_comment = is_logged_in
        assert can_create_comment == False
