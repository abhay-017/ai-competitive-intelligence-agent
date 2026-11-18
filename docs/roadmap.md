# v2 roadmap

| Priority | Feature | Why |
|---|---|---|
| P1 | 👍/👎 **feedback buttons** on Telegram alerts, written back to the log | Real-world labels to recalibrate the impact rubric and few-shot examples |
| P1 | Move storage to **Supabase (Postgres + pgvector)** | Scales beyond n8n Data Tables; semantic search over history for Q&A (RAG) |
| P1 | **Slack / Microsoft Teams** delivery | Where product teams already work |
| P2 | **Changelog and pricing-page diffing** (HTTP Request + hash comparison) | Catches silent pricing changes that never make the news |
| P2 | **Job-posting signal** (careers pages, Greenhouse/Lever APIs) | Hiring patterns reveal strategy months early |
| P2 | **Multi-language sources** with translation | Regional competitors and markets |
| P3 | Auto-generated **monthly slide deck** for leadership | Saves the consultant step |
| P3 | **Cost and quality dashboard** (Looker Studio on the log) | Tracks alert precision and volume over time |
| P3 | **LLM-as-judge regression tests** run on every prompt change | Prevents silent quality regressions |

