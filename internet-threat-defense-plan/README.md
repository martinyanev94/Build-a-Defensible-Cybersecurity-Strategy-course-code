# Internet Threat Defense Plan

This prototype models two post-compromise decisions separately:

- suspected botnet command-and-control activity on an endpoint
- DDoS traffic pressure against a service

Run it with Python 3.10 or newer:

```bash
python src/main.py
```

Expected output:

```text
contain-and-rebuild
(1.8, 'at-risk')
```

The values are teaching inputs for an explainable strategy model. They are not traffic-generation or production defense tooling.
