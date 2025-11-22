# API 명세서 (API Documentation)
# 인스타그램 릴스 자동 생성 프로그램

**버전:** 1.0  
**Base URL:** `https://api.reelmaker.ai/v1`  
**작성일:** 2025-11-22

---

## 목차
1. [개요](#1-개요)
2. [인증](#2-인증)
3. [에러 처리](#3-에러-처리)
4. [Rate Limiting](#4-rate-limiting)
5. [API 엔드포인트](#5-api-엔드포인트)
6. [Webhook](#6-webhook)
7. [SDK 및 예제](#7-sdk-및-예제)

---

## 1. 개요

### 1.1 기본 정보
- **Protocol**: HTTPS only
- **Response Format**: JSON
- **Character Encoding**: UTF-8
- **API Version**: v1 (URL 경로에 포함)

### 1.2 환경별 Base URL

| 환경 | Base URL |
|------|----------|
| **Production** | `https://api.reelmaker.ai/v1` |
| **Staging** | `https://staging-api.reelmaker.ai/v1` |
| **Development** | `http://localhost:8000/v1` |

### 1.3 공통 헤더

모든 요청에 다음 헤더를 포함해야 합니다:

```http
Content-Type: application/json
Authorization: Bearer {access_token}
Accept: application/json
```

---

## 2. 인증

### 2.1 인증 방식
JWT (JSON Web Token) 기반 Bearer Token 인증

### 2.2 토큰 획득

#### POST /auth/register
신규 회원가입

**Request**:
```http
POST /v1/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securePassword123!",
  "name": "홍길동"
}
```

**Response** (201 Created):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "홍길동",
  "subscription_plan": "free",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "created_at": "2025-11-22T10:00:00Z"
}
```

**Validation Rules**:
- `email`: 유효한 이메일 형식, 최대 255자
- `password`: 최소 8자, 영문+숫자+특수문자 조합
- `name`: 최소 2자, 최대 100자

**Error Responses**:
```json
// 이메일 중복
{
  "error": {
    "code": "EMAIL_ALREADY_EXISTS",
    "message": "이미 등록된 이메일입니다.",
    "status": 409
  }
}

// 비밀번호 규칙 위반
{
  "error": {
    "code": "INVALID_PASSWORD",
    "message": "비밀번호는 최소 8자 이상이어야 합니다.",
    "status": 400
  }
}
```

---

#### POST /auth/login
로그인

**Request**:
```http
POST /v1/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securePassword123!"
}
```

**Response** (200 OK):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "홍길동",
    "subscription_plan": "free",
    "api_quota_remaining": 10
  }
}
```

**Error Responses**:
```json
// 인증 실패
{
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "이메일 또는 비밀번호가 올바르지 않습니다.",
    "status": 401
  }
}
```

---

#### POST /auth/refresh
토큰 갱신

**Request**:
```http
POST /v1/auth/refresh
Authorization: Bearer {current_token}
```

**Response** (200 OK):
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "expires_in": 86400
}
```

---

#### POST /auth/logout
로그아웃

**Request**:
```http
POST /v1/auth/logout
Authorization: Bearer {access_token}
```

**Response** (204 No Content)

---

## 3. 에러 처리

### 3.1 에러 응답 형식

모든 에러는 다음 형식으로 반환됩니다:

```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "사용자 친화적인 에러 메시지",
    "status": 400,
    "details": {
      "field": "keyword",
      "reason": "Field is required"
    },
    "timestamp": "2025-11-22T10:00:00Z",
    "request_id": "req_abc123"
  }
}
```

### 3.2 HTTP 상태 코드

| 코드 | 의미 | 설명 |
|------|------|------|
| **200** | OK | 요청 성공 |
| **201** | Created | 리소스 생성 성공 |
| **204** | No Content | 성공 (응답 본문 없음) |
| **400** | Bad Request | 잘못된 요청 |
| **401** | Unauthorized | 인증 실패 |
| **403** | Forbidden | 권한 없음 |
| **404** | Not Found | 리소스 없음 |
| **409** | Conflict | 리소스 충돌 |
| **422** | Unprocessable Entity | 검증 실패 |
| **429** | Too Many Requests | Rate Limit 초과 |
| **500** | Internal Server Error | 서버 에러 |
| **503** | Service Unavailable | 서비스 일시 중단 |

### 3.3 에러 코드 목록

| 코드 | HTTP 상태 | 설명 |
|------|-----------|------|
| `INVALID_REQUEST` | 400 | 잘못된 요청 형식 |
| `VALIDATION_ERROR` | 422 | 입력 검증 실패 |
| `UNAUTHORIZED` | 401 | 인증 토큰 없음/만료 |
| `FORBIDDEN` | 403 | 권한 없음 |
| `NOT_FOUND` | 404 | 리소스 없음 |
| `EMAIL_ALREADY_EXISTS` | 409 | 이메일 중복 |
| `RATE_LIMIT_EXCEEDED` | 429 | 요청 제한 초과 |
| `QUOTA_EXCEEDED` | 403 | API 할당량 초과 |
| `PAYMENT_REQUIRED` | 402 | 결제 필요 (유료 기능) |
| `EXTERNAL_API_ERROR` | 502 | 외부 API 에러 |
| `RENDERING_FAILED` | 500 | 영상 렌더링 실패 |
| `INTERNAL_ERROR` | 500 | 서버 내부 에러 |

---

## 4. Rate Limiting

### 4.1 제한 정책

| 플랜 | 시간당 요청 | 일일 영상 생성 |
|------|-------------|----------------|
| **Free** | 60 | 10 |
| **Basic** | 300 | 50 |
| **Pro** | 1000 | 200 |
| **Enterprise** | 무제한 | 무제한 |

### 4.2 Rate Limit 헤더

모든 응답에 다음 헤더가 포함됩니다:

```http
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1735200000
```

### 4.3 Rate Limit 초과 시

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "시간당 요청 제한을 초과했습니다. 1시간 후 다시 시도해주세요.",
    "status": 429,
    "details": {
      "limit": 60,
      "reset_at": "2025-11-22T11:00:00Z"
    }
  }
}
```

---

## 5. API 엔드포인트

### 5.1 프로젝트 관리

#### POST /projects
새 릴스 프로젝트 생성

**Description**: 키워드를 입력하여 새로운 릴스 영상 프로젝트를 생성합니다. 생성은 비동기로 처리되며, 완료 시 webhook 또는 polling으로 확인할 수 있습니다.

**Authentication**: Required

**Request**:
```http
POST /v1/projects
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "keyword": "AI 트렌드 2025",
  "settings": {
    "duration": 30,
    "voice": {
      "gender": "female",
      "tone": "bright",
      "language": "ko"
    },
    "style": "modern",
    "music": {
      "enabled": true,
      "genre": "upbeat"
    },
    "subtitle": {
      "enabled": true,
      "style": "bold",
      "position": "bottom"
    }
  }
}
```

**Parameters**:

| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| `keyword` | string | ✅ | 릴스 주제 키워드 (2-500자) |
| `settings.duration` | integer | ❌ | 영상 길이 (15, 30, 60, 90초) (기본: 30) |
| `settings.voice.gender` | string | ❌ | 음성 성별 (male, female) (기본: female) |
| `settings.voice.tone` | string | ❌ | 음성 톤 (bright, calm, energetic) (기본: bright) |
| `settings.voice.language` | string | ❌ | 언어 (ko, en) (기본: ko) |
| `settings.style` | string | ❌ | 스타일 프리셋 (modern, news, educational, minimal, dynamic) (기본: modern) |
| `settings.music.enabled` | boolean | ❌ | 배경음악 사용 여부 (기본: true) |
| `settings.music.genre` | string | ❌ | 음악 장르 (upbeat, calm, epic) (기본: upbeat) |
| `settings.subtitle.enabled` | boolean | ❌ | 자막 사용 여부 (기본: true) |
| `settings.subtitle.style` | string | ❌ | 자막 스타일 (bold, minimal, colorful) (기본: bold) |

**Response** (202 Accepted):
```json
{
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "estimated_completion_time": 180,
  "message": "영상 생성이 시작되었습니다.",
  "webhook_url": null,
  "created_at": "2025-11-22T10:00:00Z"
}
```

**Error Responses**:
```json
// 할당량 초과
{
  "error": {
    "code": "QUOTA_EXCEEDED",
    "message": "일일 영상 생성 한도를 초과했습니다.",
    "status": 403,
    "details": {
      "quota_limit": 10,
      "quota_used": 10,
      "reset_at": "2025-11-23T00:00:00Z"
    }
  }
}

// 잘못된 duration 값
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "영상 길이는 15, 30, 60, 90초 중 하나여야 합니다.",
    "status": 422,
    "details": {
      "field": "settings.duration",
      "provided": 45,
      "allowed": [15, 30, 60, 90]
    }
  }
}
```

---

#### GET /projects/{project_id}
프로젝트 상태 조회

**Description**: 특정 프로젝트의 현재 상태와 정보를 조회합니다.

**Authentication**: Required

**Request**:
```http
GET /v1/projects/550e8400-e29b-41d4-a716-446655440000
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "keyword": "AI 트렌드 2025",
  "status": "completed",
  "progress": 100,
  "script": "안녕하세요! 2025년 AI 트렌드를 알아볼까요?\n\n첫 번째, 생성형 AI의 진화...",
  "video_url": "https://cdn.reelmaker.ai/videos/550e8400.mp4",
  "thumbnail_url": "https://cdn.reelmaker.ai/thumbnails/550e8400.jpg",
  "duration": 30,
  "file_size": 5242880,
  "settings": {
    "duration": 30,
    "voice": {
      "gender": "female",
      "tone": "bright"
    },
    "style": "modern"
  },
  "hashtags": [
    "#AI",
    "#트렌드",
    "#2025",
    "#인공지능",
    "#기술"
  ],
  "media_assets": [
    {
      "type": "image",
      "url": "https://images.unsplash.com/photo-xxx",
      "source": "unsplash",
      "order": 0
    },
    {
      "type": "audio",
      "url": "https://cdn.reelmaker.ai/audio/550e8400.mp3",
      "source": "elevenlabs",
      "order": 0
    }
  ],
  "created_at": "2025-11-22T10:00:00Z",
  "updated_at": "2025-11-22T10:03:24Z",
  "completed_at": "2025-11-22T10:03:24Z"
}
```

**Status Values**:
- `pending`: 대기 중
- `processing`: 처리 중
- `completed`: 완료
- `failed`: 실패

**Progress Values**: 0-100 (진행률 %)

**Error Responses**:
```json
// 프로젝트 없음
{
  "error": {
    "code": "NOT_FOUND",
    "message": "프로젝트를 찾을 수 없습니다.",
    "status": 404
  }
}

// 권한 없음 (다른 사용자의 프로젝트)
{
  "error": {
    "code": "FORBIDDEN",
    "message": "이 프로젝트에 접근할 권한이 없습니다.",
    "status": 403
  }
}
```

---

#### GET /projects
사용자의 모든 프로젝트 조회

**Description**: 현재 사용자의 프로젝트 목록을 페이지네이션하여 조회합니다.

**Authentication**: Required

**Request**:
```http
GET /v1/projects?page=1&limit=20&status=completed&sort=created_at:desc
Authorization: Bearer {access_token}
```

**Query Parameters**:

| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| `page` | integer | ❌ | 페이지 번호 (기본: 1) |
| `limit` | integer | ❌ | 페이지당 개수 (기본: 20, 최대: 100) |
| `status` | string | ❌ | 상태 필터 (pending, processing, completed, failed) |
| `sort` | string | ❌ | 정렬 (created_at:desc, created_at:asc, updated_at:desc) |
| `keyword` | string | ❌ | 키워드 검색 |

**Response** (200 OK):
```json
{
  "total": 45,
  "page": 1,
  "limit": 20,
  "total_pages": 3,
  "projects": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "keyword": "AI 트렌드",
      "status": "completed",
      "thumbnail_url": "https://cdn.reelmaker.ai/thumbnails/550e8400.jpg",
      "duration": 30,
      "created_at": "2025-11-22T10:00:00Z",
      "completed_at": "2025-11-22T10:03:24Z"
    },
    {
      "id": "660e8400-e29b-41d4-a716-446655440001",
      "keyword": "건강한 다이어트",
      "status": "processing",
      "progress": 65,
      "created_at": "2025-11-22T09:30:00Z"
    }
  ]
}
```

---

#### PATCH /projects/{project_id}
프로젝트 수정

**Description**: 완료된 프로젝트의 일부 내용을 수정하여 재생성합니다.

**Authentication**: Required

**Request**:
```http
PATCH /v1/projects/550e8400-e29b-41d4-a716-446655440000
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "script": "수정된 대본 내용...",
  "settings": {
    "subtitle": {
      "style": "colorful"
    }
  }
}
```

**Response** (202 Accepted):
```json
{
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "message": "프로젝트가 수정되어 재생성 중입니다."
}
```

---

#### DELETE /projects/{project_id}
프로젝트 삭제

**Description**: 프로젝트와 관련된 모든 파일을 삭제합니다.

**Authentication**: Required

**Request**:
```http
DELETE /v1/projects/550e8400-e29b-41d4-a716-446655440000
Authorization: Bearer {access_token}
```

**Response** (204 No Content)

---

### 5.2 미디어 검색

#### GET /media/search
이미지/영상 검색 (프리뷰용)

**Description**: Unsplash, Pexels 등에서 이미지/영상을 검색합니다. 프로젝트 생성 전 미리보기용입니다.

**Authentication**: Required

**Request**:
```http
GET /v1/media/search?query=AI+technology&type=image&source=all&limit=10
Authorization: Bearer {access_token}
```

**Query Parameters**:

| 파라미터 | 타입 | 필수 | 설명 |
|----------|------|------|------|
| `query` | string | ✅ | 검색 키워드 |
| `type` | string | ❌ | 미디어 타입 (image, video, all) (기본: image) |
| `source` | string | ❌ | 소스 (unsplash, pexels, all) (기본: all) |
| `limit` | integer | ❌ | 결과 개수 (기본: 10, 최대: 50) |

**Response** (200 OK):
```json
{
  "query": "AI technology",
  "total": 127,
  "results": [
    {
      "id": "abc123",
      "type": "image",
      "url": "https://images.unsplash.com/photo-xxx",
      "thumbnail_url": "https://images.unsplash.com/photo-xxx?w=400",
      "source": "unsplash",
      "width": 1920,
      "height": 1080,
      "author": {
        "name": "John Doe",
        "profile_url": "https://unsplash.com/@johndoe"
      },
      "license": "Free to use (Unsplash License)",
      "download_location": "https://api.unsplash.com/photos/xxx/download"
    }
  ]
}
```

---

### 5.3 사용자 관리

#### GET /users/me
현재 사용자 정보 조회

**Authentication**: Required

**Request**:
```http
GET /v1/users/me
Authorization: Bearer {access_token}
```

**Response** (200 OK):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "name": "홍길동",
  "subscription_plan": "pro",
  "subscription_status": "active",
  "api_quota": {
    "daily_limit": 200,
    "daily_used": 45,
    "daily_remaining": 155,
    "reset_at": "2025-11-23T00:00:00Z"
  },
  "storage": {
    "used_mb": 1024,
    "limit_mb": 10240
  },
  "created_at": "2025-01-01T00:00:00Z",
  "last_login": "2025-11-22T09:00:00Z"
}
```

---

#### PATCH /users/me
사용자 정보 수정

**Authentication**: Required

**Request**:
```http
PATCH /v1/users/me
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "name": "새 이름",
  "preferences": {
    "default_voice": "female_bright",
    "default_style": "modern",
    "default_duration": 30
  }
}
```

**Response** (200 OK):
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "email": "user@example.com",
  "name": "새 이름",
  "preferences": {
    "default_voice": "female_bright",
    "default_style": "modern",
    "default_duration": 30
  }
}
```

