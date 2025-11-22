# 🎬 Reel Maker AI - 인스타그램 릴스 자동 생성 프로그램

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **키워드만 입력하면 AI가 자동으로 바이럴 릴스를 제작해드립니다** ✨

## 📌 프로젝트 소개

Reel Maker AI는 최신 키워드를 입력하면 AI가 자동으로 대본을 작성하고, 관련 이미지/영상을 수집하여 음성, 자막, 효과가 포함된 완성도 높은 인스타그램 릴스를 생성해주는 서비스입니다.

### 🎯 핵심 기능

- 🤖 **AI 대본 생성**: GPT-4를 활용한 바이럴 대본 자동 작성
- 🖼️ **자동 미디어 수집**: Unsplash, Pexels에서 고품질 이미지/영상 자동 검색
- 🎙️ **TTS 음성 생성**: 자연스러운 한국어 음성 자동 생성
- ✍️ **자막 자동 생성**: 음성에 맞춰 타이밍 완벽한 자막 생성
- 🎬 **원클릭 영상 제작**: 모든 요소를 합쳐 릴스 포맷(9:16)으로 자동 렌더링
- #️⃣ **해시태그 추천**: 트렌드 기반 최적 해시태그 자동 생성

### ⏱️ 제작 시간

기존 2-4시간 → **단 3분**으로 단축!

## 🚀 빠른 시작

### 필수 요구사항

- Python 3.11 이상
- FFmpeg (영상 처리)
- PostgreSQL 14 이상
- Redis 7 이상

### 설치

```bash
# 저장소 클론
git clone https://github.com/sminju98/reelmacro.git
cd reelmacro

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# FFmpeg 설치 (Mac)
brew install ffmpeg

# FFmpeg 설치 (Ubuntu)
sudo apt-get install ffmpeg

# 환경 변수 설정
cp config/development.env.example .env
# .env 파일을 열어 API 키 설정
```

### 환경 변수 설정

`.env` 파일에 다음 API 키를 설정하세요:

```env
# OpenAI API (필수)
OPENAI_API_KEY=your_openai_api_key

# TTS API (필수)
ELEVENLABS_API_KEY=your_elevenlabs_api_key

# 이미지 API (필수)
UNSPLASH_ACCESS_KEY=your_unsplash_access_key
PEXELS_API_KEY=your_pexels_api_key

# 데이터베이스
DATABASE_URL=postgresql://user:password@localhost:5432/reelmaker

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT Secret
JWT_SECRET_KEY=your_random_secret_key_here
```

### 데이터베이스 초기화

```bash
# 데이터베이스 마이그레이션
alembic upgrade head

# 테스트 데이터 생성 (선택)
python scripts/seed_data.py
```

### 실행

```bash
# 개발 서버 실행
uvicorn src.main:app --reload --port 8000

# Celery Worker 실행 (별도 터미널)
celery -A src.workers worker --loglevel=info

# 프론트엔드 실행 (별도 터미널)
cd frontend
npm install
npm run dev
```

서버가 실행되면 http://localhost:8000 에서 API를 사용할 수 있습니다.

## 📖 사용 방법

### CLI 사용 예제

```bash
# 간단한 릴스 생성
python -m src.cli create "AI 트렌드 2025"

# 옵션 지정
python -m src.cli create "건강한 다이어트" \
  --duration 30 \
  --voice female_bright \
  --style modern
```

### Python SDK 사용 예제

```python
from reelmaker import ReelMaker

# 클라이언트 초기화
client = ReelMaker(api_key="your_api_key")

# 릴스 생성
project = client.projects.create(
    keyword="AI 트렌드 2025",
    settings={
        "duration": 30,
        "voice": {"gender": "female", "tone": "bright"},
        "style": "modern"
    }
)

# 완료 대기
completed = client.projects.wait_for_completion(project.id)
print(f"영상 생성 완료: {completed.video_url}")
```

### API 사용 예제

```bash
# 회원가입
curl -X POST http://localhost:8000/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "password123",
    "name": "홍길동"
  }'

# 릴스 생성
curl -X POST http://localhost:8000/v1/projects \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "AI 트렌드 2025",
    "settings": {"duration": 30}
  }'
```

## 🏗️ 프로젝트 구조

