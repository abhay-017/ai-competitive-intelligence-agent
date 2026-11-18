# PRD: AI Competitive Intelligence & Strategy Brief Agent

## 1. Problem statement
Product and marketing teams in the crowded work-management software market (Notion, Atlassian, Asana, monday.com, Linear) learn about competitor moves late and inconsistently. Today one analyst spends roughly **6–8 hours a week** reading news, blogs and changelogs, pasting links into a doc and writing a summary. Important moves, such as a pricing change or a flagship AI launch, are noticed days late, and the weekly summary describes what happened without saying what to do about it.

## 2. Users and persona
**Primary: Priya, Senior Product Manager** at a mid-size SaaS company.
- Needs to know the same day when a competitor ships something that affects her roadmap.
- Has 15 minutes on Monday to read a brief and decide what to escalate.
- Distrusts AI summaries that make up facts and wants sources.

**Secondary: Head of Marketing**, who needs competitor campaign and pricing moves to adjust positioning. **Analyst**, who maintains the competitor list and approves the brief.

## 3. User stories
1. As a PM, I get a **Telegram alert within a day** when a competitor makes a high-impact move (impact ≥ 7), with a one-line summary, why it matters, and the link.
2. As a PM, I receive a **weekly brief every Monday** covering headline moves, a SWOT delta per competitor, threats and opportunities, and 3 recommended actions.
3. As an analyst, I **approve or decline** the brief before it is marked final and emailed, so that no unreviewed AI recommendation reaches leadership.
4. As a PM, I can **ask questions in Telegram** (*"What did Asana do on pricing this quarter?"*) and get an answer with sources from our own log.
5. As an analyst, I can **add or remove competitors** by editing an n8n Data Table, without touching the workflow.
6. As the owner, I am **alerted when the pipeline fails**, with a likely cause and fix.

## 4. Scope (v1)
**In scope:** 5 competitors; Google News and blog RSS; daily classification into 6 categories with a 1–10 impact score; Telegram alerts; n8n Data Tables log; weekly agent brief with tools (Data Table lookup, web search, month-over-month comparison); human approval; Gmail delivery; Telegram Q&A; error workflow with a fallback model.

**Deliberately left out (and why):**
- *Scraping pricing pages and LinkedIn job posts*: brittle, may break terms of service, and needs paid proxies. RSS and news cover about 80% of the signal.
- *Vector database / RAG*: the log is small (hundreds of rows a month), so Gemini's long context reads it directly. Planned for v2 when the log grows.
- *Multi-language sources*: English only in v1.
- *A UI dashboard*: n8n Data Tables plus Telegram is enough to validate the value first.
- *Automatic actions on recommendations*: recommendations stay advisory and approved by a human.

## 5. Functional requirements
| ID | Requirement |
|---|---|
| F1 | Run daily at 08:00 and read the competitor list from the Competitors data table |
| F2 | Fetch Google News (last 2 days) and blog RSS per competitor; ignore failing feeds |
| F3 | Skip items seen in earlier runs and duplicate syndicated headlines |
| F4 | Classify each item with an LLM into a fixed JSON schema |
| F5 | Alert on Telegram when impact ≥ a configurable threshold (default 7) |
| F6 | Append every classified item to `Intel_Log` |
| F7 | Every Monday, generate the brief with an AI Agent and tools |
| F8 | Require Telegram approval; on approval, email it and mark it `final`; otherwise mark it `rejected` |
| F9 | Answer Telegram questions from logged data only, with citations, for an authorised chat only |
| F10 | On any failure, send a Telegram alert with an AI diagnosis; fall back to a smaller model |

## 6. Non-functional requirements
- **Cost:** ₹0 per month (free tiers only). At most 25 LLM calls per daily run.
- **Latency:** high-impact alert within 24 hours of publication. Brief ready by 09:15 Monday.
- **Trust:** every claim in the brief and Q&A has a source link. No invented facts.
- **Maintainability:** all configuration lives in a `Config` node and the Competitors data table, with no hard-coded secrets in exports.

## 7. Success metrics
| Metric | Definition | Target (v1) |
|---|---|---|
| Classification accuracy | % of items where the model's category matches the human label (eval set) | ≥ 80% |
| Alert precision (relevance rate) | % of alerts a PM would call "useful" | ≥ 70% |
| High-impact recall | % of human-labelled ≥7 items that triggered an alert | ≥ 80% |
| Time-to-brief | Monday trigger → brief in Telegram | < 5 min |
| Cost per brief | LLM and API spend | ₹0 (free tier) |
| Analyst time saved | Hours a week vs the manual process | ≥ 5 h |

## 8. Risks
Free-tier quota changes, noisy news matches for generic names ("Linear", "Notion"), LLM over-scoring, and RSS feed changes. Mitigations are listed in the case study.


