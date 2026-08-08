# fpl-agent — session orientation

This is the depth-quarter flagship: a season-long FPL decision agent with public evals.
Read `README.md` for the charter (operating model, blind-dual protocol, success bars).

- **Quarter-level state:** `~/projects/personal/research/handoff.md`. Sync it at session end.
- **Build state:** this repo's GitHub issues. Start from the lowest open issue number.
- **Rulings archive:** `mohitrawat-ai/research` issues #6–#9 (direction, charter, canon, plan).
- **Hard constraint:** a recommendation must ship before every FPL deadline. GW1: 2026-08-21 17:30 UTC.
- **Protocol invariant:** Mohit's blind pick is drafted BEFORE he sees the agent's recommendation.
  Never show him the agent's pick for a gameweek until he confirms his blind draft is logged.
- **Understanding is the point.** Mohit must understand what we are building and why, at every step.
  Do not optimize for task completion. Explain the what and why before the how. If a step would
  ship without him grasping it, slow down and explain first.

Dev: `uv sync`, `uv run pytest -q`, snapshot via `uv run python -m fpl_agent.data.snapshot`.
