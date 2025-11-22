#!/usr/bin/env python3
"""
카드 뉴스 자동 생성 프로토타입

키워드를 입력하면 웹에서 최신 트렌드를 검색하고 카드 뉴스 형식의 릴스를 생성합니다.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import requests
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import textwrap

# 프로젝트 루트 설정
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# 환경 변수 로드
load_dotenv(project_root / ".env")

# 필요한 디렉토리 생성
TEMP_DIR = project_root / "temp"
OUTPUT_DIR = project_root / "output"
TEMP_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)


class CardNewsGenerator:
    """카드 뉴스 생성기"""
    
    def __init__(self):
        """초기화"""
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        
        print("🎴 Card News Generator - 프로토타입")
        print("=" * 60)
    
    def search_web_trends(self, keyword: str) -> dict:
        """
        웹에서 최신 트렌드 검색
        
        Args:
            keyword: 검색 키워드
        
        Returns:
            트렌드 정보
        """
        print(f"\n🔍 1단계: 웹에서 '{keyword}' 트렌드 검색 중...")
        
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_key)
            
            # GPT에게 최신 정보 요청 (실제로는 웹 API 사용해야 하지만 프로토타입에서는 GPT 사용)
            prompt = f"""
다음 키워드에 대한 최신 트렌드와 핵심 정보를 조사해서 카드 뉴스용 콘텐츠를 만들어주세요.

키워드: {keyword}

출력 형식 (JSON):
{{
    "title": "메인 제목 (짧고 임팩트 있게)",
    "cards": [
        {{
            "number": 1,
            "title": "카드 제목",
            "content": "핵심 내용 (2-3문장)"
        }},
        ...5개 카드
    ],
    "hashtags": ["해시태그1", "해시태그2", ...]
}}

