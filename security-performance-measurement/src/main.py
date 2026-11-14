import csv
import json
from collections import defaultdict
from pathlib import Path

STAGES = {
    "reconnaissance": 1,
    "weaponization": 2,
    "delivery": 3,
    "exploitation": 4,
    "installation": 5,
    "actions_on_objectives": 6,
}
REQUIRED = {
    "vulnerability": {"period", "assets_in_scope", "total_assets", "unresolved_vulnerabilities", "critical_vulnerabilities"},
    "attack": {"period", "attack_stage", "detected", "stopped"},
}


def load_records(path):
    records = []
    with Path(path).open(newline="") as handle:
        for row_number, row in enumerate(csv.DictReader(handle), start=2):
            record_type = row["record_type"]
            missing = sorted(REQUIRED[record_type] - {key for key, value in row.items() if value.strip()})
            if missing:
                raise ValueError(f"row {row_number}: missing {', '.join(missing)}")
            row["record_type"] = record_type
            records.append(row)
    return records


def number(row, key):
    return int(row[key])


def aggregate(records):
    periods = defaultdict(lambda: {
        "assets_covered": None, "total_assets": None,
        "unresolved_vulnerabilities": 0, "critical_vulnerabilities": 0,
        "attacks_observed": 0, "attacks_detected": 0, "attacks_stopped": 0,
        "max_attack_stage": 0,
    })
    for row in records:
        bucket = periods[row["period"]]
        if row["record_type"] == "vulnerability":
            bucket["assets_covered"] = number(row, "assets_in_scope")
            bucket["total_assets"] = number(row, "total_assets")
            bucket["unresolved_vulnerabilities"] = number(row, "unresolved_vulnerabilities")
            bucket["critical_vulnerabilities"] = number(row, "critical_vulnerabilities")
        else:
            bucket["attacks_observed"] += 1
            bucket["attacks_detected"] += row["detected"].lower() == "yes"
            bucket["attacks_stopped"] += row["stopped"].lower() == "yes"
            bucket["max_attack_stage"] = max(bucket["max_attack_stage"], STAGES[row["attack_stage"]])
    return periods


def ratio(numerator, denominator):
    return round(numerator / denominator, 2) if denominator else None


def build_report(periods):
    report = []
    for period in sorted(periods):
        bucket = periods[period]
        attacks = bucket["attacks_observed"]
        report.append({
            "period": period,
            "asset_coverage": ratio(bucket["assets_covered"], bucket["total_assets"]),
            "unresolved_vulnerabilities": bucket["unresolved_vulnerabilities"],
            "critical_vulnerabilities": bucket["critical_vulnerabilities"],
            "attack_detection_rate": ratio(bucket["attacks_detected"], attacks),
            "attack_stopping_rate": ratio(bucket["attacks_stopped"], attacks),
            "max_attack_stage": bucket["max_attack_stage"],
        })
    return report


def main():
    root = Path(__file__).parent.parent
    records = load_records(root / "sample_data.csv")
    report = build_report(aggregate(records))
    for row in report:
        print(
            f"period={row['period']} coverage={row['asset_coverage']:.2f} "
            f"unresolved={row['unresolved_vulnerabilities']} "
            f"critical={row['critical_vulnerabilities']} "
            f"detected={row['attack_detection_rate']:.2f} "
            f"stopped={row['attack_stopping_rate']:.2f} "
            f"max_stage={row['max_attack_stage']}"
        )
    print("data_quality=PASS")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
