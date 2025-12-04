/**
 * 인증 관련 기능
 * 로그인, 회원가입, 세션 관리
 */

// ========================================
// 세션 관리
// ========================================

function isLoggedIn() {
    return localStorage.getItem('user_id') !== null;
}

function getCurrentUser() {
    return {
        userId: localStorage.getItem('user_id'),
        nickname: localStorage.getItem('nickname'),
        profileImageUrl: localStorage.getItem('profile_image_url'),
    };
}

function setCurrentUser(userId, nickname, profileImageUrl) {
    localStorage.setItem('user_id', userId);
    localStorage.setItem('nickname', nickname);
    if (profileImageUrl) {
        localStorage.setItem('profile_image_url', profileImageUrl);
    }
}

function clearCurrentUser() {
    localStorage.removeItem('user_id');
    localStorage.removeItem('nickname');
    localStorage.removeItem('profile_image_url');
}

// ========================================
// 로그인 처리
// ========================================

async function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-password').value;
    const helperText = document.getElementById('login-helper');

    // 입력 검증
    if (!email) {
        helperText.textContent = '이메일을 입력해주세요';
        return;
    }

    if (!password) {
        helperText.textContent = '비밀번호를 입력해주세요';
        return;
    }

    helperText.textContent = '';

    const result = await API.login(email, password);

    if (result.ok && result.data.message === 'login_success') {
        const userData = result.data.data;
        setCurrentUser(userData.user_id, userData.nickname, userData.profile_image_url);
        showToast('로그인 성공!', 'success');
        navigateTo('posts');
    } else {
        const errorMessages = {
            'email_required': '이메일을 입력해주세요',
            'invalid_email_format': '올바른 이메일 주소 형식을 입력해주세요',
            'password_required': '비밀번호를 입력해주세요',
            'invalid_credentials': '아이디 또는 비밀번호를 확인해주세요',
        };
        helperText.textContent = errorMessages[result.data.message] || '로그인에 실패했습니다';
    }
}

// ========================================
// 회원가입 처리
// ========================================

let signupProfileImageUrl = null;

async function handleProfileImageUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const preview = document.getElementById('signup-profile-preview');
    const placeholder = document.getElementById('signup-profile-placeholder');

    // 미리보기 표시
    const reader = new FileReader();
    reader.onload = (e) => {
        preview.src = e.target.result;
        preview.style.display = 'block';
        placeholder.style.display = 'none';
    };
    reader.readAsDataURL(file);

    // 서버에 업로드
    const result = await API.uploadProfileImage(file);

    if (result.ok) {
        signupProfileImageUrl = result.data.data.profile_image_url;
        showToast('프로필 이미지 업로드 완료', 'success');
    } else {
        showToast('프로필 이미지 업로드 실패', 'error');
        signupProfileImageUrl = null;
    }
}

async function handleSignup(event) {
    event.preventDefault();

    const email = document.getElementById('signup-email').value.trim();
    const password = document.getElementById('signup-password').value;
    const passwordCheck = document.getElementById('signup-password-check').value;
    const nickname = document.getElementById('signup-nickname').value.trim();

    const emailHelper = document.getElementById('signup-email-helper');
    const passwordHelper = document.getElementById('signup-password-helper');
    const passwordCheckHelper = document.getElementById('signup-password-check-helper');
    const nicknameHelper = document.getElementById('signup-nickname-helper');
    const profileHelper = document.getElementById('signup-profile-helper');

    // 헬퍼 텍스트 초기화
    emailHelper.textContent = '';
    passwordHelper.textContent = '';
    passwordCheckHelper.textContent = '';
    nicknameHelper.textContent = '';
    profileHelper.textContent = '';

    // 입력 검증
    let hasError = false;

    if (!email) {
        emailHelper.textContent = '이메일을 입력해주세요';
        hasError = true;
    }

    if (!password) {
        passwordHelper.textContent = '비밀번호를 입력해주세요';
        hasError = true;
    }

    if (!passwordCheck) {
        passwordCheckHelper.textContent = '비밀번호를 한번 더 입력해주세요';
        hasError = true;
    }

    if (password && passwordCheck && password !== passwordCheck) {
        passwordCheckHelper.textContent = '비밀번호가 다릅니다';
        hasError = true;
    }

    if (!nickname) {
        nicknameHelper.textContent = '닉네임을 입력해주세요';
        hasError = true;
    }

    if (!signupProfileImageUrl) {
        profileHelper.textContent = '프로필 사진을 추가해주세요';
        hasError = true;
    }

    if (hasError) return;

    const result = await API.signup(email, password, passwordCheck, nickname, signupProfileImageUrl);

    if (result.ok && result.data.message === 'register_success') {
        showToast('회원가입 성공! 로그인해주세요', 'success');
        navigateTo('login');
        // 폼 초기화
        document.getElementById('signup-form').reset();
        signupProfileImageUrl = null;
        const preview = document.getElementById('signup-profile-preview');
        const placeholder = document.getElementById('signup-profile-placeholder');
        preview.style.display = 'none';
        placeholder.style.display = 'block';
    } else {
        const errorMessages = {
            'email_required': '이메일을 입력해주세요',
            'invalid_email_format': '올바른 이메일 주소 형식을 입력해주세요',
            'invalid_email_character': '이메일은 영문과 @, .만 사용이 가능합니다',
            'duplicate_email': '중복된 이메일입니다',
            'password_required': '비밀번호를 입력해주세요',
            'invalid_password_format': '비밀번호는 8자 이상, 20자 이하이며 대문자, 소문자, 특수문자를 각각 1개 포함해야 합니다',
            'password_check_required': '비밀번호를 한번 더 입력해주세요',
            'password_mismatch': '비밀번호가 다릅니다',
            'nickname_required': '닉네임을 입력해주세요',
            'nickname_contains_space': '띄어쓰기를 없애주세요',
            'nickname_too_long': '닉네임은 최대 10자까지 작성 가능합니다',
            'duplicate_nickname': '중복된 닉네임입니다',
            'profile_image_url_required': '프로필 사진을 추가해주세요',
        };

        const message = result.data.message;
        if (message.includes('email')) {
            emailHelper.textContent = errorMessages[message] || message;
        } else if (message.includes('password_check') || message === 'password_mismatch') {
            passwordCheckHelper.textContent = errorMessages[message] || message;
        } else if (message.includes('password')) {
            passwordHelper.textContent = errorMessages[message] || message;
        } else if (message.includes('nickname')) {
            nicknameHelper.textContent = errorMessages[message] || message;
        } else if (message.includes('profile')) {
            profileHelper.textContent = errorMessages[message] || message;
        } else {
            showToast(errorMessages[message] || '회원가입에 실패했습니다', 'error');
        }
    }
}

function handleLogout() {
    clearCurrentUser();
    showToast('로그아웃 되었습니다', 'success');
    navigateTo('login');
}

// Export
window.Auth = {
    isLoggedIn,
    getCurrentUser,
    handleLogin,
    handleSignup,
    handleLogout,
    handleProfileImageUpload,
};