카드는 5-7개로 구성하고, 각 카드는 핵심만 간결하게 작성하세요.
"""
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 카드 뉴스 전문 에디터입니다. 최신 트렌드를 반영한 임팩트 있는 카드 뉴스를 만듭니다."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            import json
            content = response.choices[0].message.content.strip()
            
            # JSON 추출
            if '{' in content and '}' in content:
                json_start = content.index('{')
                json_end = content.rindex('}') + 1
                data = json.loads(content[json_start:json_end])
                
                print(f"✅ 트렌드 정보 수집 완료!")
                print(f"📰 제목: {data.get('title', '')}")
                print(f"🎴 카드: {len(data.get('cards', []))}개")
                
                return data
            
        except Exception as e:
            print(f"❌ 트렌드 검색 실패: {str(e)}")
            import traceback
            traceback.print_exc()
        
        # 기본 데이터
        return {
            "title": keyword,
            "cards": [
                {"number": 1, "title": "카드 1", "content": f"{keyword}에 대한 내용입니다."}
            ],
            "hashtags": [f"#{keyword}"]
        }
    
    def create_card_image(
        self, 
        card_data: dict, 
        total_cards: int,
        output_path: Path,
        card_type: str = "content"
    ) -> str:
        """
        카드 이미지 생성
        
        Args:
            card_data: 카드 데이터
            total_cards: 총 카드 수
            output_path: 저장 경로
            card_type: 카드 타입 (title, content, ending)
        
        Returns:
            생성된 이미지 경로
        """
        # 릴스 사이즈
        width = 1080
        height = 1920
        
        # 배경색 (그라디언트 느낌)
        if card_type == "title":
            bg_color = (138, 43, 226)  # 보라색
            text_color = (255, 255, 255)
        elif card_type == "ending":
            bg_color = (255, 20, 147)  # 핑크
            text_color = (255, 255, 255)
        else:
            # 카드 번호에 따라 색상 변경
            colors = [
                (100, 149, 237),  # 블루
                (255, 127, 80),   # 코랄
                (72, 209, 204),   # 터콰이즈
                (255, 215, 0),    # 골드
                (147, 112, 219),  # 퍼플
            ]
            idx = (card_data.get('number', 1) - 1) % len(colors)
            bg_color = colors[idx]
            text_color = (255, 255, 255)
        
        # 이미지 생성
        img = Image.new('RGB', (width, height), bg_color)
        draw = ImageDraw.Draw(img)
        
        try:
            # 한글 폰트 (macOS)
            title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/AppleGothic.ttf", 70)
            content_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/AppleGothic.ttf", 45)
            small_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/AppleGothic.ttf", 35)
        except:
            # 폰트 로드 실패 시 기본 폰트
            title_font = ImageFont.load_default()
            content_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
        
        # 타이틀 카드
        if card_type == "title":
            title = card_data.get('title', '제목')
            
            # 제목 중앙 정렬
            lines = textwrap.wrap(title, width=15)
            y = height // 2 - (len(lines) * 80)
            
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=title_font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
                
                # 텍스트 그림자
                draw.text((x+3, y+3), line, font=title_font, fill=(0, 0, 0))
                # 텍스트
                draw.text((x, y), line, font=title_font, fill=text_color)
                y += 100
        
        # 콘텐츠 카드
        elif card_type == "content":
            # 카드 번호
            number = card_data.get('number', 1)
            draw.text((50, 100), f"#{number}/{total_cards}", font=small_font, fill=(255, 255, 255, 200))
            
            # 카드 제목
            card_title = card_data.get('title', '제목')
            lines = textwrap.wrap(card_title, width=20)
            y = 400
            
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=title_font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
                
                # 텍스트 그림자
                draw.text((x+2, y+2), line, font=title_font, fill=(0, 0, 0))
                draw.text((x, y), line, font=title_font, fill=text_color)
                y += 90
            
            # 카드 내용
            content = card_data.get('content', '')
            content_lines = textwrap.wrap(content, width=25)
            y += 100
            
            for line in content_lines[:6]:  # 최대 6줄
                bbox = draw.textbbox((0, 0), line, font=content_font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
                
                draw.text((x, y), line, font=content_font, fill=text_color)
                y += 60
        
        # 엔딩 카드
        else:
            text = "팔로우 & 좋아요\n부탁드려요! 💖"
            lines = text.split('\n')
            y = height // 2 - 100
            
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=title_font)
                text_width = bbox[2] - bbox[0]
                x = (width - text_width) // 2
                
                draw.text((x+2, y+2), line, font=title_font, fill=(0, 0, 0))
                draw.text((x, y), line, font=title_font, fill=text_color)
                y += 100
        
        # 저장
        img.save(output_path, 'JPEG', quality=100)
        
        return str(output_path)
    
    def generate_voice_for_cards(self, cards: list, output_dir: Path) -> list:
        """
        각 카드별로 음성 생성
        
        Args:
            cards: 카드 데이터 리스트
            output_dir: 저장 디렉토리
        
        Returns:
            음성 파일 경로 리스트
        """
        print(f"\n🎙️  3단계: 각 카드별 음성 생성 중...")
        
        # Sarah (밝고 귀여운) 음성 사용
        voice_id = "EXAVITQu4vr4xnSDxMaL"
        
        audio_files = []
        
        for i, card in enumerate(cards, 1):
            try:
                text = f"{card.get('title', '')}. {card.get('content', '')}"
                
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
                
                headers = {
                    "xi-api-key": self.elevenlabs_key,
                    "Content-Type": "application/json"
                }
                
                data = {
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {
                        "stability": 0.3,
                        "similarity_boost": 0.85,
                        "style": 0.5,
                        "use_speaker_boost": True
                    }
                }
                
                response = requests.post(
                    url,
                    json=data,
                    headers=headers,
                    timeout=30
                )
                
                if response.status_code == 200:
                    audio_path = output_dir / f"voice_{i}.mp3"
                    audio_path.write_bytes(response.content)
                    audio_files.append(str(audio_path))
                    print(f"  ✓ 카드 {i}/{len(cards)} 음성 생성 완료")
                else:
                    print(f"  ✗ 카드 {i} 음성 생성 실패")
                    
            except Exception as e:
                print(f"  ✗ 카드 {i} 음성 생성 오류: {str(e)}")
        
        print(f"✅ 총 {len(audio_files)}개 음성 생성 완료!")
        
        return audio_files
    
    def create_card_news_video(
        self,
        cards: list,
        card_images: list,
        audio_files: list,
        title: str,
        output_path: Path
    ) -> str:
        """
        카드 뉴스 영상 생성 (고품질)
        
        Args:
            cards: 카드 데이터
            card_images: 카드 이미지 경로 리스트
            audio_files: 음성 파일 경로 리스트
            title: 제목
            output_path: 출력 경로
        
        Returns:
            생성된 영상 경로
        """
        print(f"\n🎬 4단계: 고품질 카드 뉴스 영상 생성 중...")
        
        try:
            import subprocess
            
            # 각 음성 파일의 길이 확인
            def get_audio_duration(audio_path):
                try:
                    result = subprocess.run(
                        ['ffprobe', '-v', 'error', '-show_entries',
                         'format=duration', '-of',
                         'default=noprint_wrappers=1:nokey=1', audio_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    return float(result.stdout)
                except:
                    return 3.0  # 기본 3초
            
            # 각 카드를 음성 길이만큼 영상으로 변환
            video_clips = []
            
            for i, (img_path, audio_path) in enumerate(zip(card_images, audio_files), 1):
                duration = get_audio_duration(audio_path)
                clip_path = TEMP_DIR / f"card_clip_{i}.mp4"
                
                # 이미지 + 음성을 영상 클립으로 변환 (고품질)
                cmd = [
                    'ffmpeg', '-y',
                    '-loop', '1',
                    '-i', img_path,
                    '-i', audio_path,
                    '-t', str(duration),
                    '-vf', 'fps=30,format=yuv420p',
                    '-c:v', 'libx264',
                    '-preset', 'slow',      # 고품질 인코딩
                    '-crf', '18',           # 높은 품질 (낮을수록 좋음, 18=매우 좋음)
                    '-b:v', '8M',           # 비트레이트 8Mbps
                    '-c:a', 'aac',
                    '-b:a', '192k',         # 오디오 비트레이트
                    '-shortest',
                    str(clip_path)
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    video_clips.append(str(clip_path))
                    print(f"  ✓ 카드 {i}/{len(card_images)} 클립 생성 ({duration:.1f}초)")
                else:
                    print(f"  ✗ 카드 {i} 클립 생성 실패")
            
            if not video_clips:
                print("❌ 생성된 클립이 없습니다!")
                return None
            
            # 모든 클립을 하나로 합치기
            concat_file = TEMP_DIR / "card_concat.txt"
            with open(concat_file, 'w') as f:
                for clip_path in video_clips:
                    f.write(f"file '{clip_path}'\n")
            
            print(f"\n🎥 {len(video_clips)}개 클립 합치는 중...")
            
            cmd = [
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(concat_file),
                '-c', 'copy',
                str(output_path)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ 영상 합치기 실패: {result.stderr[:200]}")
                return None
            
            # 임시 파일 정리
            for clip in video_clips:
                try:
                    os.remove(clip)
                except:
                    pass
            
            try:
                os.remove(concat_file)
            except:
                pass
            
            print(f"✅ 고품질 영상 생성 완료!")
            print(f"📁 저장 위치: {output_path}")
            
            return str(output_path)
            
        except Exception as e:
            print(f"❌ 영상 생성 실패: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def create_card_news(self, keyword: str) -> str:
        """
        전체 카드 뉴스 생성 프로세스
        
        Args:
            keyword: 키워드
        
        Returns:
            생성된 영상 경로
        """
        print(f"\n🚀 '{keyword}' 키워드로 카드 뉴스 생성을 시작합니다!\n")
        
        try:
            # 1. 웹에서 트렌드 검색 및 카드 구성
            data = self.search_web_trends(keyword)
            
            cards = data.get('cards', [])
            title = data.get('title', keyword)
            
            if not cards:
                print("❌ 카드 데이터가 없습니다!")
                return None
            
            # 2. 카드 이미지 생성
            print(f"\n🎴 2단계: 카드 이미지 생성 중... ({len(cards)}개)")
            
            card_images = []
            
            # 타이틀 카드
            title_img_path = TEMP_DIR / "card_title.jpg"
            self.create_card_image(
                {'title': title}, 
                len(cards),
                title_img_path,
                'title'
            )
            card_images.append(str(title_img_path))
            print(f"  ✓ 타이틀 카드 생성 완료")
            
            # 콘텐츠 카드들
            for i, card in enumerate(cards, 1):
                img_path = TEMP_DIR / f"card_{i}.jpg"
                self.create_card_image(card, len(cards), img_path, 'content')
                card_images.append(str(img_path))
                print(f"  ✓ 카드 {i}/{len(cards)} 생성 완료")
            
            # 엔딩 카드
            ending_img_path = TEMP_DIR / "card_ending.jpg"
            self.create_card_image(
                {'title': '감사합니다'}, 
                len(cards),
                ending_img_path,
                'ending'
            )
            card_images.append(str(ending_img_path))
            print(f"  ✓ 엔딩 카드 생성 완료")
            
            print(f"✅ 총 {len(card_images)}개 카드 이미지 생성 완료!")
            
            # 3. 각 카드별 음성 생성
            # 타이틀 음성
            title_audio = TEMP_DIR / "voice_title.mp3"
            self.generate_single_voice(title, title_audio)
            audio_files = [str(title_audio)]
            
            # 카드 음성들
            card_audios = self.generate_voice_for_cards(cards, TEMP_DIR)
            audio_files.extend(card_audios)
            
            # 엔딩 음성
            ending_audio = TEMP_DIR / "voice_ending.mp3"
            self.generate_single_voice("팔로우와 좋아요 부탁드려요!", ending_audio)
            audio_files.append(str(ending_audio))
            
            # 4. 영상 합성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"cardnews_{keyword}_{timestamp}.mp4"
            final_output = OUTPUT_DIR / output_filename
            
            video_path = self.create_card_news_video(
                cards,
                card_images,
                audio_files,
                title,
                final_output
            )
            
            # 임시 파일 정리
            print("\n🧹 임시 파일 정리 중...")
            for img in card_images:
                try:
                    os.remove(img)
                except:
                    pass
            
            for audio in audio_files:
                try:
                    os.remove(audio)
                except:
                    pass
            
            return video_path
            
        except Exception as e:
            print(f"\n❌ 카드 뉴스 생성 중 오류 발생: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def generate_single_voice(self, text: str, output_path: Path) -> str:
        """단일 음성 생성"""
        try:
            voice_id = "EXAVITQu4vr4xnSDxMaL"  # Sarah
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "xi-api-key": self.elevenlabs_key,
                "Content-Type": "application/json"
            }
            
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.3,
                    "similarity_boost": 0.85,
                    "style": 0.5,
                    "use_speaker_boost": True
                }
            }
            
            response = requests.post(
                url,
                json=data,
                headers=headers,
                timeout=30
            )
            
            if response.status_code == 200:
                output_path.write_bytes(response.content)
                return str(output_path)
            
        except Exception as e:
            print(f"  ✗ 음성 생성 실패: {str(e)}")
        
        return None


def main():
    """메인 실행 함수"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║       🎴 Card News Generator - 프로토타입 v0.1         ║
║       웹 검색으로 실시간 트렌드 카드 뉴스 생성!          ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    # 키워드 입력
    if len(sys.argv) > 1:
        keyword = ' '.join(sys.argv[1:])
    else:
        keyword = input("🔑 키워드를 입력하세요: ").strip()
    
    if not keyword:
        print("❌ 키워드를 입력해주세요!")
        return
    
    # 카드 뉴스 생성
    generator = CardNewsGenerator()
    video_path = generator.create_card_news(keyword)
    
    if video_path:
        print("\n" + "="*60)
        print("🎉 카드 뉴스 생성 완료!")
        print("="*60)
        print(f"📁 파일: {video_path}")
        print(f"📱 고품질 영상으로 인스타그램에 업로드하세요!")
        print("="*60)
    else:
        print("\n❌ 카드 뉴스 생성에 실패했습니다.")


if __name__ == "__main__":
    main()

