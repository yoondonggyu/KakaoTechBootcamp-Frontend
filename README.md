# FASTAPI_Project_front

Backend API 테스트용 Streamlit 프론트엔드

## 실행 방법

```bash
# 가상환경 활성화
conda activate env_fastapi

# Streamlit 앱 실행
streamlit run test_streamlit.py
```

또는 특정 포트로 실행:
```bash
streamlit run test_streamlit.py --server.port 8501
```

## 접속 주소

브라우저에서 다음 주소로 접속:
```
http://localhost:8501
```

## 기능

### 1. 인증
- 로그인
- 회원가입

### 2. 게시글
- 게시글 목록 조회 (페이지네이션)
- 게시글 작성
- 게시글 상세 조회

### 3. 댓글
- 댓글 목록 조회
- 댓글 작성 (Model API 감성 분석 포함)

### 4. 이미지 업로드
- 이미지 파일 업로드
- Model API 이미지 분류 (강아지/고양이) 자동 실행

### 5. API 상태
- Backend API 서버 상태 확인
- API 엔드포인트 목록

## 필수 요구사항

1. **Backend API 서버 실행 중**
   ```bash
   cd FASTAPI_Project_back
   uvicorn app.main:app --reload --port 8082
   ```

2. **Model API 서버 실행 중** (이미지 분류/감성 분석 사용 시)
   ```bash
   cd FASTAPI_Project_model
   uvicorn app.main:app --reload --port 8001
   ```

3. **필요한 패키지**
   ```bash
   pip install streamlit requests pillow
   ```

## Model API 연동

이 Streamlit 앱은 Backend API를 통해 Model API와 연동됩니다:

- **이미지 업로드**: 자동으로 이미지 분류 (강아지/고양이) 실행
- **댓글 작성**: 자동으로 감성 분석 (긍정/부정) 실행

결과는 응답에 포함되어 표시됩니다.


