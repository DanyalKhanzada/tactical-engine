# Relational Tactical Scouting Engine

## What this is
Role-first football scouting engine. Formation in, player fit scores out.
The balance layer is the IP: change one role, every adjacent role updates.

## Architecture
Three contracts: PlayerVector, RoleProfile, FitResult.
Engine never knows the data source. Everything is interchangeable.

## Stack
Python 3.11+, Pydantic v2, Polars, FastAPI, pytest, ruff, black

## Structure
engine/contracts.py   — three Pydantic contracts
engine/roles.py       — derive_role_profile()
engine/balance.py     — balance_layer()
engine/scorer.py      — score_player()
adapters/synthetic.py — fake data for testing
api/main.py           — FastAPI endpoints
tests/                — pytest tests

## Rules
Never break the contract shapes.
Every function needs a test.
Run make fmt before every commit.
