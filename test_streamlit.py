"""
Backend API 테스트용 Streamlit 앱
포트 8000에서 실행 중인 Backend API를 테스트합니다.
"""
import requests
import streamlit as st
from PIL import Image
import json

# Backend API Base URL
BASE_URL = "http://localhost:8000/api"

# 세션 상태 초기화
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "nickname" not in st.session_state:
    st.session_state.nickname = None
if "show_delete_confirm" not in st.session_state:
    st.session_state.show_delete_confirm = False
if "post_detail_like_count" not in st.session_state:
    st.session_state.post_detail_like_count = None
if "post_detail_id" not in st.session_state:
    st.session_state.post_detail_id = None
if "post_detail_data" not in st.session_state:
    st.session_state.post_detail_data = None

st.title("🚀 Backend API 테스트")
st.markdown("---")

# 사이드바 - 인증 상태
with st.sidebar:
    st.header("🔐 인증 상태")
    if st.session_state.user_id:
        st.success(f"✅ 로그인됨\n👤 {st.session_state.nickname}\n🆔 ID: {st.session_state.user_id}")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("로그아웃"):
                st.session_state.user_id = None
                st.session_state.nickname = None
                st.rerun()
        
        with col2:
            if st.button("회원 탈퇴", type="secondary"):
                st.session_state.show_delete_confirm = True
        
        # 회원 탈퇴 확인
        if st.session_state.get("show_delete_confirm", False):
            st.warning("⚠️ 정말 회원 탈퇴하시겠습니까?")
            st.caption("이 작업은 되돌릴 수 없습니다.")
            
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("탈퇴하기", type="primary", key="confirm_delete"):
                    try:
                        headers = {"X-User-Id": str(st.session_state.user_id)}
                        response = requests.delete(
                            f"{BASE_URL}/users/profile",
                            headers=headers
                        )
                        
                        if response.status_code == 200:
                            st.success("✅ 회원 탈퇴 완료")
                            st.session_state.user_id = None
                            st.session_state.nickname = None
                            st.session_state.show_delete_confirm = False
                            st.rerun()
                        else:
                            st.error(f"에러: {response.status_code}")
                            st.json(response.json())
                    except Exception as e:
                        st.error(f"요청 실패: {e}")
            
            with col_no:
                if st.button("취소", key="cancel_delete"):
                    st.session_state.show_delete_confirm = False
                    st.rerun()
    else:
        st.info("❌ 로그인 필요")

# 탭 구성
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔐 인증", 
    "📝 게시글", 
    "💬 댓글", 
    "🖼️ 이미지 업로드 (Model API)", 
    "📊 API 상태"
])