---

#### GET /users/me/usage
사용자 API 사용량 통계

**Authentication**: Required

**Request**:
```http
GET /v1/users/me/usage?period=7d
Authorization: Bearer {access_token}
```

**Query Parameters**:
- `period`: 기간 (7d, 30d, 90d) (기본: 30d)

**Response** (200 OK):
```json
{
  "period": "7d",
  "total_projects": 15,
  "completed_projects": 13,
  "failed_projects": 2,
  "total_duration_seconds": 450,
  "average_render_time_seconds": 180,
  "api_calls": {
    "openai": 15,
    "elevenlabs": 15,
    "unsplash": 45,
    "pexels": 30
  },
  "daily_breakdown": [
    {
      "date": "2025-11-22",
      "projects": 3,
      "api_calls": 12
    }
  ]
}
```

---

### 5.4 구독 관리

#### GET /subscriptions/plans
구독 플랜 목록

**Authentication**: Not Required

**Request**:
```http
GET /v1/subscriptions/plans
```

**Response** (200 OK):
```json
{
  "plans": [
    {
      "id": "free",
      "name": "Free",
      "price": 0,
      "currency": "USD",
      "interval": "month",
      "features": {
        "daily_videos": 10,
        "video_duration_max": 30,
        "storage_mb": 1024,
        "watermark": true,
        "priority_rendering": false
      }
    },
    {
      "id": "basic",
      "name": "Basic",
      "price": 9.99,
      "currency": "USD",
      "interval": "month",
      "features": {
        "daily_videos": 50,
        "video_duration_max": 60,
        "storage_mb": 5120,
        "watermark": false,
        "priority_rendering": false
      }
    },
    {
      "id": "pro",
      "name": "Pro",
      "price": 29.99,
      "currency": "USD",
      "interval": "month",
      "features": {
        "daily_videos": 200,
        "video_duration_max": 90,
        "storage_mb": 10240,
        "watermark": false,
        "priority_rendering": true,
        "api_access": true,
        "custom_branding": true
      }
    }
  ]
}
```

