# TriageDesk — AI Support Ticket Triage API
FastAPI ticket classification API with priority estimation, response suggestions, batch triage, metrics, MongoDB-ready storage, Docker, GitHub Actions CI, and pytest tests. Local default is in-memory storage and deterministic rules so it works without credentials.

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload
```
Docs: http://127.0.0.1:8000/docs

## Tests
`pytest -q`

## Docker
`docker compose up --build` starts API + MongoDB. LLM integration is disabled by default. Configure `LLM_API_URL`, `LLM_API_KEY`, and `LLM_ENABLED=true` to use a compatible chat-completions endpoint. Verify privacy and provider terms before sending ticket text externally.

Endpoints: `GET /health`, `POST /api/tickets/triage`, `POST /api/tickets/batch`, `GET /api/tickets`, `GET /api/metrics`.

The repo does not provision AWS resources automatically. Deploy the container to EC2 and configure secrets/infrastructure separately. Accuracy metrics from resume bullets must be independently evaluated.
