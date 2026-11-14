from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Scenario:
    name: str
    stages: List[str]
    impact: int
    likelihood: int
    controls: Dict[str, bool]
    owner: str


def evaluate(scenario: Scenario) -> Dict[str, object]:
    blocked_at: Optional[str] = None
    for index, stage in enumerate(scenario.stages):
        if scenario.controls.get(stage, False):
            blocked_at = stage
            break
    if blocked_at is None:
        residual = scenario.impact * scenario.likelihood
        objective_reached = True
    else:
        residual = round(
            scenario.impact * scenario.likelihood
            * (index + 1) / len(scenario.stages), 2
        )
        objective_reached = False
    return {
        "name": scenario.name,
        "blocked_at": blocked_at,
        "objective_reached": objective_reached,
        "residual": residual,
        "owner": scenario.owner,
    }


SCENARIOS = [
    Scenario(
        "Phishing", ["delivery", "trust", "credential_use", "inbox_access"],
        5, 3, {"credential_use": True}, "identity",
    ),
    Scenario(
        "Drive-by", ["web_delivery", "browser_exploit", "malware_install", "c2"],
        4, 4, {"web_delivery": True}, "endpoint",
    ),
    Scenario(
        "DDoS", ["endpoint_compromise", "c2", "traffic_pressure", "availability"],
        5, 5, {"traffic_pressure": True}, "availability",
    ),
]



def prioritized_report(scenarios: List[Scenario]) -> List[Dict[str, object]]:
    results = [evaluate(scenario) for scenario in scenarios]
    return sorted(results, key=lambda item: item["residual"], reverse=True)


if __name__ == "__main__":
    for item in prioritized_report(SCENARIOS):
        stage = item["blocked_at"] or "objective_reached"
        print(
            f'{item["name"]}: {stage} residual={item["residual"]:.2f} '
            f'owner={item["owner"]}'
        )

    drive_by_fallback = Scenario(
        "Drive-by fallback", SCENARIOS[1].stages, 4, 4,
        {"malware_install": True}, "endpoint",
    )
    ddos_fallback = Scenario(
        "DDoS fallback", SCENARIOS[2].stages, 5, 5,
        {"availability": True}, "availability",
    )
    assert evaluate(drive_by_fallback)["blocked_at"] == "malware_install"
    assert evaluate(ddos_fallback)["blocked_at"] == "availability"
    print("verification: fallback controls blocked both paths")