---

#### POST /subscriptions/checkout
구독 결제 세션 생성

**Authentication**: Required

**Request**:
```http
POST /v1/subscriptions/checkout
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "plan_id": "pro",
  "success_url": "https://reelmaker.ai/success",
  "cancel_url": "https://reelmaker.ai/cancel"
}
```

**Response** (200 OK):
```json
{
  "checkout_url": "https://checkout.stripe.com/c/pay/xxx",
  "session_id": "cs_xxx"
}
```

---

## 6. Webhook

### 6.1 Webhook 설정

사용자는 프로젝트 완료 시 알림을 받을 Webhook URL을 설정할 수 있습니다.

#### POST /webhooks
Webhook URL 등록

**Request**:
```http
POST /v1/webhooks
Authorization: Bearer {access_token}
Content-Type: application/json

{
  "url": "https://your-domain.com/webhook",
  "events": ["project.completed", "project.failed"],
  "secret": "your_webhook_secret"
}
```

**Response** (201 Created):
```json
{
  "id": "wh_123456",
  "url": "https://your-domain.com/webhook",
  "events": ["project.completed", "project.failed"],
  "active": true,
  "created_at": "2025-11-22T10:00:00Z"
}
```

### 6.2 Webhook 이벤트

#### project.completed
프로젝트 완료 시 전송

