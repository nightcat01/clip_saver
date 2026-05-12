맞아 ㅋㅋ
지금 상태는 README라기보다 거의 “사용 설명서 + 컨셉 문서”에 가까워졌어.

실제로 GitHub README는 보통:

* 이게 뭐인지
* 어떻게 설치하는지
* 어떻게 실행하는지
* 핵심 기능 몇 개
* 설정 최소 설명

정도만 있으면 충분한 경우가 많아.

특히 네 프로젝트는:

> “개인 workflow 유틸”

느낌이라 README가 길어질수록 오히려 부담스러워질 수 있어.

지금 기준이면 아래 정도 길이가 제일 예쁠 것 같아:

---

# Clip Saver

로컬 Markdown 기반 클립 저장 도구.

클립보드 내용을 빠르게 `.md` 파일로 저장하고,
AI(ChatGPT / Claude / Gemini 등)와 함께 사용하는 workflow를 지원한다.

---

# 주요 기능

* 글로벌 단축키 저장
* 시스템 트레이 상주 실행
* Markdown(.md) 저장
* AI Metadata 자동 감지
* 중복 저장 방지
* Obsidian 친화적 구조

---

# 설치

Python 3.10 이상 권장.

라이브러리 설치:

```bash
pip install -r requirements.txt
```

또는:

```txt
setup.bat 실행
```

---

# 실행

```txt
run.bat 실행
```

또는:

```bash
python clipSaver.py
```

---

# 기본 단축키

```txt
Ctrl + Alt + A
```

---

# config.json

```json
{
  "save_dir": "E:/memo/memo/clip",
  "hotkey": "ctrl+alt+a",
  "preview_length": 300,
  "default_type": "ai-log",
  "default_tags": ["ai-log"]
}
```

---

# AI Workflow 예시

```txt
#log

(내용)
```

↓

AI가:

* title 생성
* summary 생성
* tags 생성
* type 생성

↓

Markdown 저장.

---

# 사용 라이브러리

* pyperclip
* keyboard
* pystray
* pillow
