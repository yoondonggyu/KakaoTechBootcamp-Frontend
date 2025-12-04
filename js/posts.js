/**
 * 게시글 관련 기능
 */

let currentPostId = null;
let editingCommentId = null;

// ========================================
// 게시글 목록
// ========================================

async function loadPosts() {
    const postsContainer = document.getElementById('posts-list');
    postsContainer.innerHTML = '<div class="loading"><div class="spinner"></div></div>';

    const result = await API.getPosts(1, 20);

    if (result.ok) {
        const posts = result.data.data.posts;

        if (posts.length === 0) {
            postsContainer.innerHTML = `
        <div class="empty-state">
          <svg viewBox="0 0 24 24"><path d="M19 5v14H5V5h14m0-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z"/></svg>
          <p>아직 게시글이 없습니다.<br>첫 게시글을 작성해보세요!</p>
        </div>
      `;
            return;
        }

        postsContainer.innerHTML = posts.map(post => `
      <div class="card post-card" onclick="viewPost(${post.post_id})">
        <div class="card-title">${escapeHtml(post.title)}</div>
        <div class="card-meta">
          <span>좋아요 ${post.like_count}</span>
          <span>댓글 ${post.comment_count}</span>
          <span>조회수 ${post.view_count}</span>
        </div>
        <div class="card-author">
          <div class="card-author-avatar"></div>
          <span class="card-author-name">${escapeHtml(post.nickname)}</span>
          <span class="card-date">${formatDate(post.created_at)}</span>
        </div>
      </div>
    `).join('');
    } else {
        postsContainer.innerHTML = '<div class="empty-state"><p>게시글을 불러오는데 실패했습니다.</p></div>';
    }
}

// ========================================
// 게시글 상세
// ========================================

async function viewPost(postId) {
    currentPostId = postId;
    navigateTo('post-detail');

    // 조회수 증가
    await API.incrementViewCount(postId);

    const result = await API.getPost(postId);

    if (result.ok) {
        const post = result.data.data;
        renderPostDetail(post);
    } else {
        showToast('게시글을 불러오는데 실패했습니다', 'error');
        navigateTo('posts');
    }
}

function renderPostDetail(post) {
    const user = Auth.getCurrentUser();
    const isOwner = user.userId && parseInt(user.userId) === post.user_id;

    document.getElementById('post-detail-content').innerHTML = `
    <div class="post-detail-header">
      <h2 class="post-detail-title">${escapeHtml(post.title)}</h2>
      <div class="post-detail-meta">
        <div class="post-detail-author">
          <div class="card-author-avatar"></div>
          <span>${escapeHtml(post.nickname)}</span>
          <span class="card-date">${formatDate(post.created_at)}</span>
        </div>
        ${isOwner ? `
          <div class="post-detail-actions">
            <button class="btn btn-secondary btn-small" onclick="editPost(${post.post_id})">수정</button>
            <button class="btn btn-secondary btn-small" onclick="confirmDeletePost(${post.post_id})">삭제</button>
          </div>
        ` : ''}
      </div>
    </div>
    
    <div class="post-detail-content">
      ${post.image_url ? `
        <img src="${post.image_url}" alt="게시글 이미지" class="post-detail-image">
        <div class="ai-result" id="image-classification-result">
          <span class="ai-label">🤖 AI 이미지 분류:</span>
          ${post.image_class ? `
            <span class="ai-value ${post.image_class.toLowerCase() === 'dog' ? 'ai-dog' : 'ai-cat'}">
              ${post.image_class.toLowerCase() === 'dog' ? '🐕 강아지' : '🐈 고양이'}
            </span>
          ` : `
            <span class="ai-value ai-neutral">분류 정보 없음</span>
          `}
        </div>
      ` : ''}
      <div class="post-detail-text">${escapeHtml(post.content)}</div>
      <div class="ai-result" id="sentiment-analysis-result">
        <span class="ai-label">💭 AI 감정 분석:</span>
        <span class="ai-value">분석 중...</span>
      </div>
    </div>
    
    <div class="post-detail-stats">
      <div class="stat-item" id="like-button" onclick="handleLike(${post.post_id})" style="cursor: pointer;">
        <div class="stat-value" id="like-count">${post.like_count}</div>
        <div class="stat-label">좋아요</div>
      </div>
      <div class="stat-item">
        <div class="stat-value">${post.view_count}</div>
        <div class="stat-label">조회수</div>
      </div>
      <div class="stat-item">
        <div class="stat-value" id="comment-count">${post.comments ? post.comments.length : 0}</div>
        <div class="stat-label">댓글</div>
      </div>
    </div>
    
    <div class="comments-section">
      <div class="comment-form">
        <input type="text" class="comment-input" id="comment-input" placeholder="댓글을 남겨주세요">
        <button class="comment-submit" onclick="submitComment()">댓글 등록</button>
      </div>
      <div id="comments-list">
        ${renderComments(post.comments || [], post.post_id)}
      </div>
    </div>
  `;

    // 댓글 입력 엔터키 처리
    document.getElementById('comment-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            submitComment();
        }
    });

    // AI 감정 분석 실행
    analyzePostSentiment(post.content);
}

