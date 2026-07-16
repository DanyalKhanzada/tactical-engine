import pytest
from pydantic import ValidationError

from engine.contracts import (
    FitResult,
    MetricRequirement,
    MetricResult,
    PlayerVector,
    RoleProfile,
)

# --- PlayerVector ---


def test_player_vector_valid():
    pv = PlayerVector(
        internal_id="p1",
        league="Premier League",
        position="CM",
        metrics={"pass_accuracy": 87.5, "pressing_intensity": 72.0},
    )
    assert pv.internal_id == "p1"
    assert pv.metrics["pass_accuracy"] == 87.5


def test_player_vector_empty_metrics():
    pv = PlayerVector(internal_id="p2", league="La Liga", position="ST", metrics={})
    assert pv.metrics == {}


def test_player_vector_missing_field():
    with pytest.raises(ValidationError):
        PlayerVector(league="Bundesliga", position="CB", metrics={})


# --- MetricRequirement ---


def test_metric_requirement_valid():
    mr = MetricRequirement(metric_name="dribbles_per90", threshold=3.0, weight=1.5)
    assert mr.weight == 1.5


def test_metric_requirement_missing_field():
    with pytest.raises(ValidationError):
        MetricRequirement(metric_name="dribbles_per90", threshold=3.0)


# --- RoleProfile ---


def test_role_profile_valid():
    rp = RoleProfile(
        position="CM",
        formation="4-3-3",
        tactical_toggles={"press_high": True, "wide_attacks": False},
        requirements=[
            MetricRequirement(metric_name="pass_accuracy", threshold=80.0, weight=2.0)
        ],
    )
    assert rp.formation == "4-3-3"
    assert len(rp.requirements) == 1


def test_role_profile_empty_requirements():
    rp = RoleProfile(
        position="GK",
        formation="4-4-2",
        tactical_toggles={},
        requirements=[],
    )
    assert rp.requirements == []


def test_role_profile_missing_position():
    with pytest.raises(ValidationError):
        RoleProfile(formation="4-3-3", tactical_toggles={}, requirements=[])


# --- MetricResult ---


def test_metric_result_valid():
    mr = MetricResult(
        metric_name="pass_accuracy",
        actual_value=85.0,
        threshold=80.0,
        passed=True,
    )
    assert mr.passed is True


def test_metric_result_failed():
    mr = MetricResult(
        metric_name="dribbles_per90",
        actual_value=1.2,
        threshold=3.0,
        passed=False,
    )
    assert mr.passed is False


# --- FitResult ---


def test_fit_result_valid():
    fr = FitResult(
        player_id="p1",
        role="CM",
        score=78.5,
        breakdown=[
            MetricResult(
                metric_name="pass_accuracy",
                actual_value=85.0,
                threshold=80.0,
                passed=True,
            )
        ],
        verdict="Good fit",
    )
    assert fr.score == 78.5
    assert fr.verdict == "Good fit"


def test_fit_result_score_zero():
    fr = FitResult(player_id="p2", role="ST", score=0.0, breakdown=[], verdict="No fit")
    assert fr.score == 0.0


def test_fit_result_score_hundred():
    fr = FitResult(
        player_id="p3", role="CB", score=100.0, breakdown=[], verdict="Perfect fit"
    )
    assert fr.score == 100.0


def test_fit_result_score_above_100():
    with pytest.raises(ValidationError):
        FitResult(
            player_id="p4", role="CM", score=101.0, breakdown=[], verdict="Invalid"
        )


def test_fit_result_score_below_0():
    with pytest.raises(ValidationError):
        FitResult(
            player_id="p5", role="CM", score=-1.0, breakdown=[], verdict="Invalid"
        )


def test_fit_result_missing_player_id():
    with pytest.raises(ValidationError):
        FitResult(role="CM", score=50.0, breakdown=[], verdict="Ok")


# --- FitResult.from_breakdown ---


def test_from_breakdown_all_pass():
    breakdown = [
        MetricResult(
            metric_name="pass_accuracy", actual_value=85.0, threshold=80.0, passed=True
        ),
        MetricResult(
            metric_name="pressing_intensity",
            actual_value=74.0,
            threshold=70.0,
            passed=True,
        ),
    ]
    weights = {"pass_accuracy": 2.0, "pressing_intensity": 1.0}
    fr = FitResult.from_breakdown("p1", "CM", breakdown, weights)

    assert fr.score == 100.0
    assert fr.verdict == "Meets all requirements"


def test_from_breakdown_one_fail_verdict_contains_details():
    breakdown = [
        MetricResult(
            metric_name="long_passing", actual_value=4.2, threshold=6.5, passed=False
        ),
        MetricResult(
            metric_name="pass_accuracy", actual_value=85.0, threshold=80.0, passed=True
        ),
    ]
    weights = {"long_passing": 1.0, "pass_accuracy": 1.0}
    fr = FitResult.from_breakdown("p2", "CM", breakdown, weights)

    assert "long_passing" in fr.verdict
    assert "4.2" in fr.verdict
    assert "6.5" in fr.verdict
    assert fr.score == 50.0


def test_from_breakdown_all_fail_score_zero():
    breakdown = [
        MetricResult(
            metric_name="dribbles_per90", actual_value=1.0, threshold=3.0, passed=False
        ),
        MetricResult(
            metric_name="sprint_distance", actual_value=5.0, threshold=9.0, passed=False
        ),
    ]
    weights = {"dribbles_per90": 1.0, "sprint_distance": 1.0}
    fr = FitResult.from_breakdown("p3", "ST", breakdown, weights)

    assert fr.score == 0.0
    assert "dribbles_per90" in fr.verdict


def test_from_breakdown_weighted_partial_pass():
    breakdown = [
        MetricResult(
            metric_name="high_metric", actual_value=10.0, threshold=5.0, passed=True
        ),
        MetricResult(
            metric_name="low_metric", actual_value=1.0, threshold=5.0, passed=False
        ),
    ]
    weights = {"high_metric": 3.0, "low_metric": 1.0}
    fr = FitResult.from_breakdown("p4", "CB", breakdown, weights)

    assert fr.score == 75.0


def test_from_breakdown_empty_breakdown():
    fr = FitResult.from_breakdown("p5", "GK", [], {})
    assert fr.score == 0.0
    assert fr.verdict == "No metrics available to evaluate"
