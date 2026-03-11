"""
Database layer for GovGuard.

This module is responsible for:
- Connecting to a Postgres-compatible database (e.g. Supabase, local Postgres).
- Defining ORM models that map to tables.
- Providing helper functions for storing decisions after they are scored.

Design goals:
- No secrets or hard-coded credentials in code. The database URL MUST come
  from an environment variable so that:
  - You never accidentally commit credentials.
  - Different environments (local, staging, production) can be configured safely.
"""

import os
import uuid
from typing import Any, Dict

from sqlalchemy import (
    Column,
    Float,
    Text,
    TIMESTAMP,
    text,
    create_engine,
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import declarative_base, sessionmaker

from engine.core import Decision


# Base class for SQLAlchemy ORM models.
# All tables will inherit from this.
Base = declarative_base()


def _get_database_url() -> str:
    """
    Read the Postgres connection string from an environment variable.

    Environment variable:
      - GOVGUARD_DATABASE_URL

    Example value for local development:
      postgresql://postgres:postgres@localhost:5432/govguard

    This function raises a clear error if the variable is missing so
    you do not accidentally run without a database configuration.
    """
    database_url = os.getenv("GOVGUARD_DATABASE_URL")
    if not database_url:
        raise RuntimeError(
            "GOVGUARD_DATABASE_URL environment variable is not set. "
            "Set it to your Postgres connection string "
            "(e.g. postgresql://user:password@host:5432/dbname)."
        )
    return database_url


# Create a SQLAlchemy engine and session factory.
# The engine manages the actual DB connections.
engine = create_engine(_get_database_url())
SessionLocal = sessionmaker(bind=engine)


class DecisionRecord(Base):
    """
    ORM model representing one scanned decision stored in Postgres.

    This table is the foundation for:
    - The Monitor Agent (trend analysis and alerts).
    - The dashboard (lists of decisions and their scores).
    - Audit/reporting queries.
    """

    __tablename__ = "decisions"

    # Unique identifier for this decision record.
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Timestamp when the record was created in the database.
    created_at = Column(
        TIMESTAMP(timezone=True),
        server_default=text("NOW()"),
        nullable=False,
    )

    # Key decision metadata – useful for filtering and analytics.
    system_name = Column(Text, nullable=False)
    department = Column(Text, nullable=True)
    decision_type = Column(Text, nullable=False)
    affected_party = Column(Text, nullable=False)
    outcome = Column(Text, nullable=False)

    # Governance-related metadata from the scoring engine.
    framework = Column(Text, nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(Text, nullable=False)
    action = Column(Text, nullable=False)

    # Original payload sent by the client (pre-normalisation),
    # stored as JSONB so you can always reconstruct or re-score later.
    raw_payload = Column(JSONB, nullable=False)


def init_db() -> None:
    """
    Create tables if they do not exist.

    This should be called once at application startup so that the
    'decisions' table is ready before any requests are handled.
    """
    Base.metadata.create_all(bind=engine)


def store_decision(
    decision: Decision,
    scoring_result: Dict[str, Any],
    raw_payload: Dict[str, Any],
) -> str:
    """
    Persist a scanned decision in the database and return its ID.

    Parameters:
      - decision: the normalised Decision object used for scoring.
      - scoring_result: the dictionary returned by score_uk_ai_playbook,
        containing risk_score, risk_level, action, and framework.
      - raw_payload: the original JSON payload received by the API
        before normalisation. This is stored for audit and potential
        re-scoring under new frameworks in the future.

    Returns:
      - The UUID of the stored DecisionRecord as a string.
    """
    session = SessionLocal()
    try:
        record = DecisionRecord(
            system_name=decision.system_name,
            department=decision.department,
            decision_type=decision.decision_type,
            affected_party=decision.affected_party,
            outcome=decision.outcome,
            framework=str(scoring_result.get("framework", "uk_ai_playbook")),
            risk_score=float(scoring_result.get("risk_score", 0.0)),
            risk_level=str(scoring_result.get("risk_level", "")),
            action=str(scoring_result.get("action", "")),
            raw_payload=raw_payload,
        )

        # Add and commit the new record.
        session.add(record)
        session.commit()

        # Refresh to ensure the 'id' and 'created_at' fields are populated.
        session.refresh(record)

        # Return the UUID as a string so it can be included in API responses.
        return str(record.id)

    finally:
        # Always close the session to free the connection back to the pool.
        session.close()