function renderComments(comments, postId) {
    const user = Auth.getCurrentUser();

    if (comments.length === 0) {
        return '<div class="empty-state"><p>아직 댓글이 없습니다.</p></div>';
    }

    return comments.map(comment => {
        const isOwner = user.userId && parseInt(user.userId) === comment.user_id;
        return `
      <div class="comment-item" id="comment-${comment.comment_id}">
        <div class="comment-header">
          <div class="comment-author">
            <div class="comment-author-avatar"></div>
            <span class="comment-author-name">${escapeHtml(comment.nickname)}</span>
          </div>
          <span class="comment-date">${formatDate(comment.created_at)}</span>
        </div>
        <div class="comment-content">${escapeHtml(comment.content)}</div>
        ${isOwner ? `
          <div class="comment-actions">
            <button class="comment-action-btn" onclick="editComment(${postId}, ${comment.comment_id}, '${escapeHtml(comment.content)}')">수정</button>
            <button class="comment-action-btn" onclick="confirmDeleteComment(${postId}, ${comment.comment_id})">삭제</button>
          </div>
        ` : ''}
      </div>
    `;
    }).join('');
}

// ========================================
// 좋아요
// ========================================

async function handleLike(postId) {
    if (!Auth.isLoggedIn()) {
        showToast('로그인이 필요합니다', 'error');
        return;
    }

    const result = await API.toggleLike(postId);

    if (result.ok) {
        const likeCount = result.data.data.like_count;
        const liked = result.data.data.liked;
        document.getElementById('like-count').textContent = likeCount;
        showToast(liked ? '좋아요!' : '좋아요 취소', 'success');
    } else {
        showToast('좋아요 처리 실패', 'error');
    }
}

// ========================================
// 게시글 작성/수정
// ========================================

let editingPostId = null;
let postImageUrl = null;
let postImageClass = null;  // 이미지 분류 결과 저장

function showCreatePost() {
    editingPostId = null;
    postImageUrl = null;
    postImageClass = null;
    document.getElementById('create-post-title').textContent = '게시글 작성';
    document.getElementById('post-form').reset();
    document.getElementById('post-image-preview').style.display = 'none';
    const classificationPreview = document.getElementById('image-classification-preview');
    if (classificationPreview) classificationPreview.style.display = 'none';
    navigateTo('create-post');
}

async function editPost(postId) {
    editingPostId = postId;
    const result = await API.getPost(postId);

    if (result.ok) {
        const post = result.data.data;
        document.getElementById('create-post-title').textContent = '게시글 수정';
        document.getElementById('post-title-input').value = post.title;
        document.getElementById('post-content-input').value = post.content;

        if (post.image_url) {
            postImageUrl = post.image_url;
            const preview = document.getElementById('post-image-preview');
            preview.src = post.image_url;
            preview.style.display = 'block';
        }

        navigateTo('create-post');
    } else {
        showToast('게시글을 불러오는데 실패했습니다', 'error');
    }
}

