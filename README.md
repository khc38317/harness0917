# 📋 Wiki Harness — 회의록 기반 SSOT

**목적**: 회의록을 원본으로 하는 의사결정 추적 및 액션 관리 시스템

**주요 기능**:
- ✅ 의사결정 추적 (D-XXXX)
- ✅ 액션아이템 관리 (A-XXXX)
- ✅ 용어/시스템명 정의
- ✅ 다음 회의 아젠다 자동 생성

---

## 🚀 빠른 시작

### 1. 회의록 저장

Notion에서 .md 형태로 내보낸 회의록을 여기 저장:
```
wiki/meetings/YYYY-MM-DD-제목.md
```

예시:
```
wiki/meetings/2026-03-12-주간개발.md
```

### 2. 회의록 처리

LJM 커맨드로 자동 처리:
```
/ingest wiki/meetings/2026-03-12-주간개발.md
```

→ 메타 파일 자동 갱신 (decisions.md, actions.md, glossary.md)

### 3. 다음 회의 준비

회의 전에 브리핑 생성:
```
/brief
```

→ 기한 임박, 미결 사항, 추천 아젠다 확인

---

## 📂 디렉토리 구조

```
wiki_harness/
├─ CLAUDE.md              # 도구 설명 (필독!)
├─ SCHEMA.md              # 포맷 정의 (필독!)
│
├─ raw/                   # (비어있음, 향후 다른 원본용)
│
├─ wiki/
│  └─ meetings/           # 모든 것이 여기!
│     ├─ 2026-03-05-주간개발.md     # 원본 회의록 (불변)
│     ├─ decisions.md               # 결정 목록
│     ├─ actions.md                 # 액션아이템
│     ├─ index.md                   # 전체 카탈로그
│     ├─ log.md                     # 운영 기록
│     ├─ open-items.md              # 미결 사항
│     └─ glossary.md                # 용어/시스템명
│
└─ .claude/
   └─ commands/           # LJM 커맨드 정의
      ├─ ingest.md        # /ingest 프롬프트
      ├─ lint.md          # /lint 프롬프트
      └─ brief.md         # /brief 프롬프트
```

---

## 🔑 3가지 핵심 원칙

### 1️⃣ wiki/meetings = SSOT (불변)

- **원본**: 사람만 작성 (Notion .md)
- **메타**: LJM이 자동 생성 (decisions.md, actions.md)
- **변경**: 절대 금지

→ 원본이 바뀌면 SSOT가 무너집니다.

### 2️⃣ wiki/meetings = LJM 소유, 사람 검토

- **LJM**: 빠르게 생성/갱신
- **사람**: 품질 검토 + 승인

→ 협업으로 신뢰도 높음

### 3️⃣ 규칙은 사람만 변경

- **CLAUDE.md**: 커맨드 정의 (사람만 수정)
- **SCHEMA.md**: 포맷 정의 (사람만 수정)

→ LJM이 규칙을 우회할 수 없음

---

## 📖 문서

| 문서 | 설명 |
|---|---|
| **CLAUDE.md** | 도구 설명 + 경로별 소유권 + 커맨드 개요 |
| **SCHEMA.md** | 포맷 정의 (D/A/용어 구조) + ID 규칙 |
| **wiki/meetings/index.md** | 전체 카탈로그 + 현재 상태 (중요!) |
| **.claude/commands/ingest.md** | /ingest 프로토콜 (자세함) |
| **.claude/commands/lint.md** | /lint 검사 항목 (10가지) |
| **.claude/commands/brief.md** | /brief 항목 (6가지) |

---

## 🎯 커맨드

### /ingest
회의록 1건을 읽고 → 메타 파일 자동 갱신

**사용**:
```
/ingest wiki/meetings/YYYY-MM-DD-제목.md
```

**결과**:
- wiki/meetings/decisions.md 갱신
- wiki/meetings/actions.md 갱신
- wiki/meetings/glossary.md 갱신
- wiki/meetings/index.md 갱신
- wiki/meetings/log.md append

자세한 프로토콜: **.claude/commands/ingest.md** 참고

### /lint
위키 건강도 검사

**사용**:
```
/lint
```

**검사 항목**:
- 출처 링크 누락
- 기한 임박 / 초과 액션
- 좀비 액션 (30일 비활동)
- 미결 사항 미배정
- 용어 일관성
- 포맷 오류
- ID 중복

자세한 항목: **.claude/commands/lint.md** 참고

### /brief
다음 회의 전 브리핑

**사용**:
```
/brief
```

**출력**:
- 기한 임박 액션 (오늘/내일)
- 진행 중인 액션 전체
- 최근 번복된 결정
- 미해결 질문
- 추천 아젠다

자세한 형식: **.claude/commands/brief.md** 참고

---

## 🔄 워크플로우

