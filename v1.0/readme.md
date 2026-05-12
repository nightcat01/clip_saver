# Clip Saver

작은 개인용 AI 로그 저장 유틸.

---

# 목적

Clip Saver는:

- 생산성 앱
- 지식 관리 시스템
- 정리 도구

보다는,

```txt
생각 흔적 보관 도구
```

에 가까움.

목표는:

- 까먹어도 된다
- 잊어버려도 괜찮다
- 나중에 다시 찾을 수만 있으면 된다

임.

---

# 주요 기능

- 시스템 트레이 상주
- 단축키 저장
- Obsidian md 자동 저장
- 저장 전 미리보기 확인
- 백그라운드 실행
- 중복 저장 방지

---

# 단축키

```txt
CTRL + ALT + A
```

---

# 저장 위치

기본 저장 위치:

```txt
E:/memo/memo/Inbox
```

필요하면 `aiLogSaver.py` 내부의 `SAVE_PATH` 수정.

---

# 설치 방법

## 1. Python 설치

Python 3.10 이상 권장.

다운로드:
https://www.python.org/downloads/

설치 시:

```txt
Add Python to PATH
```

체크 추천.

---

## 2. setup.bat 실행

```txt
setup.bat
```

실행하면 자동으로:

- venv 생성
- 라이브러리 설치
- 실행 환경 구성

진행됨.

---

# 실행 방법

```txt
run.bat
```

실행.

성공하면:

- 시스템 트레이에 Clip Saver 아이콘 생성
- 백그라운드 대기 상태 진입

---

# 사용 방법

## 저장 흐름

```txt
1. AI 답변 복사 (CTRL+C)
2. CTRL + ALT + A
3. 저장 여부 확인
4. md 저장 완료
```

---

# 저장 형식

파일명:

```txt
2026-05-07_235959.md
```

내용:

````md
---
created: 2026-05-07 23:59:59
type: ai-log
---

복사한 내용