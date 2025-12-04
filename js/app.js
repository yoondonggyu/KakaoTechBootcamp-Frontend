/**
 * 앱 초기화 및 라우팅
 */

// 현재 페이지
let currentPage = 'login';

// ========================================
// 페이지 전환 (SPA 방식)
// ========================================

function navigateTo(page) {
    // 모든 페이지 숨기기
    document.querySelectorAll('.page').forEach(p => {
        p.classList.remove('active');
    });

    // 해당 페이지 표시
    const pageElement = document.getElementById(`page-${page}`);
    if (pageElement) {
        pageElement.classList.add('active');
    }

    currentPage = page;

    // 페이지별 초기화
    switch (page) {
        case 'posts':
            loadPosts();
            updateHeader(true);
            break;
        case 'post-detail':
            updateHeader(true, true);
            break;
        case 'create-post':
            updateHeader(true, true);
            break;
        case 'login':
        case 'signup':
            updateHeader(false);
            break;
    }
}

function updateHeader(showProfile = false, showBack = false) {
    const header = document.getElementById('main-header');
    const backBtn = document.getElementById('header-back-btn');
    const profileBtn = document.getElementById('header-profile-btn');

    if (showBack) {
        backBtn.style.display = 'block';
    } else {
        backBtn.style.display = 'none';
    }

    if (showProfile && Auth.isLoggedIn()) {
        profileBtn.style.display = 'flex';
    } else {
        profileBtn.style.display = 'none';
    }
}

function goBack() {
    if (currentPage === 'post-detail' || currentPage === 'create-post') {
        navigateTo('posts');
    }
}

// ========================================
// 유틸리티 함수
// ========================================

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

// ========================================
// Toast 알림
// ========================================

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.textContent = message;

    container.appendChild(toast);

    // 애니메이션
    setTimeout(() => toast.classList.add('show'), 10);

    // 3초 후 제거
    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// ========================================
// Modal
// ========================================

let modalConfirmCallback = null;

function showModal(title, message, onConfirm) {
    const overlay = document.getElementById('modal-overlay');
    document.getElementById('modal-title').textContent = title;
    document.getElementById('modal-message').textContent = message;
    modalConfirmCallback = onConfirm;
    overlay.classList.add('active');
}

function hideModal() {
    const overlay = document.getElementById('modal-overlay');
    overlay.classList.remove('active');
    modalConfirmCallback = null;
}

function confirmModal() {
    if (modalConfirmCallback) {
        modalConfirmCallback();
    }
}

// ========================================
// 초기화
// ========================================

document.addEventListener('DOMContentLoaded', () => {
    // 로그인 상태 확인
    if (Auth.isLoggedIn()) {
        navigateTo('posts');
    } else {
        navigateTo('login');
    }

    // 이벤트 리스너 등록

    // 로그인 폼
    document.getElementById('login-form').addEventListener('submit', Auth.handleLogin);

    // 회원가입 폼
    document.getElementById('signup-form').addEventListener('submit', Auth.handleSignup);

    // 프로필 이미지 업로드
    document.getElementById('signup-profile-input').addEventListener('change', Auth.handleProfileImageUpload);

    // 게시글 이미지 업로드
    document.getElementById('post-image-input').addEventListener('change', Posts.handlePostImageUpload);

    // 모달 이벤트
    document.getElementById('modal-cancel').addEventListener('click', hideModal);
    document.getElementById('modal-confirm').addEventListener('click', confirmModal);
    document.getElementById('modal-overlay').addEventListener('click', (e) => {
        if (e.target === e.currentTarget) {
            hideModal();
        }
    });
});

// 전역 함수들
window.navigateTo = navigateTo;
window.goBack = goBack;
window.showToast = showToast;
window.showModal = showModal;
window.hideModal = hideModal;
window.escapeHtml = escapeHtml;
window.formatDate = formatDate;

// Posts 모듈의 함수들을 전역으로 노출
window.loadPosts = () => Posts.loadPosts();
window.viewPost = (id) => Posts.viewPost(id);
window.showCreatePost = () => Posts.showCreatePost();
window.editPost = (id) => Posts.editPost(id);
window.submitPost = () => Posts.submitPost();
window.confirmDeletePost = (id) => Posts.confirmDeletePost(id);
window.handleLike = (id) => Posts.handleLike(id);
window.submitComment = () => Posts.submitComment();
window.editComment = (postId, commentId, content) => Posts.editComment(postId, commentId, content);
window.confirmDeleteComment = (postId, commentId) => Posts.confirmDeleteComment(postId, commentId);