# ========== 탭 1: 인증 ==========
with tab1:
    st.header("인증")
    
    auth_tab1, auth_tab2 = st.tabs(["로그인", "회원가입"])
    
    with auth_tab1:
        st.subheader("로그인")
        login_email = st.text_input("이메일", key="login_email")
        login_password = st.text_input("비밀번호", type="password", key="login_password")
        
        if st.button("로그인", type="primary"):
            try:
                response = requests.post(
                    f"{BASE_URL}/auth/login",
                    json={"email": login_email, "password": login_password}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("message") == "login_success":
                        user_data = data.get("data", {})
                        st.session_state.user_id = user_data.get("user_id")
                        st.session_state.nickname = user_data.get("nickname")
                        st.success("✅ 로그인 성공!")
                        st.json(data)
                        st.rerun()
                    else:
                        st.error(f"로그인 실패: {data.get('message')}")
                else:
                    st.error(f"에러: {response.status_code}")
                    st.json(response.json())
            except Exception as e:
                st.error(f"요청 실패: {e}")
    
    with auth_tab2:
        st.subheader("회원가입")
        signup_email = st.text_input("이메일", key="signup_email")
        signup_password = st.text_input("비밀번호", type="password", key="signup_password")
        signup_password_check = st.text_input("비밀번호 확인", type="password", key="signup_password_check")
        signup_nickname = st.text_input("닉네임", key="signup_nickname")
        
        # 프로필 이미지 업로드
        st.markdown("**프로필 이미지 (선택)**")
        profile_image = st.file_uploader(
            "프로필 이미지를 선택하세요",
            type=["jpg", "jpeg", "png"],
            key="signup_profile_image",
            help="선택하지 않으면 기본 이미지가 사용됩니다"
        )
        
        if profile_image is not None:
            # 이미지 미리보기
            image = Image.open(profile_image)
            st.image(image, caption="프로필 이미지 미리보기", width=200)
        
        if st.button("회원가입", type="primary"):
            try:
                # 프로필 이미지가 있으면 먼저 업로드
                profile_image_url = "https://example.com/default.jpg"  # 기본값
                
                if profile_image is not None:
                    try:
                        # 프로필 이미지 업로드
                        files = {"file": (profile_image.name, profile_image.getvalue(), profile_image.type)}
                        upload_response = requests.post(
                            f"{BASE_URL}/users/profile/upload",
                            files=files
                        )
                        
                        if upload_response.status_code == 200:
                            upload_data = upload_response.json()
                            profile_image_url = upload_data.get("data", {}).get("profile_image_url", profile_image_url)
                            st.info("✅ 프로필 이미지 업로드 완료")
                        else:
                            st.warning("⚠️ 프로필 이미지 업로드 실패, 기본 이미지 사용")
                    except Exception as e:
                        st.warning(f"⚠️ 프로필 이미지 업로드 실패: {e}, 기본 이미지 사용")
                
                # 회원가입 요청
                response = requests.post(
                    f"{BASE_URL}/auth/signup",
                    json={
                        "email": signup_email,
                        "password": signup_password,
                        "password_check": signup_password_check,
                        "nickname": signup_nickname,
                        "profile_image_url": profile_image_url
                    }
                )
                
                if response.status_code == 201:
                    st.success("✅ 회원가입 성공!")
                    st.json(response.json())
                else:
                    st.error(f"에러: {response.status_code}")
                    st.json(response.json())
            except Exception as e:
                st.error(f"요청 실패: {e}")

# ========== 탭 2: 게시글 ==========
with tab2:
    st.header("게시글 관리")
    
    post_tab1, post_tab2, post_tab3 = st.tabs(["게시글 목록", "게시글 작성", "게시글 상세"])
    
    with post_tab1:
        st.subheader("게시글 목록")
        page = st.number_input("페이지", min_value=1, value=1, key="post_page")
        limit = st.number_input("개수", min_value=1, max_value=100, value=10, key="post_limit")
        
        headers = {}
        if st.session_state.user_id:
            headers["X-User-Id"] = str(st.session_state.user_id)
        
        if st.button("조회", type="primary", key="get_posts_list"):
            try:
                response = requests.get(
                    f"{BASE_URL}/posts",
                    params={"page": page, "limit": limit},
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    posts = data.get("data", {}).get("posts", [])
                    
                    st.success(f"✅ 총 {data.get('data', {}).get('total', 0)}개 게시글")
                    
                    for post in posts:
                        with st.expander(f"📌 {post.get('title', '제목 없음')} (ID: {post.get('post_id')})"):
                            st.write(f"**작성자:** {post.get('nickname')}")
                            st.write(f"**내용:** {post.get('content')}")
                            st.write(f"👍 좋아요: {post.get('like_count')} | 👁️ 조회수: {post.get('view_count')} | 💬 댓글: {post.get('comment_count')}")
                            if post.get('image_url'):
                                st.image(post.get('image_url'), width=200)
                else:
                    st.error(f"에러: {response.status_code}")
                    st.json(response.json())
            except Exception as e:
                st.error(f"요청 실패: {e}")
    
    with post_tab2:
        st.subheader("게시글 작성")
        if not st.session_state.user_id:
            st.warning("⚠️ 로그인이 필요합니다.")
        else:
            post_title = st.text_input("제목", key="create_post_title")
            post_content = st.text_area("내용", key="create_post_content", height=150)
            post_image_url = st.text_input("이미지 URL (선택)", key="create_post_image_url")
            
            headers = {"X-User-Id": str(st.session_state.user_id)}
            
            if st.button("작성", type="primary", key="create_post"):
                try:
                    response = requests.post(
                        f"{BASE_URL}/posts",
                        json={
                            "title": post_title,
                            "content": post_content,
                            "image_url": post_image_url if post_image_url else None
                        },
                        headers=headers
                    )
                    
                    if response.status_code == 201:
                        st.success("✅ 게시글 작성 성공!")
                        st.json(response.json())
                    else:
                        st.error(f"에러: {response.status_code}")
                        st.json(response.json())
                except Exception as e:
                    st.error(f"요청 실패: {e}")
    
    with post_tab3:
        st.subheader("게시글 상세")
        post_id = st.number_input("게시글 ID", min_value=1, value=1, key="detail_post_id")
        if st.session_state.post_detail_id and st.session_state.post_detail_id != post_id:
            st.session_state.post_detail_like_count = None
            st.session_state.post_detail_data = None
        
        headers = {}
        if st.session_state.user_id:
            headers["X-User-Id"] = str(st.session_state.user_id)
        
        if st.button("조회", type="primary", key="get_post_detail"):
            try:
                response = requests.get(
                    f"{BASE_URL}/posts/{post_id}",
                    headers=headers
                )
                
                if response.status_code == 200:
                    data = response.json()
                    post_data = data.get("data", {})
                    st.session_state.post_detail_id = post_id
                    st.session_state.post_detail_like_count = post_data.get('like_count', 0)
                    st.session_state.post_detail_data = post_data
                    st.success("✅ 게시글 조회 성공!")
                else:
                    st.error(f"에러: {response.status_code}")
                    st.json(response.json())
            except Exception as e:
                st.error(f"요청 실패: {e}")

        post_data = st.session_state.get("post_detail_data")
        if post_data and st.session_state.post_detail_id == post_id:
            st.markdown("---")
            st.write(f"**제목:** {post_data.get('title')}")
            st.write(f"**작성자:** {post_data.get('nickname')}")
            st.write(f"**내용:** {post_data.get('content')}")
            current_like_count = post_data.get('like_count', 0)
            if st.session_state.post_detail_like_count is not None:
                current_like_count = st.session_state.post_detail_like_count
            st.write(f"👍 좋아요: {current_like_count} | 👁️ 조회수: {post_data.get('view_count')}")
            
            if post_data.get('image_url'):
                st.image(post_data.get('image_url'), width=300)
            
            if st.session_state.user_id:
                like_col1, like_col2 = st.columns([1, 3])
                with like_col1:
                    if st.button("👍 좋아요 토글", key="toggle_like_button"):
                        try:
                            headers = {"X-User-Id": str(st.session_state.user_id)}
                            like_response = requests.post(
                                f"{BASE_URL}/posts/{post_id}/like",
                                headers=headers
                            )
                            if like_response.status_code == 200:
                                like_data = like_response.json().get("data", {})
                                like_count = like_data.get("like_count", current_like_count)
                                liked = like_data.get("liked", False)
                                st.session_state.post_detail_like_count = like_count
                                # post_data는 dict이므로 바로 업데이트
                                st.session_state.post_detail_data["like_count"] = like_count
                                st.success(f"👍 좋아요 {'등록' if liked else '취소'} (총 {like_count}개)")
                            else:
                                st.error(f"좋아요 실패: {like_response.status_code}")
                                st.json(like_response.json())
                        except Exception as e:
                            st.error(f"좋아요 요청 실패: {e}")
            else:
                st.info("👍 좋아요를 사용하려면 로그인하세요.")
            
            comments = post_data.get('comments', [])
            if comments:
                st.subheader("💬 댓글")
                for comment in comments:
                    st.write(f"- **{comment.get('nickname')}:** {comment.get('content')}")

# ========== 탭 3: 댓글 ==========
with tab3:
    st.header("댓글 관리")
    
    if not st.session_state.user_id:
        st.warning("⚠️ 로그인이 필요합니다.")
    else:
        comment_post_id = st.number_input("게시글 ID", min_value=1, value=1, key="comment_post_id")
        
        comment_tab1, comment_tab2 = st.tabs(["댓글 목록", "댓글 작성"])
        
        with comment_tab1:
            st.subheader("댓글 목록")
            headers = {}
            
            if st.button("조회", type="primary", key="get_comments"):
                try:
                    response = requests.get(
                        f"{BASE_URL}/posts/{comment_post_id}/comments",
                        headers=headers
                    )
                    
                    if response.status_code == 200:
                        data = response.json()
                        comments = data.get("data", {}).get("comments", [])
                        
                        st.success(f"✅ {len(comments)}개 댓글")
                        
                        for comment in comments:
                            st.write(f"**{comment.get('nickname')}:** {comment.get('content')}")
                    else:
                        st.error(f"에러: {response.status_code}")
                        st.json(response.json())
                except Exception as e:
                    st.error(f"요청 실패: {e}")
        
        with comment_tab2:
            st.subheader("댓글 작성 (감성 분석 포함)")
            comment_content = st.text_area("댓글 내용", key="comment_content", height=100)
            
            headers = {"X-User-Id": str(st.session_state.user_id)}
            
            if st.button("작성", type="primary", key="create_comment"):
                try:
                    response = requests.post(
                        f"{BASE_URL}/posts/{comment_post_id}/comments",
                        json={"content": comment_content},
                        headers=headers
                    )
                    
                    if response.status_code == 201:
                        data = response.json()
                        st.success("✅ 댓글 작성 성공!")
                        
                        # Model API 결과 표시
                        sentiment_data = data.get("data", {}).get("sentiment")
                        if sentiment_data:
                            st.info("🎯 **Model API 감성 분석 결과:**")
                            label = sentiment_data.get("label", "unknown")
                            confidence = sentiment_data.get("confidence", 0)
                            
                            if label == "positive":
                                st.success(f"😊 긍정적 (신뢰도: {confidence:.2%})")
                            elif label == "negative":
                                st.error(f"😞 부정적 (신뢰도: {confidence:.2%})")
                            else:
                                st.info(f"😐 {label} (신뢰도: {confidence:.2%})")
                        
                        st.json(data)
                    else:
                        st.error(f"에러: {response.status_code}")
                        st.json(response.json())
                except Exception as e:
                    st.error(f"요청 실패: {e}")

# ========== 탭 4: 이미지 업로드 (Model API 연동) ==========
with tab4:
    st.header("🖼️ 이미지 업로드 (Model API 연동)")
    st.markdown("이미지를 업로드하면 **자동으로 이미지 분류 (강아지/고양이)**가 실행됩니다.")
    
    uploaded_file = st.file_uploader(
        "이미지를 선택하세요",
        type=["jpg", "jpeg", "png"],
        help="강아지 또는 고양이 이미지를 업로드하세요"
    )
    
    if uploaded_file is not None:
        # 이미지 미리보기
        image = Image.open(uploaded_file)
        st.image(image, caption="업로드할 이미지", width=300)
        
        if st.button("업로드 및 분류", type="primary"):
            try:
                files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                response = requests.post(
                    f"{BASE_URL}/posts/upload",
                    files=files
                )
                
                if response.status_code == 200:
                    data = response.json()
                    st.success("✅ 이미지 업로드 성공!")
                    
                    # Model API 결과 표시
                    response_data = data.get("data", {})
                    prediction_data = response_data.get("prediction")
                    prediction_error = response_data.get("prediction_error")
                    
                    if prediction_data:
                        class_name = prediction_data.get("class_name", "Unknown")
                        confidence = prediction_data.get("confidence_score", 0)
                        
                        # 한글 클래스명 매핑
                        class_name_kr = ""
                        if class_name.lower() == "dog":
                            class_name_kr = "강아지"
                        elif class_name.lower() == "cat":
                            class_name_kr = "고양이"
                        else:
                            class_name_kr = class_name
                        
                        # 출력 형식: "Model API 이미지 분류 결과: dog(강아지)"
                        result_text = f"**Model API 이미지 분류 결과:** {class_name.lower()}({class_name_kr})"
                        st.success(result_text)
                    elif prediction_error:
                        st.warning(f"⚠️ **이미지 분류 실패:** {prediction_error}")
                        # 에러 메시지에서 포트 정보 추출 (있는 경우)
                        if "포트" in prediction_error or "port" in prediction_error.lower():
                            st.info("💡 Model API 서버가 실행 중인지 확인하세요.")
                        else:
                            st.info("💡 Model API 서버(포트 8002 또는 8001)가 실행 중인지 확인하세요.")
                    
                    st.json(data)
                else:
                    st.error(f"에러: {response.status_code}")
                    st.json(response.json())
            except Exception as e:
                st.error(f"요청 실패: {e}")

# ========== 탭 5: API 상태 ==========
with tab5:
    st.header("📊 API 상태 확인")
    
    if st.button("상태 확인", type="primary"):
        try:
            response = requests.get("http://localhost:8000/")
            
            if response.status_code == 200:
                st.success("✅ Backend API 서버 정상 작동 중")
                st.json(response.json())
            else:
                st.error(f"❌ 서버 응답 오류: {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("❌ Backend API 서버에 연결할 수 없습니다.\n포트 8000에서 서버가 실행 중인지 확인하세요.")
        except Exception as e:
            st.error(f"❌ 오류: {e}")
    
    st.markdown("---")
    st.subheader("🔗 API 엔드포인트")
    st.code(f"""
Base URL: {BASE_URL}

인증:
  POST {BASE_URL}/auth/login
  POST {BASE_URL}/auth/signup

게시글:
  GET  {BASE_URL}/posts
  POST {BASE_URL}/posts
  GET  {BASE_URL}/posts/{{post_id}}
  POST {BASE_URL}/posts/upload (Model API 연동)

댓글:
  GET  {BASE_URL}/posts/{{post_id}}/comments
  POST {BASE_URL}/posts/{{post_id}}/comments (Model API 연동)
    """)

