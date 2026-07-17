# Fonbet utilities

This repository contains legacy parsing helpers for Fonbet payloads.

## Safe dashboard

`dashboard_server.py` starts a read-only web dashboard:

```bash
PORT=8011 TENNIS_API_DIR=/opt/fonbet_suite/tenniss_api python3 dashboard_server.py
```

The dashboard intentionally does not:

- log in to bookmaker accounts;
- store phone numbers, passwords, cookies, or session tokens;
- check account balances;
- submit coupons or place bets.

It only shows repository status, `tenniss_api` model metadata, documentation, and local artifact files.

## Legacy modules

The existing modules are kept for compatibility with old scripts:

- `apifb.py` parses saved Fonbet JSON payloads.
- `classy.py` fetches and reads `json.txt`.
- `mongo_class.py` contains MongoDB helpers.
- `bet.py` contains legacy coupon helpers and is not used by the dashboard.
