REQUIRED_CHECKS = ("unit_tests", "security_scan")


def evaluate_change(change):
    failures = [
        check for check in REQUIRED_CHECKS
        if not change.get(check, False)
    ]
    if not change.get("owner"):
        failures.append("owner")
    if failures:
        return {
            "status": "blocked",
            "owner": change.get("owner", "unassigned"),
            "failures": failures,
            "feedback": "Fix failed checks, then rerun the pipeline.",
        }
    return {
        "status": "ready",
        "owner": change["owner"],
        "failures": [],
        "feedback": "All required checks passed; continue delivery.",
    }


changes = [
    {"name": "payment-api", "unit_tests": True,
     "security_scan": False, "owner": "payments-team"},
    {"name": "payment-api-fixed", "unit_tests": True,
     "security_scan": True, "owner": "payments-team"},
]

for change in changes:
    result = evaluate_change(change)
    print(change["name"], result["status"],
          result["failures"], result["owner"])
