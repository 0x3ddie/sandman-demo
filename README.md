# Northstar Supply demo

Northstar is a realistic but side-effect-free storefront used to demonstrate Sandman’s
production debugging workflow. No payments, accounts, customer data, databases, email, or
other external services are present.

The default page looks and behaves normally for US shipping. The intentionally broken
`production` branch fails only when the delivery country is changed to Canada. Sandman
replays that exact contract against `known-good`, `production`, and a candidate hotfix in
separate Modal Sandboxes.

## Run locally

```bash
uv sync
uv run python app.py
```

Open <http://127.0.0.1:8000>. The production probe is:

```bash
curl -X POST http://127.0.0.1:8000/api/checkout/quote \
  -H 'Content-Type: application/json' \
  -d '{"subtotal_cents":12800,"country":"CA"}'
```

## Demo branch story

- `main` and `known-good`: Canada checkout returns CAD with complimentary shipping.
- `production`: a one-character configuration regression returns HTTP 500 for Canada.
- `sandman/*`: generated candidates are published only after bounded Codex generation.

## Deploy the intentionally broken production branch

```bash
modal deploy modal_app.py
```

The app scales to zero when idle and does not receive real traffic or secrets.
