# Public SDK entrypoint for GovGuard.
# This lets users do: from govguard import GovernanceCheck

from .governance_check import GovernanceCheck, GovernanceResult

__all__ = ["GovernanceCheck", "GovernanceResult"]