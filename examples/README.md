# examples

| Folder | What |
|---|---|
| [ko_demo/](ko_demo/) | 주간 매출 CSV 요약 (Korean). Planted with `seed.py init --lang ko`, two sealed work items: 000 harness setup, 001 a product-totals script with three passing tests. Run `python3 scripts/_shared/chain.py verify` inside it — it prints the same head as when it was sealed |

The examples do not include the `harness_engineering/` seed folder (it is in their `.gitignore`), so `seed.py check` is not run inside them; `chain.py verify` is.
