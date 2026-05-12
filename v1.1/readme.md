# Clip Saver

작은 개인용 AI 로그 저장 유틸.

클립보드 내용을 단축키로 빠르게 Markdown 파일로 저장한다.
Obsidian, 기본 검색, Smart Connections, AI 정리 하네스에 넘기기 좋은 형태를 목표로 한다.

---

# 주요 기능

- 시스템 트레이 상주
- 단축키로 클립보드 저장
- 저장 전 미리보기 확인
- 중복 저장 방지
- Markdown 자동 저장
- 설정값을 `config.json`으로 분리
- 저장 문서 형식을 `note_template.md`로 분리
- AI 정리용 지시문 `ai_harness_prompt.md` 포함

---

# 파일 구성

```txt
clipSaver.py           실행 소스
clipSaver.bat          백그라운드 실행용 bat
setup.bat              설치용 bat
requirements.txt       Python 라이브러리 목록
config.json            저장 경로/단축키/기본 태그 설정
note_template.md       저장될 md 문서 템플릿
ai_harness_prompt.md   AI에게 정리 요청할 때 쓰는 지시문
```

---

# 설치 방법

## 1. Python 설치

Python 3.10 이상 권장.

설치 시 아래 옵션 체크 추천.

```txt
Add Python to PATH
```

## 2. setup.bat 실행

```txt
setup.bat
```

자동으로:

- venv 생성
- 라이브러리 설치
- 실행 환경 구성

진행.

---

# 실행 방법

```txt
clipSaver.bat
```

성공하면 시스템 트레이에 Clip Saver 아이콘이 생긴다.

---

# 기본 단축키

```txt
CTRL + ALT + A
```

변경은 `config.json`의 `hotkey` 수정.

---

# config.json

```json
{
  "save_path": "E:/memo/memo/clip",
  "hotkey": "ctrl+alt+a",
  "preview_length": 300,
  "filename_format": "%Y-%m-%d_%H%M%S.md",
  "default_type": "ai-log",
  "default_tags": [
    "ai-log"
  ],
  "default_title": "Clipboard Note",
  "source": "clipboard"
}
```

## 주요 설정

| 항목 | 설명 |
|---|---|
| `save_path` | md 파일 저장 폴더 |
| `hotkey` | 저장 단축키 |
| `preview_length` | 저장 확인창에 보여줄 글자 수 |
| `filename_format` | 저장 파일명 형식 |
| `default_type` | 기본 문서 타입 |
| `default_tags` | 기본 태그 목록 |
| `source` | 저장 출처 |

---

# note_template.md

저장될 Markdown 형식을 관리하는 파일.

```md
---
created: {{created}}
type: {{type}}
source: {{source}}
tags:
{{tags}}
---

# {{title}}

## Summary
{{summary}}

## Content
{{content}}
```

## 사용 가능한 치환값

| 값 | 설명 |
|---|---|
| `{{created}}` | 저장 시간 |
| `{{type}}` | 문서 타입 |
| `{{source}}` | 출처 |
| `{{tags}}` | 태그 목록 |
| `{{title}}` | 클립보드 첫 줄 기반 제목 |
| `{{summary}}` | 현재는 빈 값. AI 정리 단계에서 사용 가능 |
| `{{content}}` | 클립보드 원문 |

---

# AI 정리 하네스 사용 아이디어

`ai_harness_prompt.md`와 `note_template.md`를 AI에게 같이 주고:

```txt
이 형식으로 정리해서 md 파일로 만들어줘.
```

라고 요청하면 `title`, `summary`, `type`, `tags`를 AI가 자동으로 채운 문서를 만들 수 있다.

현재 Clip Saver 자체는 API 호출을 하지 않는다.
즉, 저장은 빠르게 하고 정리는 필요할 때 AI에게 맡기는 구조다.

---

# 사용 흐름

```txt
1. 저장하고 싶은 텍스트 복사
2. CTRL + ALT + A
3. 미리보기 확인
4. md 저장
5. 필요하면 AI에게 note_template.md 형식으로 재정리 요청
```

---

# 변경 기록

## v1.1 후보

- `SAVE_PATH`, `HOTKEY` 등 설정값을 `config.json`으로 분리
- 저장 Markdown 형식을 `note_template.md`로 분리
- AI 정리 요청용 `ai_harness_prompt.md` 추가
- 트레이 메뉴에 `설정 폴더 열기` 추가
