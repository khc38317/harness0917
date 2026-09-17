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
   └─ commands/           # LLM 커맨드 정의
      ├─ ingest.md        # /ingest 프롬프트
      ├─ lint.md          # /lint 프롬프트
      └─ brief.md         # /brief 프롬프트
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

## 🎯 3개 커맨드

### /ingest — 회의록 수집 및 처리

**역할**: wiki/meetings/ 원본 1건을 읽고 → 메타 파일 자동 갱신

**프로토콜**:
1. **State 확인** (먼저!)
   - wiki/meetings/index.md에서 마지막 D 번호 읽기
   - wiki/meetings/index.md에서 마지막 A 번호 읽기

2. **회의록 읽기**
   - wiki/meetings/YYYY-MM-DD-*.md 전문 분석

3. **추출**
   - 결정 목록
   - 액션아이템 목록
   - 미결 사항
   - 신규 용어

4. **검증**
   - 사용자에게 추출 결과 제시 ("이렇게 추출했는데 맞나요?")

5. **생성/갱신**
   - wiki/meetings/decisions.md 갱신
   - wiki/meetings/actions.md 갱신
   - wiki/meetings/glossary.md 신규 용어 추가
   - wiki/meetings/index.md 갱신
   - wiki/meetings/log.md append

6. **commit**
   - "ingest: YYYY-MM-DD 회의명"

**사용 예시**:
```
/ingest wiki/meetings/2026-03-12-주간개발.md
```

자세한 프롬프트: **.claude/commands/ingest.md** 참고

---

### /lint — 위키 건강도 검사

**역할**: wiki/meetings/ 전체를 스캔하고 문제 플래그

**검사 항목**:
- ✅ 출처 링크 누락 (SCHEMA.md 규칙 위반)
- ⚠️ 기한 임박 액션 (3일 이내)
- ❌ 기한 초과 액션
- 🔄 30일 이상 상태 변경 없는 액션
- 📌 미결 사항 중 Action 미배정 항목
- [TBD] 추가 검사 항목

**사용 예시**:
```
/lint
```

자세한 프롬프트: **.claude/commands/lint.md** 참고

---

### /brief — 다음 회의 전 브리핑

**역할**: 다음 회의 아젠다 준비용 브리핑 생성

**출력 내용**:
- 📍 즉시 확인할 사항 (오늘 기한 액션)
- 🎯 진행 중인 액션 (담당/기한/진행률)
- 💥 최근 번복된 결정
- ❓ 미해결 질문 (지난 회의 미결)
- 📌 추천 아젠다

**사용 예시**:
```
/brief
```

→ 다음 회의 전날 또는 당일 아침 실행

자세한 프롬프트: **.claude/commands/brief.md** 참고

---

## 🔄 워크플로우

```
1️⃣ 회의 진행
   ↓
2️⃣ 회의록 원본을 wiki/meetings/ 저장
   └─ 파일명: YYYY-MM-DD-제목.md
   ↓
3️⃣ /ingest 실행
   ├─ LJM: 회의록 분석 → decisions.md, actions.md 갱신
   ├─ 사람: 검토 → 피드백
   ├─ LJM: 수정
   └─ 사람: 승인 → commit
   ↓
4️⃣ 메타 파일 갱신 완료
   ├─ wiki/meetings/decisions.md 갱신
   ├─ wiki/meetings/actions.md 갱신
   ├─ wiki/meetings/glossary.md 갱신
   └─ wiki/meetings/index.md 갱신
   ↓
5️⃣ 다음 회의 전
   └─ /brief 실행 → 아젠다 준비
   ↓
6️⃣ (선택) 주기적
   └─ /lint 실행 → 건강도 체크
```

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
