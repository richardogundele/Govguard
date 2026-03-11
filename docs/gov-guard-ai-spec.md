SECTION 1 — EXECUTIVE SUMMARY

1. Executive Summary
GovGuard AI is an AI Decision Governance Infrastructure platform. It intercepts, evaluates, and scores decisions made by AI agents and automated decision systems — before or after they execute — against regulatory compliance frameworks.

The platform is built as a middleware governance layer that organisations plug into their existing AI systems without replacing or redesigning them. It functions like a compliance gateway: every AI decision passes through GovGuard, is scored for governance risk, and is either allowed, flagged for human review, or blocked.

The One-Sentence Product Definition
GovGuard AI is the Snyk for AI decisions — a governance scanner that detects regulatory risk in AI agent behaviour before it becomes a liability.

1.1 The Problem
Organisations across the UK public sector, financial services, healthcare, and enterprise are deploying AI agents and automated decision systems at speed. These systems make consequential decisions — rejecting benefit claims, screening job candidates, triaging patients, approving loans — with minimal human oversight.

The regulatory environment is hardening. The UK Information Commissioner's Office (ICO) expects organisations to explain automated decisions. The Government Digital Service (GDS) AI Playbook mandates human oversight and audit trails. The AI Assurance Innovation Fund (opening Spring 2026) signals government investment in compliance infrastructure. Organisations face a growing gap between the pace of AI deployment and the maturity of their governance.

The core questions every organisation must now answer:
•	Why did the AI make this decision?
•	Was a human involved?
•	Can the decision be challenged?
•	Is there a complete audit trail?
•	Does this system meet regulatory requirements?

Most cannot answer any of these. That is the market GovGuard AI enters.

1.2 The Solution
GovGuard AI provides three integrated capabilities:

Pre-Decision Check	Intercepts proposed AI decisions before they execute, scores governance risk, and returns ALLOW / FLAG / BLOCK.
Post-Decision Audit	Accepts decision logs after execution, scores them, and generates structured compliance reports.
Continuous Monitoring	Tracks compliance scores over time, detects drift, and fires alerts when governance standards are degrading.

1.3 Business Model
Open source framework. Commercial service. The governance scoring engine and compliance frameworks are published open source on GitHub — building credibility, attracting contributors, and creating a public CV-quality proof of concept. Revenue comes from the hosted platform, dashboard, compliance reports, integration support, and enterprise SLAs.

Open Source (Free)	Core SDK, scoring engine, UK AI Playbook compliance framework. Published on GitHub.
Hosted Platform (Paid)	Cloud-hosted governance service, dashboard, PDF audit reports, API access.
Enterprise (Paid)	SLA guarantees, custom policy engines, dedicated support, multi-jurisdiction scoring.
Government Contracts	Integration support for public sector deployments, AI Assurance Innovation Fund applications.
 
SECTION 2 — MARKET & OPPORTUNITY

2. Market & Opportunity
2.1 Why Now
2026 is the inflection point. Several converging forces create an immediate market window:

•	The UK AI Assurance Innovation Fund (£11 million) opens Spring 2026 — direct government investment in assurance infrastructure.
•	NIST released a formal Request for Information in January 2026 on agentic AI governance — a precursor to mandatory US federal contractor standards.
•	The EU AI Act is fully enforceable August 2026 — high-risk AI systems must demonstrate human oversight and audit trails.
•	The UK GDS AI Playbook is live and referenced in every public sector AI procurement decision.
•	The ICO has enforcement powers over automated decision-making and is actively watching.

Market Timing Signal
The UK AI Opportunities Action Plan One Year On (January 2026) identified governance of AI tools in production as the critical unsolved challenge in public sector AI deployment. This is the gap GovGuard AI fills.

2.2 Target Customer Segments
Segment 1 — UK Public Sector (Primary, Phase 1)
Local councils, NHS trusts, HMRC, DWP, Home Office, and government agencies deploying AI tools under the AI Exemplars programme. These organisations must demonstrate auditability, fairness, and human oversight. They have budget, regulatory exposure, and no internal tooling to solve this.

Specific UK councils deploying AI for planning, benefits, and service delivery are your first reachable customers — geographically close, technically unsophisticated about governance, and facing real ICO risk.

