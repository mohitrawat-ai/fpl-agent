# fpl-agent: a season-long FPL decision agent with public evals

An autonomous agent plays the 2026-27 Fantasy Premier League season. It recommends a squad,
transfers, captaincy, and chips before every deadline. A human (me) executes the final call on a
real team. Every decision is logged and scored in public.

This is a harness-engineering project wearing a game. FPL is a 38-round sequential decision
problem: budget constraints, transfer costs, chip timing, rotation risk, and hard weekly
deadlines with no do-overs. The interesting problems are long-horizon agent design,
decision-making under uncertainty, and evals that survive variance.

## Operating model

1. The agent produces a recommendation before each gameweek deadline.
2. I draft my own decision **before** opening the agent's (I've played this game for 15 years).
3. I make the final call and apply it to my real team.
4. All three — my blind pick, the agent's pick, the final — are logged in [`decisions/`](decisions/)
   and scored after the gameweek.

That third line is the eval. Over a season it yields 38 graded head-to-heads between the agent
and a 15-year human baseline, plus a disagreement log where every split becomes an eval case.

## Success bars

- **Stretch:** top 5k overall rank (top ~0.05% of ~11M players).
- **Variance-resistant:** the agent outscores my blind picks over the season, and beats
  template/naive baselines and my own historical seasons in backtests.
- **Process:** a recommendation shipped before all 38 deadlines, decision log complete.

## Status

Pre-season. Phase 1: data pipeline + a v1 recommender that ships a legal GW1 squad.
Progress is tracked in this repo's issues. Write-ups land in [`essays/`](essays/) at the end of
each build phase.
