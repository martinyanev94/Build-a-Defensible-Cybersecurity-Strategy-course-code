from dataclasses import dataclass


@dataclass
class KeyDecision:
    lifecycle: str
    authorized_identities: list[str]
    rotation_days: int
    recovery_owner: str
    recovery_tested: bool


def validate_key_decision(decision: dict) -> str:
    required = {
        "lifecycle",
        "authorized_identities",
        "rotation_days",
        "recovery_owner",
        "recovery_tested",
    }
    missing = required - decision.keys()
    if missing:
        return "blocked: missing " + ", ".join(sorted(missing))
    if not decision["lifecycle"]:
        return "blocked: lifecycle is empty"
    if not decision["recovery_owner"]:
        return "blocked: recovery owner is empty"
    if not decision["authorized_identities"]:
        return "blocked: no authorized identities"
    if decision["rotation_days"] <= 0:
        return "blocked: rotation must be positive"
    if not decision["recovery_tested"]:
        return "blocked: recovery is untested"
    return "ready"


def strategy_scorecard(metrics: dict, cloud_gaps: list[str], key_status: str) -> dict:
    scorecard = {name: dict(value) for name, value in metrics.items()}
    stage = scorecard["maximum_observed_stage"]["current"]
    if "exploitation" in stage:
        next_priority = "interrupt exploitation transition"
    elif key_status != "ready":
        next_priority = "complete key recovery evidence"
    elif cloud_gaps:
        next_priority = "close customer cloud control gap"
    else:
        next_priority = "maintain controls and review next cycle"
    return {
        "metrics": scorecard,
        "cloud_gaps": cloud_gaps,
        "key_status": key_status,
        "next_priority": next_priority,
    }


def main() -> None:
    key_record = {
        "lifecycle": "create-use-rotate-recover-retire",
        "authorized_identities": ["payments-service", "recovery-service"],
        "rotation_days": 90,
        "recovery_owner": "platform-operations",
        "recovery_tested": True,
    }
    key_status = validate_key_decision(key_record)
    metrics = {
        "maximum_observed_stage": {
            "type": "outcome",
            "baseline": "installation",
            "current": "exploitation",
            "denominator": "2 simulated intrusion paths",
            "evidence_period": "2026-Q4",
            "decision_mapping": "interrupt exploitation transition",
        },
        "cloud_control_reviews": {
            "type": "activity",
            "baseline": 1,
            "current": 3,
            "denominator": "customer cloud controls",
            "evidence_period": "2026-Q4",
            "decision_mapping": "review customer evidence",
        },
    }
    report = strategy_scorecard(
        metrics,
        cloud_gaps=["customer identity review evidence"],
        key_status=key_status,
    )
    print("Northstar cloud strategy scorecard")
    print("key readiness:", key_status)
    print("cloud gaps:", len(report["cloud_gaps"]))
    print("next priority:", report["next_priority"])


if __name__ == "__main__":
    main()