Segment 2 — AI Product Companies
Fintechs, HR platforms, insurance automation, and healthcare AI companies building products on LLM agents and ML models. They need governance evidence for enterprise procurement, regulatory audits, and investor due diligence.

Segment 3 — Enterprise Internal AI Teams
Large organisations deploying AI for customer support, fraud detection, recruitment screening, and marketing automation. Their legal and compliance teams want visibility and audit trails. This is a subscription monitoring sale.

2.3 Competitive Landscape & The Gap
The AI governance space has three types of existing solutions — and all three have a critical gap that GovGuard AI fills:

Component	Phase	Description
AI Safety Platforms (e.g. Credo AI, Fiddler)	Existing	Focused on model bias and fairness evaluation at training time. Do not intercept live agent decisions.
MLOps Monitoring (e.g. Weights & Biases)	Existing	Infrastructure and model performance monitoring. Not compliance or governance focused.
Manual Audit Frameworks	Existing	Spreadsheet-based governance checklists. Not automated, not real-time, not scalable.
GovGuard AI	New	Intercepts live AI decisions, scores against regulatory frameworks in real time, enforces policy. The gap no one has filled.

The Real Moat
GovGuard AI is not a dashboard or a report. It sits in the decision path — between the AI agent and the action it takes. Once organisations route decisions through GovGuard, it becomes infrastructure. Like Cloudflare for networks or Stripe for payments, removing it becomes operationally costly. That is the defensibility.
 
