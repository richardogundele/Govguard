# This file contains the "Intercept Agent" for GovGuard.
# Its job is to take any incoming raw payload (possibly messy, with different
# field names or structure) and convert it into the clean Decision dataclass
# used by the scoring engine.
#
# In this first version, we handle:
# - Payloads that already match the Decision schema (pass-through).
# - Simple aliases like "user_type" → "affected_party" or "result" → "outcome".
#
# Later, this agent can become more intelligent:
# - Use an LLM (via Ollama + Mistral) to interpret arbitrary logs.
# - Extract missing fields from free-text explanations, etc.

from typing import Any, Dict, List, Optional

from engine.core import Decision


class InterceptAgent:
    """
    InterceptAgent is responsible for:
      1. Accepting a raw decision payload (dictionary from JSON).
      2. Normalising the keys and values into GovGuard's standard Decision schema.
      3. Returning a Decision object that the scoring engine can understand.

    This keeps the "brain" (scoring) separate from the "ears" (input formats).
    """

    def __init__(self) -> None:
        """
        For now, the InterceptAgent has no configuration.
        In the future, we could pass:
          - organisation-specific mappings,
          - framework preferences,
          - or model/config handles for LLM-based interpretation.
        """
        pass

    def _get_bool(self, data: Dict[str, Any], keys: List[str], default: bool = False) -> bool:
        """
        Helper method to safely extract boolean values.

        - 'data' is the original payload.
        - 'keys' is a list of possible key names (aliases) we will check.
        - 'default' is the value we return if nothing is found.

        We:
          - Look through each key name in order.
          - If found, try to interpret its value as a boolean.
        """
        for key in keys:
            if key in data:
                value = data[key]
                # If it's already a bool, just return it.
                if isinstance(value, bool):
                    return value
                # Strings like "true"/"false" (case-insensitive).
                if isinstance(value, str):
                    lowered = value.strip().lower()
                    if lowered in ("true", "yes", "1"):
                        return True
                    if lowered in ("false", "no", "0"):
                        return False
        return default

    def _get_float(self, data: Dict[str, Any], keys: List[str], default: float = 0.0) -> float:
        """
        Helper method to safely extract float values.

        - Tries each key in order.
        - Attempts to convert numeric or string values into a float.
        """
        for key in keys:
            if key in data:
                value = data[key]
                try:
                    return float(value)
                except (TypeError, ValueError):
                    # If conversion fails, we just continue to the next key.
                    continue
        return default

    def _get_str(self, data: Dict[str, Any], keys: List[str], default: str = "") -> str:
        """
        Helper method to safely extract string values.

        - Returns the first key that exists and is not None.
        - Converts non-string values to strings when reasonable.
        """
        for key in keys:
            if key in data and data[key] is not None:
                value = data[key]
                # If already a string, return as is.
                if isinstance(value, str):
                    return value
                # Otherwise, convert basic types to string.
                return str(value)
        return default

    def _get_list_str(
        self,
        data: Dict[str, Any],
        keys: List[str],
        default: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Helper to extract a list of strings, handling a few common patterns:

        - The payload already provides a list of strings.
        - The payload provides a single string (we wrap it in a list).
        - If nothing is found, we return an empty list or the provided default.
        """
        if default is None:
            default = []

        for key in keys:
            if key in data:
                value = data[key]
                # If it's already a list, we try to cast each item to string.
                if isinstance(value, list):
                    return [str(item) for item in value]
                # If it's a single string, wrap it in a list.
                if isinstance(value, str):
                    return [value]
        return default

    def normalise(self, raw: Dict[str, Any]) -> Decision:
        """
        Main entry point for the Intercept Agent.

        - 'raw' is the original JSON payload from the client.
        - We use helper methods to map various possible key names to the
          Decision fields defined in engine.core.Decision.

        This version is deliberately simple:
          - It assumes a flat dictionary structure.
          - It handles a few common alias names for fields.

        Later versions can:
          - Traverse nested structures,
          - Use an LLM to interpret free-text,
          - Apply organisation-specific mappings.
        """

        # System and context fields
        system_name = self._get_str(raw, ["system_name", "system", "app_name"])
        department = self._get_str(raw, ["department", "org", "organisation"], default=None)
        timestamp = self._get_str(raw, ["timestamp", "time", "decision_time"], default=None)

        decision_type = self._get_str(
            raw,
            ["decision_type", "type", "category"],
        )

        affected_party = self._get_str(
            raw,
            ["affected_party", "subject_type", "user_type"],
        )

        outcome = self._get_str(
            raw,
            ["outcome", "result", "decision_outcome"],
        )

        # Scoring-related numeric and boolean fields
        confidence_score = self._get_float(
            raw,
            ["confidence_score", "score", "model_confidence"],
            default=0.0,
        )

        model_used = self._get_str(
            raw,
            ["model_used", "model_name", "model"],
            default=None,
        )

        data_sources = self._get_list_str(
            raw,
            ["data_sources", "sources", "datasets"],
            default=[],
        )

        human_in_loop = self._get_bool(
            raw,
            ["human_in_loop", "human_reviewed", "human_oversight"],
            default=False,
        )

        explanation_provided = self._get_bool(
            raw,
            ["explanation_provided", "has_explanation", "explanation"],
            default=False,
        )

        appeal_pathway = self._get_bool(
            raw,
            ["appeal_pathway", "can_appeal", "appeal_available"],
            default=False,
        )

        audit_trail = self._get_bool(
            raw,
            ["audit_trail", "logged", "has_audit_trail"],
            default=False,
        )

        sensitive_data_used = self._get_bool(
            raw,
            ["sensitive_data_used", "uses_sensitive_data"],
            default=False,
        )

        model_version_recorded = self._get_bool(
            raw,
            ["model_version_recorded", "has_model_version"],
            default=True,
        )

        data_sources_complete = self._get_bool(
            raw,
            ["data_sources_complete", "complete_sources"],
            default=True,
        )

        # Construct and return the normalised Decision object.
        return Decision(
            system_name=system_name,
            department=department,
            timestamp=timestamp,
            decision_type=decision_type,
            affected_party=affected_party,
            outcome=outcome,
            confidence_score=confidence_score,
            model_used=model_used,
            data_sources=data_sources,
            human_in_loop=human_in_loop,
            explanation_provided=explanation_provided,
            appeal_pathway=appeal_pathway,
            audit_trail=audit_trail,
            sensitive_data_used=sensitive_data_used,
            model_version_recorded=model_version_recorded,
            data_sources_complete=data_sources_complete,
        )