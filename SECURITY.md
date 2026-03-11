# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in GovGuard AI, please report it
responsibly by emailing the maintainer directly rather than opening a public
issue.

We will acknowledge receipt within 48 hours and provide an estimated timeline
for a fix.

## Security Design Principles

GovGuard AI is designed with the following security principles:

1. **No external LLM APIs by default**  
   Decision data never leaves your environment. The scoring engine runs
   locally using deterministic rules; any future LLM features (e.g. via
   Ollama) are self-hosted.

2. **No hardcoded credentials**  
   Database connection strings and API keys must be provided via environment
   variables (e.g. `GOVGUARD_DATABASE_URL`). Nothing sensitive is committed
   to the repository.

3. **Sensitive files excluded**  
   Business documents, `.env` files, and other private data are listed in
   `.gitignore` and should never be tracked.

4. **Minimal dependencies**  
   The core stack uses well-known, audited libraries (FastAPI, SQLAlchemy,
   requests). We avoid unnecessary dependencies to reduce attack surface.

## Best Practices for Deployment

- Run GovGuard behind a reverse proxy (e.g. nginx, Caddy) with TLS in
  production.
- Restrict database access to the GovGuard service only.
- Use secrets management (e.g. HashiCorp Vault, AWS Secrets Manager) for
  production credentials.
- Regularly update dependencies to patch known vulnerabilities.
