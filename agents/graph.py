# This file defines a LangGraph workflow for:
#   raw payload → Intercept Agent → UK Scoring Agent → Report Agent
#
# At this stage:
# - Report Agent can just wrap the scoring result + decision into a simple dict.
# - Later you can expand it into full audit reports and multi-framework scoring.

from typing import Any, Dict, TypedDict

from langgraph.graph import StateGraph, START, END

from agents.intercept import InterceptAgent
from engine.core import Decision, score_uk_ai_playbook


# ---- Define the graph state ----

class GovGuardState(TypedDict):
    """
    Shared state passed between nodes in the LangGraph.
    Keys:
      - raw_payload: original JSON from the client
      - decision: normalised Decision object
      - scoring_result: dict from score_uk_ai_playbook
      - report: structured report dict (output of Report Agent)
    """
    raw_payload: Dict[str, Any]
    decision: Decision
    scoring_result: Dict[str, Any]
    report: Dict[str, Any]


# ---- Node implementations ----

# Single InterceptAgent instance for reuse
_interceptor = InterceptAgent()


def intercept_node(state: GovGuardState) -> GovGuardState:
    """
    Intercept node:
      - Takes raw_payload from state.
      - Uses InterceptAgent to produce a normalised Decision.
      - Stores Decision back into state.
    """

raw = state["raw_payload"]
    decision = _interceptor.normalise(raw)
    state["decision"] = decision
    return state


def uk_scoring_node(state: GovGuardState) -> GovGuardState:
    """
    UK Scoring node:
      - Takes Decision from state.
      - Calls score_uk_ai_playbook.
      - Stores scoring_result back into state.
    """
    decision = state["decision"]
    scoring_result = score_uk_ai_playbook(decision)
    state["scoring_result"] = scoring_result
    return state


def report_node(state: GovGuardState) -> GovGuardState:
    """
    Report node:
      - Takes Decision + scoring_result.
      - Builds a simple structured report dict (v1).
      - Later, this can be expanded to full audit reports and PDF output.
    """
    decision = state["decision"]
    scoring = state["scoring_result"]

    # Simple v1 report structure – human-readable but still JSON.
    report = {
        "system_name": decision.system_name,
        "department": decision.department,
        "decision_type": decision.decision_type,
        "affected_party": decision.affected_party,
        "outcome": decision.outcome,
        "framework": scoring.get("framework", "uk_ai_playbook"),
        "risk_score": scoring.get("risk_score"),
        "risk_level": scoring.get("risk_level"),
        "action": scoring.get("action"),
        "violations": scoring.get("violations", []),
    }

    state["report"] = report
    return state

# ---- Build the graph ----

def build_govguard_graph() -> StateGraph:
    """
    Construct the GovGuard LangGraph:

        START → intercept_node → uk_scoring_node → report_node → END

    Caller is responsible for running the compiled graph with an initial state.
    """
    graph = StateGraph(GovGuardState)

    graph.add_node("intercept", intercept_node)
    graph.add_node("uk_scoring", uk_scoring_node)
    graph.add_node("report", report_node)

    graph.add_edge(START, "intercept")
    graph.add_edge("intercept", "uk_scoring")
    graph.add_edge("uk_scoring", "report")
    graph.add_edge("report", END)

    return graph