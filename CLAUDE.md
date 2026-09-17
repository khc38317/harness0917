# CLAUDE.md — LLM Wiki 하네스 가이드

**목적**: 회의록 기반 SSOT (Single Source of Truth) 구축  
**주요 기능**: 의사결정 추적 + 액션아이템 관리  
**편집 도구**: Obsidian  
**원본 형식**: Notion .md 내보내기

---

## 🔐 경로별 소유권

| 경로 | LLM | 사람 | 역할 |
|---|---|---|---|
| **wiki/meetings/** | 읽기만 (회의록) | 원본 작성 + 메타 편집 | SSOT 기반 (절대 불변) |
| **wiki/meetings/*.md** | 생성/갱신 | 검토 | LLM 소유, 사람 품질 보증 |
| **CLAUDE.md** | 제안 | 승인/수정 | LLM이 규칙을 우회할 수 없게 |
| **SCHEMA.md** | 제안 | 승인/수정 | 스키마 변경은 사람만 |
| **scripts/** | 실행 | 변경 승인 | 검사 규칙은 사람이 관리 |

---

## 📂 프로젝트 구조

```
wiki_harness/
├─ CLAUDE.md              # 이 파일
├─ SCHEMA.md              # 포맷 정의 (LLM이 따라야 할 규칙)
│
├─ raw/                   # (비어있음, 향후 다른 원본용)
│
├─ wiki/
│  └─ meetings/           # 모든 것이 여기
│     ├─ YYYY-MM-DD-제목.md     # 원본 회의록 (절대 수정 금지)
│     ├─ decisions.md           # 결정 목록
│     ├─ index.md               # 위키 전체 카탈로그
│     ├─ log.md                 # append-only 운영 기록
│     ├─ actions.md             # 액션아이템 (상태 머신)
│     ├─ open-items.md          # 미결 사항
│     └─ glossary.md            # 용어/시스템명 참고
│
└─ .claude/
   ├─ commands/           # 간단한 커맨드 프롬프트
   │  ├─ ingest.md        # /ingest 프롬프트
   │  ├─ lint.md          # /lint 프롬프트
   │  └─ brief.md         # /brief 프롬프트
   │
   └─ skills/             # 복잡한 절차 스킬 (frontmatter + 상세 가이드)
      └─ review/
         └─ skill.md      # /review 스킬
```

---

## 🔑 핵심 원칙 5가지

### 1. wiki/meetings = SSOT (불변의 원천)

- **원본 회의록**: 사람만 작성 (Notion .md 내보내기)
- **메타 파일**: LJM이 생성 (decisions.md, actions.md 등)
- **읽기 권한**: LJM은 읽기만 가능
- **변경**: Git으로 모든 변경 추적

→ 원본이 바뀌면 SSOT가 무너지므로 절대 수정 불가

### 2. wiki/meetings/ = LJM이 소유, 사람이 검토

- **생성**: LJM이 회의록 분석해서 decisions.md, actions.md 갱신
- **검토**: 사람이 파싱 오류/분류 오류 인라인 수정
- **승인**: 최종 OK 후 commit

→ LJM이 빠르게 만들고, 사람이 품질 보증

### 3. 규칙은 사람만 변경 (LJM은 제안만)

- **CLAUDE.md**: 커맨드 정의 (사람만 수정)
- **SCHEMA.md**: 포맷 정의 (사람만 수정)
- **scripts/**: 검사 규칙 (사람만 수정)

→ LJM이 "효율성 때문에" 규칙을 우회하면 신뢰도 하락

### 4. 출처 추적은 필수

모든 진술이 어느 회의에서 나왔는지 `[[YYYY-MM-DD]]` 링크로 기록

→ wiki가 틀렸을 때 원문을 바로 확인 가능

### 5. ID는 증가만 (중복 금지)

- D: D-0001, D-0002, ... (절대 뒤로 갈 수 없음)
- A: A-0001, A-0002, ... (절대 뒤로 갈 수 없음)

→ index.md의 "현재 상태"를 항상 읽고 +1부터 시작

---

## 🛠️ 커맨드 vs 스킬

Wiki Harness는 **커맨드**와 **스킬**을 역할에 따라 구분합니다.

### Commands (.claude/commands/)

**특징**: 간단한 프롬프트 (plain markdown)

**포함**:
- `/ingest`: 회의록 분석 및 메타 파일 생성
- `/lint`: wiki 건강도 검사
- `/brief`: 회의 전 브리핑 생성

**사용 시기**: 단순한 입력 → 출력 프로세스

**형식**: 일반 `.md` 파일 (frontmatter 없음)

### Skills (.claude/skills/)

**특징**: 복잡한 절차를 체계화한 가이드 (frontmatter + 상세 문서)

**포함**:
- `/review`: 컨텐츠 검증 (회의록 vs wiki 비교)

**사용 시기**: 여러 단계, 선택지, 체크리스트가 필요한 프로세스

**형식**: frontmatter가 있는 `skill.md` 파일

```yaml
---
name: review
description: "Wiki 컨텐츠 검증..."
---

# 실제 내용
```

### 구분 기준

| 구분 | Commands | Skills |
|---|---|---|
| 복잡도 | 낮음 (단순) | 높음 (다단계) |
| 형식 | plain .md | skill.md + frontmatter |
| 선택지 | 거의 없음 | 여러 선택지/옵션 |
| 체크리스트 | 짧음 | 상세함 |
| 사용 빈도 | 자주 | 필요시 |

---

## 📋 문서별 책임 분담

Wiki Harness는 **규칙**, **구조**, **절차**를 명확히 분리하여 관리합니다.

### CLAUDE.md — 전반적인 규칙 & 원칙

**책임**: LLM의 행동 기준을 정의하고, 하네스 전체의 운영 원칙 수립

**포함 내용**:
- 🔐 경로별 소유권 (LLM/사람의 역할)
- 🔑 핵심 원칙 (SSOT, 출처 추적, ID 증가 규칙 등)
- ⚙️ LLM의 행동 규칙 (할 수 있는 것 / 안 되는 것)
- 🤔 모호한 상황 처리 프로토콜
- 📊 일정 연장 추적 규칙 (이슈 관리 기준)

**예시**:
- "원본 회의록은 절대 수정 금지" ← CLAUDE.md
- "ID는 증가만, 감소 불가" ← CLAUDE.md
- "불명확한 상황에서는 즉시 중단" ← CLAUDE.md

### SCHEMA.md — 구조적인 규칙 & 포맷 정의

**책임**: wiki의 데이터 구조와 각 문서의 형식을 정의

**포함 내용**:
- 1️⃣ D (결정) 파일의 필수/선택 필드
- 2️⃣ A (액션) 파일의 상태 머신 정의
- 3️⃣ 용어(glossary)의 테이블 구조
- 4️⃣ 출처 링크([[YYYY-MM-DD]]) 규칙
- 5️⃣ ID 부여 규칙 (형식, 범위, 중복 금지)
- 6️⃣ 파일 명명 규칙
- 7️⃣ Git 커밋 메시지 규칙
- 8️⃣ 마이그레이션/아카이브 규칙

**예시**:
- "D 파일은 반드시 '## 결정 내용' 섹션을 가져야 함" ← SCHEMA.md
- "모든 bullet point는 [[YYYY-MM-DD]] 필수" ← SCHEMA.md
- "A 파일의 상태는 [진행중|대기중|보류|완료|취소됨]" ← SCHEMA.md

### 스킬 (.claude/skills/ingest/*.md) — 반복적인 절차

**책임**: 자동화할 수 있는 반복적인 작업의 단계별 프로세스 정의

**포함 내용**:
- 입력 방식 (사용자가 제공할 정보)
- 단계별 프로세스 (1단계: State 확인 → 2단계: 분석 → ... → 6단계: Commit)
- 각 단계별 체크리스트
- 핵심 규칙 (CLAUDE.md, SCHEMA.md 준수)
- 모호한 상황 처리 방법

**예시**:
- "Stage 1: index.md에서 마지막 D, A 번호 읽기" ← 스킬
- "Stage 3: 추출 결과를 사용자에게 제시 후 확인받기" ← 스킬
- "모든 진술에 [[YYYY-MM-DD]] 출처 링크 추가" ← SCHEMA.md를 스킬이 실행

### 세 가지의 관계

```
CLAUDE.md (원칙)
    ↓
    "LLM이 규칙을 우회할 수 없다"
    "불명확할 땐 즉시 중단"
    ↓
SCHEMA.md (구조)
    ↓
    "D 파일은 반드시 이 포맷을 따라야 함"
    "출처 링크는 모든 항목에 필수"
    ↓
스킬 (절차)
    ↓
    "/ingest 실행 시 6단계를 따르고,
     SCHEMA.md를 준수하며,
     CLAUDE.md의 행동 규칙을 적용"
```

### 변경 권한

| 문서 | LJM | 사람 | 기준 |
|---|---|---|---|
| **CLAUDE.md** | 제안만 | 승인/수정 | 원칙 변경은 신중하게 |
| **SCHEMA.md** | 제안만 | 승인/수정 | 포맷 변경은 명시적으로 |
| **스킬** | 실행/개선 | 검증 | 절차는 LJM이 최적화 가능 |

---

## 🎯 도구 & 커맨드

### 📍 Stage 1: `/ingest` 스킬
회의록 → decisions.md, actions.md, glossary.md 자동 생성  
**상세 프로토콜**: 아래 "표준 회의록 처리 파이프라인" Stage 1 참고

### 📍 Stage 2: `python scripts/lint_structure.py`
메타 파일 기계검증 (포맷, 필드, ID, 출처 링크)  
**상세 검증**: 아래 "표준 회의록 처리 파이프라인" Stage 2 참고

### 📍 Stage 3: `/skill_review` 스킬
내용 검증 (회의록 ↔ wiki 일치도, 누락, 오분류)  
**상세 검증**: 아래 "표준 회의록 처리 파이프라인" Stage 3 참고

---

### 📍 보조 커맨드

**`/lint`** — 위키 전체 건강도 검사
- 출처 링크 누락, 기한 임박/초과 액션, 장기 비활동 액션 감지
- 정기적으로 실행 (선택사항)

**`/brief`** — 다음 회의 전 브리핑
- 즉시 확인 사항, 진행 중인 액션, 번복 결정, 미결 사항 제시
- 회의 전날 또는 당일 아침 실행

---

## 🔄 워크플로우

```
1️⃣ 회의 진행
   ↓
2️⃣ 회의록 저장 (wiki/meetings/YYYY-MM-DD-제목.md)
   ↓
3️⃣ 3단계 파이프라인 실행 (⬇️ 아래 상세 참고)
   ├─ Stage 1: /ingest (메타 파일 생성)
   ├─ Stage 2: lint_structure.py (기계검증)
   ├─ Stage 3: /skill_review (컨텐츠 검증)
   └─ 최종 commit
   ↓
4️⃣ 다음 회의 전
   └─ /brief 실행 → 아젠다 준비
   ↓
5️⃣ (선택) 주기적
   └─ /lint 실행 → 건강도 체크
```

→ **상세한 3단계 파이프라인**: 아래 "표준 회의록 처리 파이프라인" 섹션 참고

---

## 🚀 표준 회의록 처리 파이프라인 (3단계)

회의록 기반 wiki를 생성 → 기계검증 → 컨텐츠 검증하는 **표준 워크플로우**입니다.

### 📍 언제 사용하는가?

- 새로운 회의록을 `wiki/meetings/YYYY-MM-DD-제목.md`에 저장했을 때
- 회의록을 수정하고 메타 파일을 갱신해야 할 때

### 🎯 순서 (필수!)

**Stage 1 → Stage 2 → Stage 3 순서대로 실행**

---

### Stage 1️⃣ — `/ingest` 스킬 (위키 생성)

**목적**: 회의록을 분석하여 decisions.md, actions.md, glossary.md 등 자동 생성/갱신

**사용**:
```bash
/ingest wiki/meetings/YYYY-MM-DD-제목.md
```

**수행 내용**:
- 회의록 전문 분석
- 결정(D-XXXX) 추출
- 액션(A-XXXX) 추출
- 신규 용어 추가
- index.md, log.md 갱신
- **출처 링크([[YYYY-MM-DD]]) 자동 추가**

**결과**:
- ✅ wiki/meetings/decisions.md (갱신 또는 생성)
- ✅ wiki/meetings/actions.md (갱신 또는 생성)
- ✅ wiki/meetings/glossary.md (신규 용어만 추가)
- ✅ wiki/meetings/index.md (ID 카운터 업데이트)
- ✅ wiki/meetings/log.md (기록 추가)

**주의사항**:
- Stage 2, 3을 거쳐야 최종 확정 (이 단계는 임시 생성만)
- index.md의 현재 D/A 번호를 먼저 읽고 +1부터 시작
- 모든 항목에 출처 링크 필수

---

### Stage 2️⃣ — `python scripts/lint_structure.py` (기계검증)

**목적**: 생성된 메타 파일의 포맷/구조 검증

**사용**:
```bash
python scripts/lint_structure.py wiki/meetings/YYYY-MM-DD-제목.md
```

**검증 항목**:
- ✅ Frontmatter 필수 필드 (title, date, state 등)
- ✅ 필수 섹션 존재 (## 결정 내용, ## 액션 등)
- ✅ 파일명 규칙 (D-XXXX.md, YYYY-MM-DD 형식)
- ✅ ID 형식 (D-0001, A-0001 등)
- ✅ 출처 링크 형식 ([[YYYY-MM-DD]] 정확성)
- ✅ 필드 값 타입 (date, state 등)

**결과**:
- 오류(❌): 반드시 수정 후 Stage 3으로 진행
- 경고(⚠️): 권장하지만 무시 가능 (하지만 권장 안 함)

**주의사항**:
- Frontmatter가 `---`로 시작/종료하는지 확인
- 모든 필수 섹션이 ## 로 시작하는지 확인
- ID 중복 체크 (index.md와 비교)

---

### Stage 3️⃣ — `/skill_review` 스킬 (컨텐츠 검증)

**목적**: 회의록과 메타 파일의 **내용 일치도** 검증 (LJM 검증)

**사용**:
```bash
/skill_review wiki/meetings/YYYY-MM-DD-제목.md
```

**검증 항목**:
- ✅ decisions.md ↔ 회의록 일치도
- ✅ actions.md ↔ 회의록 일치도
- ✅ glossary.md ↔ 회의록 일치도
- ✅ 출처 링크 정확성 ([[YYYY-MM-DD]] 링크 유효성)
- ✅ 누락 감지 (회의에서 나왔지만 wiki에 없는 항목)
- ✅ 잘못된 분류 감지 (결정인데 액션으로 분류됨 등)
- ✅ 상태 추적 (조용한 사라짐 감지)

**결과**:
- 🟢 정상: 모든 검증 통과
- 🔴 오류: 수정 후 재실행
- 🟡 경고: 검토 후 적절히 처리

**주의사항**:
- Stage 2 (기계검증)를 먼저 완료해야 함
- 누락이나 불일치가 발견되면 decisions.md, actions.md 수정
- 출처 링크 오류 발견 시 즉시 수정

---

### ✅ 최종 Commit

**모든 Stage 통과 후** git commit:

```bash
git add wiki/meetings/
git commit -m "ingest: YYYY-MM-DD 회의명 (SK1, SK3 검증 완료)"
```

**Commit 메시지 규칙**:
- 형식: `ingest: YYYY-MM-DD 회의명`
- 선택: `(SK1, SK3 검증 완료)` 추가 가능
- SK1 = Stage 1 (/ingest)
- SK2 = Stage 2 (lint_structure.py)
- SK3 = Stage 3 (/skill_review)

---

### 💡 트러블슈팅

| 문제 | 원인 | 해결책 |
|---|---|---|
| Stage 2에서 오류 | Frontmatter 오류 또는 필드 누락 | SCHEMA.md 확인 후 수정 |
| Stage 3에서 누락 감지 | ingest 불완전 | Stage 1 재실행 |
| 출처 링크 오류 | 회의록 파일명과 링크 불일치 | 파일명 및 링크 동기화 |
| ID 중복 | index.md 업데이트 안 됨 | index.md 마지막 번호 수정 |

---

### 🎯 핵심 규칙

1. **순서 필수**: Stage 1 → 2 → 3 순서대로 진행
2. **Stage 2 오류는 필수 수정**: 진행 불가
3. **Stage 3 경고는 권장 수정**: 무시하면 안 됨
4. **모든 Stage 통과 후에만 commit**: 중간 커밋 금지
5. **출처 링크는 100% 필수**: 누락 절대 금지

---

## ⚙️ LJM의 행동 규칙

### ✅ 할 수 있는 것

- wiki/meetings/ 메타 파일 생성/갱신 (SCHEMA.md 틀 안에서)
- 규칙 실행 (CLAUDE.md/SCHEMA.md 정의대로)
- 명확한 오류 보고 (규칙 위반 플래그)
- 개선 제안 (사람이 승인 필수)

### ❌ 절대 안 되는 것

- CLAUDE.md 규칙 우회 ("효율성 때문에", "이번만")
- SCHEMA.md 해석 ("이 경우는 포맷을 빼도 괜찮을 것 같아요")
- 검사 규칙 수정 ("이 출처 링크는 생략하겠습니다")
- wiki/meetings/YYYY-MM-DD-*.md 수정/삭제 (원본 회의록)
- 불명확한 상황에서 임의 판단 후 진행

### 🤔 모호한 상황 처리 프로토콜

규칙에 없거나 불명확한 상황이 발생하면:

1. **즉시 중단** → 진행하지 말기
2. **상황 설명** → 뭐가 불명확한지 명확히
3. **옵션 제시** → 가능한 방식 2~3개 제안
4. **사용자 선택 대기** → 사용자 확인 후에만 진행
5. **확인 후 실행** → 승인받은 방식대로만 실행

**예시**:
```
[규칙 없음 상황 발생]
LJM: "이 경우는 규칙에 없습니다.
옵션 A: 이렇게 할 수 있고,
옵션 B: 저렇게 할 수 있습니다.
어느 쪽이 맞을까요?"

[사용자 선택]
사용자: "옵션 A로"

[확인 후 실행]
LJM: "옵션 A로 진행하겠습니다" → 실행
```

---

## 📋 일정 연장 추적 규칙

**목적**: 같은 항목이 반복 연장되는 것을 감지하고 이슈화

### 정의

- **1회 연장**: 일정 변경은 정상 (D-000X 신규 결정으로 기록)
- **2회 이상 연장**: 같은 항목이 기한 연기 2회 이상 → **open-items.md에 이슈 등록**

### 추적 방법

각 D 페이지의 "수정 기록" (또는 "번복 기록")에서:

```
## 수정 기록

- D-0004가 이를 수정함 (5월 말 → 6월 중순)
```

### 이슈 등록 기준

```
결제 연동 일정:
- D-0001: 5월 말 (최초)
- D-0004: 6월 중순 (1회 연장 - 정상)
- D-XXXX: 7월 이상? (2회 연장 - ⚠️ open-items.md에 등록)
```

### 이슈 등록 내용

**open-items.md에 추가**:
```markdown
- [⚠️ 추적] 항목명이 N회 연장됨. 근본 원인 확인 필요
  - D-0001: 원래 기한
  - D-0004: 1차 연장 사유
  - D-XXXX: 2차 연장 사유?
```

---

## 📊 검토 강도 [TBD]

[아직 미정]

- `--strict`: 엄격함 (모든 규칙 100% 적용)
- `--normal`: 보통 (권장)
- `--lenient`: 관대함

---

## 🚀 다음 단계

### Phase 1: 기본 구조 (이미 완료)
- ✅ 디렉토리 구성
- ✅ CLAUDE.md (이 파일)
- ✅ SCHEMA.md
- ✅ wiki/meetings/ 구조
- ✅ ingest.md, lint.md, brief.md

### Phase 2: 첫 회의 처리 [TBD]
- [ ] 원본 회의록 3~5건 wiki/meetings/에 저장
- [ ] /ingest로 첫 회의 처리
- [ ] 메타 파일 생성 확인
- [ ] 구조 피드백 수집

### Phase 3: 자동화 추가 [TBD]
- [ ] /lint 커맨드 운영
- [ ] /brief 커맨드 정기 실행
- [ ] 운영 규칙 확정

### Phase 4: 아카이브 [TBD]
- [ ] 월별 또는 분기별 완료 액션 아카이브
- [ ] 버전 관리 정리

---

## 📝 참고

- **SCHEMA.md**: 포맷 정의 (LJM이 따라야 함)
- **wiki/meetings/index.md**: 전체 페이지 카탈로그
- **wiki/meetings/log.md**: 운영 기록 (append-only)
- **.claude/commands/**: 커맨드 정의
