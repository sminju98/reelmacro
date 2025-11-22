# 기여 가이드 (Contributing Guide)

Reel Maker AI 프로젝트에 기여해주셔서 감사합니다! 🎉

## 🌟 기여 방법

### 1. 버그 리포트

버그를 발견하셨나요? 다음 정보와 함께 [Issue](https://github.com/yourusername/macro/issues)를 생성해주세요:

- **제목**: 버그를 명확하게 설명하는 제목
- **환경**: OS, Python 버전, 브라우저 등
- **재현 단계**: 버그를 재현할 수 있는 단계
- **예상 결과**: 무엇이 발생해야 하는지
- **실제 결과**: 실제로 무엇이 발생했는지
- **스크린샷**: 가능하다면 스크린샷 첨부

**예시**:
```
**환경**
- OS: macOS 14.0
- Python: 3.11.5
- 브라우저: Chrome 120

**재현 단계**
1. 키워드 "AI 트렌드"로 프로젝트 생성
2. 30초 대기
3. 렌더링 실패 에러 발생

**예상 결과**
영상이 정상적으로 생성되어야 함

**실제 결과**
"RENDERING_FAILED" 에러 발생

**에러 로그**
[에러 메시지 복사]
```

### 2. 기능 제안

새로운 기능을 제안하고 싶으신가요? [Feature Request Issue](https://github.com/yourusername/macro/issues/new?template=feature_request.md)를 생성해주세요:

- **제목**: 기능을 명확하게 설명하는 제목
- **동기**: 왜 이 기능이 필요한지
- **제안**: 어떻게 동작해야 하는지
- **대안**: 고려한 다른 방법들
- **추가 컨텍스트**: 스크린샷, 예시 등

### 3. Pull Request

코드로 기여하고 싶으신가요? 다음 단계를 따라주세요:

#### Step 1: Fork & Clone

```bash
# 저장소 Fork (GitHub에서)
# 그 후 Clone
git clone https://github.com/YOUR_USERNAME/macro.git
cd macro
```

#### Step 2: 환경 설정

```bash
# 가상환경 생성
python -m venv venv
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Pre-commit hooks 설치
pre-commit install
```

#### Step 3: 브랜치 생성

```bash
# 기능 개발
git checkout -b feature/amazing-feature

# 버그 수정
git checkout -b fix/bug-description

# 문서 수정
git checkout -b docs/update-readme
```

#### Step 4: 코드 작성

우리의 [코딩 컨벤션](#-코딩-컨벤션)을 따라주세요.

#### Step 5: 테스트

```bash
# 테스트 실행
pytest

# 커버리지 확인
pytest --cov=src --cov-report=html

# 린트 체크
flake8 src/
black --check src/
mypy src/
```

#### Step 6: 커밋

```bash
# 변경사항 추가
git add .

# 커밋 (커밋 메시지 규칙 준수)
git commit -m "feat: Add amazing feature"
```

#### Step 7: Push & PR

```bash
# Push
git push origin feature/amazing-feature

# GitHub에서 Pull Request 생성
```

## 📋 커밋 메시지 규칙

우리는 [Conventional Commits](https://www.conventionalcommits.org/) 규칙을 따릅니다.

### 포맷

```
<타입>: <제목>

<본문> (선택)

<푸터> (선택)
```

### 타입

- `feat`: 새로운 기능 추가
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅 (기능 변경 없음)
- `refactor`: 코드 리팩토링
- `test`: 테스트 추가/수정
- `chore`: 빌드, 설정 변경
- `perf`: 성능 개선
- `ci`: CI 설정 변경

### 예시

```bash
# 좋은 예시
git commit -m "feat: GPT-4를 활용한 대본 생성 기능 추가"
git commit -m "fix: 영상 렌더링 시 메모리 누수 문제 해결"
git commit -m "docs: API 명세서에 인증 섹션 추가"
git commit -m "refactor: ContentService를 독립적인 모듈로 분리"

# 나쁜 예시
git commit -m "update"
git commit -m "fix bug"
git commit -m "코드 수정"
```

### 상세 커밋 메시지

중요한 변경사항은 본문을 추가하세요:

```bash
git commit -m "feat: 배치 처리 기능 추가

여러 키워드를 한 번에 입력하여 다수의 릴스를 동시에 생성할 수 있습니다.

- 최대 10개 키워드 동시 처리
- 진행 상황 실시간 표시
- 완료 알림 기능

Closes #123"
```

## 💻 코딩 컨벤션

### Python

#### 1. 스타일 가이드

- **PEP 8** 준수
- **Black** 포맷터 사용 (line-length=88)
- **flake8** 린터 사용
- **mypy** 타입 체크 사용

```bash
# 자동 포맷팅
black src/

# 린트 체크
flake8 src/

# 타입 체크
mypy src/
```

#### 2. 네이밍 규칙

```python
# 클래스: PascalCase
class ContentService:
    pass

# 함수/변수: snake_case
def generate_script(keyword: str) -> dict:
    user_name = "홍길동"
    
# 상수: UPPER_SNAKE_CASE
MAX_RETRIES = 3
API_TIMEOUT = 30

# Private: _prefix
def _internal_function():
    pass
```

#### 3. 타입 힌팅

**필수**로 타입 힌팅을 사용하세요:

```python
from typing import Dict, List, Optional, Any

async def generate_script(
    keyword: str, 
    duration: int = 30,
    style: Optional[str] = None
) -> Dict[str, Any]:
    """
    키워드를 기반으로 릴스 대본을 생성합니다.
    
    Args:
        keyword: 검색 키워드
        duration: 영상 길이 (초 단위)
        style: 스타일 프리셋
        
    Returns:
        생성된 대본 정보를 담은 딕셔너리
        
    Raises:
        ValueError: 키워드가 비어있는 경우
        APIError: GPT API 호출 실패 시
    """
    pass
```

#### 4. Docstring

**Google 스타일**로 작성하며, **한국어**로 작성합니다:

```python
def calculate_video_duration(scenes: List[Scene]) -> float:
    """
    장면들의 총 영상 길이를 계산합니다.
    
    각 장면의 duration을 합산하여 전체 영상 길이를 반환합니다.
    음성 파일이 있는 경우 음성 길이를 우선으로 사용합니다.
    
    Args:
        scenes: 장면 리스트
        
    Returns:
        총 영상 길이 (초)
        
    Raises:
        ValueError: scenes가 비어있는 경우
        
    Example:
        >>> scenes = [Scene(duration=10), Scene(duration=20)]
        >>> calculate_video_duration(scenes)
        30.0
    """
    pass
```

#### 5. 에러 처리

```python
# 좋은 예시
try:
    result = await api_client.call()
except APIError as e:
    logger.error(f"API 호출 실패: {e}")
    raise ContentGenerationError(f"대본 생성 중 오류 발생: {str(e)}")
except Exception as e:
    logger.exception("예상치 못한 에러 발생")
    raise

# 나쁜 예시
try:
    result = api_client.call()
except:  # bare except
    pass  # silent fail
```

#### 6. 비동기 코드

```python
# 좋은 예시
async def fetch_multiple_images(keywords: List[str]) -> List[Image]:
    """여러 키워드에 대해 병렬로 이미지를 가져옵니다."""
    tasks = [fetch_image(kw) for kw in keywords]
    return await asyncio.gather(*tasks)

# 나쁜 예시
async def fetch_multiple_images(keywords: List[str]) -> List[Image]:
    """순차적으로 이미지를 가져옵니다 (느림)."""
    images = []
    for kw in keywords:
        img = await fetch_image(kw)  # 비효율적
        images.append(img)
    return images
```

### JavaScript/TypeScript

#### 1. 스타일 가이드

- **ESLint** + **Prettier** 사용
- **TypeScript** 필수

```typescript
// 좋은 예시
interface ProjectSettings {
  duration: number;
  voice: {
    gender: 'male' | 'female';
    tone: string;
  };
  style: string;
}

const createProject = async (
  keyword: string,
  settings: ProjectSettings
): Promise<Project> => {
  // 구현
};

// 나쁜 예시
const createProject = async (keyword, settings) => {
  // 타입 없음
};
```

## 🧪 테스트 작성

### 테스트 커버리지

- **최소 80% 이상** 유지
- 모든 public 함수는 테스트 필수
- Edge case 테스트 포함

### 테스트 구조

```python
# tests/unit/test_content_service.py
import pytest
from src.services.content_service import ContentService

@pytest.fixture
def content_service():
    """ContentService 인스턴스를 반환하는 fixture"""
    return ContentService()

class TestContentService:
    """ContentService 테스트 모음"""
    
    async def test_generate_script_success(self, content_service):
        """대본 생성 성공 케이스"""
        # Given
        keyword = "AI 트렌드"
        
        # When
        result = await content_service.generate_script(keyword)
        
        # Then
        assert "script" in result
        assert len(result["script"]) > 0
        assert result["estimated_duration"] == 30
    
    async def test_generate_script_empty_keyword(self, content_service):
        """빈 키워드로 대본 생성 시 에러 발생"""
        # Given
        keyword = ""
        
        # When & Then
        with pytest.raises(ValueError, match="키워드는 필수입니다"):
            await content_service.generate_script(keyword)
```

### Mock 사용

외부 API는 항상 mock 처리:

```python
from unittest.mock import AsyncMock, patch

async def test_generate_script_api_error(content_service):
    """API 에러 시 적절한 예외 발생"""
    with patch('openai.AsyncOpenAI') as mock_openai:
        mock_openai.return_value.chat.completions.create = AsyncMock(
            side_effect=APIError("API 호출 실패")
        )
        
        with pytest.raises(ContentGenerationError):
            await content_service.generate_script("테스트")
```

## 📚 문서화

### 코드 문서화

- 모든 public 함수/클래스는 docstring 필수
- 복잡한 로직은 주석으로 설명
- TODO, FIXME, HACK 태그 활용

```python
def complex_algorithm(data: List[int]) -> int:
    """
    복잡한 알고리즘 설명
    
    TODO: 성능 최적화 필요
    FIXME: edge case 처리 누락
    """
    # 1단계: 데이터 정렬
    sorted_data = sorted(data)
    
    # 2단계: 중앙값 계산
    # HACK: 임시 해결책, 나중에 리팩토링 필요
    median = sorted_data[len(sorted_data) // 2]
    
    return median
```

### README 및 문서 업데이트

새로운 기능을 추가하면 관련 문서도 업데이트하세요:

- `README.md`: 사용 방법
- `docs/API명세서.md`: API 엔드포인트
- `docs/기술명세서.md`: 아키텍처 변경사항

## 🎨 UI/UX 기여

### 디자인 원칙

- **직관성**: 3번의 클릭으로 목표 달성
- **반응성**: 모든 화면 크기 지원
- **접근성**: WCAG 2.1 AA 준수
- **일관성**: 디자인 시스템 준수

### 컴포넌트 작성

```typescript
// components/Button.tsx
interface ButtonProps {
  children: React.ReactNode;
  variant?: 'primary' | 'secondary';
  size?: 'sm' | 'md' | 'lg';
  onClick?: () => void;
}

export const Button: React.FC<ButtonProps> = ({
  children,
  variant = 'primary',
  size = 'md',
  onClick
}) => {
  return (
    <button
      className={`btn btn-${variant} btn-${size}`}
      onClick={onClick}
    >
      {children}
    </button>
  );
};
```

## 🔒 보안

### 보안 이슈 리포트

보안 취약점을 발견하셨나요? **공개 Issue를 생성하지 마세요.**

대신 이메일로 연락주세요: security@reelmaker.ai

### 보안 체크리스트

- [ ] API 키가 코드에 포함되지 않았는지 확인
- [ ] 사용자 입력 검증 및 sanitize
- [ ] SQL Injection 방지
- [ ] XSS 방지
- [ ] 민감 정보 로깅 방지

## ✅ PR 체크리스트

Pull Request를 생성하기 전에 다음을 확인하세요:

- [ ] 코드가 [코딩 컨벤션](#-코딩-컨벤션)을 따름
- [ ] 모든 테스트 통과 (`pytest`)
- [ ] 린트 체크 통과 (`flake8`, `black --check`)
- [ ] 타입 체크 통과 (`mypy`)
- [ ] 테스트 커버리지 80% 이상
- [ ] 커밋 메시지가 규칙을 따름
- [ ] 관련 문서 업데이트
- [ ] CHANGELOG.md 업데이트 (주요 변경사항)

## 🏷️ 라벨 가이드

GitHub Issues와 PRs에 사용하는 라벨:

- `bug`: 버그 리포트
- `feature`: 새로운 기능 제안
- `enhancement`: 기존 기능 개선
- `documentation`: 문서 관련
- `good first issue`: 초보자에게 적합한 이슈
- `help wanted`: 도움이 필요한 이슈
- `priority: high`: 높은 우선순위
- `priority: low`: 낮은 우선순위
- `wontfix`: 수정하지 않을 이슈

## 💬 커뮤니티

- **Discord**: [Join our community](https://discord.gg/reelmaker)
- **GitHub Discussions**: [Discussions](https://github.com/yourusername/macro/discussions)
- **Email**: support@reelmaker.ai

## 📜 행동 강령

우리는 모든 기여자를 환영하며, 다음을 지켜주세요:

- 존중과 배려
- 건설적인 피드백
- 다양성과 포용성
- 전문성

자세한 내용은 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)를 참고하세요.

## 🙏 감사합니다!

여러분의 기여가 Reel Maker AI를 더 나은 프로젝트로 만듭니다. 🎉

---

**질문이 있으신가요?** [GitHub Discussions](https://github.com/yourusername/macro/discussions)에서 물어보세요!

