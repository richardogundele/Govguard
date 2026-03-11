# This file implements the public GovGuard Python SDK interface.
# It wraps HTTP calls to the GovGuard API so that client code can
# simply call GovernanceCheck.check_decision(...) with a Python dict
# and receive a strongly-typed GovernanceResult object back.

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


@dataclass
class GovernanceResult:
    """
    Represents the result of a governance check returned by GovGuard.

    Fields:
      - risk_score: numeric risk score between 0.0 and 1.0
      - risk_level: textual band, e.g. "GREEN", "AMBER", "HIGH", "CRITICAL"
      - action: recommended action, e.g. "ALLOW", "REQUIRE_HUMAN_REVIEW"
      - violations: list of violation codes that explain the risk
      - framework: name of the framework used, e.g. "uk_ai_playbook"
    """
    risk_score: float
    risk_level: str
    action: str
    violations: List[str]
    framework: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GovernanceResult":
        """
        Helper constructor to build a GovernanceResult from a JSON dictionary.
        This is used by the SDK after receiving the API response.
        """
        return cls(
            risk_score=float(data.get("risk_score", 0.0)),
            risk_level=str(data.get("risk_level", "")),
            action=str(data.get("action", "")),
            violations=list(data.get("violations", [])),
            framework=str(data.get("framework", "")),
        )


class GovernanceCheck:
    """
    Main GovGuard SDK client.

    Typical usage:

        from govguard import GovernanceCheck

        gv = GovernanceCheck(
            api_key="YOUR_KEY",  # optional for now
            base_url="http://127.0.0.1:8000",  # GovGuard API URL
            framework="uk_ai_playbook",
        )

        result = gv.check_decision({
            "system_name": "benefits_eligibility_agent",
            "decision_type": "eligibility_assessment",
            "outcome": "denied",
            ...
        })

        print(result.risk_score, result.risk_level, result.action)

    For now, api_key is not enforced by the backend, but we accept it
    so the interface is future-proof when you add auth.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: str = "http://127.0.0.1:8000",
        framework: str = "uk_ai_playbook",
        timeout_seconds: float = 10.0,
    ) -> None:
        """
        Initialise the SDK client.

        - api_key: optional API key for auth (future use).
        - base_url: base URL of the GovGuard API (local or hosted).
        - framework: default framework to use (currently uk_ai_playbook).
        - timeout_seconds: HTTP timeout for requests.
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")  # normalise trailing slash
        self.framework = framework
        self.timeout_seconds = timeout_seconds

    @property
    def _scan_decision_url(self) -> str:
        """
        Build the full URL for the /scan-decision endpoint.
        """
        return f"{self.base_url}/scan-decision"

    def check_decision(self, decision: Dict[str, Any]) -> GovernanceResult:
        """
        Public method used by client code to submit a decision for governance scanning.

        Parameters:
          - decision: a dictionary describing the decision. It can be:
              * Already in GovGuard's standard schema, OR
              * A slightly messy / aliased structure.
            The backend Intercept Agent will normalise it.

        Returns:
          - A GovernanceResult instance containing risk_score, risk_level,
            action, violations, and framework.

        Raises:
          - requests.RequestException if the HTTP request fails.
          - ValueError if the response is not in the expected format.
        """
        # Prepare headers. We include an API key header for future auth,
        # but the backend can ignore it for now.
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        # Optionally attach framework information so, in the future,
        # the backend can route to different scoring agents.
        payload = dict(decision)  # shallow copy so we don't mutate caller data
        payload.setdefault("framework", self.framework)

        # Send the HTTP POST request to the GovGuard API.
        response = requests.post(
            self._scan_decision_url,
            json=payload,
            headers=headers,
            timeout=self.timeout_seconds,
        )

        # Raise for obvious HTTP errors (4xx, 5xx) so callers can handle them.
        response.raise_for_status()

        data = response.json()

        # Validate minimal expected structure.
        if not isinstance(data, dict) or "risk_score" not in data:
            raise ValueError(f"Unexpected response from GovGuard API: {data}")

        # Convert the raw dict into a GovernanceResult for nicer usage.
        return GovernanceResult.from_dict(data)