# This file exposes the core GovGuard engine over HTTP using FastAPI.
# It implements the /scan-decision endpoint described in the spec.
#
# Flow:
#   HTTP POST /scan-decision  →  InterceptAgent normalises raw JSON → Decision → score_uk_ai_playbook → JSON response

from fastapi import FastAPI, Body
from typing import Dict, Any

from engine.core import Decision, score_uk_ai_playbook
from agents.intercept import InterceptAgent

# Create the FastAPI app instance. This is the HTTP server object.
app = FastAPI(title="GovGuard AI – UK MVP API")

interceptor = InterceptAgent()

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

    # Step 2: run the governance scoring engine on the normalised Decision
    result = score_uk_ai_playbook(decision)

    # Step 3: return the result as JSON response
    return result