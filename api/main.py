# This file exposes the core GovGuard engine over HTTP using FastAPI.
# It implements the /scan-decision endpoint described in the spec.
#
# Flow:
#   HTTP POST /scan-decision  →  InterceptAgent normalises raw JSON → Decision → score_uk_ai_playbook → JSON response

from fastapi import FastAPI, Body
from typing import Dict, Any

from engine.core import Decision, score_uk_ai_playbook
from agents.intercept import InterceptAgent
from persistence.db import init_db, store_decision

# Create the FastAPI app instance. This is the HTTP server object.
app = FastAPI(title="GovGuard AI – UK MVP API")

# Single InterceptAgent instance reused across requests.
interceptor = InterceptAgent()


@app.on_event("startup")
def on_startup() -> None:
    """
    FastAPI startup hook.

    This runs once when the application starts and:
    - Ensures the database schema is created (decisions table).
    """
    init_db()


@app.post("/scan-decision")
def scan_decision(payload: Dict[str, Any] = Body(...)):
    """
    Main API endpoint for Phase 1, now using the Intercept Agent.

    1. Receive a raw decision log as JSON (any key names, minimal validation).
    2. Let the InterceptAgent normalise that raw dictionary into a Decision object.
    3. Call the UK AI Playbook scoring function.
    4. Return the scoring result as JSON.
    """

    # Step 1: pass the raw dictionary through the Intercept Agent so it can
    #         handle alias keys and map everything into the Decision schema.
    decision: Decision = interceptor.normalise(payload)

    # Step 2: run the governance scoring engine on the normalised Decision.
    result = score_uk_ai_playbook(decision)

    # Step 3: persist the decision and scoring result in Postgres so that
    #         the Monitor Agent and dashboard can use this data later.
    decision_id = store_decision(
        decision=decision,
        scoring_result=result,
        raw_payload=payload,
    )

    # Step 4: return the scoring result, now enriched with the decision_id.
    return {
        "decision_id": decision_id,
        **result,
    }