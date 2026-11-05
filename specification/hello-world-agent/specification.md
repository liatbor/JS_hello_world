# Specification: hello-world-agent

> **Guidelines**: Read all applicable guidelines before executing ANY tasks below:
> - [guidelines.md](../guidelines.md) — Universal execution rules
> - [guidelines-agent.md](../guidelines-agent.md) — Universal agent patterns
> - [guidelines-agent-python.md](../guidelines-agent-python.md) — Python implementation details
> - [guidelines-agent-skills.md](../guidelines-agent-skills.md) — Runtime skills patterns
> - [guidelines-agent-mcp.md](../guidelines-agent-mcp.md) — MCP integration patterns

---

## Basic Setup

- [x] Read `product-requirements-document.md` and `intent.md` to understand the full context before starting.
- [x] Bootstrap agent code in `assets/hello-world-agent/` using instructions from the sap-agent-bootstrap section.
- [x] Install dependencies, validate the agent starts and responds at `/.well-known/agent.json`

---

## Runtime Skills

No runtime skills are needed for this agent — the single response ("Hello World") does not require multi-step workflows, domain-specific knowledge, or external reference material.

---

## Project-Specific Tasks

## Hello World Response

- [x] Open `assets/hello-world-agent/app/agent.py` and locate the system prompt section.
- [x] Update the system prompt so the agent always responds with "Hello World" to any user input.
- [x] Verify that the agent's response logic does not require any external tool calls or data lookups.
- [x] Confirm the agent's `name` and `description` reflect a Hello World demo agent.

## A2A API Endpoint

- [x] Confirm the agent exposes `/.well-known/agent.json` and that the endpoint is reachable when the server is running locally.
- [x] Send a test message to the agent endpoint and verify the response body contains "Hello World".

---

## Business Instrumentation

- [x] Implement business step instrumentation for each milestone from the PRD using structured logging and OpenTelemetry custom spans.
  - M1: `M1.achieved: agent project scaffolded and server started successfully` in `main.py`
  - M2: `M2.achieved: agent responded with Hello World to user input` in `agent.py` `_run_agent()`
  - M3: emitted via startup probe success at deploy time
- [x] Verify `bootstrap(app)` is called after `app = server.build()` in `main.py`

---

## MCP Tool Integration

No MCP servers or external APIs are required for this agent. Skipped.

---

## Testing

- [x] `conftest.py` only sets `IBD_TESTING=true`
- [x] Write a unit test in `assets/hello-world-agent/tests/` that sends a message to the agent and asserts the response contains "Hello World"
- [x] Write one integration test executing the end-to-end agent flow with mocked LLM response
- [x] Run `pytest` from `assets/hello-world-agent/` — coverage at 71% (≥70% threshold met)
- [x] Run `pytest` again to generate final `test_report.json`
- [x] Verify `test_report.json` exists in `assets/hello-world-agent/`
