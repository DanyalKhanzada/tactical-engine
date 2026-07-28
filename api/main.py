from fastapi import FastAPI

from adapters.statsbomb import get_central_midfielder_vectors
from engine.contracts import PlayerVector

app = FastAPI(title="Tactical Engine API")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/players/central-midfielders", response_model=list[PlayerVector])
def central_midfielders():
    return get_central_midfielder_vectors()