**Payload**:
```json
{
  "event": "project.completed",
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "video_url": "https://cdn.reelmaker.ai/videos/550e8400.mp4",
  "thumbnail_url": "https://cdn.reelmaker.ai/thumbnails/550e8400.jpg",
  "completed_at": "2025-11-22T10:03:24Z",
  "timestamp": "2025-11-22T10:03:25Z"
}
```

#### project.failed
프로젝트 실패 시 전송

**Payload**:
```json
{
  "event": "project.failed",
  "project_id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "error": {
    "code": "RENDERING_FAILED",
    "message": "영상 렌더링 중 오류가 발생했습니다."
  },
  "failed_at": "2025-11-22T10:02:15Z",
  "timestamp": "2025-11-22T10:02:16Z"
}
```

### 6.3 Webhook 서명 검증

보안을 위해 모든 webhook 요청은 서명됩니다.

**Header**:
```
X-Webhook-Signature: sha256=abc123...
```

**검증 방법** (Python):
```python
import hmac
import hashlib

def verify_webhook(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(
        secret.encode(),
        payload,
        hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(f"sha256={expected}", signature)
```

---

## 7. SDK 및 예제

### 7.1 Python SDK

```python
from reelmaker import ReelMaker

# 클라이언트 초기화
client = ReelMaker(api_key="your_api_key")

# 프로젝트 생성
project = client.projects.create(
    keyword="AI 트렌드 2025",
    settings={
        "duration": 30,
        "voice": {"gender": "female", "tone": "bright"},
        "style": "modern"
    }
)

print(f"프로젝트 ID: {project.id}")
print(f"상태: {project.status}")

# 상태 확인 (polling)
import time

while project.status != "completed":
    time.sleep(10)
    project = client.projects.get(project.id)
    print(f"진행률: {project.progress}%")

print(f"영상 URL: {project.video_url}")

# 다운로드
client.projects.download(project.id, "output.mp4")
```

