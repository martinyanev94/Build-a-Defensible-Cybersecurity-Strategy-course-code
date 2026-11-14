# Cloud Security Strategy

This standard-library Python prototype presents a measured, cloud-ready strategy for Northstar Payments.

## Run

```bash
python src/main.py
```

Expected output:

```text
Northstar cloud strategy scorecard
key readiness: ready
cloud gaps: 1
next priority: interrupt exploitation transition
```

The prototype preserves metric type, baseline, current value, denominator, evidence period, and decision mapping. It keeps provider evidence separate from customer-owned controls. It validates a key-management decision across lifecycle, authorized identities, rotation, and recovery, then selects the next priority from attack-stage evidence, key readiness, and remaining cloud control gaps.

This is a decision-system prototype, not production security tooling. Replace the sample records with validated organizational evidence before using the approach for an actual decision.
