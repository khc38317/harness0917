# 핸즈오버 (Handover) — Wiki Harness 최종 정리

**작성일**: 2026-09-17  
**최종 갱신**: 2026-09-17  
**상태**: ✅ 운영 준비 완료

---

## 📌 프로젝트 개요

**Wiki Harness**는 회의록 기반 SSOT(Single Source of Truth)를 구축하는 LLM-Human 협업 시스템입니다.

**목표**: 회의에서 나온 의사결정과 액션을 자동으로 추적하고, 기계 검증 + LLM 검증으로 완벽한 wiki 관리

---

## 🔑 핵심 원칙 5가지

### 1. wiki/meetings = SSOT (불변의 원천)
- 원본 회의록: 사람만 작성
- 메타 파일: LJM 생성 (decisions.md, actions.md 등)
- **원본은 절대 수정 불가**

### 2. wiki/meetings/ = LJM 소유, 사람 검토
- LJM이 회의록 분석 → 메타 파일 생성
- 사람이 검토 후 승인
- 품질은 사람이 보증

### 3. 규칙은 사람만 변경
- CLAUDE.md: 규칙 정의 (사람만 수정)
- SCHEMA.md: 포맷 정의 (사람만 수정)
- LJM은 제안만 가능

### 4. 출처 추적은 필수
- 모든 항목에 `[[YYYY-MM-DD]]` 링크 필수
- wiki가 틀렸을 때 원문 확인 가능

### 5. ID는 증가만 (중복 금지)
- D: D-0001, D-0002, ... (뒤로 갈 수 없음)
- A: A-0001, A-0002, ... (뒤로 갈 수 없음)
- index.md의 마지막 번호를 항상 읽고 +1부터 시작

---

## 📂 프로젝트 구조

```
wiki_harness/
├─ CLAUDE.md              # 핵심 규칙 및 원칙
├─ SCHEMA.md              # 데이터 포맷 정의
│
├─ scripts/
│  └─ validate.py         # 기계 검증 스크립트
│
├─ wiki/
│  ├─ decisions/          # D-XXXX 결정 파일들
│  └─ meetings/           # 회의록, 메타 파일
│     ├─ YYYY-MM-DD-*.md  # 원본 회의록
│     ├─ decisions.md     # 결정 목록
│     ├─ actions.md       # 액션 추적
│     ├─ glossary.md      # 용어 정의
│     ├─ index.md         # 전체 카탈로그
│     ├─ log.md           # 운영 기록
│     └─ open-items.md    # 미결 사항
│
└─ .claude/
   ├─ commands/
   │  ├─ ingest.md        # /ingest 프롬프트
   │  ├─ lint.md          # /lint 프롬프트
   │  └─ brief.md         # /brief 프롬프트
   │
   └─ skills/
      ├─ review/
      │  └─ skill.md      # /review (LJM 검증)
      │
      └─ skill_review/
         └─ skill.md      # /skill_review (통합 검증)
```

---

## 🛠️ 도구 & 스킬

### 1️⃣ ingest (자동 메타 파일 생성)
**사용**: `/ingest wiki/meetings/YYYY-MM-DD-제목.md`

역할:
- 회의록 분석 → 결정/액션/용어 추출
- decisions.md, actions.md, glossary.md 자동 갱신
- index.md 상태 업데이트
- log.md에 기록 추가

### 2️⃣ lint (wiki 건강도 검사)
**사용**: `/lint`

검사:
- 출처 링크 누락
- 기한 임박 액션 (3일 이내)
- 기한 초과 액션
- 30일 이상 비활동 액션

### 3️⃣ brief (회의 전 브리핑)
**사용**: `/brief`

생성:
- 오늘 기한 액션
- 진행 중인 액션
- 최근 번복된 결정
- 미해결 질문

### 4️⃣ validate.py (기계 검증)
**사용**: `python scripts/validate.py`

검증:
- Frontmatter (필수 필드)
- 스키마 구조 (필수 섹션)
- 파일명 규칙
- 출처 링크 형식
- ID 형식 (D-XXXX, A-XXXX)

### 5️⃣ review (컨텐츠 검증)
**사용**: `/review wiki/meetings/YYYY-MM-DD-제목.md`

검증:
- 회의록과 decisions 일치도
- 회의록과 actions 일치도
- 회의록과 glossary 일치도
- 누락 감지
- 상태 추적 (조용한 사라짐 감지)

### 6️⃣ skill_review (통합 검증) ⭐ 권장
**사용**: `/skill_review wiki/meetings/YYYY-MM-DD-제목.md`

수행:
- Stage 1: python scripts/validate.py (기계 검증)
- Stage 2: /review 스킬 (컨텐츠 검증)
- Stage 3: 통합 리포트 생성

---

## 🚀 운영 워크플로우

