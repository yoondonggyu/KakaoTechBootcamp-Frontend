/**
 * API 통신 모듈
 * Backend API와의 통신을 담당합니다.
 */

const API_BASE_URL = 'http://localhost:8000/api';

/**
 * API 요청 헬퍼 함수
 */
async function apiRequest(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;

  const defaultHeaders = {
    'Content-Type': 'application/json',
  };

  // 사용자 ID가 있으면 헤더에 추가
  const userId = localStorage.getItem('user_id');
  if (userId) {
    defaultHeaders['X-User-Id'] = userId;
  }

  const config = {
    ...options,
    headers: {
      ...defaultHeaders,
      ...options.headers,
    },
  };

  // body가 있으면 JSON으로 변환 (FormData가 아닌 경우)
  if (config.body && !(config.body instanceof FormData)) {
    config.body = JSON.stringify(config.body);
  }

  // FormData인 경우 Content-Type 헤더 제거 (브라우저가 자동 설정)
  if (config.body instanceof FormData) {
    delete config.headers['Content-Type'];
  }

  try {
    const response = await fetch(url, config);
    const data = await response.json();

    return {
      ok: response.ok,
      status: response.status,
      data: data,
    };
  } catch (error) {
    console.error('API Request Error:', error);
    return {
      ok: false,
      status: 0,
      data: { message: 'network_error', data: null },
    };
  }
}

// ========================================
// 인증 API
// ========================================

/**
 * 로그인
 */
async function login(email, password) {
  return apiRequest('/auth/login', {
    method: 'POST',
    body: { email, password },
  });
}

/**
 * 회원가입
 */
async function signup(email, password, passwordCheck, nickname, profileImageUrl) {
  return apiRequest('/auth/signup', {
    method: 'POST',
    body: {
      email,
      password,
      password_check: passwordCheck,
      nickname,
      profile_image_url: profileImageUrl,
    },
  });
}

/**
 * 프로필 이미지 업로드
 */
async function uploadProfileImage(file) {
  const formData = new FormData();
  formData.append('file', file);

  return apiRequest('/users/profile/upload', {
    method: 'POST',
    body: formData,
  });
}

// ========================================
// 게시글 API
// ========================================

/**
 * 게시글 목록 조회
 */
async function getPosts(page = 1, limit = 10) {
  return apiRequest(`/posts?page=${page}&limit=${limit}`, {
    method: 'GET',
  });
}

/**
 * 게시글 상세 조회
 */
async function getPost(postId) {
  return apiRequest(`/posts/${postId}`, {
    method: 'GET',
  });
}

/**
 * 게시글 작성
 */
async function createPost(title, content, imageUrl = null, imageClass = null) {
  return apiRequest('/posts', {
    method: 'POST',
    body: { title, content, image_url: imageUrl, image_class: imageClass },
  });
}

/**
 * 게시글 수정
 */
async function updatePost(postId, title, content, imageUrl = null, imageClass = null) {
  return apiRequest(`/posts/${postId}`, {
    method: 'PATCH',
    body: { title, content, image_url: imageUrl, image_class: imageClass },
  });
}

/**
 * 게시글 삭제
 */
async function deletePost(postId) {
  return apiRequest(`/posts/${postId}`, {
    method: 'DELETE',
  });
}

/**
 * 좋아요 토글
 */
async function toggleLike(postId) {
  return apiRequest(`/posts/${postId}/like`, {
    method: 'POST',
  });
}

/**
 * 조회수 증가
 */
async function incrementViewCount(postId) {
  return apiRequest(`/posts/${postId}/view`, {
    method: 'PATCH',
  });
}

/**
 * 게시글 이미지 업로드
 */
async function uploadPostImage(file) {
  const formData = new FormData();
  formData.append('file', file);

  return apiRequest('/posts/upload', {
    method: 'POST',
    body: formData,
  });
}

// ========================================
// 댓글 API
// ========================================

/**
 * 댓글 목록 조회
 */
async function getComments(postId) {
  return apiRequest(`/posts/${postId}/comments`, {
    method: 'GET',
  });
}

/**
 * 댓글 작성
 */
async function createComment(postId, content) {
  return apiRequest(`/posts/${postId}/comments`, {
    method: 'POST',
    body: { content },
  });
}

/**
 * 댓글 수정
 */
async function updateComment(postId, commentId, content) {
  return apiRequest(`/posts/${postId}/comments/${commentId}`, {
    method: 'PATCH',
    body: { content },
  });
}

/**
 * 댓글 삭제
 */
async function deleteComment(postId, commentId) {
  return apiRequest(`/posts/${postId}/comments/${commentId}`, {
    method: 'DELETE',
  });
}

// ========================================
// Model API (AI 분석)
// ========================================

const MODEL_API_URL = 'http://localhost:8001/api';

/**
 * 감정 분석 API (기존 ML 모델 - 영어만 지원)
 */
async function analyzeSentiment(text) {
  try {
    const response = await fetch(`${MODEL_API_URL}/sentiment`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text, explain: false }),
    });

    if (response.ok) {
      return await response.json();
    }
    return null;
  } catch (error) {
    console.error('Sentiment API Error:', error);
    return null;
  }
}

/**
 * Gemini 기반 감정 분석 API (한글/영어 모두 지원)
 */
async function analyzeSentimentGemini(text) {
  try {
    const response = await fetch(`${MODEL_API_URL}/sentiment/gemini`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ text, explain: false }),
    });

    if (response.ok) {
      return await response.json();
    }
    return null;
  } catch (error) {
    console.error('Gemini Sentiment API Error:', error);
    return null;
  }
}

// Export for use in other modules
window.API = {
  login,
  signup,
  uploadProfileImage,
  getPosts,
  getPost,
  createPost,
  updatePost,
  deletePost,
  toggleLike,
  incrementViewCount,
  uploadPostImage,
  getComments,
  createComment,
  updateComment,
  deleteComment,
  analyzeSentiment,
  analyzeSentimentGemini,
};
