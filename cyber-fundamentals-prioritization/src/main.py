PATHS = [
    {"path_id": "credential_compromise", "name": "Credential compromise", "probability": 4, "impact": 5, "control_maturity": 0.2},
    {"path_id": "unpatched_vulnerability", "name": "Unpatched vulnerability", "probability": 4, "impact": 5, "control_maturity": 0.3},
    {"path_id": "social_engineering", "name": "Social engineering", "probability": 3, "impact": 4, "control_maturity": 0.4},
    {"path_id": "misconfiguration", "name": "Misconfiguration", "probability": 3, "impact": 4, "control_maturity": 0.5},
    {"path_id": "insider_threat", "name": "Insider threat", "probability": 2, "impact": 5, "control_maturity": 0.6},
]


def score_path(path):
    residual_exposure = 1 - path["control_maturity"]
    priority = path["probability"] * path["impact"] * residual_exposure
    return {**path, "priority": round(priority, 2)}


ranked_paths = sorted(
    (score_path(path) for path in PATHS),
    key=lambda path: path["priority"],
    reverse=True,
)

for rank, path in enumerate(ranked_paths, start=1):
    print(f"{rank}. {path['name']}: {path['priority']}")
