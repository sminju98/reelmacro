# 🚀 설치 및 환경 설정 가이드

이 문서는 Reel Maker AI를 로컬 개발 환경에서 설정하는 방법을 안내합니다.

## 📋 사전 요구사항

### 필수 설치 항목

1. **Python 3.11 이상**
   ```bash
   python --version  # 3.11 이상 확인
   ```

2. **PostgreSQL 14 이상**
   ```bash
   # Mac (Homebrew)
   brew install postgresql@14
   brew services start postgresql@14
   
   # Ubuntu
   sudo apt-get install postgresql-14
   sudo systemctl start postgresql
   ```

3. **Redis 7 이상**
   ```bash
   # Mac (Homebrew)
   brew install redis
   brew services start redis
   
   # Ubuntu
   sudo apt-get install redis-server
   sudo systemctl start redis
   ```

4. **FFmpeg** (영상 처리)
   ```bash
   # Mac (Homebrew)
   brew install ffmpeg
   
   # Ubuntu
   sudo apt-get install ffmpeg
   ```

## 📦 프로젝트 설정

### 1. 저장소 클론

```bash
git clone https://github.com/yourusername/macro.git
cd macro
```

### 2. 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python -m venv venv

# 활성화
source venv/bin/activate  # Mac/Linux
# 또는
venv\Scripts\activate  # Windows
```

### 3. 의존성 설치

```bash
# 프로덕션 의존성
pip install -r requirements.txt

# 개발 의존성 (테스트, 린트 등)
pip install -r requirements-dev.txt
```

## 🔐 환경 변수 설정

### 방법 1: 자동 설정 (권장)

```bash
# 환경 설정 도우미 실행
python scripts/setup_env.py

# 또는 대화형 모드
python scripts/setup_env.py
```

스크립트가 다음을 자동으로 처리합니다:
- `.env` 파일 생성
- JWT Secret Key 자동 생성
- API 키 발급 가이드 제공
- 환경 변수 검증

### 방법 2: 수동 설정

```bash
# 예시 파일 복사
cp config/development.env.example .env

# .env 파일 편집
vim .env  # 또는 원하는 에디터
```

### 필수 API 키 발급

#### 1. OpenAI API (GPT-4)
- **URL**: https://platform.openai.com/api-keys
- **비용**: GPT-4 대본 1개당 약 $0.01-0.05
- **발급 방법**:
  1. OpenAI 계정 가입/로그인
  2. API Keys 페이지 접속
  3. "Create new secret key" 클릭
  4. 생성된 키를 `.env`의 `OPENAI_API_KEY`에 설정

#### 2. ElevenLabs API (TTS)
- **URL**: https://elevenlabs.io/app/settings/api-keys
- **비용**: 프리티어 10,000 chars/month (약 20개 영상)
- **발급 방법**:
  1. ElevenLabs 계정 가입/로그인
  2. Settings > API Keys 접속
  3. "Generate API Key" 클릭
  4. 생성된 키를 `.env`의 `ELEVENLABS_API_KEY`에 설정

#### 3. Unsplash API (이미지)
- **URL**: https://unsplash.com/oauth/applications
- **비용**: 무료 (50 requests/hour)
- **발급 방법**:
  1. Unsplash 계정 가입/로그인
  2. "New Application" 클릭
  3. 약관 동의 후 애플리케이션 생성
  4. Access Key를 `.env`의 `UNSPLASH_ACCESS_KEY`에 설정

#### 4. Pexels API (영상)
- **URL**: https://www.pexels.com/api/
- **비용**: 무료 (200 requests/hour)
- **발급 방법**:
  1. Pexels 계정 가입/로그인
  2. "Request API" 버튼 클릭
  3. 이메일로 받은 API 키 확인
  4. API 키를 `.env`의 `PEXELS_API_KEY`에 설정

### 환경 변수 검증

```bash
# 환경 변수가 올바르게 설정되었는지 확인
python scripts/setup_env.py validate
```

## 🗄️ 데이터베이스 설정

### 1. PostgreSQL 데이터베이스 생성

```bash
# PostgreSQL 접속
psql postgres