async function handlePostImageUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const preview = document.getElementById('post-image-preview');
    const classificationResult = document.getElementById('image-classification-preview');

    // 미리보기 표시
    const reader = new FileReader();
    reader.onload = (e) => {
        preview.src = e.target.result;
        preview.style.display = 'block';
    };
    reader.readAsDataURL(file);

    // 분류 결과 로딩 표시
    if (classificationResult) {
        classificationResult.innerHTML = `
            <span class="ai-label">🤖 AI 이미지 분류:</span>
            <span class="ai-value">분석 중...</span>
        `;
        classificationResult.style.display = 'flex';
    }

    // 서버에 업로드
    const result = await API.uploadPostImage(file);

    if (result.ok) {
        postImageUrl = result.data.data.image_url;

        // Model API 결과 표시
        const prediction = result.data.data.prediction;
        if (prediction) {
            postImageClass = prediction.class_name;  // 분류 결과 저장
            const className = prediction.class_name.toLowerCase() === 'dog' ? '강아지' : '고양이';
            const emoji = prediction.class_name.toLowerCase() === 'dog' ? '🐕' : '🐈';
            const confidence = (prediction.confidence_score * 100).toFixed(1);
            const cssClass = prediction.class_name.toLowerCase() === 'dog' ? 'ai-dog' : 'ai-cat';

            if (classificationResult) {
                classificationResult.innerHTML = `
                    <span class="ai-label">🤖 AI 이미지 분류:</span>
                    <span class="ai-value ${cssClass}">${emoji} ${className} (${confidence}%)</span>
                `;
            }
            showToast(`이미지 분류: ${className} (${confidence}%)`, 'success');
        } else {
            postImageClass = null;
            if (classificationResult) {
                classificationResult.innerHTML = `
                    <span class="ai-label">🤖 AI 이미지 분류:</span>
                    <span class="ai-value ai-neutral">분류 실패</span>
                `;
            }
            showToast('이미지 업로드 완료', 'success');
        }
    } else {
        showToast('이미지 업로드 실패', 'error');
        postImageUrl = null;
        if (classificationResult) {
            classificationResult.style.display = 'none';
        }
    }
}

async function submitPost() {
    const title = document.getElementById('post-title-input').value.trim();
    const content = document.getElementById('post-content-input').value.trim();

    if (!title) {
        showToast('제목을 입력해주세요', 'error');
        return;
    }

    if (!content) {
        showToast('내용을 입력해주세요', 'error');
        return;
    }

    let result;

    if (editingPostId) {
        result = await API.updatePost(editingPostId, title, content, postImageUrl, postImageClass);
    } else {
        result = await API.createPost(title, content, postImageUrl, postImageClass);
    }

    if (result.ok) {
        showToast(editingPostId ? '게시글이 수정되었습니다' : '게시글이 작성되었습니다', 'success');
        navigateTo('posts');
        loadPosts();
    } else {
        const errorMessages = {
            'title_too_long': '제목은 최대 26자까지 작성 가능합니다',
            'missing_fields': '제목과 내용을 입력해주세요',
        };
        showToast(errorMessages[result.data.message] || '게시글 저장 실패', 'error');
    }
}

// ========================================
// 게시글 삭제
// ========================================

function confirmDeletePost(postId) {
    showModal(
        '게시글을 삭제하시겠습니까?',
        '삭제된 내용은 복구 할 수 없습니다.',
        () => deletePostConfirmed(postId)
    );
}

async function deletePostConfirmed(postId) {
    const result = await API.deletePost(postId);

    if (result.ok) {
        showToast('게시글이 삭제되었습니다', 'success');
        navigateTo('posts');
        loadPosts();
    } else {
        showToast('게시글 삭제 실패', 'error');
    }

    hideModal();
}

