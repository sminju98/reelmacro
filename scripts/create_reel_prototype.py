#!/usr/bin/env python3
"""
릴스 자동 생성 프로토타입

키워드를 입력하면 자동으로 릴스를 생성합니다.
"""

import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv
import requests
from datetime import datetime

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


class ReelMakerPrototype:
    """릴스 자동 생성 프로토타입"""
    
    def __init__(self):
        """초기화"""
        self.openai_key = os.getenv("OPENAI_API_KEY")
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        self.unsplash_key = os.getenv("UNSPLASH_ACCESS_KEY")
        
        print("🎬 Reel Maker AI - 프로토타입")
        print("=" * 60)
    
    def generate_script(self, keyword: str, duration: int = 30) -> dict:
        """
        OpenAI로 대본 생성
        
        Args:
            keyword: 키워드
            duration: 영상 길이 (초)
        
        Returns:
            대본 및 장면 정보
        """
        print(f"\n📝 1단계: 대본 생성 중... (키워드: '{keyword}')")
        
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_key)
            
            prompt = f"""
다음 키워드로 {duration}초 분량의 인스타그램 릴스 대본을 작성해주세요.

키워드: {keyword}

요구사항:
1. 첫 3초에 시선을 사로잡는 훅(Hook) 포함
2. 핵심 내용 3-4개 포인트로 구성
3. 마지막에 CTA(Call to Action) 포함
4. 각 장면마다 필요한 이미지 키워드 제시

형식:
[장면 1] 내용 - 이미지: 키워드
[장면 2] 내용 - 이미지: 키워드
...
"""
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 바이럴 인스타그램 릴스 전문 작가입니다."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            script = response.choices[0].message.content
            
            # 장면 파싱 (간단하게)
            scenes = []
            for line in script.split('\n'):
                if line.strip().startswith('[장면') or line.strip().startswith('장면'):
                    scenes.append(line.strip())
            
            if not scenes:
                # 장면 구분이 없으면 전체를 하나로
                scenes = [script]
            
            print(f"✅ 대본 생성 완료! ({len(scenes)}개 장면)")
            print(f"💰 사용 토큰: {response.usage.total_tokens}")
            
            return {
                "script": script,
                "scenes": scenes,
                "keyword": keyword
            }
            
        except Exception as e:
            print(f"❌ 대본 생성 실패: {str(e)}")
            raise
    
    def translate_keyword(self, keyword: str) -> str:
        """
        한국어 키워드를 영어로 번역 (이미지 검색용)
        
        Args:
            keyword: 한국어 키워드
        
        Returns:
            영어 키워드
        """
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_key)
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 번역가입니다. 주어진 한국어 키워드를 영어로 번역하세요. 이미지 검색에 최적화된 간단한 영어 단어로 번역하세요."
                    },
                    {
                        "role": "user",
                        "content": f"다음 키워드를 영어로 번역하세요: {keyword}\n\n짧은 영어 키워드만 반환하세요."
                    }
                ],
                max_tokens=20,
                temperature=0.3
            )
            
            translated = response.choices[0].message.content.strip()
            print(f"  🌐 번역: '{keyword}' → '{translated}'")
            return translated
            
        except:
            # 번역 실패 시 원본 반환
            return keyword
    
    def search_images(self, keyword: str, count: int = 5) -> list:
        """
        Unsplash에서 이미지 검색
        
        Args:
            keyword: 검색 키워드
            count: 이미지 개수
        
        Returns:
            이미지 URL 리스트
        """
        print(f"\n🖼️  2단계: 이미지 검색 중... ('{keyword}')")
        
        # 한국어 키워드면 영어로 번역
        search_keyword = keyword
        if any('\uac00' <= char <= '\ud7a3' for char in keyword):
            search_keyword = self.translate_keyword(keyword)
        
        try:
            params = {
                "query": search_keyword,
                "per_page": count,
                "client_id": self.unsplash_key,
                "orientation": "portrait"  # 세로 이미지 우선
            }
            
            response = requests.get(
                "https://api.unsplash.com/search/photos",
                params=params,
                timeout=10
            )
            
            if response.status_code != 200:
                print(f"⚠️  Unsplash 오류: {response.status_code}")
                return []
            
            results = response.json().get("results", [])
            
            images = []
            for photo in results:
                images.append({
                    "url": photo["urls"]["regular"],
                    "download_url": photo["links"]["download_location"],
                    "author": photo["user"]["name"]
                })
            
            print(f"✅ 이미지 {len(images)}개 검색 완료!")
            
            return images
            
        except Exception as e:
            print(f"❌ 이미지 검색 실패: {str(e)}")
            return []
    
    def download_images(self, images: list, output_dir: Path) -> list:
        """
        이미지 다운로드
        
        Args:
            images: 이미지 정보 리스트
            output_dir: 저장 디렉토리
        
        Returns:
            다운로드된 파일 경로 리스트
        """
        print(f"\n⬇️  3단계: 이미지 다운로드 중...")
        
        downloaded = []
        
        for i, img in enumerate(images, 1):
            try:
                # 이미지 다운로드
                response = requests.get(img["url"], timeout=10)
                
                if response.status_code == 200:
                    filepath = output_dir / f"image_{i}.jpg"
                    filepath.write_bytes(response.content)
                    downloaded.append(str(filepath))
                    print(f"  ✓ 이미지 {i}/{len(images)} 다운로드 완료")
                    
            except Exception as e:
                print(f"  ✗ 이미지 {i} 다운로드 실패: {str(e)}")
        
        print(f"✅ 총 {len(downloaded)}개 이미지 다운로드 완료!")
        
        return downloaded
    
    def select_voice_by_concept(self, keyword: str, script: str) -> dict:
        """
        GPT가 컨셉에 맞는 음성을 자동 선택
        
        Args:
            keyword: 키워드
            script: 대본
        
        Returns:
            음성 정보 딕셔너리
        """
        print(f"\n🎤 음성 선택 중...")
        
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_key)
            
            prompt = f"""
다음 릴스 컨셉에 가장 어울리는 음성을 선택해주세요.

키워드: {keyword}
대본 일부: {script[:200]}...

사용 가능한 음성:
1. Sarah (cute) - 밝고 귀여운 여성 목소리, 뷰티/패션/일상 콘텐츠에 적합
2. Rachel (calm) - 차분하고 지적인 여성 목소리, 교육/뉴스 콘텐츠에 적합
3. Adam (energetic) - 활기차고 역동적인 남성 목소리, 스포츠/동기부여 콘텐츠에 적합
4. Bella (friendly) - 친근하고 따뜻한 여성 목소리, 브이로그/일상 콘텐츠에 적합
5. Antoni (professional) - 전문적인 남성 목소리, 비즈니스/기술 콘텐츠에 적합

출력 형식 (JSON):
{{"voice": "Sarah", "reason": "뷰티 콘텐츠라서 밝고 귀여운 톤이 적합"}}
"""
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "당신은 음성 디렉터입니다. 컨셉에 가장 어울리는 음성을 선택하세요."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=100,
                temperature=0.3
            )
            
            import json
            result_text = response.choices[0].message.content.strip()
            
            # JSON 추출
            if '{' in result_text and '}' in result_text:
                json_start = result_text.index('{')
                json_end = result_text.rindex('}') + 1
                result = json.loads(result_text[json_start:json_end])
                
                selected_voice = result.get("voice", "Sarah")
                reason = result.get("reason", "자동 선택")
                
                print(f"  ✅ 선택된 음성: {selected_voice}")
                print(f"  💡 이유: {reason}")
                
                return {"voice": selected_voice, "reason": reason}
            
        except Exception as e:
            print(f"  ⚠️  자동 선택 실패, 기본 음성 사용: {str(e)}")
        
        # 기본값
        return {"voice": "Sarah", "reason": "기본 음성"}
    
    def generate_voice(self, text: str, output_path: Path, voice_name: str = "Sarah") -> str:
        """
        ElevenLabs로 음성 생성
        
        Args:
            text: 대본 텍스트
            output_path: 저장 경로
            voice_name: 음성 이름
        
        Returns:
            음성 파일 경로
        """
        print(f"\n🎙️  4단계: 음성 생성 중... (음성: {voice_name})")
        
        try:
            # 음성 ID 매핑
            voice_map = {
                "Sarah": "EXAVITQu4vr4xnSDxMaL",      # 밝고 귀여운 여성
                "Rachel": "21m00Tcm4TlvDq8ikWAM",     # 차분한 여성
                "Adam": "pNInz6obpgDQGcFmaJgB",       # 활기찬 남성
                "Bella": "EXAVITQu4vr4xnSDxMaL",      # 친근한 여성 (Sarah와 동일)
                "Antoni": "ErXwobaYiN019PkySvjV"      # 전문적인 남성
            }
            
            voice_id = voice_map.get(voice_name, voice_map["Sarah"])
            
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            
            headers = {
                "xi-api-key": self.elevenlabs_key,
                "Content-Type": "application/json"
            }
            
            data = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {
                    "stability": 0.3,          # 낮을수록 더 밝고 귀여운 톤
                    "similarity_boost": 0.85,  # 높을수록 더 표현력 있음
                    "style": 0.5,              # 스타일 강도
                    "use_speaker_boost": True  # 목소리 강화
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
                print(f"✅ 음성 생성 완료! ({len(response.content)} bytes)")
                return str(output_path)
            else:
                print(f"❌ 음성 생성 실패: {response.status_code}")
                print(f"   응답: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ 음성 생성 실패: {str(e)}")
            return None
    
    def create_subtitles(self, script: str, duration: float) -> list:
        """
        대본에서 핵심 자막 생성 (타이밍 포함)
        
        Args:
            script: 대본 텍스트
            duration: 총 영상 길이
        
        Returns:
            자막 정보 리스트 [{text, start, end}]
        """
        print(f"\n✍️  자막 생성 중...")
        
        # GPT로 핵심 문장만 추출
        try:
            from openai import OpenAI
            
            client = OpenAI(api_key=self.openai_key)
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system",
                        "content": "대본에서 릴스 자막으로 적합한 핵심 문장 3-5개만 추출하세요. 각 문장은 짧고 임팩트 있어야 합니다."
                    },
                    {
                        "role": "user",
                        "content": f"다음 대본에서 자막으로 쓸 핵심 문장 3-5개만 추출해주세요:\n\n{script}\n\n출력 형식: 한 줄에 하나씩, 번호 없이"
                    }
                ],
                max_tokens=200,
                temperature=0.3
            )
            
            subtitle_text = response.choices[0].message.content.strip()
            sentences = [s.strip() for s in subtitle_text.split('\n') if s.strip()]
            
        except:
            # GPT 실패 시 대본에서 직접 추출
            sentences = []
            for line in script.split('\n'):
                line = line.strip()
                if line and not line.startswith('[') and not line.startswith('장면') and not line.startswith('-') and not line.startswith('이미지:'):
                    if '?' in line or '!' in line or len(line) > 10:
                        sentences.append(line)
                        if len(sentences) >= 5:
                            break
        
        # 최대 5개로 제한
        sentences = sentences[:5]
        
        if not sentences:
            sentences = ["자막을 생성할 수 없습니다"]
        
        # 각 자막에 균등하게 시간 할당
        time_per_subtitle = duration / len(sentences)
        
        subtitles = []
        current_time = 0
        
        for sentence in sentences:
            # 문장이 너무 길면 줄여서
            if len(sentence) > 50:
                sentence = sentence[:47] + "..."
            
            subtitles.append({
                'text': sentence,
                'start': current_time,
                'end': current_time + time_per_subtitle
            })
            
            current_time += time_per_subtitle
        
        print(f"✅ 자막 {len(subtitles)}개 생성 완료!")
        
        return subtitles
    
    def create_video(
        self, 
        images: list, 
        audio_path: str, 
        script: str,
        output_path: Path
    ) -> str:
        """
        FFmpeg로 영상 생성 (자막 포함)
        
        Args:
            images: 이미지 파일 경로 리스트
            audio_path: 음성 파일 경로
            script: 대본
            output_path: 출력 경로
        
        Returns:
            생성된 영상 파일 경로
        """
        print(f"\n🎬 6단계: 영상 합성 중...")
        
        try:
            from PIL import Image
            import subprocess
            
            # 음성 로드하여 길이 확인
            if audio_path and os.path.exists(audio_path):
                # FFprobe로 음성 길이 확인
                try:
                    result = subprocess.run(
                        ['ffprobe', '-v', 'error', '-show_entries',
                         'format=duration', '-of',
                         'default=noprint_wrappers=1:nokey=1', audio_path],
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    total_duration = float(result.stdout)
                except:
                    total_duration = 30
            else:
                print("⚠️  음성 파일이 없어 기본 길이(30초) 사용")
                total_duration = 30
            
            # 각 이미지당 시간 계산
            if images:
                time_per_image = total_duration / len(images)
            else:
                print("❌ 이미지가 없습니다!")
                return None
            
            print(f"📊 영상 정보:")
            print(f"   - 이미지: {len(images)}개")
            print(f"   - 총 길이: {total_duration:.1f}초")
            print(f"   - 이미지당: {time_per_image:.1f}초")
            
            # 이미지 리사이즈 (1080x1920, 9:16)
            resized_images = []
            for i, img_path in enumerate(images):
                try:
                    img = Image.open(img_path)
                    
                    # 세로 길이를 1920으로 조정
                    aspect_ratio = img.width / img.height
                    new_height = 1920
                    new_width = int(new_height * aspect_ratio)
                    
                    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # 중앙 크롭 (1080x1920)
                    if new_width > 1080:
                        left = (new_width - 1080) // 2
                        img_resized = img_resized.crop((left, 0, left + 1080, 1920))
                    elif new_width < 1080:
                        # 패딩 추가
                        new_img = Image.new('RGB', (1080, 1920), (0, 0, 0))
                        left = (1080 - new_width) // 2
                        new_img.paste(img_resized, (left, 0))
                        img_resized = new_img
                    
                    # 저장
                    resized_path = TEMP_DIR / f"resized_{i}.jpg"
                    img_resized.save(resized_path, 'JPEG', quality=95)
                    resized_images.append(str(resized_path))
                    
                    print(f"  ✓ 이미지 {i+1}/{len(images)} 처리 완료")
                    
                except Exception as e:
                    print(f"  ✗ 이미지 {i+1} 처리 실패: {str(e)}")
            
            if not resized_images:
                print("❌ 처리된 이미지가 없습니다!")
                return None
            
            print("\n🎥 FFmpeg으로 영상 생성 중...")
            
            # 각 이미지를 영상 클립으로 변환
            video_clips = []
            for i, img_path in enumerate(resized_images):
                clip_path = TEMP_DIR / f"clip_{i}.mp4"
                
                # 이미지를 지정된 길이의 영상으로 변환
                cmd = [
                    'ffmpeg', '-y',
                    '-loop', '1',
                    '-i', img_path,
                    '-t', str(time_per_image),
                    '-vf', 'fps=30,format=yuv420p',
                    '-c:v', 'libx264',
                    '-preset', 'medium',
                    '-crf', '23',
                    str(clip_path)
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    video_clips.append(str(clip_path))
                else:
                    print(f"  ✗ 클립 {i+1} 생성 실패")
            
            if not video_clips:
                print("❌ 생성된 영상 클립이 없습니다!")
                return None
            
            # 2. 모든 클립을 하나로 합치기
            concat_file = TEMP_DIR / "concat_list.txt"
            with open(concat_file, 'w') as f:
                for clip_path in video_clips:
                    f.write(f"file '{clip_path}'\n")
            
            temp_video = TEMP_DIR / "temp_video.mp4"
            
            cmd = [
                'ffmpeg', '-y',
                '-f', 'concat',
                '-safe', '0',
                '-i', str(concat_file),
                '-c', 'copy',
                str(temp_video)
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"❌ 영상 합치기 실패: {result.stderr[:200]}")
                return None
            
            print("✅ 영상 클립 생성 및 합치기 완료!")
            
            # 3. 자막 생성
            subtitles = self.create_subtitles(script, total_duration)
            
            # 4. SRT 자막 파일 생성
            srt_file = TEMP_DIR / "subtitles.srt"
            with open(srt_file, 'w', encoding='utf-8') as f:
                for i, sub in enumerate(subtitles, 1):
                    # SRT 형식
                    start_time = self._format_time(sub['start'])
                    end_time = self._format_time(sub['end'])
                    
                    f.write(f"{i}\n")
                    f.write(f"{start_time} --> {end_time}\n")
                    f.write(f"{sub['text']}\n")
                    f.write("\n")
            
            print("✅ SRT 자막 파일 생성 완료!")
            
            # 5. 음성 및 자막 추가
            if audio_path and os.path.exists(audio_path):
                print("🎙️  음성 및 자막 추가 중...")
                
                # 한국어 폰트 경로 (macOS 기본 폰트)
                font_path = "/System/Library/Fonts/Supplemental/AppleGothic.ttf"
                
                # 자막 스타일 설정 (작고 하단에 표시)
                subtitle_filter = (
                    f"subtitles={srt_file}:force_style='"
                    f"FontName=AppleSDGothicNeo-Bold,"
                    f"FontSize=24,"              # 작은 크기
                    f"PrimaryColour=&HFFFFFF&,"  # 흰색
                    f"OutlineColour=&H000000&,"  # 검은색 테두리
                    f"Outline=2,"                # 테두리 두께 줄임
                    f"Shadow=1,"                 # 그림자 줄임
                    f"Alignment=2,"              # 하단 중앙
                    f"MarginV=50"                # 하단 여백 줄임 (더 아래로)
                    f"'"
                )
                
                cmd = [
                    'ffmpeg', '-y',
                    '-i', str(temp_video),
                    '-i', audio_path,
                    '-vf', subtitle_filter,
                    '-c:v', 'libx264',
                    '-c:a', 'aac',
                    '-shortest',
                    str(output_path)
                ]
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode != 0:
                    print(f"❌ 자막 추가 실패: {result.stderr[:200]}")
                    # 자막 없이 음성만 추가
                    cmd = [
                        'ffmpeg', '-y',
                        '-i', str(temp_video),
                        '-i', audio_path,
                        '-c:v', 'copy',
                        '-c:a', 'aac',
                        '-shortest',
                        str(output_path)
                    ]
                    subprocess.run(cmd, capture_output=True, text=True)
            else:
                # 음성 없이 저장
                import shutil
                shutil.copy(temp_video, output_path)
            
            # 임시 파일 정리
            for img in resized_images:
                try:
                    os.remove(img)
                except:
                    pass
            
            # 클립 파일들도 정리
            if 'video_clips' in locals():
                for clip in video_clips:
                    try:
                        os.remove(clip)
                    except:
                        pass
            
            try:
                os.remove(temp_video)
                os.remove(concat_file)
                if 'srt_file' in locals():
                    os.remove(srt_file)
            except:
                pass
            
            print(f"✅ 영상 생성 완료!")
            print(f"📁 저장 위치: {output_path}")
            
            return str(output_path)
    
            
        except Exception as e:
            print(f"❌ 영상 생성 실패: {str(e)}")
            import traceback
            traceback.print_exc()
            return None
    
    def _format_time(self, seconds: float) -> str:
        """
        초를 SRT 시간 형식으로 변환
        
        Args:
            seconds: 초 단위 시간
        
        Returns:
            HH:MM:SS,mmm 형식 문자열
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
    
    def create_reel(self, keyword: str, duration: int = 30, voice_style: str = "cute") -> str:
        """
        전체 릴스 생성 프로세스
        
        Args:
            keyword: 키워드
            duration: 영상 길이
        
        Returns:
            생성된 영상 경로
        """
        print(f"\n🚀 '{keyword}' 키워드로 릴스 생성을 시작합니다!\n")
        
        try:
            # 1. 대본 생성
            script_data = self.generate_script(keyword, duration)
            
            # 2. 이미지 검색
            images = self.search_images(keyword, count=5)
            
            if not images:
                print("⚠️  대체 키워드로 재검색...")
                images = self.search_images("abstract art", count=5)
            
            # 3. 이미지 다운로드
            downloaded_images = self.download_images(images, TEMP_DIR)
            
            if not downloaded_images:
                print("❌ 다운로드된 이미지가 없습니다!")
                return None
            
            # 4. GPT가 컨셉에 맞는 음성 선택
            voice_info = self.select_voice_by_concept(keyword, script_data["script"])
            
            # 5. 음성 생성
            audio_path = TEMP_DIR / "voice.mp3"
            
            # 대본에서 실제 텍스트만 추출 (간단하게)
            script_text = script_data["script"]
            # '[장면 X]' 같은 마커 제거
            clean_text = []
            for line in script_text.split('\n'):
                if not line.strip().startswith('[') and not line.strip().startswith('장면'):
                    if line.strip() and not line.strip().startswith('-') and not line.strip().startswith('이미지:'):
                        clean_text.append(line.strip())
            
            voice_text = ' '.join(clean_text[:8])  # 처음 8줄
            
            if len(voice_text) < 10:
                voice_text = f"{keyword}에 대한 이야기입니다. 자세한 내용을 알아보겠습니다."
            
            voice_path = self.generate_voice(voice_text, audio_path, voice_info["voice"])
            
            # 6. 영상 합성
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"reel_{keyword}_{timestamp}.mp4"
            output_path = OUTPUT_DIR / output_filename
            
            video_path = self.create_video(
                downloaded_images,
                voice_path,
                script_data["script"],
                output_path
            )
            
            # 임시 파일 정리
            print("\n🧹 임시 파일 정리 중...")
            for img in downloaded_images:
                try:
                    os.remove(img)
                except:
                    pass
            
            if voice_path and os.path.exists(voice_path):
                try:
                    os.remove(voice_path)
                except:
                    pass
            
            return video_path
            
        except Exception as e:
            print(f"\n❌ 릴스 생성 중 오류 발생: {str(e)}")
            import traceback
            traceback.print_exc()
            return None


def main():
    """메인 실행 함수"""
    print("""
╔═══════════════════════════════════════════════════════════╗
║       🎬 Reel Maker AI - 프로토타입 v0.1               ║
║          키워드만 입력하면 릴스 자동 생성!                ║
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
    
    # 릴스 생성
    maker = ReelMakerPrototype()
    video_path = maker.create_reel(keyword)
    
    if video_path:
        print("\n" + "="*60)
        print("🎉 릴스 생성 완료!")
        print("="*60)
        print(f"📁 파일: {video_path}")
        print(f"📱 이제 인스타그램에 업로드하세요!")
        print("="*60)
    else:
        print("\n❌ 릴스 생성에 실패했습니다.")


if __name__ == "__main__":
    main()

