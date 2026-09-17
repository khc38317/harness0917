# Obsidian 설정 가이드

**목적**: Wiki Harness를 Obsidian vault로 사용하기

---

## 🚀 빠른 시작

### 1️⃣ Vault 열기

Obsidian을 열고:
```
파일 → 다른 폴더에서 vault 열기
→ C:\Users\KOSTA\wiki_harness 선택
```

### 2️⃣ 신뢰 설정

처음 열면 "신뢰하시겠습니까?" 묻습니다.
```
예, 신뢰합니다 클릭
```

### 3️⃣ 기본 설정 확인

```
설정 → 언어 → 한국어 (이미 설정됨)
```

---

## 📁 Obsidian에서 보이는 구조

```
wiki_harness/ (Vault)
├── raw/                   ← (비어있음)
├── wiki/
│   └── meetings/          ← 원본 회의록
│   ├── decisions/         ← 결정 페이지 (자동 생성)
│   ├── actions/
│   │   └── actions.md
│   └── glossary.md
├── .claude/commands/      ← 숨김 (기술 문서)
├── README.md              ← 📍 여기서 시작
├── CLAUDE.md
├── SCHEMA.md
├── index.md
└── log.md
```

---

## 🎨 권장 Obsidian 기본 설정

**이미 .obsidian/obsidian.json에 설정됨:**

- ✅ 언어: 한국어
- ✅ 테마: Obsidian (다크 모드 자동)
- ✅ 줄 번호 표시: ON
- ✅ 읽기 모드 길이: ON (가독성)
- ✅ Live Preview: ON
- ✅ 철자 검사: ON (한글 포함)

---

## 🔌 추천 플러그인 (선택사항)

### 필수는 아니지만 유용한 플러그인들:

#### 1. **Dataview**
- 역할: frontmatter 데이터를 쿼리 가능
- 사용례: 모든 A-XXXX 액션을 기한순으로 정렬해서 보기
- 설치: Community plugins → "Dataview" 검색 → Install

#### 2. **Calendar**
- 역할: 캘린더 뷰로 회의 일정 시각화
- 사용례: 어느 날 회의가 있었는지 한눈에 보기
- 설치: Community plugins → "Calendar" 검색 → Install

#### 3. **Templater**
- 역할: 템플릿으로 D/A 페이지 자동 생성
- 사용례: 새 결정 페이지 만들 때 포맷 자동 입력
- 설치: Community plugins → "Templater" 검색 → Install

#### 4. **Graph Analysis**
- 역할: 그래프를 더 상세하게 분석
- 사용례: D-A 연결 관계 분석, 고아 페이지 찾기
- 설치: Community plugins → "Graph Analysis" 검색 → Install

---

## 🖼️ Obsidian에서 활용하기

### 1️⃣ Left Sidebar (왼쪽) — 파일 탐색

```
파일 탐색기 보이기 (설정 → 파일 탐색기)

wiki_harness/
├── wiki/meetings/        ← 원본 보기/편집 금지
├── wiki/decisions/       ← D 페이지 검색
├── wiki/actions/         ← A 페이지
└── wiki/glossary.md      ← 용어 찾기
```

**팁**: Cmd+P (또는 Ctrl+P) 로 빠르게 파일 검색

### 2️⃣ Right Sidebar (오른쪽) — 메타데이터

```
설정 → Plugins → Backlinks / Outline 활성화

1. Backlinks: 현재 페이지를 링크하는 다른 페이지들
   예: D-0001 페이지에서 "역링크"를 보면
   → A-0021, A-0022 액션이 이 결정을 참고하는 것 확인

2. Outline: 현재 페이지의 목차
   예: D-0001을 열면
   → ## 결정 내용 / ## 검토한 대안 / 등 섹션 확인
```

### 3️⃣ Graph View (그래프) — 관계 시각화

```
메뉴 → Open local graph (또는 Ctrl+Alt+G)
```

**보이는 것:**
- 노드: D, A, 용어 페이지들
- 링크: `[[D-0001]]` 형태의 연결
- 색상: (기본 설정)

**활용:**
- D-A 연결 관계 확인
- 고아 페이지 (고립된 노드) 찾기
- 미결이 어느 A와 연결되는지 시각적으로 보기

**팁**: 마우스로 노드 클릭 → 페이지 미리보기

### 4️⃣ Search (검색) — 전체 검색

```
Cmd+Shift+F (또는 Ctrl+Shift+F)

예시 검색:
- "D-" → 모든 결정 찾기
- "상태: 진행중" → 진행 중인 액션 찾기
- "Bob" → Bob 담당 항목 찾기
```

---

## 📌 Obsidian 작업 흐름

### 회의 후 ingest 단계

```
1️⃣ 회의록을 wiki/meetings/에 추가
   Obsidian 좌측 파일탐색기에서 "새 폴더" / "새 파일"
   또는 외부 파일 드래그앤드롭

2️⃣ /ingest 커맨드 실행
   → Claude가 D/A/용어 페이지 자동 생성

3️⃣ wiki/ 폴더를 새로고침 (F5 또는 설정 → 새로고침)
   → 새 D 페이지들이 decisions/ 폴더에 나타남

4️⃣ Graph view 열기 (Ctrl+Alt+G)
   → D-A 연결 구조를 시각적으로 확인
```

