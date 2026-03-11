# examples/messy_payload.py
# This script demonstrates how the Intercept Agent handles "messy" payloads
# with aliased key names. Instead of the standard field names, we use
# alternatives like "result" instead of "outcome", "user_type" instead of
# "affected_party", etc.
#
# The Intercept Agent should normalise these into the standard Decision
# schema, and the scoring should still work correctly.
#
# Before running:
# 1. Start the FastAPI server (py -m uvicorn api.main:app --reload).
# 2. Ensure GOVGUARD_DATABASE_URL is set (for persistence).
# 3. Run this script: py examples/messy_payload.py

import sys
import os

# Add project root to path so we can import from sdk/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdk.governance_check import GovernanceCheck


def main() -> None:
    """
    Demonstrate that the Intercept Agent handles aliased field names:
    - "system" instead of "system_name"
    - "org" instead of "department"
    - "type" instead of "decision_type"
    - "user_type" instead of "affected_party"
    - "result" instead of "outcome"
    - "score" instead of "confidence_score"
    - "model_name" instead of "model_used"
    - "sources" instead of "data_sources"
    - "human_reviewed" instead of "human_in_loop"
    - "has_explanation" instead of "explanation_provided"
    - "can_appeal" instead of "appeal_pathway"
    - "logged" instead of "audit_trail"
    """

    gv = GovernanceCheck(
        api_key=None,
        base_url="http://127.0.0.1:8000",
        framework="uk_ai_playbook",
    )

    # Build a "messy" payload using alias keys.
    messy_payload = {
        "system": "Benefits Eligibility Checker v2",
        "org": "DWP",
        "decision_time": "2026-03-05T09:32:00Z",
        "type": "eligibility_assessment",
        "user_type": "individual",
        "result": "denied",
        "score": 0.87,
        "model_name": "mistral-7b-v2.1",
        "sources": ["HMRC feed", "UC database"],
        "human_reviewed": False,
        "has_explanation": False,
        "can_appeal": False,
        "logged": True,
    }

    print("Sending MESSY payload (aliased keys) to GovGuard API...")
    print()

    result = gv.check_decision(messy_payload)

    print("=== GovGuard Governance Result ===")
    print(f"Risk score:  {result.risk_score}")
    print(f"Risk level:  {result.risk_level}")
    print(f"Action:      {result.action}")
    print(f"Framework:   {result.framework}")
    print(f"Violations:  {result.violations}")
    print()

    # Check that the result is the same as for the "clean" payload.
    if result.risk_level == "HIGH" and result.action == "REQUIRE_HUMAN_REVIEW":
        print("[OK] Intercept Agent correctly normalised the messy payload.")
    else:
        print("[WARN] Result differs – check Intercept Agent alias mappings.")


if __name__ == "__main__":
    main()
