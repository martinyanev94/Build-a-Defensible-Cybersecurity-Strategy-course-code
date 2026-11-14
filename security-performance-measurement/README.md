# Security performance measurement

This project builds a reproducible baseline report from vulnerability-management and attack-centric records.

## Run

From this directory:

```text
python3 src/main.py
```

The input CSV keeps vulnerability exposure and attack outcomes in separate record types. The pipeline validates required fields, aggregates records by period, preserves denominators, and prints both a compact report and JSON output.

A blank required value is rejected. A zero is retained as an observed zero. Attack stages are ordered so the report can identify the furthest observed stage without relying on actor attribution.
