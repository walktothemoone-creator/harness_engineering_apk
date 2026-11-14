# {{PROJECT}} — {{TITLE}}

<!-- FILL: 이 폴더가 무엇을 위한 곳인지 한두 문장 (누구의 무엇을, 왜 계속 하는가) -->
**어떤 작업이든 이 문서를 먼저 읽는다.** 작업 절차는 [SKILL.md](SKILL.md)에 있다.
이 폴더의 절차는 맥락을 유지하면서 에이전트와 사용자가 목표를 분명히 다잡아 가며 목적과 목표를 달성하기 위한 것이다.

표기: ✅ 확인됨 · ❌ 문제 · ⏳ 미확인/진행 중

---

## 1. 과거 이력 — 무엇을 읽으면 되나

| 순서 | 문서 | 알 수 있는 것 |
|---|---|---|
<!-- FILL: 작업마다 한 줄. | 1 | [docs/history/파일명](docs/history/파일명) | <이 보고에서 알 수 있는 것> | -->

- 작업 기록(`docs/history/`)을 작업 순서대로 읽으면 일의 흐름을, 코드 변경 기록(`docs/logs/`)을 작업 순서대로 읽으면 코드가 어떻게 변해 왔는지를 알 수 있다. 더 깊이 볼 때만 같은 파일명의 `docs/req/`(무엇을 원했나) → `docs/plan/`(어떻게 하기로 했나) → `docs/instruction/`(구체적으로 무엇을 했나) → `scripts/{작업ID}_…/MANIFEST.md`(어떤 코드가 남았나) 순으로 본다.
- 문서 여섯 종류의 역할과 이어지는 방식: [docs/README.md](docs/README.md)
- 작업 목록과 문서 현황: `python3 scripts/_shared/chain.py status` / 작업 순서대로 나열: `python3 scripts/_shared/chain.py list history` (`list logs`)

## 2. 현재 상황 (기준: <!-- FILL: yyyy-mm-dd HH:MM, 무엇으로 확인했나 -->)

**목적:** <!-- FILL: 이 프로젝트가 결국 이루려는 것 한 문장 -->
**지금 단계:** <!-- FILL: 어디까지 왔고 다음은 무엇인가 -->

| 항목 | 상태 | 근거 |
|---|---|---|
<!-- FILL: 사람·역할, 대상(시스템/장비/데이터)의 상태, 접속 경로, 결정된 것과 미정인 것. 근거 칸에는 파일명·명령·작업 ID -->

남은 일 (다음 작업은 1번부터)

<!-- FILL: 1. ... 2. ... -->

> 이 절은 작업이 끝날 때마다 고친다. 기준 시각 이후 현실이 바뀌었을 수 있으니 SKILL 1단계의 "현실 확인"을 먼저 한다. 과거 시점의 상태는 각 작업 기록(`docs/history/`)에 남아 있다.

## 3. 폴더 구성

```
{{PROJECT}}/
├── README.md            이 문서 (시작점, 현재 상황)
├── SKILL.md             에이전트 공통 작업 절차
├── .env                 실제 설정값 — 공유·커밋 금지
├── .env.example         설정 키 목록·설명·키↔스크립트 대응표
├── harness_engineering/ 이 구조를 만든 씨앗(별도 저장소) — 체인 밖, 커밋 안 함
├── docs/                작업의 뼈대 — 연결고리이자 기록 (설명: docs/README.md)
│   ├── README.md        문서 체계 설명
│   ├── _templates/      문서 양식 (chain.py new 가 읽음)
│   ├── LEDGER.md        봉인 원장 — 도구가 쓴다, 손으로 고치지 않음 (첫 봉인 때 생김)
│   ├── req/             요구사항 정의서   (REQ)     무엇을 원하는가
│   ├── plan/            작업계획서        (PLAN)    어떻게 할 것인가
│   ├── instruction/     작업지시서        (INS)     구체적으로 무엇을 실행하는가
│   ├── logs/            코드 변경 기록    (LOG)     코드의 개념·로직이 어떻게 시작해 어떻게 바뀌었는가
│   └── history/         작업 기록         (HISTORY) 무엇이 됐고 무엇이 남았는가 — 작업 순서대로
├── scripts/             내가 작업하는 코드 — 시험·분석·초안·도구
│   ├── _shared/                  여러 작업이 같이 쓰는 모듈 (chain.py, envload.py)
│   └── {yyyymmdd}_{순번}_{slug}/  작업별 코드 + MANIFEST.md (TASK)
└── vendor/              배포되는 대상의 코드(application) — 배포 요구가 있을 때만 생김
    └── {앱}/                     사용자가 만드는 폴더: SDK, 기존 개발자 코드, 배포할 코드 + README.md
```

