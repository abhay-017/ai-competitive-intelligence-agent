# Case study: automating competitive intelligence for a work-management SaaS team

**Client (illustrative):** a mid-size B2B SaaS company that competes with Notion, Atlassian, Asana, monday.com and Linear.

## Client problem
- One analyst spends **about 7 hours a week** collecting competitor news and writing a summary.
- High-impact moves (pricing changes, AI launches) reach product leadership **2–4 days late**.
- The weekly summary says *what* happened, not *so what* or *now what*.

## Approach
1. **Scoped the signal**: 6 categories that map to decisions (pricing, product launch, hiring, partnership, campaign, other) and a 1–10 impact rubric agreed with stakeholders.
2. **Built a daily pipeline in n8n**: RSS and news collection, deduplication, Gemini classification with a strict JSON schema, Telegram alerts for impact ≥ 7, and a n8n Data Tables log.
3. **Built a weekly analyst agent** (Gemini AI Agent with Data Table lookup, web search and month-over-month comparison tools) that writes a partner-style brief: headline moves, SWOT delta, threats and opportunities, 3 actions.
4. **Kept a human in the loop**: the brief stays *DRAFT* until approved in Telegram.
5. **Made it reliable**: retries, a fallback model, and an error workflow with an AI-diagnosed alert.
6. **Measured quality**: a labelled evaluation set of 40 items, with accuracy, alert precision and recall reported honestly.

## Results (target / to be filled from your eval run)
| | Before | After |
|---|---|---|
| Analyst time on CI per week | ~7 h | ~1 h (review and approve) |
| Delay before leadership hears of a high-impact move | 2–4 days | < 24 h |
| Weekly brief includes recommended actions | No | Yes, 3 per week, human-approved |
| Monthly tooling cost | n/a | **₹0** (free tiers) |

## ROI estimate
| Assumption | Value |
|---|---|
| Analyst hours saved per week | 6 h |
| Loaded cost of an analyst | ₹800 per hour (≈ ₹12 LPA) |
| Weekly saving | 6 × ₹800 = **₹4,800** |
| Annual saving (48 weeks) | **≈ ₹2.3 lakh** |
| Setup effort | ~40 h one-time ≈ ₹32,000 |
| Maintenance | ~1 h a month ≈ ₹9,600 a year |
| Running cost | ₹0 (free tier); ~₹500 a month if moved to paid Gemini |
| **Payback period** | **≈ 7 weeks** |

The bigger value is not counted here: reacting to a competitor's pricing change days earlier.

## Risks and limitations
- **Free-tier quotas** can change. Mitigation: per-run caps, retries, a fallback model, and a one-line switch to paid Gemini or Groq.
- **Noisy matches** for generic names ("Linear", "Notion"). Mitigation: tuned `news_query` per competitor and an `is_relevant` flag.
- **LLM over-scoring.** Mitigation: a calibrated rubric, the evaluation set, and a threshold kept in Config.
- **Hallucination in briefs.** Mitigation: agents are told to use tool data only, cite sources, and get human approval.
- **Data and compliance (for a real client):** only public sources are used; no personal data is processed. For enterprise use, move to n8n with SSO, a Vertex AI or Azure OpenAI region the client approves, and Supabase or Postgres with access control.

## What I would change for a real client
Connect to their CRM win/loss notes and sales call transcripts (internal signal); store embeddings in pgvector for semantic search; add a 👍/👎 feedback button on alerts to recalibrate scoring; deliver to Slack or Teams instead of Telegram.


