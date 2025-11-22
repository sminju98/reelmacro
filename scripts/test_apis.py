#!/usr/bin/env python3
"""
API 연동 테스트 스크립트

OpenAI, ElevenLabs, Unsplash API가 올바르게 작동하는지 테스트합니다.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 프로젝트 루트를 Python path에 추가
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 환경 변수 로드
load_dotenv(project_root / ".env")


def test_openai():
    """OpenAI API 테스트 - 간단한 대본 생성"""
    print("\n" + "="*60)
    print("🤖 OpenAI API 테스트")
    print("="*60)
    
    try:
        from openai import OpenAI
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key.startswith("sk-your-"):
            print("❌ OPENAI_API_KEY가 설정되지 않았습니다.")
            return False
        
        print("📡 OpenAI API 연결 중...")
        client = OpenAI(api_key=api_key)
        
        # 간단한 대본 생성 테스트
        print("✍️  테스트 대본 생성 중... (키워드: 'AI 트렌드')")
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": "당신은 바이럴 인스타그램 릴스 대본 작가입니다. 30초 분량의 짧고 임팩트 있는 대본을 작성하세요."
                },
                {
                    "role": "user",
                    "content": "키워드: 'AI 트렌드'\n30초 분량의 인스타그램 릴스 대본을 작성해주세요."
                }
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        script = response.choices[0].message.content
        
        print("\n✅ OpenAI API 연결 성공!")
        print(f"📝 생성된 대본 (일부):")
        print("-" * 60)
        print(script[:200] + "..." if len(script) > 200 else script)
        print("-" * 60)
        print(f"💰 사용 토큰: {response.usage.total_tokens} tokens")
        
        return True
        
    except ImportError:
        print("❌ openai 패키지가 설치되지 않았습니다.")
        print("   설치: pip install openai")
        return False
    except Exception as e:
        print(f"❌ OpenAI API 테스트 실패: {str(e)}")
        return False


def test_elevenlabs():
    """ElevenLabs API 테스트 - 간단한 TTS"""
    print("\n" + "="*60)
    print("🎙️  ElevenLabs API 테스트")
    print("="*60)
    
    try:
        import requests
        
        api_key = os.getenv("ELEVENLABS_API_KEY")
        if not api_key or api_key.startswith("your-"):
            print("❌ ELEVENLABS_API_KEY가 설정되지 않았습니다.")
            return False
        
        print("📡 ElevenLabs API 연결 중...")
        
        # 사용 가능한 음성 목록 조회
        headers = {"xi-api-key": api_key}
        response = requests.get(
            "https://api.elevenlabs.io/v1/voices",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            voices = response.json().get("voices", [])
            print(f"\n✅ ElevenLabs API 연결 성공!")
            print(f"🎤 사용 가능한 음성: {len(voices)}개")
            
            if voices:
                print("\n사용 가능한 음성 목록 (일부):")
                for voice in voices[:3]:
                    print(f"  - {voice['name']} ({voice['voice_id']})")
            
            # 간단한 TTS 테스트 (실제 생성은 생략 - 비용 절약)
            print("\n💡 TTS 음성 생성은 실제 개발 시 테스트됩니다.")
            print("   (API 연결만 확인하여 비용을 절약합니다)")
            
            return True
        else:
            print(f"❌ ElevenLabs API 오류: {response.status_code}")
            print(f"   응답: {response.text}")
            return False
            
    except ImportError:
        print("❌ requests 패키지가 설치되지 않았습니다.")
        print("   설치: pip install requests")
        return False
    except Exception as e:
        print(f"❌ ElevenLabs API 테스트 실패: {str(e)}")
        return False


def test_unsplash():
    """Unsplash API 테스트 - 이미지 검색"""
    print("\n" + "="*60)
    print("🖼️  Unsplash API 테스트")
    print("="*60)
    
    try:
        import requests
        
        api_key = os.getenv("UNSPLASH_ACCESS_KEY")
        if not api_key or api_key.startswith("your-"):
            print("❌ UNSPLASH_ACCESS_KEY가 설정되지 않았습니다.")
            return False
        
        print("📡 Unsplash API 연결 중...")
        print("🔍 테스트 검색: 'coffee'")
        
        # 이미지 검색 테스트
        params = {
            "query": "coffee",
            "per_page": 3,
            "client_id": api_key
        }
        
        response = requests.get(
            "https://api.unsplash.com/search/photos",
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            total = data.get("total", 0)
            
            print(f"\n✅ Unsplash API 연결 성공!")
            print(f"📊 검색 결과: {total}개 이미지")
            
            if results:
                print("\n검색된 이미지 (상위 3개):")
                for i, photo in enumerate(results, 1):
                    print(f"\n  {i}. 이미지 정보:")
                    desc = photo.get('description') or photo.get('alt_description', 'N/A')
                    print(f"     - 설명: {desc[:50] if desc != 'N/A' else 'N/A'}...")
                    print(f"     - 작가: {photo.get('user', {}).get('name', 'Unknown')}")
                    print(f"     - 크기: {photo.get('width', 'N/A')} x {photo.get('height', 'N/A')}")
                    print(f"     - URL: {photo.get('urls', {}).get('regular', 'N/A')[:60]}...")
            
            return True
        else:
            print(f"❌ Unsplash API 오류: {response.status_code}")
            print(f"   응답: {response.text}")
            return False
            
    except ImportError:
        print("❌ requests 패키지가 설치되지 않았습니다.")
        print("   설치: pip install requests")
        return False
    except Exception as e:
        print(f"❌ Unsplash API 테스트 실패: {str(e)}")
        return False


def main():
    """메인 테스트 실행"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║          🎬 Reel Maker AI - API 연동 테스트             ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    print("📋 테스트 항목:")
    print("   1. OpenAI API (대본 생성)")
    print("   2. ElevenLabs API (음성 생성)")
    print("   3. Unsplash API (이미지 검색)")
    
    results = {
        "OpenAI": False,
        "ElevenLabs": False,
        "Unsplash": False
    }
    
    # 각 API 테스트 실행
    results["OpenAI"] = test_openai()
    results["ElevenLabs"] = test_elevenlabs()
    results["Unsplash"] = test_unsplash()
    
    # 결과 요약
    print("\n" + "="*60)
    print("📊 테스트 결과 요약")
    print("="*60)
    
    for api, success in results.items():
        status = "✅ 성공" if success else "❌ 실패"
        print(f"  {api:15} : {status}")
    
    total = sum(results.values())
    print(f"\n총 {total}/3 개 API 연결 성공")
    
    if total == 3:
        print("\n🎉 모든 API가 정상 작동합니다!")
        print("   이제 릴스 자동 생성 개발을 시작할 수 있습니다.")
    elif total > 0:
        print("\n⚠️  일부 API에 문제가 있습니다.")
        print("   실패한 API의 키를 확인해주세요.")
    else:
        print("\n❌ 모든 API 연결에 실패했습니다.")
        print("   .env 파일의 API 키를 확인해주세요.")
    
    print("\n" + "="*60)
    
    return total == 3


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

