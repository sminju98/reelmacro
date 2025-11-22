#!/usr/bin/env python3
"""
환경 설정 도우미 스크립트

이 스크립트는 .env 파일 생성과 필수 환경 변수 검증을 도와줍니다.
"""

import os
import secrets
import sys
from pathlib import Path


def generate_secret_key():
    """랜덤 시크릿 키 생성"""
    return secrets.token_urlsafe(32)


def create_env_file():
    """개발용 .env 파일 생성"""
    project_root = Path(__file__).parent.parent
    env_example = project_root / "config" / "development.env.example"
    env_file = project_root / ".env"
    
    if env_file.exists():
        response = input(".env 파일이 이미 존재합니다. 덮어쓰시겠습니까? (y/N): ")
        if response.lower() != 'y':
            print("취소되었습니다.")
            return False
    
    # 예시 파일 복사
    with open(env_example, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # JWT 시크릿 키 자동 생성
    secret_key = generate_secret_key()
    content = content.replace(
        'JWT_SECRET_KEY=CHANGE_THIS_TO_RANDOM_SECRET_KEY',
        f'JWT_SECRET_KEY={secret_key}'
    )
    
    # .env 파일 저장
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ .env 파일이 생성되었습니다: {env_file}")
    print(f"🔑 JWT Secret Key가 자동 생성되었습니다.")
    return True


def validate_env():
    """필수 환경 변수 검증"""
    from dotenv import load_dotenv
    
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    
    if not env_file.exists():
        print("❌ .env 파일이 없습니다. 먼저 .env 파일을 생성하세요.")
        return False
    
    load_dotenv(env_file)
    
    required_vars = {
        'OPENAI_API_KEY': 'OpenAI API 키',
        'ELEVENLABS_API_KEY': 'ElevenLabs API 키',
        'UNSPLASH_ACCESS_KEY': 'Unsplash Access 키',
        'PEXELS_API_KEY': 'Pexels API 키',
        'DATABASE_URL': '데이터베이스 URL',
        'REDIS_URL': 'Redis URL',
        'JWT_SECRET_KEY': 'JWT Secret 키',
    }
    
    missing = []
    placeholder_values = [
        'your-', 'CHANGE_THIS', 'sk-your-', 'your_'
    ]
    
    print("\n🔍 환경 변수 검증 중...\n")
    
    for var, description in required_vars.items():
        value = os.getenv(var, '')
        
        if not value:
            missing.append(f"  ❌ {var}: 값이 설정되지 않았습니다")
        elif any(placeholder in value for placeholder in placeholder_values):
            missing.append(f"  ⚠️  {var}: 예시 값입니다. 실제 값으로 변경하세요")
        else:
            print(f"  ✅ {var}: 설정됨")
    
    if missing:
        print("\n⚠️  다음 환경 변수를 확인하세요:\n")
        for msg in missing:
            print(msg)
        print("\n.env 파일을 열어 위 값들을 실제 API 키로 변경하세요.")
        return False
    else:
        print("\n✅ 모든 필수 환경 변수가 올바르게 설정되었습니다!")
        return True


def show_api_key_guide():
    """API 키 발급 가이드 출력"""
    print("\n" + "="*60)
    print("📚 API 키 발급 가이드")
    print("="*60)
    
    guides = {
        "OpenAI API": {
            "url": "https://platform.openai.com/api-keys",
            "steps": [
                "1. OpenAI 계정 가입/로그인",
                "2. API Keys 페이지 접속",
                "3. 'Create new secret key' 클릭",
                "4. 생성된 키를 OPENAI_API_KEY에 설정"
            ],
            "cost": "GPT-4: ~$0.03/1K tokens (대본 1개당 약 $0.01-0.05)"
        },
        "ElevenLabs API": {
            "url": "https://elevenlabs.io/app/settings/api-keys",
            "steps": [
                "1. ElevenLabs 계정 가입/로그인",
                "2. Settings > API Keys 페이지 접속",
                "3. 'Generate API Key' 클릭",
                "4. 생성된 키를 ELEVENLABS_API_KEY에 설정"
            ],
            "cost": "프리티어: 10,000 chars/month (약 20개 영상)"
        },
        "Unsplash API": {
            "url": "https://unsplash.com/oauth/applications",
            "steps": [
                "1. Unsplash 계정 가입/로그인",
                "2. 'New Application' 클릭",
                "3. 약관 동의 후 애플리케이션 생성",
                "4. Access Key를 UNSPLASH_ACCESS_KEY에 설정"
            ],
            "cost": "무료 (50 requests/hour)"
        },
        "Pexels API": {
            "url": "https://www.pexels.com/api/",
            "steps": [
                "1. Pexels 계정 가입/로그인",
                "2. 'Request API' 버튼 클릭",
                "3. 이메일로 받은 API 키 확인",
                "4. API 키를 PEXELS_API_KEY에 설정"
            ],
            "cost": "무료 (200 requests/hour)"
        }
    }
    
    for service, info in guides.items():
        print(f"\n🔑 {service}")
        print(f"   URL: {info['url']}")
        print(f"   비용: {info['cost']}")
        print("   발급 방법:")
        for step in info['steps']:
            print(f"      {step}")
    
    print("\n" + "="*60)
    print("💡 팁: 개발 단계에서는 무료 티어로 충분히 테스트 가능합니다!")
    print("="*60 + "\n")


def main():
    """메인 실행 함수"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║          🎬 Reel Maker AI - 환경 설정 도우미            ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'create':
            create_env_file()
        elif command == 'validate':
            validate_env()
        elif command == 'guide':
            show_api_key_guide()
        else:
            print(f"알 수 없는 명령어: {command}")
            print_usage()
    else:
        # 대화형 모드
        print("무엇을 하시겠습니까?")
        print("1. .env 파일 생성")
        print("2. 환경 변수 검증")
        print("3. API 키 발급 가이드 보기")
        print("4. 모두 실행")
        
        choice = input("\n선택 (1-4): ").strip()
        
        if choice == '1':
            create_env_file()
        elif choice == '2':
            validate_env()
        elif choice == '3':
            show_api_key_guide()
        elif choice == '4':
            if create_env_file():
                print("\n다음 단계로 API 키 발급 가이드를 확인하세요.")
                show_api_key_guide()
                input("\nAPI 키를 .env 파일에 입력한 후 Enter를 누르세요...")
                validate_env()
        else:
            print("잘못된 선택입니다.")


def print_usage():
    """사용법 출력"""
    print("""
사용법:
    python scripts/setup_env.py [command]

명령어:
    create      .env 파일 생성
    validate    환경 변수 검증
    guide       API 키 발급 가이드 보기
    (없음)      대화형 모드
    """)


if __name__ == "__main__":
    main()

