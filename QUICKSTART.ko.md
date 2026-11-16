# 5분 빠른 시작

[English](QUICKSTART.md) · **한국어** · 자세한 것은 [README.ko.md](README.ko.md)

필요한 것: Python 3.8 이상, git, 명령을 실행할 수 있는 AI 에이전트(예: Claude Code). 설치할 패키지는 없다.

## 0. 가장 짧은 방법

에이전트에서 빈 폴더를 열고 "이 저장소로 내 일에 맞는 하네스를 만들어 줘: https://github.com/walktothemoone-creator/harness_engineering_apk"라고 말한다. 아래 단계를 에이전트가 모두 대신 한다. 아래는 손으로 할 때의 방법이다.

## 1. 프로젝트 폴더에 씨앗 받기 (1분)

```bash
mkdir my-project && cd my-project
git clone https://github.com/walktothemoone-creator/harness_engineering_apk.git harness_engineering
```

## 2. 에이전트에게 맡기기 (3분)

그동안 이 일에 대해 에이전트와 나눈 채팅이 있다면 **같은 채팅에서** 이렇게 말한다.

> harness_engineering/build_skill.ko.md 를 읽고 지금까지 나눈 내용으로 이 폴더에 하네스를 만들어 줘

에이전트가 목적·목표·규칙을 정리해 보여 주면 확인하거나 고쳐 준다. 그러면 `README.md`, `SKILL.md`, `docs/`, `scripts/`가 생기고 대화가 작업 000으로 봉인된다.

새로 시작하는 일이라 나눈 대화가 없으면, 하려는 일의 목적을 두세 문장으로 먼저 말하고 위 문장을 보내면 된다.

## 3. 잘 됐는지 확인 (30초)

```bash
python3 harness_engineering/tools/seed.py check
```

"하네스 완성"이 나오면 끝이다.

## 4. 그다음부터

이 폴더에서 무엇을 시키든 에이전트가 `SKILL.md` 절차로 일한다: 요청(REQ) → 계획(PLAN) → 지시(INS) → 코드 → 코드 변경 기록(LOG) → 작업 기록(HISTORY) → 봉인.

- 지금 상황 보기: `README.md` 2절
- 지금까지의 일: `python3 scripts/_shared/chain.py list history`
- 기록이 온전한지: `python3 scripts/_shared/chain.py verify`

완성된 모습이 궁금하면 [examples/ko_demo/](examples/ko_demo/)를 본다. 여럿이 쓸 때는 [TEAM.ko.md](TEAM.ko.md)를 먼저 읽는다.

## Windows

- `python3` 대신 `py` 또는 `python`을 쓴다 (예: `py harness_engineering\tools\seed.py check`).
- `tests/property_test.sh`는 bash 스크립트라 Git Bash나 WSL에서 돌린다.
- Windows에서는 아직 시험하지 않았다. 막히면 Issue로 알려 주면 좋다.
