# 운영 기록 (Log)

**append-only 기록**: 이 파일은 절대 뒤로 가지 않습니다.

각 항목은 다음 형식으로 기록됩니다:
```
## [YYYY-MM-DD] {커맨드} | {설명}
```

이 기록을 `grep "^## \[" log.md | tail -10` 같은 Unix 도구로 쿼리할 수 있습니다.

---

## [2026-09-17] init | 프로젝트 초기화

- 디렉토리 구조 생성
- CLAUDE.md, SCHEMA.md, index.md, log.md 작성
- .claude/commands/ 커맨드 프롬프트 작성

---

## [TBD] ingest | {회의명}

- D-XXXX 생성: {제목}
- A-XXXX 생성: {제목}
- 용어 N개 추가

---

[이곳에 운영 기록이 추가됩니다]
