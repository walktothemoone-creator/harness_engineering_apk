# ENVIRONMENT — 이 일을 하려면 컴퓨터에 필요한 것

에이전트가 작업 전에 확인하고(SKILL 1단계) 늘 지금 상태로 유지한다. 체인 밖이다. 개인적인 것은 적지 않는다: 사용자 이름, 컴퓨터 이름, 절대 경로 없음.

## 1. 이 컴퓨터 (도구가 쓴다)

`python3 scripts/_shared/envcheck.py --write` 가 아래 표를 다시 쓴다. 다른 컴퓨터에서나 업데이트 뒤에는 다시 실행한다.

<!-- auto:begin -->
<!-- auto:end -->

## 2. 기본 요건 (모든 하네스 공통)

| 필요한 것 | 이유 | 없으면 |
|---|---|---|
| Python 3.8 이상 | `chain.py`, `envcheck.py`, 작업 스크립트를 실행한다 (표준 라이브러리만) | macOS: `xcode-select --install` 또는 `brew install python` · Windows: `winget install Python.Python.3.12` · Linux: `sudo apt install python3` |
| git | 씨앗을 받는다. 폴더를 저장소로 만들면 이력을 남긴다 | macOS: `xcode-select --install` · Windows: `winget install Git.Git` · Linux: `sudo apt install git` |
| UTF-8 파일명과 내용 | 문서 이름이 한글일 수 있다 | Windows: UTF-8 터미널을 쓴다 (Windows Terminal, `chcp 65001`) |

시스템 프로그램 설치는 사용자의 컴퓨터를 바꾸는 일이다. 무엇을 왜 설치하는지 쉬운 말로 알리고, 사용자가 동의한 뒤에만 설치한다. 비밀번호를 묻는 명령은 사용자가 실행한다.

## 3. 이 프로젝트에 필요한 것 (에이전트가 관리)

패키지는 시스템 파이썬이 아니라 이 폴더의 가상 환경에 설치한다. 한 번 만든다: `python3 -m venv .venv`. 설치: `.venv/bin/pip install -r requirements.txt` (Windows: `.venv\Scripts\pip`). 모든 패키지는 `requirements.txt`에 버전을 고정해 적고, 도입한 작업 기록(HIST ID)을 남긴다.

| 도구·패키지 | 버전 | 쓰는 곳 | 언제부터 (HIST ID) |
|---|---|---|---|

그 밖의 도구 (CLI, 브라우저, 계정, 시스템 접근 권한):

| 도구 | 용도 | 동작 확인 방법 | 언제부터 (HIST ID) |
|---|---|---|---|