// ========================================
// 댓글 CRUD
// ========================================

async function submitComment() {
    if (!Auth.isLoggedIn()) {
        showToast('로그인이 필요합니다', 'error');
        return;
    }

    const input = document.getElementById('comment-input');
    const content = input.value.trim();

    if (!content) {
        showToast('댓글 내용을 입력해주세요', 'error');
        return;
    }

    let result;

    if (editingCommentId) {
        result = await API.updateComment(currentPostId, editingCommentId, content);
    } else {
        result = await API.createComment(currentPostId, content);
    }

    if (result.ok) {
        input.value = '';
        editingCommentId = null;

        // 감성 분석 결과 표시
        const sentiment = result.data.data?.sentiment;
        if (sentiment) {
            const label = sentiment.label === 'positive' ? '긍정적' : '부정적';
            const confidence = (sentiment.confidence * 100).toFixed(0);
            showToast(`댓글 등록! (${label} ${confidence}%)`, 'success');
        } else {
            showToast(editingCommentId ? '댓글이 수정되었습니다' : '댓글이 등록되었습니다', 'success');
        }

        // 게시글 다시 로드
        viewPost(currentPostId);
    } else {
        showToast('댓글 저장 실패', 'error');
    }
}

function editComment(postId, commentId, content) {
    editingCommentId = commentId;
    const input = document.getElementById('comment-input');
    input.value = content;
    input.focus();

    // 버튼 텍스트 변경
    document.querySelector('.comment-submit').textContent = '댓글 수정';
}

function confirmDeleteComment(postId, commentId) {
    showModal(
        '댓글을 삭제하시겠습니까?',
        '삭제된 내용은 복구 할 수 없습니다.',
        () => deleteCommentConfirmed(postId, commentId)
    );
}

async function deleteCommentConfirmed(postId, commentId) {
    const result = await API.deleteComment(postId, commentId);

    if (result.ok) {
        showToast('댓글이 삭제되었습니다', 'success');
        viewPost(postId);
    } else {
        showToast('댓글 삭제 실패', 'error');
    }

    hideModal();
}

// ========================================
// AI 감정 분석
// ========================================

async function analyzePostSentiment(content) {
    const resultElement = document.getElementById('sentiment-analysis-result');
    if (!resultElement) return;

    // Gemini API로 감정 분석 (한글/영어 모두 지원)
    const result = await API.analyzeSentimentGemini(content);

    if (result && !result.error) {
        const label = result.label;
        const confidence = (result.confidence * 100).toFixed(1);
        let emoji, labelKr, className;

        if (label === 'positive') {
            emoji = '😊';
            labelKr = '긍정적';
            className = 'ai-positive';
        } else if (label === 'negative') {
            emoji = '😞';
            labelKr = '부정적';
            className = 'ai-negative';
        } else {
            emoji = '😐';
            labelKr = '중립적';
            className = 'ai-neutral';
        }

        resultElement.innerHTML = `
            <span class="ai-label">💭 AI 감정 분석 (Gemini):</span>
            <span class="ai-value ${className}">${emoji} ${labelKr} (${confidence}%)</span>
        `;

        // 설명이 있으면 추가 표시
        if (result.description) {
            resultElement.innerHTML += `
                <div class="ai-description" style="font-size: 0.75rem; color: var(--text-muted); margin-top: 4px;">
                    ${escapeHtml(result.description)}
                </div>
            `;
        }
    } else {
        resultElement.innerHTML = `
            <span class="ai-label">💭 AI 감정 분석:</span>
            <span class="ai-value ai-neutral">분석 실패 (Model API 또는 Gemini API 확인)</span>
        `;
    }
}

// Export
window.Posts = {
    loadPosts,
    viewPost,
    showCreatePost,
    editPost,
    submitPost,
    handlePostImageUpload,
    confirmDeletePost,
    handleLike,
    submitComment,
    editComment,
    confirmDeleteComment,
    analyzePostSentiment,
};