### 다음 회의 준비 단계

```
1️⃣ index.md 열기
   → 현재 상태 확인 (마지막 D/A 번호)

2️⃣ /brief 커맨드 실행
   → brief 결과를 claude.md 나 별도 메모에 붙이기

3️⃣ actions/actions.md 열기
   → 기한 임박 액션 확인 (Outline에서 보기)

4️⃣ glossary.md 열기
   → 팀 용어 확인
```

### 정기 점검

```
1️⃣ /lint 커맨드 실행
   → 오류 목록 확인

2️⃣ Graph view에서 고아 페이지 찾기
   → 혼자 떨어져 있는 노드 = 링크가 없는 페이지

3️⃣ backlinks 확인
   → 각 D 페이지가 어느 A에서 참조되는지 확인
```

---

## ⚙️ 고급 설정 (선택사항)

### Daily Notes (일일 노트)

회의 아젠다나 회의 중 메모를 저장하는 용도:

```
설정 → Core plugins → Daily notes 활성화
→ 새 daily note 만들기 (Cmd+Alt+T)

파일명: 2026-03-15-회의전브리핑.md 같은 식으로 별도 관리 가능
```

### Workspaces (작업 공간)

다양한 레이아웃을 저장:

```
레이아웃 구성 후:
우상단 "Workspaces" → "Save as new workspace"

예시:
- "Review" workspace: 결정 검토용 (decisions 열어놓음)
- "Ingest" workspace: ingest 작업용 (wiki/meetings + decisions)
- "Brief" workspace: 회의 준비용 (actions/glossary 열어놓음)
```

---

## 📚 Obsidian 숨김 폴더

이미 설정되어 있는 숨김 폴더:
- **.obsidian/** — 설정 파일 (보통 숨김)
- **.claude/commands/** — 기술 문서 (평상시 볼 필요 없음)

**보이게 하려면:**
```
설정 → 파일 탐색기 → "숨겨진 파일 표시" 활성화
```

---

## 🔒 보안 주의

### 절대 하면 안 되는 것

❌ **wiki/meetings/ 파일 직접 편집**
- Obsidian에서 meetings 파일을 보기만 하고 수정하지 않기
- 수정이 필요하면 외부 에디터(VS Code 등)에서 변경

❌ **wiki/decisions/ 파일 임의로 삭제**
- 삭제하면 Git에서 복구 불가
- 정말 필요하면 Git으로 삭제 후 commit

---

## 💡 팁

### Wikilink 활용

Obsidian에서 문서 작성 중:
```markdown
이 결정은 [[D-0001-인증방식결정]]에 기반합니다.
이 액션은 [[A-0021]]로 처리됩니다.
```

작성하면 자동으로 파란 링크가 생기고, 클릭 시 해당 페이지로 이동

### 미리보기 (Preview)

```
Alt + Click (또는 Cmd+Click) 페이지 링크
→ 별도 패널에서 미리보기 (현재 페이지는 유지)
```

### 빠른 전환

```
Cmd/Ctrl + Tab → 최근 열었던 파일 간 이동
```

---

## 🆘 문제 해결

### "파일이 보이지 않습니다"

```
→ 설정 → 파일 탐색기 → "숨겨진 파일 표시" ON
→ F5 (새로고침)
```

### "백링크가 안 나타납니다"

```
→ 설정 → Core plugins → "Backlinks" 활성화
→ 우측 패널 Backlinks 클릭
```

### "Graph view가 비어있습니다"

```
→ 페이지들이 [[링크]]로 연결되어야 그래프에 나타남
→ /ingest가 제대로 출처 링크를 생성했는지 확인
```

### "Git 커밋이 자꾸 충돌합니다"

```
→ .obsidian/ 폴더는 자주 변경됨 (설정 저장)
→ .gitignore에 .obsidian/ 추가할 수 있음 (선택)
```

---

## 📖 추천 학습 순서

1. **이 파일** (5분) 읽기
2. Obsidian 열기 → 프로젝트 폴더 vault로 설정
3. **README.md** 열어서 읽기
4. **index.md** → **SCHEMA.md** 순서로 읽기
5. Graph view 열어보기 (아직 페이지가 없으니 비어있음)
6. 원본 회의록을 wiki/meetings/에 저장 후 /ingest 실행
7. 새로고침 후 Graph view 다시 보기 (D-A 연결이 나타남)

---

## [TBD] 추후 추가 가능

- [ ] Templater로 D/A 페이지 자동 생성 스크립트
- [ ] Dataview로 기한 임박 액션 자동 리스트
- [ ] Daily notes와의 통합
- [ ] Obsidian publish (공개 공유 기능)

---

**설정 파일**: `.obsidian/obsidian.json` (자동 생성됨)  
**Vault 열기**: `C:\Users\KOSTA\wiki_harness`  
**Obsidian 버전**: 최신 권장 (1.4.0+)
