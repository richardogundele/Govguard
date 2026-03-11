## GovGuard AI – AI Decision Governance Infrastructure

GovGuard AI is an **AI Decision Governance Infrastructure** platform. It acts as a **governance gateway** that sits between AI agents and the real world, intercepting their decisions, scoring governance risk, and returning **ALLOW / REVIEW / BLOCK** style actions before those decisions are applied to real people.

This repository contains the **open source core** of GovGuard:

- A **Python governance engine** that implements the UK GDS **AI Playbook** scoring rules.
- A **FastAPI HTTP gateway** exposing a `/scan-decision` endpoint.
- An **Intercept Agent** that normalises messy decision payloads into a standard schema.
- A small **Python SDK** (`GovernanceCheck`) that makes it easy for other projects to integrate.

For full product and architecture details, see `docs/gov-guard-ai-spec.md`.

## Architecture (current MVP scope)

At this early MVP stage the system focuses on the **UK AI Playbook** use case:

- **Engine (`engine/`)**
  - `Decision` dataclass describing the standard decision schema (who, what, when, how, governance flags).
  - `score_uk_ai_playbook(decision)` function that applies weighted rules from the spec and returns:
    - `risk_score` \[0.0–1.0\]
    - `risk_level` (`GREEN | AMBER | HIGH | CRITICAL`)
    - `action` (`ALLOW | LOG_FOR_AUDIT | REQUIRE_HUMAN_REVIEW | BLOCK_ACTION`)
    - list of violation codes.
- **Intercept Agent (`agents/intercept.py`)**
  - Accepts raw JSON decision logs with varying key names.
  - Normalises them into the `Decision` schema (handles aliases like `result` → `outcome`, `user_type` → `affected_party`, etc.).
- **API Gateway (`api/main.py`)**
  - FastAPI app exposing `POST /scan-decision`.
  - Receives raw JSON, passes it through the Intercept Agent, and invokes the scoring engine.
- **Python SDK (`sdk/`)**
  - `GovernanceCheck` client wraps HTTP calls to `/scan-decision`.
  - Returns a typed `GovernanceResult` object instead of raw dictionaries.

The stack is intentionally simple and fully open source: **Python, FastAPI, requests**, with no external LLM APIs. LangGraph, Supabase/Postgres, React dashboard, and multi‑framework scoring will be layered on next, as described in the spec.

## Quick start – run the local gateway

### 1. Start the FastAPI service

- Create and activate a Python environment.
- Install FastAPI and Uvicorn, along with any other dependencies defined in the project.
- From the project root (`AgenGov`), run the Uvicorn server, pointing at the `app` object in `api/main.py`.

After the server starts, it will listen on `http://127.0.0.1:8000` by default.

### 2. Send a sample decision via HTTP

You can use any HTTP client (curl, Postman, Thunder Client, etc.) to call `POST /scan-decision`.

Example JSON body that matches the **DWP benefits eligibility** decision in the spec:

```json
{
  "system_name": "Benefits Eligibility Checker v2",
  "department": "DWP",
  "timestamp": "2026-03-05T09:32:00Z",
  "decision_type": "eligibility_assessment",
  "affected_party": "individual",
  "outcome": "denied",
  "confidence_score": 0.87,
  "model_used": "mistral-7b-v2.1",
  "data_sources": ["HMRC feed", "UC database"],
  "human_in_loop": false,
  "explanation_provided": false,
  "appeal_pathway": false,
  "audit_trail": true,
  "sensitive_data_used": false,
  "model_version_recorded": true,
  "data_sources_complete": true
}
```

You should receive a response similar to:

```json
{
  "risk_score": 0.65,
  "risk_level": "HIGH",
  "action": "REQUIRE_HUMAN_REVIEW",
  "violations": [
    "human_oversight_missing",
    "no_appeal_pathway",
    "no_explanation_provided"
  ],
  "framework": "uk_ai_playbook"
}
```

## Quick start – use the Python SDK

The SDK is designed to make GovGuard feel like a **simple library call** from inside any Python agent.

Example usage (assuming `govguard` is installed and points at this SDK):

```python
from govguard import GovernanceCheck

# Create a client pointing at your GovGuard API gateway
gv = GovernanceCheck(
    api_key="dev-key-123",                 # optional for now (no auth enforced yet)
    base_url="http://127.0.0.1:8000",      # where your FastAPI service is running
    framework="uk_ai_playbook",            # default framework
)

# Describe a decision in a simple dictionary
decision_payload = {
    "system_name": "Benefits Eligibility Checker v2",
    "decision_type": "eligibility_assessment",
    "affected_party": "individual",
    "outcome": "denied",
    "confidence_score": 0.87,
    "human_in_loop": False,
    "explanation_provided": False,
    "appeal_pathway": False,
    "audit_trail": True,
}

# Send the decision to GovGuard for scoring
result = gv.check_decision(decision_payload)

print("Risk score:", result.risk_score)
print("Risk level:", result.risk_level)
print("Action:", result.action)
print("Violations:", result.violations)
```

The SDK will handle:

- Building the HTTP request to `/scan-decision`.
- Passing any messy keys through the Intercept Agent in the backend.
- Parsing the JSON response into a structured `GovernanceResult`.

## Roadmap (from the spec)

Planned next steps that will be added to this repository over time:

- **Persistence with Supabase/Postgres** – store all decisions, scores, and audit reports.
- **LangGraph orchestration** – implement the four-agent architecture:
  - Intercept Agent → Scoring Agents (per framework) → Report Agent → Monitor Agent.
- **Report Agent** – generate structured, plain‑English audit reports and PDF exports.
- **Monitor Agent** – scheduled trend tracking and drift alerts over time.
- **React + Tailwind dashboard** – upload logs, view live scores, download reports.
- **Additional frameworks** – UAE AI Charter, NIST AI RMF, EU AI Act as parallel scoring agents.

## License

This project is licensed under the **MIT License**. See the `LICENSE` file for details.

