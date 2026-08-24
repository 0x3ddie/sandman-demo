# Northstar Supply demo

Northstar is a realistic but side-effect-free storefront used to demonstrate Sandman’s
production debugging workflow. No payments, accounts, customer data, databases, email, or
other external services are present.

The default page looks and behaves normally, including Canadian shipping. The staged
`demo-bug` branch contains a one-character regression that fails only when the delivery
country is changed to Canada. Pushing that branch to `production` deploys the regression and
starts Sandman automatically. Sandman replays the exact contract against `known-good`,
`production`, and a candidate hotfix in separate Modal Sandboxes.

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
- [`production`](https://github.com/0x3ddie/sandman-demo/tree/production): the currently
  deployed, healthy storefront before the demo begins.
- [`demo-bug`](https://github.com/0x3ddie/sandman-demo/tree/demo-bug): the staged one-character
  Canada pricing regression used to start the incident.
- `sandman/*`: candidate branches published by the remediation workflow.

## Run the incident demo

When `OPENAI_API_KEY` exists, candidate generation uses the pinned Codex action; otherwise it
falls back to the transparently labeled deterministic generator. When `MODAL_TOKEN_ID` and
`MODAL_TOKEN_SECRET` exist, verification uses three real Modal Sandboxes; otherwise it uses the
explicitly simulated runtime. Every path publishes a real candidate branch, GitHub Check, and
draft pull request for Greptile.

Start the clean demo with one production push:

```bash
git push origin demo-bug:production
```

That push deploys the exact production revision to Modal, opens the `production` → `main`
incident pull request, and runs the entire remediation sequence. **Run workflow** remains
available as a rehearsal fallback.

The pull request comment path remains available for an existing incident PR:

```text
/sandman probe=canada-checkout known-good=known-good@59da828d7d2f76ff1089caec29b827d0902fce9f
```

Sandman generates the known demo candidate, publishes it on a `sandman/*` branch, runs the
three-lane verdict, posts a GitHub Check, and opens the verified hotfix as a draft pull request
for Greptile to review.

Fully API-backed runs require all three GitHub Actions secrets: `OPENAI_API_KEY`,
`MODAL_TOKEN_ID`, and `MODAL_TOKEN_SECRET`.

### What to show during the demo

1. Open the live production storefront and show that **Canada** works.
2. Push `demo-bug` to `production` and watch **Actions → Sandman incident remediation** start.
3. Refresh the storefront and reproduce the newly deployed checkout failure.
4. Show the three tagged executions in the `sandman-northstar-probes` Modal App.
5. Open the resulting `sandman/*` draft pull request and show the three-lane Check and
   Greptile review.

The app scales to zero when idle and does not receive real traffic or secrets. Sandman does
not merge the verified draft automatically; production changes only after human approval.
