from pydantic import BaseModel, Field


class PlayerVector(BaseModel):
    internal_id: str
    league: str
    position: str
    metrics: dict[str, float]


class MetricRequirement(BaseModel):
    metric_name: str
    threshold: float
    weight: float


class RoleProfile(BaseModel):
    position: str
    formation: str
    tactical_toggles: dict
    requirements: list[MetricRequirement]


class MetricResult(BaseModel):
    metric_name: str
    actual_value: float
    threshold: float
    passed: bool


class FitResult(BaseModel):
    player_id: str
    role: str
    score: float = Field(ge=0.0, le=100.0)
    breakdown: list[MetricResult]
    verdict: str

    @classmethod
    def from_breakdown(
        cls,
        player_id: str,
        role: str,
        breakdown: list[MetricResult],
        weights: dict[str, float],
    ) -> "FitResult":
        if not breakdown:
            return cls(
                player_id=player_id,
                role=role,
                score=0.0,
                breakdown=[],
                verdict="No metrics available to evaluate",
            )

        total_weight = sum(weights.get(m.metric_name, 1.0) for m in breakdown)
        passed_weight = sum(
            weights.get(m.metric_name, 1.0) for m in breakdown if m.passed
        )
        score = (passed_weight / total_weight) * 100.0

        failed = [m for m in breakdown if not m.passed]
        if failed:
            f = failed[0]
            verdict = (
                f"Fails {f.metric_name}: {f.actual_value} vs {f.threshold} required"
            )
        else:
            verdict = "Meets all requirements"

        return cls(
            player_id=player_id,
            role=role,
            score=score,
            breakdown=breakdown,
            verdict=verdict,
        )