`vendor/` 현황: <!-- FILL: 앱 폴더마다 한 줄 (무엇이고 어디에 배포되나, 원본 출처). 없으면 "없음 — 배포 요구가 생기면 사용자가 폴더를 만든다" -->

| 작업 ID | 내용 | 상태 | 코드 폴더 |
|---|---|---|---|
<!-- FILL: | {yyyymmdd}_000 | 하네스 구축 | 완료 | `scripts/{yyyymmdd}_000_harness_genesis/` | -->

## 4. 작업 절차 (요약 — 자세한 것은 SKILL.md)

1. 이 `README.md`를 읽고, 기준 시각 이후 현실이 바뀌었는지 확인한다
2. 채팅 또는 `docs/req/`에서 요청을 파악해 **REQ**로 남긴다 (목적·목표를 적고 사용자와 맞춘다)
3. **PLAN**을 `docs/plan/`에 쓴다 (항목마다 대응 REQ)
4. **INS**를 `docs/instruction/`에 쓴다 (항목마다 대응 PLAN)
5. 코드는 `scripts/{작업ID}_{slug}/`에 만들고 **MANIFEST.md**에 적는다 (항목마다 대응 INS)
6. **LOG**를 `docs/logs/`에 쓴다 (코드의 개념·로직이 이전 → 이후 어떻게 바뀌었나, 항목마다 대응 INS)
7. **HISTORY**를 `docs/history/`에 쓴다 (REQ→PLAN→INS→결과물→LOG 추적표 포함)
8. 문서·코드를 체인으로 잇는다: `chain.py seal --dry-run`으로 확인 → `chain.py seal` → "체인 정상". **봉인은 확정이다** (다시 봉인할 수 없다)
9. 이 `README.md`의 1·2·3절을 고쳐 마무리한다
10. 사용자에게 목표 달성 여부부터 보고한다. 요청이 목적·목표와 어긋나면 진행 전에 되묻는다 (SKILL "맥락이 흐려질 때")

## 5. 규칙

- **이름**: 문서는 `{yyyymmdd}_{순번3자리}_{제목}.md`(이름순 = 작업 순서), 한 작업의 문서는 다섯 폴더(`req` `plan` `instruction` `logs` `history`)에서 같은 파일명. 제목은 `{{PREFIX}}_`로 시작. 코드 폴더는 `{yyyymmdd}_{순번}_{slug}`
- **체인**: 문서 머리말의 `prev_hash`가 앞 문서의 `hash`를 가리킨다 (REQ → PLAN → INS → TASK → LOG → HISTORY → 다음 작업의 REQ). 봉인된 문서·코드는 고치지 않는다. 고칠 일은 새 작업으로 남긴다. `docs/`는 블록체인처럼 멱등성과 불변성을 지킨다 — 결정론적 실행, 중복 실행 방지, 무결성, 상태 일치성, 완결성 (SKILL "docs/는 블록체인처럼")
- **비밀값**: `.env`의 값을 문서·출력에 옮기지 않는다
- **코드 위치**: 내가 작업하는 코드는 `scripts/`, 배포되는 대상의 코드는 `vendor/{앱}/`. scripts에서 검증한 것만 vendor에 적용하고, vendor의 변화는 `docs/logs/`에 적는다
- **사실 표기**: 확인한 것(✅)과 못 한 것(⏳), 추정을 구분해 적고 근거 파일명을 남긴다
<!-- FILL: 이 프로젝트만의 규칙 (SKILL "대상·권한"의 요약) -->

## 6. 자주 쓰는 명령 (`{{PROJECT}}/`에서)

체인 검증

```bash
python3 scripts/_shared/chain.py verify
```

하네스 점검 (빈칸·필수 파일·체인)

```bash
python3 harness_engineering/tools/seed.py check
```

<!-- FILL: 현실 확인 명령 등 반복해서 쓰는 명령. 없으면 이 줄을 지운다 -->