SECTION 3 — PRODUCT ARCHITECTURE
3. Product Architecture
3.1 Architecture Overview
GovGuard AI is built as a multi-layer governance infrastructure system. The architecture has four distinct layers, each adding value independently and compounding when combined.
EXTERNAL AI AGENT (client's system)
          │
          │  POST /scan-decision
          ▼
┌─────────────────────────────────────────────────┐
│           GOVGUARD GOVERNANCE GATEWAY           │
│              (FastAPI — Python)                 │
└───────────────────┬─────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│          LANGGRAPH ORCHESTRATOR                 │
│                                                 │
│  ┌─────────────┐  ┌──────────────────────────┐  │
│  │  INTERCEPT  │→ │   SCORING ENGINE         │  │
│  │   AGENT     │  │   (parallel agents)      │  │
│  │             │  │                          │  │
│  │ Normalises  │  │  • UK AI Playbook Agent  │  │
│  │ any input   │  │  • NIST AI RMF Agent     │  │
│  │ to standard │  │  • UAE Charter Agent     │  │
│  │ schema      │  │  (Phase 1 = UK only)     │  │
│  └─────────────┘  └──────────────┬───────────┘  │
│                                  │              │
│                    ┌─────────────▼───────────┐  │
│                    │     REPORT AGENT        │  │
│                    │  Synthesises scores →   │  │
│                    │  Risk report + action   │  │
│                    └─────────────────────────┘  │
│                                                 │
│  ┌──────────────────────────────────────────┐   │
│  │  MONITOR AGENT (scheduled — continuous) │   │
│  │  Tracks compliance trends, fires alerts │   │
│  └──────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│              SUPABASE (PostgreSQL)              │
│   Decision logs │ Audit reports │ Score history │
└─────────────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────────────┐
│           REACT DASHBOARD                       │
│  Live scores │ Alerts │ Reports │ PDF export    │
└─────────────────────────────────────────────────┘
3.2 The Four Core Agents

Agent 1 — Intercept Agent
The universal adapter. Every AI system sends decisions in a different format. The Intercept Agent uses an LLM (Ollama/Mistral running locally or self-hosted) to intelligently parse whatever payload arrives and normalise it into GovGuard's standard decision schema.

This is the intelligence layer — it handles messy real-world input so the scoring agents always receive clean, structured data. It also extracts the five governance-critical signals from any payload:
•	What decision was made (outcome, confidence, decision type)
•	Who or what was affected (individual, organisation, system)
•	How it was made (model, data sources, version)
•	Whether a human was involved (human_in_loop flag)
•	Whether it can be explained and challenged (explanation, appeal pathway, audit trail)

Agent 2 — Scoring Agents (parallel)
One scoring agent per regulatory framework, running in parallel via LangGraph. Each receives the normalised decision schema and evaluates it against its specific framework, returning a colour-coded risk score per principle.

UK AI Playbook Agent	Evaluates against GDS guidance: transparency, human oversight, accountability, explainability, fairness. This is Phase 1 — UK only.
NIST AI RMF Agent	Evaluates against the four NIST functions: Govern, Map, Measure, Manage. Relevant for US market expansion.
UAE AI Charter Agent	Evaluates against the 12 UAE Charter principles including human oversight, data privacy, transparency. Relevant for UAE market expansion.

Agent 3 — Report Agent
Receives all scoring outputs and synthesises them into a single structured audit report. Output is formatted for a civil servant, board member, or ministerial audience — plain English, not technical jargon. Report includes:
•	Executive summary with overall risk level (Green / Amber / Red / Critical)
•	Per-framework compliance scorecard
•	Specific violations flagged with the decision log entries that triggered them
•	Prioritised remediation recommendations
•	Timestamp, system name, and audit reference number

Agent 4 — Monitor Agent
Runs on a schedule (hourly or daily depending on client configuration). Pulls historical compliance scores from Supabase, detects drift over time, and fires alerts when a pattern is degrading. This is what makes the system agentic rather than a simple script — it operates autonomously without human prompting and provides continuous governance assurance.
 
SECTION 4 — SDK & INTEGRATION

4. SDK & Integration
4.1 Integration Philosophy
GovGuard AI does not replace existing AI systems. It sits next to them as a safety checkpoint. The integration must be as frictionless as possible — two lines of code in the simplest case, a webhook configuration in others.

There are three integration models, designed for different adoption contexts:

4.2 Integration Model 1 — Python SDK (Primary)
Developers install the GovGuard SDK directly into their agent codebase. This is the fastest adoption path and creates the deepest visibility — the SDK can see prompts, tool calls, reasoning chains, and decisions.

pip install govguard-sdk

Usage inside an agent:

from govguard import GovernanceCheck
 
gv = GovernanceCheck(api_key="YOUR_KEY", framework="uk_ai_playbook")
 
# Pre-decision check
result = gv.check_decision({
    "system_name": "benefits_eligibility_agent",
    "decision_type": "eligibility_assessment",
    "affected_party": "individual",
    "outcome": "denied",
    "confidence_score": 0.87,
    "human_in_loop": False,
    "explanation_provided": False,
    "appeal_pathway": False,
    "audit_trail": True,
    "model_used": "mistral-7b",
    "data_sources": ["DWP database", "HMRC feed"]
})
 
print(result.risk_score)    # 0.74
print(result.risk_level)    # "HIGH"
print(result.action)        # "REQUIRE_HUMAN_REVIEW"
print(result.violations)    # ["human_oversight_missing", "no_explanation_provided"]

4.3 Integration Model 2 — REST API
For organisations that cannot modify their agent codebase, GovGuard exposes a REST API. Decision logs are posted to the endpoint either in real time or in batches.

POST https://api.govguard.ai/v1/scan-decision
 
{
  "system_name": "hiring_agent_v2",
  "decision_type": "candidate_screening",
  "affected_party": "individual",
  "outcome": "candidate_rejected",
  "confidence_score": 0.82,
  "human_in_loop": false,
  "explanation_provided": false,
  "appeal_pathway": false
}
 
Response:
{
  "decision_id": "GVG-2026-00412",
  "risk_score": 0.71,
  "risk_level": "HIGH",
  "action": "REQUIRE_HUMAN_REVIEW",
  "violations": ["automation_without_review", "no_explanation"],
  "framework": "uk_ai_playbook",
  "report_url": "https://dashboard.govguard.ai/report/GVG-2026-00412"
}











4.4 The Standard Decision Schema
This is the normalised schema every decision is mapped to internally. Input can be messy — the Intercept Agent maps it to this structure before scoring.

decision_id	Unique reference generated by GovGuard
system_name	Name of the client AI system
department / org	Deploying organisation
timestamp	ISO 8601 datetime
decision_type	Category: eligibility, screening, triage, approval, flagging
affected_party	individual / organisation / system
outcome	What was decided
confidence_score	0.0 to 1.0 — model certainty
model_used	Model name and version
data_sources	List of data inputs used
human_in_loop	Boolean — was a human reviewer involved
explanation_provided	Boolean — was an explanation given to the affected party
appeal_pathway	Boolean — is there a mechanism to challenge the decision
audit_trail	Boolean — is the decision logged for future audit

Instant Value Demonstration
Three boolean fields — human_in_loop: false, explanation_provided: false, appeal_pathway: false — immediately trigger violations against the UK AI Playbook. A client can send one log and receive meaningful governance risk output within seconds of integration.
 
SECTION 5 — GOVERNANCE SCORING ENGINE

5. Governance Scoring Engine
5.1 UK AI Playbook Framework (Phase 1)
The UK GDS AI Playbook is the primary scoring framework for Phase 1. It represents the current standard for safe and effective AI use in UK public sector organisations. GovGuard maps every decision against these core principles:

Component	Phase	Description
Human Oversight	Phase 1	Was a human meaningfully involved in or able to review the decision?
Explainability	Phase 1	Can the decision be explained clearly to the affected individual?
Accountability	Phase 1	Is there a clear chain of responsibility for the decision?
Fairness	Phase 1	Does the decision create disproportionate impact on any group?
Transparency	Phase 1	Are data sources, model version, and decision logic recorded?
Appeal Rights	Phase 1	Does the affected party have a pathway to challenge the decision?
Audit Trail	Phase 1	Is there a complete, retrievable log of the decision?
Data Governance	Phase 1	Are data sources appropriate and consent-compliant?

5.2 Risk Scoring Logic
Each principle is evaluated as pass, partial, or fail based on the decision schema fields. A weighted composite score is calculated:

Risk Score Calculation (UK AI Playbook):
 
CRITICAL violations (score impact: 0.25 each):
  → human_in_loop = false           (automation without oversight)
  → appeal_pathway = false          (no right to challenge)
 
HIGH violations (score impact: 0.15 each):
  → explanation_provided = false    (transparency failure)
  → audit_trail = false             (no accountability record)
 
MEDIUM violations (score impact: 0.10 each):
  → confidence_score > 0.95         (over-reliance on automation)
  → sensitive_data_used = true      (privacy risk flag)
 
LOW violations (score impact: 0.05 each):
  → model_version not recorded      (traceability gap)
  → data_sources incomplete         (provenance gap)
 
Final Risk Score: sum of violation impacts (0.0 = clean, 1.0 = critical)
 
Risk Level:
  0.00 - 0.20  →  GREEN   (compliant)
  0.21 - 0.40  →  AMBER   (review recommended)
  0.41 - 0.65  →  HIGH    (human review required)
  0.66 - 1.00  →  CRITICAL (block / escalate)

5.3 Action Responses
Every scan returns one of four action responses:

ALLOW	Decision meets governance standards. Logged for audit. No intervention required.
LOG_FOR_AUDIT	Decision passes but has minor gaps. Logged with recommendations. No blocking.
REQUIRE_HUMAN_REVIEW	Decision has HIGH risk. System flags for human reviewer before action executes.
BLOCK_ACTION	Decision has CRITICAL violations. Action is halted. Escalation triggered.

5.4 Sample Audit Report Output

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GOVGUARD AI — GOVERNANCE AUDIT REPORT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Report ID:       GVG-2026-00412
System:          Benefits Eligibility Agent v2
Department:      DWP / Manchester Council
Decision Type:   Eligibility Assessment
Timestamp:       2026-03-05T09:32:00Z
Framework:       UK AI Playbook (GDS 2025)
 
OVERALL RISK LEVEL:  ██ HIGH (Score: 0.65)
ACTION REQUIRED:     REQUIRE HUMAN REVIEW
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPLIANCE SCORECARD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ PASS    Audit Trail Present
✅ PASS    Model Version Recorded
⚠️  FAIL   Human Oversight Missing        [CRITICAL]
⚠️  FAIL   No Explanation Provided        [HIGH]
⚠️  FAIL   No Appeal Pathway              [CRITICAL]
⚠️  WARN   High Confidence Score (0.87)   [MEDIUM]
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
VIOLATIONS DETAIL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Human oversight missing
   The decision was made fully autonomously with no
   human reviewer involved. UK AI Playbook Section 4.2
   requires meaningful human oversight for decisions
   affecting individuals' access to public services.
 
2. No explanation provided to affected party
   The individual received a rejection with no
   explanation of the reasoning. ICO guidance under
   UK GDPR Article 22 requires meaningful information
   about automated decisions.
 
3. No appeal pathway communicated
   No mechanism was provided for the individual to
   challenge the decision. This creates legal exposure
   under administrative law principles.
 
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
RECOMMENDED ACTIONS (Priority Order)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
[1] IMMEDIATE: Route this decision to a human reviewer
    before communicating outcome to applicant.
[2] SHORT-TERM: Add explanation generation to the
    agent output pipeline.
[3] SHORT-TERM: Implement and communicate appeal
    pathway in all decision communications.
[4] ONGOING: Configure human-in-loop threshold for
    decisions with confidence score above 0.80.
 
SECTION 6 — TECHNOLOGY STACK

6. Technology Stack
6.1 Stack Principles
The GovGuard stack is built on three non-negotiable principles:
•	Fully open source — no vendor lock-in, no black boxes, full auditability of the governance tool itself
•	Self-hostable — decision data never needs to leave the client's environment, critical for government and enterprise adoption
•	Transparent by design — every agent decision and scoring step is logged and explainable
6.2 Core Stack
Component	Phase	Description
LangGraph	Orchestration	Multi-agent workflow orchestration. Explicit state management — every node, edge, and transition is visible and auditable. Chosen over CrewAI because governance infrastructure cannot rely on abstracted black box agent behaviour.
Ollama + Mistral 7B	LLM Runtime	Open source LLMs running locally or self-hosted. No API keys. No data sent to third parties. Decision data stays on-premises. Critical for government and regulated industry clients.
FastAPI (Python)	API Gateway	High-performance REST API layer. Handles incoming decision payloads, routes to LangGraph, returns governance responses.
Supabase (PostgreSQL)	Data Layer	Open source Postgres-backed database. Stores all decision logs, audit reports, compliance scores, and trend data. Self-hostable.
Docker + Docker Compose	Deployment	Full stack containerisation. One command deployment. Clients can run entirely on-premises with zero cloud dependency.
React + Tailwind	Dashboard	Clean, minimal governance dashboard. Upload logs, view live compliance scores, receive alerts, download PDF audit reports.
6.3 Why Not Claude or OpenAI APIs
A deliberate and important architectural decision. GovGuard is selling governance and trust. Routing client AI decision data through a third-party LLM API would:
•	Create a data privacy risk for clients (especially government and healthcare)
•	Introduce vendor dependency in the governance layer itself
•	Undermine the credibility of a governance tool that relies on unauditable external services

Ollama with Mistral 7B or LLaMA 3 runs entirely on-premises or in a client-controlled cloud environment. This is a selling point, not a limitation.
 
SECTION 7 — BUILD ROADMAP

7. Build Roadmap
7.1 Phase 1 — UK MVP (Weeks 1–8)
The goal of Phase 1 is one working, demonstrable prototype: a governance gateway that accepts a UK public sector AI decision log, scores it against the UK AI Playbook, and returns a structured audit report. This is the proof of concept for the AI Assurance Innovation Fund application and the primary CV artefact.

Week 1–2: Foundation
•	Set up project repository (GitHub, open source MIT licence)
•	FastAPI service scaffold with /scan-decision endpoint
•	Intercept Agent — normalises any JSON input to standard decision schema
•	Ollama setup with Mistral 7B for local LLM inference
•	Basic Supabase schema: decisions table, audit_reports table

Week 3–4: UK Scoring Engine
•	UK AI Playbook scoring agent — 8 principle evaluations
•	Risk score calculation logic
•	ALLOW / FLAG / REQUIRE_HUMAN_REVIEW / BLOCK action responses
•	LangGraph orchestration connecting Intercept → Scoring → Report agents

Week 5: Report Agent
•	Structured audit report generation in plain English
•	PDF export of compliance report
•	Supabase persistence of all decision logs and reports

Week 6: Monitor Agent
•	Scheduled compliance trend tracking
•	Drift detection — alert when compliance score degrades over time
•	Email / webhook alert system

Week 7–8: Dashboard & SDK
•	React dashboard — upload logs, live scorecard, alert feed, report download
•	Python SDK — pip install govguard-sdk with two-line integration
•	Documentation, README, and GitHub publish
•	Demo video for AI Assurance Innovation Fund application

Phase 1 Milestone
A working governance scanner that a UK council or NHS trust can integrate in under 30 minutes, immediately receive governance risk scores on their AI decisions, and download a compliance report formatted for board-level review.

7.2 Phase 2 — Live Monitoring Platform (Months 3–6)
•	Streaming decision log ingestion (real-time rather than batch)
•	Policy engine — clients define custom governance rules and thresholds
•	Multi-tenant platform — each client has isolated data environment
•	Subscription billing integration
•	Enterprise SSO and role-based access control
•	Webhook integrations with Slack, Teams, PagerDuty for alerts
•	First paying customers — target 3 UK councils or NHS trusts

7.3 Phase 3 — Agent Chain Governance (Months 6–12)
Agentic systems introduce a new governance challenge: multi-step reasoning chains where one agent calls another, calls a tool, accesses external data, and then executes an action. Each step carries governance risk. Phase 3 introduces chain-level governance:

Agent Chain Governance — Example:
 
Customer Service Agent
Step 1: Read customer email           → logged
Step 2: Access account database       → logged + data sensitivity check
Step 3: Evaluate refund eligibility   → governance scan
Step 4: Trigger payment action        → pre-decision check → ALLOW/BLOCK
 
Chain Risk Score: aggregate of all step scores
Chain Audit Trail: complete end-to-end decision provenance

•	Agent action-space monitoring — what tools and APIs the agent can access
•	Tool permission controls — restrict which tools require human approval
•	Chain-of-custody audit trail — complete provenance from input to action
•	Agent registry — catalogue of all deployed agents with governance profiles

7.4 Phase 4 — Agent Runtime Controller (Year 2+)
The long-term infrastructure vision. GovGuard becomes the Kubernetes of AI agent governance — not just monitoring agents but controlling how they operate at runtime:
•	Define what data agents can access
•	Set risk thresholds per agent and per decision type
•	Enforce human approval gates for high-risk actions
•	Manage agent credentials and tool permissions
•	Deploy governance policies across entire agent fleets

The Infrastructure Moat
When organisations rely on GovGuard to control agent behaviour in production, removing it becomes operationally impossible. This is the same dynamic that made Kubernetes, Cloudflare, and HashiCorp Vault infrastructure companies rather than tools.
 
SECTION 8 — GLOBAL EXPANSION ROADMAP

8. Global Expansion Roadmap
8.1 Expansion Philosophy
Start deep, not wide. UK first, done properly. Then expand jurisdiction by jurisdiction, each time adding the relevant regulatory framework as a new scoring agent. The architecture is designed for this — adding a new framework means adding one new scoring agent and a new set of framework principles. The rest of the system is unchanged.

8.2 UAE Expansion (Phase 2 — Months 4–8)
The UAE is the second target jurisdiction for three strategic reasons: the UAE AI Strategy 2031 positions the country as a global AI governance leader; the UAE Charter for the Development and Use of AI (2024) provides a clear 12-principle framework to score against; and Dubai's World Government Summit and AI governance ambitions create direct government-level entry points.

UAE AI Charter — 12 principles GovGuard will score against:
•	Human-machine relationship strengthening
•	Safety and reliability
•	Algorithmic bias mitigation
•	Data privacy protection
•	Transparency of AI systems
•	Human oversight mechanisms
•	Governance and accountability
•	Technological excellence
•	Human commitment and control
•	Peaceful coexistence with AI
•	Inclusive access
•	Compliance with applicable laws

UAE positioning: GovGuard becomes the governance layer for AI systems deployed across UAE federal government and Dubai Smart Government initiatives — with a direct pitch to the UAE Ministry of State for Artificial Intelligence.

8.3 US Expansion (Phase 3 — Months 8–14)
The US market entry point is federal contractors and regulated industries (finance, healthcare, insurance). NIST released a formal RFI in January 2026 on agentic AI governance — a direct signal that NIST AI RMF compliance will become mandatory for federal contractors. GovGuard adds the NIST AI RMF scoring agent to cover the US market.

NIST AI RMF — four functions GovGuard scores against:
GOVERN	Organisational policies, accountability structures, and culture for AI risk management
MAP	AI system context understanding — intended purpose, stakeholders, risk categories
MEASURE	Risk and impact quantification — metrics, testing, bias evaluation
MANAGE	Risk response and monitoring — controls, remediation, ongoing oversight

US positioning: GovGuard becomes the NIST AI RMF compliance layer for AI systems deployed by federal agencies and contractors — with a direct pitch aligned to the January 2026 NIST RFI on agentic AI.

8.4 EU Expansion (Phase 4 — Year 2)
EU AI Act becomes fully enforceable August 2026. High-risk AI systems — those affecting fundamental rights, safety, employment, education, and public services — must demonstrate human oversight, audit trails, and conformity assessments. GovGuard adds an EU AI Act scoring agent covering:
•	Risk classification scoring (minimal / limited / high / unacceptable)
•	Conformity assessment documentation generation
•	Transparency obligation verification
•	Human oversight mandate compliance

EU positioning: GovGuard becomes the EU AI Act compliance layer for any organisation operating in or serving EU markets — positioning as the tool that closes the gap between deployment and the August 2026 enforcement deadline.

8.5 Multi-Jurisdiction Scoring (Phase 4+)
For multinational organisations operating across UK, UAE, US, and EU, GovGuard runs all four framework scoring agents simultaneously on every decision. The output is a single composite report with jurisdiction-by-jurisdiction compliance status — the world's only multi-framework AI governance scanner.

Multi-Jurisdiction Report Example:
 
Decision: Candidate screening — Rejected
System: AI Hiring Agent v3
 
┌─────────────────────┬───────────┬────────────────────────┐
│ Framework           │ Score     │ Status                 │
├─────────────────────┼───────────┼────────────────────────┤
│ UK AI Playbook      │ 0.65      │ ⚠️  HIGH — Review      │
│ NIST AI RMF         │ 0.58      │ ⚠️  HIGH — Review      │
│ UAE AI Charter      │ 0.72      │ 🔴 CRITICAL — Block    │
│ EU AI Act           │ 0.81      │ 🔴 CRITICAL — Block    │
├─────────────────────┼───────────┼────────────────────────┤
│ COMPOSITE           │ 0.69      │ 🔴 CRITICAL            │
└─────────────────────┴───────────┴────────────────────────┘
 
Action: BLOCK — Human review required before outcome communicated.
Primary violation: Automated decision on employment affecting
individual rights without human oversight (EU AI Act Article 14).
 
SECTION 9 — BUSINESS MODEL & REVENUE

9. Business Model & Revenue
9.1 Open Source + Commercial Service
The GovGuard governance engine and UK AI Playbook scoring framework are published open source on GitHub under an MIT licence. This is a deliberate strategic choice, not a limitation. Open source builds credibility, attracts enterprise trust (especially government), grows the contributor community, and creates the strongest possible CV and proof of concept artefact.

Revenue is generated from the hosted service, enterprise features, and professional services — not from the core technology. This is the same model used by HashiCorp (Terraform), Elastic, Supabase, and Sentry.

9.2 Revenue Tiers

Component	Phase	Description
Free / Open Source	Phase 1	Core SDK + UK AI Playbook scoring engine on GitHub. Self-hosted. No limits. Designed to drive adoption and build credibility.
Starter (£299/month)	Phase 2	Hosted platform. Up to 10,000 decisions/month. Dashboard. PDF reports. Email alerts. Single framework.
Professional (£999/month)	Phase 2-3	Up to 100,000 decisions/month. All frameworks. Custom policy rules. API access. Priority support.
Enterprise (custom)	Phase 3+	Unlimited decisions. On-premises deployment. SLA guarantees. Dedicated support. Custom framework integration. Audit sign-off service.
Government Contract	Phase 2+	Direct contract with public sector bodies. Integration support. Compliance reporting service. AI Assurance Innovation Fund aligned.

9.3 The AI Assurance Innovation Fund Opportunity
The UK Government's £11 million AI Assurance Innovation Fund opens for applications in Spring 2026. GovGuard AI is directly aligned with its stated objectives: building a domestic market for trusted AI assurance services and creating standards for testing, verification, and validation of AI systems.

The fund application is strengthened by: open source publication of the framework, demonstrable UK public sector use cases, multi-framework coverage, and a solo-founder technical proof of concept with clear commercial viability.
 
