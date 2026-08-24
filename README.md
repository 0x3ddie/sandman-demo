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
- `sandman/*`: candidate branches published by the remediation workflow.

## Run the zero-secret incident demo

No OpenAI or Modal API credentials are required. The workflow transparently labels candidate
generation and the three sandbox observations as deterministic simulations. It still publishes
a real candidate branch, GitHub Check, and draft pull request for the installed Greptile app.

Open a pull request from `production` into `main` and comment:

```text
/sandman probe=canada-checkout known-good=known-good@59da828d7d2f76ff1089caec29b827d0902fce9f
```

Sandman generates the known demo candidate, publishes it on a `sandman/*` branch, runs the
three-lane deterministic verdict, posts a GitHub Check, and opens the verified hotfix as a
draft pull request for Greptile to review.

For the production-authentic path, replace the deterministic generation step with the pinned
Codex action and run the same comparison with `--runtime modal`. That path requires
`OPENAI_API_KEY`, `MODAL_TOKEN_ID`, and `MODAL_TOKEN_SECRET` as GitHub Actions secrets.

### What to show during the demo

1. Open the live production storefront and change the destination to **Canada** to reproduce
   the quiet checkout failure.
2. Open the `production` → `main` pull request and show its failing storefront check.
3. Paste the `/sandman` command above as a pull request comment.
4. Open **Actions → Sandman comment remediation** to watch generation, publication, and
   verification complete.
5. Open the resulting `sandman/*` draft pull request and show the three-lane Check and
   Greptile review.

Nothing needs to be entered in a terminal for this flow.

## Deploy the intentionally broken production branch

```bash
modal deploy modal_app.py
```

The app scales to zero when idle and does not receive real traffic or secrets.
