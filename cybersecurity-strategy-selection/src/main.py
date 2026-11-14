from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StrategyLens:
    name: str
    score: float
    strength: str
    blind_spot: str


def rank_lenses(lenses: list[StrategyLens]) -> list[dict[str, object]]:
    return [
        {
            "name": lens.name,
            "score": lens.score,
            "strength": lens.strength,
            "blind_spot": lens.blind_spot,
        }
        for lens in sorted(lenses, key=lambda item: item.score, reverse=True)
    ]


def select_portfolio(ranked_lenses: list[dict[str, object]]) -> dict[str, object]:
    selected_names = {"identity-centric", "endpoint", "application-centric"}
    selected = [lens for lens in ranked_lenses if lens["name"] in selected_names]
    return {
        "outcome": "protect payment access and delivery flow",
        "lenses": selected,
        "rationale": "Identity limits access; endpoint adds device context; application checks reduce release risk.",
        "boundaries": [
            "does not eliminate every attack",
            "does not replace recovery planning",
            "legacy systems need staged adoption",
        ],
        "delivery": [
            "application checks at commit and build",
            "identity and endpoint conditions at deploy",
            "security, developers, and operations own different feedback steps",
        ],
        "measures": [
            "privileged-access coverage",
            "high-risk endpoint containment time",
            "recurring application findings reaching production",
        ],
    }


def present(portfolio: dict[str, object]) -> None:
    names = ", ".join(lens["name"] for lens in portfolio["lenses"])
    print(f"portfolio lenses: {names}")
    print(f"boundaries: {len(portfolio['boundaries'])}")
    print(f"delivery checkpoints: {len(portfolio['delivery'])}")
    print(f"measures: {len(portfolio['measures'])}")


if __name__ == "__main__":
    lenses = [
        StrategyLens("identity-centric", 8.8, "access decisions", "authorized misuse"),
        StrategyLens("endpoint", 8.2, "device visibility", "application logic"),
        StrategyLens("application-centric", 7.9, "release checks", "runtime identity"),
        StrategyLens("protect-and-recover", 7.5, "resilience", "early access"),
    ]
    present(select_portfolio(rank_lenses(lenses)))