# 데이터베이스 및 사용자 생성
CREATE DATABASE reelmaker_dev;
CREATE USER reelmaker WITH PASSWORD 'reelmaker123';
GRANT ALL PRIVILEGES ON DATABASE reelmaker_dev TO reelmaker;
\q
```

### 2. 데이터베이스 마이그레이션

```bash
# Alembic 초기화 (이미 설정됨)
# alembic init migrations

# 마이그레이션 실행
alembic upgrade head
```

### 3. 테스트 데이터 생성 (선택)

```bash
python scripts/seed_data.py
```

## 🚀 애플리케이션 실행

### 1. 개발 서버 실행

```bash
# FastAPI 서버 시작
uvicorn src.main:app --reload --port 8000
```

서버가 실행되면 다음 URL에서 접속 가능:
- API: http://localhost:8000
- API 문서 (Swagger): http://localhost:8000/docs
- API 문서 (ReDoc): http://localhost:8000/redoc

### 2. Celery Worker 실행 (별도 터미널)

```bash
# Celery worker 시작
celery -A src.workers worker --loglevel=info

# 또는 개발 모드 (자동 재시작)
watchmedo auto-restart --directory=./src --pattern=*.py --recursive -- celery -A src.workers worker --loglevel=info
```

### 3. 프론트엔드 실행 (별도 터미널, 나중에 구현)

```bash
cd frontend
npm install
npm run dev
```

## ✅ 설치 확인

### 1. API 서버 테스트

```bash
# 헬스 체크
curl http://localhost:8000/health

# 예상 응답: {"status": "healthy"}
```

### 2. 간단한 릴스 생성 테스트

```bash
# 회원가입
curl -X POST http://localhost:8000/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test1234!",
    "name": "테스트 사용자"
  }'

# 로그인 및 토큰 획득
curl -X POST http://localhost:8000/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "test1234!"
  }'

# 릴스 생성 (토큰 사용)
curl -X POST http://localhost:8000/v1/projects \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "AI 트렌드 테스트",
    "settings": {"duration": 30}
  }'
```

## 🧪 테스트 실행

```bash
# 전체 테스트
pytest

# 커버리지 확인
pytest --cov=src --cov-report=html

# 특정 테스트만 실행
pytest tests/unit/test_content_service.py

# 린트 체크
flake8 src/
black --check src/
mypy src/
```

## 🐛 문제 해결

### PostgreSQL 연결 오류

```bash
# PostgreSQL이 실행 중인지 확인
brew services list  # Mac
sudo systemctl status postgresql  # Linux

# 포트 확인
psql -p 5432 -U postgres
```

### Redis 연결 오류

```bash
# Redis가 실행 중인지 확인
brew services list  # Mac
sudo systemctl status redis  # Linux

# Redis CLI로 테스트
redis-cli ping  # 응답: PONG
```

### FFmpeg 설치 확인

```bash
ffmpeg -version
```

### API 키 오류

```bash
# 환경 변수 검증
python scripts/setup_env.py validate

# .env 파일 확인
cat .env | grep API_KEY
```

### 포트 충돌

```bash
# 8000번 포트 사용 중인 프로세스 확인
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# 다른 포트로 실행
uvicorn src.main:app --reload --port 8001
```

## 📁 디렉토리 권한

개발 중 필요한 디렉토리들이 자동으로 생성되지만, 권한 문제가 있을 경우:

```bash
# 디렉토리 생성
mkdir -p temp output media_cache

# 권한 설정
chmod 755 temp output media_cache
```

## 🔄 업데이트

프로젝트를 최신 버전으로 업데이트하려면:

```bash
# Git pull
git pull origin main

# 의존성 업데이트
pip install -r requirements.txt --upgrade

# 데이터베이스 마이그레이션
alembic upgrade head
```

## 💡 개발 팁

### Pre-commit Hooks 설정

```bash
# Pre-commit 설치
pip install pre-commit

# Hooks 설치
pre-commit install

# 수동 실행
pre-commit run --all-files
```

### VSCode 설정

`.vscode/settings.json` 추천 설정:

```json
{
  "python.linting.enabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "python.testing.pytestEnabled": true
}
```

## 📞 도움이 필요하신가요?

- **GitHub Issues**: [Issues](https://github.com/yourusername/macro/issues)
- **Discord**: [Join our community](https://discord.gg/reelmaker)
- **이메일**: support@reelmaker.ai

---

**문제가 해결되지 않으면 Issue를 생성해주세요!** 🙏