```
1️⃣ 회의 진행
   ↓
2️⃣ 회의록 저장 (wiki/meetings/YYYY-MM-DD-제목.md)
   ↓
3️⃣ /ingest 실행
   ├─ decisions.md, actions.md 자동 생성
   ├─ glossary.md 신규 용어 추가
   └─ index.md 상태 업데이트
   ↓
4️⃣ /skill_review 실행
   ├─ Stage 1: 기계 검증 (형식/포맷)
   ├─ Stage 2: LJM 검증 (내용/의미)
   └─ Stage 3: 통합 리포트
   ↓
5️⃣ 결과 검토
   ├─ 오류 수정 (있으면)
   └─ 경고 확인 (권장)
   ↓
6️⃣ 최종 commit
   └─ git commit 수행
   ↓
7️⃣ 다음 회의 전
   └─ /brief 실행 → 아젠다 준비
```

---

## 📋 문서별 역할

| 문서 | 목적 | 수정 권한 | 변경 빈도 |
|---|---|---|---|
| **CLAUDE.md** | 핵심 규칙 | 사람만 | 거의 안 함 |
| **SCHEMA.md** | 포맷 정의 | 사람만 | 거의 안 함 |
| **wiki/meetings/*.md** | 원본 회의록 | 사람만 (읽기만) | 회의마다 1회 |
| **decisions.md** | 결정 목록 | LJM + 사람 검토 | 회의마다 갱신 |
| **actions.md** | 액션 추적 | LJM + 사람 검토 | 회의마다 갱신 |
| **glossary.md** | 용어 정의 | LJM + 사람 검토 | 필요시 갱신 |
| **index.md** | 전체 카탈로그 | LJM이 자동 갱신 | 회의마다 갱신 |
| **log.md** | 운영 기록 | LJM이 append | 회의마다 기록 |

---

## ⚙️ LJM(Claude)의 행동 규칙

### ✅ 할 수 있는 것
- wiki/meetings/ 메타 파일 생성/갱신 (SCHEMA.md 틀 안에서)
- 규칙 실행 (CLAUDE.md/SCHEMA.md 정의대로)
- 명확한 오류 보고
- 개선 제안 (사람이 승인 필수)

### ❌ 절대 안 되는 것
- CLAUDE.md 규칙 우회
- SCHEMA.md 포맷 해석
- 검사 규칙 수정
- wiki/meetings/YYYY-MM-DD-*.md 수정/삭제 (원본 회의록)
- 불명확한 상황에서 임의 판단

### 🤔 모호한 상황 처리
1. 즉시 중단 (진행하지 말기)
2. 상황 설명 (뭐가 불명확한지)
3. 옵션 제시 (2~3개 방안 제안)
4. 사용자 선택 대기
5. 확인 후 실행 (승인받은 방식대로만)

---

## 📊 성공 지표

### 기계 검증
- ❌ 오류: 0개
- ⚠️ 경고: 최소화

### LJM 검증
- ✅ Decisions: 100% 커버
- ✅ Actions: 100% 커버
- ✅ Glossary: 100% 커버
- ✅ 출처 링크: 100% 완성
- ✅ 상태 추적: 완벽

### 종합 정확도
- 목표: 99% 이상

---

## 🔧 문제 해결

### Q: validate.py에서 오류가 난다
A: 다음을 확인하세요:
1. Frontmatter가 ---로 시작/종료하는가?
2. 필수 섹션이 모두 있는가?
3. 파일명이 규칙을 따르는가? (D-XXXX, YYYY-MM-DD)

### Q: /ingest 후 내용이 빠졌다
A: /skill_review로 검증하면 LJM이 누락을 감지합니다.
또는 /review로 상세 검증을 수행하세요.

### Q: 액션이 "조용히 사라졌다"고 나온다
A: /review의 "조용한 사라짐" 경고는:
- 마지막 업데이트가 90일 이상 전
- 상태가 여전히 "진행중" 또는 "대기중"
→ 상태를 "완료"/"취소됨"으로 변경하거나 최근 업데이트를 기록

### Q: 새로운 규칙을 추가하고 싶다
A: CLAUDE.md에 제안을 추가하세요.
사람이 검토 후 승인하면 추가됩니다.
(규칙 변경은 사람만 가능)

---

## 📚 관련 문서

- **CLAUDE.md**: 핵심 규칙
- **SCHEMA.md**: 포맷 정의
- **ONBOARDING.md**: 새 팀원 교육용
- **README.md**: 프로젝트 소개
- **handover/**: 핸즈오버 단계별 문서

---

## 🎓 다음 단계

### Phase 1: 기본 구조 (✅ 완료)
- ✅ 디렉토리 구성
- ✅ 핵심 문서 작성
- ✅ 검증 도구 완성
- ✅ 스킬 구현
- ✅ 테스트 완료

### Phase 2: 운영 확대 (진행 중)
- [ ] 실제 회의록 적재
- [ ] /ingest 워크플로우 정상화
- [ ] /skill_review 정기 실행
- [ ] 팀원 교육

### Phase 3: 최적화 (향후)
- [ ] /lint 정기 실행 자동화
- [ ] /brief 정기 생성
- [ ] 월별 아카이브 규칙

---

**작성자**: Claude Haiku 4.5  
**마지막 업데이트**: 2026-09-17  
**상태**: ✅ 운영 준비 완료
