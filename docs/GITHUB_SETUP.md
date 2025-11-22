# 🐙 GitHub 저장소 설정 가이드

이 문서는 프로젝트를 GitHub에 연결하고 푸시하는 방법을 안내합니다.

## 📝 사전 준비

1. **GitHub 계정**: [github.com](https://github.com)에서 계정 생성
2. **Git 설치 확인**:
   ```bash
   git --version
   ```

## 🚀 GitHub 저장소 생성 및 연결

### 1. GitHub에서 새 저장소 생성

1. GitHub 웹사이트 접속: https://github.com
2. 우측 상단 `+` 버튼 클릭 → `New repository` 선택
3. 저장소 설정:
   - **Repository name**: `reelmacro`
   - **Description**: `🎬 AI 기반 인스타그램 릴스 자동 생성 프로그램`
   - **Public/Private**: 원하는 옵션 선택
   - **Initialize this repository**: 체크하지 않음 (이미 로컬에 있음)
4. `Create repository` 클릭

### 2. 로컬 저장소와 GitHub 연결

GitHub에서 저장소를 만들면 다음과 같은 화면이 나타납니다. 아래 명령어를 실행하세요:

```bash
# GitHub 저장소를 원격 저장소로 추가
git remote add origin https://github.com/YOUR_USERNAME/reelmacro.git

# 원격 저장소 확인
git remote -v

# main 브랜치로 푸시
git push -u origin main
```

**YOUR_USERNAME**을 본인의 GitHub 사용자명으로 변경하세요!

### 3. SSH 사용 (선택, 권장)

HTTPS 대신 SSH를 사용하면 매번 비밀번호를 입력하지 않아도 됩니다.

#### SSH 키 생성 (없는 경우)

```bash
# SSH 키 생성
ssh-keygen -t ed25519 -C "your_email@example.com"

# SSH 키 복사 (Mac)
pbcopy < ~/.ssh/id_ed25519.pub

# SSH 키 복사 (Linux)
cat ~/.ssh/id_ed25519.pub
```

#### GitHub에 SSH 키 등록

1. GitHub → Settings → SSH and GPG keys
2. `New SSH key` 클릭
3. 복사한 키를 붙여넣고 저장

#### SSH로 원격 저장소 설정

```bash
# SSH URL로 변경
git remote set-url origin git@github.com:YOUR_USERNAME/reelmacro.git

# 확인
git remote -v
```

## 📤 코드 푸시

### 첫 푸시

```bash
# 현재 상태 확인
git status

# 모든 변경사항 커밋 (필요시)
git add .
git commit -m "chore: 프로젝트 초기 설정"

# GitHub에 푸시
git push -u origin main
```

### 이후 푸시

```bash
# 변경사항 추가
git add .

# 커밋
git commit -m "feat: 새로운 기능 추가"

# 푸시
git push
```

## 🌿 브랜치 전략

### 기본 브랜치

- `main`: 프로덕션 코드 (안정된 버전만)
- `develop`: 개발 브랜치 (기능 통합)

### 기능 개발 워크플로우

```bash
# develop 브랜치 생성 및 체크아웃
git checkout -b develop

# develop을 기본 브랜치로 푸시
git push -u origin develop

# 새 기능 개발 시
git checkout develop
git checkout -b feature/awesome-feature

# 개발 후 커밋
git add .
git commit -m "feat: 새로운 기능 추가"

# develop에 머지
git checkout develop
git merge feature/awesome-feature

# 푸시
git push origin develop

# 기능 브랜치 삭제
git branch -d feature/awesome-feature
```

## 📋 .gitignore 주요 항목

다음 파일들은 자동으로 무시됩니다:

```
.env                 # 환경 변수 (중요!)
__pycache__/         # Python 캐시
*.pyc                # Python 컴파일 파일
venv/                # 가상환경
.DS_Store            # macOS 파일
*.log                # 로그 파일
temp/                # 임시 파일
output/              # 생성된 영상
*.mp4, *.mp3         # 미디어 파일
```

**중요**: `.env` 파일은 절대 Git에 커밋하지 마세요!

## 🔒 민감 정보 관리

### .env 파일 보호

```bash
# .env 파일이 .gitignore에 있는지 확인
cat .gitignore | grep .env

# 혹시 .env가 커밋되었다면 (절대 안 됨!)
git rm --cached .env
git commit -m "chore: .env 파일 제거"
git push
```

### API 키가 노출된 경우

1. **즉시 해당 API 키를 폐기하고 재발급**
2. Git 히스토리에서 완전히 제거:
   ```bash
   # git-filter-repo 설치 필요
   git filter-repo --path .env --invert-paths
   git push origin --force --all
   ```

## 📊 Git 커밋 규칙

프로젝트의 커밋 메시지 규칙을 따라주세요:

```
<타입>: <제목>

<본문> (선택)
```

**타입**:
- `feat`: 새로운 기능
- `fix`: 버그 수정
- `docs`: 문서 수정
- `style`: 코드 포맷팅
- `refactor`: 코드 리팩토링
- `test`: 테스트 코드
- `chore`: 빌드, 설정 변경

**예시**:
```bash
git commit -m "feat: GPT-4 기반 대본 생성 기능 추가"
git commit -m "fix: 영상 렌더링 시 메모리 누수 해결"
git commit -m "docs: README에 설치 가이드 추가"
```

## 🔄 협업 워크플로우

### Pull Request (PR) 생성

1. 기능 브랜치에서 작업 완료
2. GitHub에 푸시:
   ```bash
   git push origin feature/your-feature
   ```
3. GitHub 웹에서 `Compare & pull request` 버튼 클릭
4. PR 제목과 설명 작성
5. 리뷰어 지정 (팀원)
6. `Create pull request` 클릭

### 코드 리뷰 후 머지

```bash
# 최신 develop 가져오기
git checkout develop
git pull origin develop

# 기능 브랜치 삭제 (로컬)
git branch -d feature/your-feature

# 기능 브랜치 삭제 (원격)
git push origin --delete feature/your-feature
```

## 🏷️ 태그 및 릴리스

### 버전 태그 생성

```bash
# 현재 버전 태그 확인
git tag

# 새 버전 태그 생성
git tag -a v0.1.0 -m "Release version 0.1.0"

# 태그 푸시
git push origin v0.1.0

# 모든 태그 푸시
git push origin --tags
```

### GitHub Release 생성

1. GitHub → Releases → `Draft a new release`
2. 태그 선택 (또는 새로 생성)
3. 릴리스 노트 작성
4. `Publish release` 클릭

## 🔍 유용한 Git 명령어

### 상태 확인

```bash
# 현재 상태
git status

# 커밋 히스토리
git log --oneline --graph --all

# 브랜치 목록
git branch -a
```

### 변경사항 되돌리기

```bash
# 작업 디렉토리 변경사항 취소
git checkout -- <file>

# 스테이징 취소
git reset HEAD <file>

# 마지막 커밋 취소 (변경사항 유지)
git reset --soft HEAD~1

# 마지막 커밋 완전 취소
git reset --hard HEAD~1
```

### 원격 저장소 동기화

```bash
# 원격 변경사항 가져오기 (머지하지 않음)
git fetch origin

# 원격 변경사항 가져오고 머지
git pull origin main

# 충돌 발생 시
# 1. 충돌 파일 수정
# 2. git add <file>
# 3. git commit
```

## 📚 추가 자료

- [GitHub Docs](https://docs.github.com)
- [Git Book (한글)](https://git-scm.com/book/ko/v2)
- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Conventional Commits](https://www.conventionalcommits.org/ko/v1.0.0/)

## 🛠️ 문제 해결

### "fatal: remote origin already exists"

```bash
# 기존 원격 저장소 제거
git remote remove origin

# 새로 추가
git remote add origin https://github.com/YOUR_USERNAME/macro.git
```

### "! [rejected] main -> main (fetch first)"

```bash
# 강제 푸시 (주의: 원격 히스토리 덮어씀)
git push -f origin main

# 또는 pull 후 푸시
git pull origin main --allow-unrelated-histories
git push origin main
```

### "Permission denied (publickey)"

SSH 키 문제입니다:

```bash
# SSH 연결 테스트
ssh -T git@github.com

# SSH 키 재등록 필요
cat ~/.ssh/id_ed25519.pub
```

## ✅ 체크리스트

푸시 전 확인사항:

- [ ] `.env` 파일이 Git에 포함되지 않았는지 확인
- [ ] API 키가 코드에 하드코딩되지 않았는지 확인
- [ ] 테스트 통과 (`pytest`)
- [ ] 린트 체크 통과 (`flake8`, `black`)
- [ ] 커밋 메시지가 규칙을 따르는지 확인
- [ ] 불필요한 파일이 포함되지 않았는지 확인 (`git status`)

---

**GitHub 저장소**: https://github.com/sminju98/reelmacro

**문제가 있으면 Issue를 생성해주세요!** 🙏

