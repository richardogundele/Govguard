# This demo script shows how to use the core GovGuard engine
# to score a single decision against the UK AI Playbook.
# It uses the sample decision from Section 12.3 of your spec.

from engine.core import Decision, score_uk_ai_playbook

def build_sample_decision() -> Decision:
    """
    Build a Decision object from the sample JSON in the spec.

    This mirrors the example:

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
      "audit_trail": true
    }
    """

    # We construct the Decision dataclass using keyword arguments that
    # match the field names defined in engine.core.Decision.
    return Decision(
        system_name="Benefits Eligibility Checker v2",
        department="DWP",
        timestamp="2026-03-05T09:32:00Z",
        decision_type="eligibility_assessment",
        affected_party="individual",
        outcome="denied",
        confidence_score=0.87,
        model_used="mistral-7b-v2.1",
        data_sources=["HMRC feed", "UC database"],
        human_in_loop=False,
        explanation_provided=False,
        appeal_pathway=False,
        audit_trail=True,
        # For now we assume:
        # - no obviously sensitive data flag set
        # - model version is recorded
        # - data sources list is complete
        sensitive_data_used=False,
        model_version_recorded=True,
        data_sources_complete=True,
    )


def main() -> None:
    """
    Entry point for the demo.

    1. Build the sample Decision.
    2. Score it against the UK AI Playbook.
    3. Print the result so you can compare it with the expected output
       in Section 12.3 of the spec.
    """

    # Step 1: build the Decision object from the sample log
    decision = build_sample_decision()

    # Step 2: call the scoring function to evaluate governance risk
    result = score_uk_ai_playbook(decision)

    # Step 3: print the result so you can inspect score, level, action, violations
    print("GovGuard UK AI Playbook scoring result:")
    print(result)


if __name__ == "__main__":
    # This ensures main() only runs when you execute this file directly,
    # and not when it is imported from somewhere else.
    main()