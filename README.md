# 🎉 동물 감정일기 - Frontend

> **바닐라 JavaScript**로 **FastAPI 모델 서빙 API**를 사용하는 커뮤니티 게시판

[![JavaScript](https://img.shields.io/badge/Vanilla_JS-ES6+-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/CSS)

## 📋 프로젝트 소개

**동물 감정일기**는 **카카오테크 부트캠프** FastAPI 프로젝트의 프론트엔드입니다.

### 🎯 핵심 목표: 바닐라 JS로 FastAPI 모델 서빙 사용

이 프로젝트는 **프레임워크 없이 순수 JavaScript**만으로 FastAPI 기반 AI 모델 서빙 API를 호출하여:
- 📸 **이미지 분류**: 업로드된 이미지에서 🐕 강아지 / 🐈 고양이 자동 분류
- 💭 **감정 분석**: 게시글/댓글의 😊 긍정 / 😞 부정 / 😐 중립 감정 분석
- 📝 **텍스트 요약**: 긴 게시글 내용 자동 요약

을 웹 브라우저에서 직접 사용할 수 있는 풍부한 사용자 경험을 제공합니다.

## 🔗 관련 저장소

| 저장소 | 설명 | 링크 |
|--------|------|------|
| **Frontend** | Vanilla JS 기반 웹 UI | [현재 저장소](https://github.com/yoondonggyu/KakaoTechBootcamp-Frontend) |
| **Backend** | FastAPI 기반 REST API | [KakaoTechBootcamp-Backend](https://github.com/yoondonggyu/KakaoTechBootcamp-Backend) |
| **Model** | AI 모델 서빙 API | [KakaoTechBootcamp-Model](https://github.com/yoondonggyu/KakaoTechBootcamp-Model) |

## ✨ 주요 기능

### 🔐 사용자 인증
- 회원가입 (프로필 이미지 업로드)
- 로그인/로그아웃
- 세션 기반 인증

### 📝 게시판 기능
- 게시글 CRUD (작성/조회/수정/삭제)
- 이미지 업로드
- 좋아요 기능
- 댓글 기능
- 조회수 카운트

### 🤖 AI 기능
- **Gemini 감정 분석**: 게시글 내용의 감정(긍정/부정/중립) 분석 (한글/영어 지원)
- **이미지 분류**: 업로드된 이미지에서 강아지/고양이 자동 분류

## 🛠 기술 스택

| 분류 | 기술 |
|------|------|
| **Language** | HTML5, CSS3, JavaScript (ES6+) |
| **Design** | Vanilla CSS, Google Fonts (Noto Sans KR) |
| **Architecture** | Single Page Application (SPA) |
| **HTTP Client** | Fetch API |

## 📁 프로젝트 구조

```
FASTAPI_Project_front/
├── index.html          # 메인 HTML (SPA)
├── css/
│   └── index.css       # 전체 스타일시트
├── js/
│   ├── api.js          # API 통신 모듈
│   ├── auth.js         # 인증 관련 로직
│   ├── posts.js        # 게시글 관련 로직
│   └── app.js          # 앱 초기화 및 라우팅
└── README.md
```

## 🚀 실행 방법

### 1. 저장소 클론
```bash
git clone https://github.com/yoondonggyu/KakaoTechBootcamp-Frontend.git
cd KakaoTechBootcamp-Frontend
```

### 2. 로컬 서버 실행
```bash
# Python 사용
python -m http.server 3000

# 또는 Node.js 사용
npx serve -p 3000
```

### 3. 브라우저에서 접속
```
http://localhost:3000
```

> ⚠️ **주의**: Backend API 서버(포트 8000)와 Model API 서버(포트 8001)가 실행 중이어야 합니다.

## 📸 스크린샷

### 로그인 화면
- 이메일/비밀번호 입력
- 회원가입 링크

### 게시글 목록
- 게시글 카드 형태 표시
- 작성자, 좋아요, 댓글 수 표시

### 게시글 상세
- 이미지 표시
- AI 이미지 분류 결과 (🐕 강아지 / 🐈 고양이)
- AI 감정 분석 결과 (😊 긍정 / 😞 부정 / 😐 중립)
- 댓글 작성/수정/삭제

## 📄 API 연동

| 기능 | 엔드포인트 | 설명 |
|------|-----------|------|
| 로그인 | `POST /api/auth/login` | 사용자 로그인 |
| 회원가입 | `POST /api/auth/signup` | 신규 회원 등록 |
| 게시글 목록 | `GET /api/posts` | 게시글 목록 조회 |
| 게시글 상세 | `GET /api/posts/{id}` | 게시글 상세 조회 |
| 게시글 작성 | `POST /api/posts` | 새 게시글 작성 |
| 이미지 업로드 | `POST /api/posts/upload` | 이미지 업로드 + AI 분류 |
| 감정 분석 | `POST /api/sentiment/gemini` | Gemini 감정 분석 |

## 👨‍💻 개발자

- **윤동규** - [GitHub](https://github.com/yoondonggyu)

## 📝 라이선스

This project is licensed under the MIT License.
