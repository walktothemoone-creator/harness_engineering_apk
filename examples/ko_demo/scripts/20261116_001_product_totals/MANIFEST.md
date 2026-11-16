---
id: TASK-20261116-001
work: 20261116_001
type: task
title: SALES 제품별 합계 스크립트
date: 2026-11-16
status: 완료
prev: INS-20261116-001
prev_hash: 71dbbe310973f9eaa0c8638659c23ded6d774588402c69ac0a498cb1d69b1886
hash: dd11bb978ebf1072d29fba2ab0d3e648e64d5272d2cfc1febaf6c512d0570297
tree_hash: 19a40847e6e0820b55c0fef854900625c7288f30cadb6aae42942dca9a9738dd
---

# SALES 제품별 합계 스크립트 — 작업 결과물 목록 (TASK-20261116-001)

## 1. 목적 (대응 지시)

INS-20261116-001 I1·I2.

## 2. 파일

| 파일 | 하는 일 | 대응 INS | 검증 상태 |
|---|---|---|---|
| `summarize.py` | CSV를 읽어 제품별 합계 마크다운 표를 출력. 빈·숫자 아닌 금액 행은 건너뛰고 수를 알림. 입력 파일은 읽기만 | I1 | 시험 ✅ |
| `test_summarize.py` | 시험 3개 (예시 합계, 전체 합 표시, 잘못된 헤더) | I2 | 3/3 ✅ |
| `sample.csv` | 시험용 예시 데이터 (가짜) | I2 | — |

다시 돌려도 됨: 읽기만 하므로 결과가 같다.

## 3. vendor 적용

없음.

## 4. 실행 방법

```bash
python3 summarize.py sample.csv
```
