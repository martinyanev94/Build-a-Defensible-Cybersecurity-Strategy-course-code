from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class AccessScenario:
    scenario_id: str
    dependency: str
    data_type: str
    jurisdiction: str
    data_custody: str
    access_mechanism: str
    notice_assumption: str
    mitigation_layer: str
    owner: str


SCENARIOS = [
    AccessScenario(
        "customer-records-direct-order",
        "customer records",
        "customer records",
        "Northstar operating jurisdiction",
        "Northstar",
        "direct order",
        "company process receives request",
        "request review",
        "Legal and Compliance",
    ),
    AccessScenario(
        "customer-records-partner-order",
        "customer records",
        "customer records",
        "provider jurisdiction",
        "Cloud Provider",
        "partner order",
        "unknown",
        "provider notification contract",
        "Vendor Risk",
    ),
]


def decision_record(scenario: AccessScenario) -> dict[str, str]:
    if scenario.access_mechanism == "direct order":
        notice_state = (
            "notice expected"
            if scenario.notice_assumption == "company process receives request"
            else "notification gap"
        )
    else:
        notice_state = (
            "notice expected"
            if scenario.notice_assumption == "provider must notify"
            else "notification gap"
        )
    return {
        "scenario_id": scenario.scenario_id,
        "dependency": scenario.dependency,
        "notice_state": notice_state,
        "mitigation_layer": scenario.mitigation_layer,
        "owner": scenario.owner,
    }


def publish_assessment(scenarios: list[AccessScenario]) -> list[dict[str, str]]:
    return [decision_record(scenario) for scenario in scenarios]


def join_assessment(
    signals: list[dict[str, str]],
    scenarios: list[AccessScenario],
) -> list[dict[str, str]]:
    by_dependency = {signal["dependency"]: signal for signal in signals}
    joined = []
    for record in publish_assessment(scenarios):
        signal = by_dependency.get(record["dependency"])
        joined.append({
            **record,
            "implication": (
                signal["implication"] if signal else "unclassified dependency"
            ),
            "escalation_state": (
                signal["escalation_state"] if signal else "review required"
            ),
        })
    return joined


if __name__ == "__main__":
    for record in publish_assessment(SCENARIOS):
        print(
            f"scenario_id={record['scenario_id']} | "
            f"dependency={record['dependency']} | "
            f"notice_state={record['notice_state']} | "
            f"mitigation={record['mitigation_layer']} | owner={record['owner']}"
        )
