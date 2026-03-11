# examples/demo_cli.py
# This script demonstrates how to use the GovGuard Python SDK
# to send a sample decision to the local API gateway and print
# the governance scoring result.
#
# Before running:
# 1. Start the FastAPI server (py -m uvicorn api.main:app --reload).
# 2. Ensure GOVGUARD_DATABASE_URL is set (for persistence).
# 3. Run this script: py examples/demo_cli.py

import sys
import os

# Add project root to path so we can import from sdk/
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sdk.governance_check import GovernanceCheck


def main() -> None:
    """
    Demonstrate basic SDK usage:
    1. Create a GovernanceCheck client pointing at the local API.
    2. Build a sample decision payload (the DWP example from the spec).
    3. Call check_decision() and print the result.
    """

    # Create the SDK client.
    # api_key is optional (no auth enforced yet).
    # base_url should match where your FastAPI server is running.
    gv = GovernanceCheck(
        api_key=None,
        base_url="http://127.0.0.1:8000",
        framework="uk_ai_playbook",
    )

    # Build a sample decision payload matching the spec's DWP example.
    decision_payload = {
        "system_name": "Benefits Eligibility Checker v2",
        "department": "DWP",
        "timestamp": "2026-03-05T09:32:00Z",
        "decision_type": "eligibility_assessment",
        "affected_party": "individual",
        "outcome": "denied",
        "confidence_score": 0.87,
        "model_used": "mistral-7b-v2.1",
        "data_sources": ["HMRC feed", "UC database"],
        "human_in_loop": False,
        "explanation_provided": False,
        "appeal_pathway": False,
        "audit_trail": True,
    }

    print("Sending decision to GovGuard API...")
    print()

    # Call the SDK method to check the decision.
    result = gv.check_decision(decision_payload)

    # Print the governance result.
    print("=== GovGuard Governance Result ===")
    print(f"Risk score:  {result.risk_score}")
    print(f"Risk level:  {result.risk_level}")
    print(f"Action:      {result.action}")
    print(f"Framework:   {result.framework}")
    print(f"Violations:  {result.violations}")
    print()

    # Quick pass/fail check for expected values.
    if result.risk_level == "HIGH" and result.action == "REQUIRE_HUMAN_REVIEW":
        print("[OK] Result matches expected UK AI Playbook scoring.")
    else:
        print("[WARN] Result differs from expected values – review scoring logic.")


if __name__ == "__main__":
    main()