```
1️⃣ 회의 진행
   ↓
2️⃣ 회의록을 wiki/meetings/ 저장
   ↓
3️⃣ /ingest 실행
   ├─ LJM: 분석 + 갱신
   ├─ 사람: 검토 + 피드백
   ├─ LJM: 수정
   └─ 사람: 승인 + commit
   ↓
4️⃣ 메타 파일 갱신 완료
   ├─ decisions.md
   ├─ actions.md
   └─ 용어/로그 갱신
   ↓
5️⃣ 다음 회의 전
   └─ /brief 실행
   ↓
6️⃣ (선택) 주기적
   └─ /lint 실행
```

---

## 🔢 ID 규칙 (중요!)

### D (결정)
- 형식: `D-0001`, `D-0002`, ...
- 변경: 절대 뒤로 갈 수 없음
- 번복: 새 D를 만들고 이전 D에 표시

### A (액션)
- 형식: `A-0001`, `A-0002`, ...
- 변경: 절대 뒤로 갈 수 없음
- 재사용: 완료된 ID는 절대 재사용 금지

### State 확인
**매 /ingest 전에 wiki/meetings/index.md에서 읽기:**
```
- 마지막 할당된 D 번호: D-XXXX
- 마지막 할당된 A 번호: A-XXXX
```

→ 새 번호는 항상 +1부터

---

## ⚠️ 출처 링크 (필수)

모든 **진술**에 `[[YYYY-MM-DD]]` 링크:

```markdown
JWT 기반 인증을 세션 기반으로 변경한다. [[2026-03-12]]
```

**필수 대상**:
- D의 결정 내용
- D의 검토 대안
- D의 근거
- A의 설명
- 용어의 정의

**불필요**:
- 헤더, 메타데이터
- 테이블 헤더
- 구조 데이터 (날짜, 숫자)

→ 자세히: **SCHEMA.md** 출처 링크 섹션

---

## 📊 [TBD] 미정 항목

- [ ] 검토 강도 지정
- [ ] /ask 커맨드 (추후 추가)
- [ ] 자동 아카이브 일정
- [ ] log.md 정식 운영 여부
- [ ] 추가 메타데이터

---

## 🎓 권장 학습 순서

1. **CLAUDE.md** 읽기 (10분)
   - 전체 개요 + 경로별 소유권

2. **SCHEMA.md** 정독 (20분)
   - D/A/용어 포맷
   - ID 규칙
   - 출처 링크

3. **.claude/commands/ingest.md** 정독 (30분)
   - 프로토콜의 각 단계
   - 예시 보며 이해

4. **첫 회의 처리** (실습)
   - 원본 회의록 wiki/meetings/에 저장
   - /ingest 실행해보기
   - 메타 파일 확인

5. **.claude/commands/lint.md** 읽기 (15분)
   - 검사 항목 이해

6. **.claude/commands/brief.md** 읽기 (10분)
   - 다음 회의 준비

---

## 💬 주의사항

### LJM이 절대 하면 안 됨

- ❌ 규칙 우회 ("효율성 때문에")
- ❌ SCHEMA.md 해석 (명확한 규칙만 실행)
- ❌ wiki/meetings/YYYY-MM-DD-*.md 수정/삭제
- ❌ ID 중복 생성

→ 규칙이 부족하면 **사람에게 물어보세요**

### 사람이 꼭 해야 할 일

- ✅ 원본 회의록 작성 (wiki/meetings/)
- ✅ /ingest 결과 검토
- ✅ CLAUDE.md, SCHEMA.md 수정 (규칙 변경)
- ✅ 최종 승인 후 commit

---

## 🔗 빠른 링크

| 파일 | 역할 |
|---|---|
| CLAUDE.md | 도구 설명 (필독!) |
| SCHEMA.md | 포맷 정의 (참고) |
| wiki/meetings/index.md | 현재 상태 (매번 확인) |
| .claude/commands/ingest.md | /ingest 프로토콜 (실행 전) |
| .claude/commands/lint.md | /lint 항목 (실행 시) |
| .claude/commands/brief.md | /brief 형식 (실행 시) |

---

## 🎯 다음 단계

### Phase 2: 첫 회의 처리
1. 원본 회의록 3~5건을 wiki/meetings/에 저장
2. /ingest로 첫 회의 처리
3. 메타 파일 생성 확인
4. 구조 피드백 수집

### Phase 3: 자동화 추가
1. /lint 커맨드 운영
2. /brief 커맨드 정기 실행
3. 운영 규칙 확정

### Phase 4: 아카이브
1. 월별 또는 분기별 완료 액션 아카이브
2. 버전 관리 정리

---

**프로젝트 생성**: 2026-09-17  
**마지막 수정**: 2026-09-17  
**상태**: 🟢 구축 완료, Phase 2 대기
