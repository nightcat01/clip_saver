# AI Harness Prompt

사용자가 특정 command keyword를 입력하면
다음 규칙으로 Markdown 문서를 생성한다.

---

# Commands

## #log

개발 로그 / AI 메모 정리용 command.

규칙:

- Markdown 형식 사용
- YAML frontmatter 포함
- title 생성
- summary 생성
- tags 생성
- tags는 kebab-case 사용
- type 자동 분류

추가 규칙:

- 반드시 하나의 완성된 Markdown 문서만 출력
- 코드블럭 사용 금지
- 설명 문장 출력 금지
- 바로 .md 저장 가능한 형태 유지
- Obsidian 호환 Markdown 기준 사용

---

# Tags Rules

- 영어 소문자 사용
- kebab-case 사용
- 최대 5개
- 핵심 주제 중심 생성

---

# Type Examples

- architecture
- ai-log
- troubleshooting
- prompt
- reference
- feature
