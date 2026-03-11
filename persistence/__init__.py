"""
Persistence package for GovGuard.

This package is responsible for:
- Database connection and configuration (e.g. Postgres / Supabase).
- ORM models that map to persisted tables (decisions, audit reports, alerts, etc.).
- Helper functions for storing and retrieving governance data.

At this early stage we only define storage for scanned decisions, which
the Monitor Agent and dashboard can later build on.
"""

