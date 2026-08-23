# Northstar Supply demo

Northstar is a realistic but side-effect-free storefront used to demonstrate Sandman’s
production debugging workflow. No payments, accounts, customer data, databases, email, or
other external services are present.

The default page looks and behaves normally for US shipping. The intentionally broken
`production` branch fails only when the delivery country is changed to Canada. Sandman
replays that exact contract against `known-good`, `production`, and a candidate hotfix in
separate Modal Sandboxes.

**Live production:**
[Northstar Supply on Modal](https://echen1246-1--northstar-demo-production-storefront.modal.run)

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

- [`known-good`](https://github.com/0x3ddie/sandman-demo/tree/known-good): Canada checkout
  returns CAD with complimentary shipping.
- [`main`](https://github.com/0x3ddie/sandman-demo/tree/main): the healthy storefront plus
  CI and Sandman workflow configuration.
- [`production`](https://github.com/0x3ddie/sandman-demo/tree/production): a one-character
  configuration regression returns HTTP 500 for Canada.
- `sandman/*`: generated candidates are published only after bounded Codex generation.

## Run the full incident workflow

The repository needs these GitHub Actions secrets:

- `OPENAI_API_KEY`
- `MODAL_TOKEN_ID`
- `MODAL_TOKEN_SECRET`

Greptile must also have access to this repository. Then open a pull request from
`production` into `main` and comment:

```text
/sandman probe=canada-checkout known-good=known-good@59da828d7d2f76ff1089caec29b827d0902fce9f
```

Sandman asks Codex for a bounded candidate, publishes the patch on a `sandman/*` branch,
probes all three exact revisions in isolated Modal Sandboxes, posts a GitHub Check, and
opens the verified hotfix as a draft pull request for Greptile to review.

## Deploy the intentionally broken production branch

```bash
modal deploy modal_app.py
```

The app scales to zero when idle and does not receive real traffic or secrets.
