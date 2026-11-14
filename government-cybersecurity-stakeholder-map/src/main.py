from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class GovernmentSignal:
    institution: str
    role: str
    action: str
    dependency: str
    implication: str
    owner: str
    escalation_state: str


SIGNALS = [
    GovernmentSignal(
        "National standards body",
        "standards body",
        "publishes a security baseline",
        "security baseline",
        "compare baseline with current controls",
        "CISO",
        "routine review",
    ),
    GovernmentSignal(
        "Regulatory authority",
        "enforcement",
        "issues a regulatory obligation",
        "compliance boundary",
        "interpret obligation before implementation",
        "Legal and Compliance",
        "decision required",
    ),
    GovernmentSignal(
        "Public-sector buyer",
        "market participation",
        "sets procurement requirements",
        "sales and procurement",
        "validate requirements before bid commitment",
        "Procurement and Security",
        "decision required",
    ),
    GovernmentSignal(
        "Incident coordination center",
        "defense",
        "coordinates defensive response",
        "incident response",
        "define the trusted coordination channel",
        "Incident Response Lead",
        "immediate coordination",
    ),
]


def publish_map(signals: list[GovernmentSignal]) -> list[dict[str, str]]:
    return [asdict(signal) for signal in signals]


if __name__ == "__main__":
    for signal in publish_map(SIGNALS):
        print(
            f"institution={signal['institution']} | role={signal['role']} | "
            f"owner={signal['owner']} | escalation={signal['escalation_state']}"
        )