### 7.2 JavaScript SDK

```javascript
import { ReelMaker } from '@reelmaker/sdk';

// 클라이언트 초기화
const client = new ReelMaker({ apiKey: 'your_api_key' });

// 프로젝트 생성
const project = await client.projects.create({
  keyword: 'AI 트렌드 2025',
  settings: {
    duration: 30,
    voice: { gender: 'female', tone: 'bright' },
    style: 'modern'
  }
});

console.log('프로젝트 ID:', project.id);

// Webhook으로 완료 알림 받기
client.webhooks.create({
  url: 'https://your-domain.com/webhook',
  events: ['project.completed']
});

// 또는 polling
const completed = await client.projects.waitForCompletion(project.id);
console.log('영상 URL:', completed.videoUrl);
```

### 7.3 cURL 예제

```bash
# 회원가입
curl -X POST https://api.reelmaker.ai/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securePassword123!",
    "name": "홍길동"
  }'

# 프로젝트 생성
curl -X POST https://api.reelmaker.ai/v1/projects \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "keyword": "AI 트렌드 2025",
    "settings": {
      "duration": 30,
      "voice": {"gender": "female", "tone": "bright"}
    }
  }'

# 프로젝트 상태 확인
curl -X GET https://api.reelmaker.ai/v1/projects/PROJECT_ID \
  -H "Authorization: Bearer YOUR_TOKEN"

# 영상 다운로드
curl -O -J -L "VIDEO_URL_FROM_RESPONSE"
```

---

## 부록

### A. 변경 이력

| 버전 | 날짜 | 변경 내용 |
|------|------|----------|
| 1.0 | 2025-11-22 | 초안 작성 |

### B. 지원 및 문의

- **이메일**: support@reelmaker.ai
- **문서**: https://docs.reelmaker.ai
- **Discord**: https://discord.gg/reelmaker
- **GitHub**: https://github.com/reelmaker/sdk

---

**문서 작성자**: API Team  
**최종 수정일**: 2025-11-22