```
reelmacro/
├── src/                    # 소스 코드
│   ├── api/               # API 라우터
│   ├── core/              # 핵심 설정
│   ├── models/            # DB 모델
│   ├── schemas/           # Pydantic 스키마
│   ├── services/          # 비즈니스 로직
│   ├── workers/           # Celery workers
│   ├── integrations/      # 외부 API 연동
│   └── utils/             # 유틸리티
├── tests/                 # 테스트
├── scripts/               # 유틸리티 스크립트
├── migrations/            # DB 마이그레이션
├── config/                # 설정 파일
├── docs/                  # 문서
│   ├── PRD.md
│   ├── 기술명세서.md
│   └── API명세서.md
├── docker/                # Docker 설정
├── frontend/              # 프론트엔드 (React)
├── .cursorrules          # Cursor AI 규칙
├── requirements.txt       # Python 의존성
└── README.md
```

## 🛠️ 기술 스택

### 백엔드
- **Python 3.11+**: 주 개발 언어
- **FastAPI**: 웹 프레임워크
- **SQLAlchemy**: ORM
- **PostgreSQL**: 데이터베이스
- **Redis**: 캐싱 및 작업 큐
- **Celery**: 비동기 작업 처리

### 영상 처리
- **MoviePy**: 영상 편집
- **FFmpeg**: 영상 인코딩
- **Pillow**: 이미지 처리
- **OpenCV**: 고급 영상 처리

### AI 및 외부 API
- **OpenAI GPT-4**: 대본 생성
- **ElevenLabs**: TTS 음성 생성
- **Unsplash API**: 이미지 검색
- **Pexels API**: 영상 검색

### 프론트엔드
- **React 18**: UI 라이브러리
- **TypeScript**: 타입 안정성
- **Tailwind CSS**: 스타일링
- **Vite**: 빌드 도구

### 인프라
- **AWS EC2**: 애플리케이션 서버
- **AWS S3**: 파일 저장
- **CloudFront**: CDN
- **Docker**: 컨테이너화

## 📊 개발 로드맵

### Phase 1: MVP (현재)
- [x] 프로젝트 기획 및 설계
- [ ] GPT 기반 대본 생성
- [ ] 이미지 수집 및 다운로드
- [ ] TTS 음성 생성
- [ ] 기본 영상 합성
- [ ] 자막 오버레이
- [ ] API 서버 구축

### Phase 2: 기능 확장 (2-3개월)
- [ ] 배치 처리 (다중 영상 생성)
- [ ] 5가지 스타일 프리셋
- [ ] 배경음악 라이브러리
- [ ] 브랜드 키트
- [ ] 사용자 대시보드

### Phase 3: 고도화 (4-6개월)
- [ ] AI 이미지 생성 (DALL-E)
- [ ] 인스타그램 자동 업로드
- [ ] 성과 분석 대시보드
- [ ] 음성 클로닝
- [ ] 모바일 앱 (iOS, Android)

## 🧪 테스트

```bash
# 전체 테스트 실행
pytest

# 커버리지 리포트
pytest --cov=src --cov-report=html

# 특정 테스트만 실행
pytest tests/unit/test_content_service.py
```

## 📝 문서

- [PRD (제품 요구사항 명세서)](docs/PRD.md)
- [기술 명세서](docs/기술명세서.md)
- [API 명세서](docs/API명세서.md)
- [기여 가이드](CONTRIBUTING.md)

## 🤝 기여하기

기여를 환영합니다! 자세한 내용은 [CONTRIBUTING.md](CONTRIBUTING.md)를 참고해주세요.

### 기여 프로세스

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.

## 👥 팀

- **Product Manager**: 프로젝트 기획 및 관리
- **Backend Developer**: API 및 영상 처리
- **Frontend Developer**: 웹 인터페이스
- **DevOps Engineer**: 인프라 및 배포

## 📧 문의

- **이메일**: support@reelmaker.ai
- **GitHub Issues**: [Issues](https://github.com/sminju98/reelmacro/issues)
- **Discord**: [Join our community](https://discord.gg/reelmaker)

## 🙏 감사의 말

이 프로젝트는 다음 오픈소스 프로젝트들을 사용합니다:

- [FastAPI](https://fastapi.tiangolo.com/)
- [MoviePy](https://zulko.github.io/moviepy/)
- [OpenAI](https://openai.com/)
- [Unsplash](https://unsplash.com/)
- [Pexels](https://www.pexels.com/)

## ⭐ Star History

프로젝트가 마음에 드신다면 ⭐️를 눌러주세요!

---

**Made with ❤️ by Reel Maker AI Team**

