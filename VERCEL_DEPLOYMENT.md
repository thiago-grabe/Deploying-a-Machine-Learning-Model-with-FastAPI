# Vercel Deployment Guide

Canonical guide for the Vercel deployment of the Census Income Classification
API and its web UI. The Render.com deployment (documented in
[`starter/DEPLOYMENT.md`](starter/DEPLOYMENT.md)) remains live and unchanged —
Vercel is an additional deployment target, and both serve identical API paths.

## 1. Architecture

```
                        ┌──────────────────────────────────────────────┐
   Browser ───────────► │                Vercel Edge/CDN               │
                        │                                              │
     GET /ui/  ───────► │  public/ui/index.html   (static, CDN-served) │
                        │                                              │
     everything else ─► │  Python Function (FastAPI preset)            │
                        │    app.py ──► starter/main.py  `app`         │
                        │       │  loads at cold start:                │
                        │       ├── starter/model/model.pkl   (4.2 MB) │
                        │       ├── starter/model/encoder.pkl          │
                        │       └── starter/model/lb.pkl               │
                        └──────────────────────────────────────────────┘

   Delivery loop (matches the course rubric):
   git push master ──► GitHub Actions `test` (flake8 + train + pytest)
                          └─ only if green ──► `deploy` (vercel deploy --prod)
                                                  └──► live URL ──► smoke test
```

Key properties:
- **Same API paths as Render** (`/`, `/predict`, `/docs`, `/health`) — Vercel's
  zero-config FastAPI preset routes every request to the app unrewritten, so
  `starter/query_live_api.py` works unchanged against either deployment.
- **No deploy-before-CI**: Vercel's Git integration is never connected and
  `vercel.json` sets `"git": {"deploymentEnabled": false}`. The GitHub Actions
  `deploy` job (gated on `test`) is the only path to production.
- **Model artifacts ship in the bundle**: everything the API needs at request
  time was saved and committed at training time (`starter/model/*.pkl`).

## 2. File map

| File | Role |
|---|---|
| `app.py` | Vercel entrypoint shim — re-exports `app` from `starter/main.py` (the preset requires a root-level entrypoint) |
| `requirements.txt` (root) | Slim inference-only pins installed by Vercel (~207 MB, fits the 500 MB Python function limit). Keep in lockstep with `starter/requirements.txt` |
| `starter/requirements.txt` | Full dev/CI dependency set (Jupyter, plotting, aequitas…) — used by CI and Render, never by Vercel |
| `vercel.json` | Region (`gru1`), function `maxDuration`, bundle `excludeFiles`, Git auto-deploy disabled |
| `.vercelignore` | Upload trim (`.venv`, data, screenshots). Never lists `starter/model/` or `public/` |
| `public/ui/index.html` | Web UI, CDN-served at `/ui/` (deliberately not `public/index.html`, which would shadow the rubric-required `GET /` JSON) |
| `.github/workflows/python-app.yml` | `test` job (CI) + `deploy` job (CD, gated on `test`, master pushes only) |

## 3. First-time setup runbook

1. **Login** (interactive, once): `npx vercel@latest login`
2. **Link the project** from the repo root (creates `.vercel/`, git-ignored):
   `npx vercel link` — choose your scope, create project
   `census-income-classification`, project root = repo root.
   Do **not** connect the GitHub integration when the dashboard offers it.
3. **Preview deploy**: `npx vercel deploy` — verify the printed URL
   (see Troubleshooting for the preview 401).
4. **Production deploy** (first time, manual): `npx vercel deploy --prod`.
5. **Wire CI**: create a token at vercel.com → Account Settings → Tokens, then
   add three repository secrets under GitHub → Settings → Secrets and
   variables → Actions:
   - `VERCEL_TOKEN` — the token you created
   - `VERCEL_ORG_ID` — `orgId` from `.vercel/project.json`
   - `VERCEL_PROJECT_ID` — `projectId` from `.vercel/project.json`

After that, every merge to `master` deploys automatically once CI is green.

## 4. CI/CD flow

- Push/PR → `test` job: flake8 (hard-fail on syntax/undefined names), retrains
  the model, runs the full pytest suite (18 tests).
- Push to `master` only, after `test` passes → `deploy` job: installs the
  Vercel CLI, runs `vercel deploy --prod` (remote build on Vercel's image),
  then smoke-tests `https://census-income-classification.vercel.app/health`.
- The deployed URL is printed in the job log (`Deployed: https://…`).
- PRs never deploy (the `deploy` job's `if` excludes non-push events).

## 5. Endpoints

| Method & path | Purpose | Example |
|---|---|---|
| `GET /` | Welcome JSON (rubric-asserted) | `{"message": "Welcome to the Census Income Classification API!", …}` |
| `GET /health` | Uptime/deploy checks | `{"status":"ok","model_loaded":true,"model_type":"RandomForestClassifier","sklearn_version":"1.7.2"}` |
| `POST /predict` | Model inference | body below → `{"prediction": ">50K"}` or `{"prediction": "<=50K"}` |
| `GET /docs` | Swagger UI | interactive |
| `GET /ui/` | Web UI (static) | form with 5 test presets |

`POST /predict` body (keys use hyphens; all fields required; bounds enforced —
invalid input returns 422):

```json
{
  "age": 52, "workclass": "Self-emp-inc", "fnlgt": 287927,
  "education": "HS-grad", "education-num": 9,
  "marital-status": "Married-civ-spouse", "occupation": "Exec-managerial",
  "relationship": "Wife", "race": "White", "sex": "Female",
  "capital-gain": 15024, "capital-loss": 0, "hours-per-week": 40,
  "native-country": "United-States"
}
```

## 6. Logging

Format: `TIMESTAMP LEVEL logger_name message`, written to **stdout**
(required on Vercel: stderr lines are classified as errors, and an
unconfigured root logger drops INFO entirely).

| Level | What you'll see |
|---|---|
| INFO | Cold-start stamp (python/sklearn/numpy versions, model shape, load ms per pickle), one line per request (`GET /predict status=200 elapsed_ms=41.2 rid=…`), one line per prediction (`predict prediction=>50K elapsed_ms=39.8 rid=…`) |
| WARNING | Input category outside the training vocabulary (feature name + count — the encoder zero-encodes it silently otherwise); sklearn version-drift warnings via `captureWarnings` |
| DEBUG | Full feature dict per request, per-column detail, inference timings (enable with env var `LOG_LEVEL=DEBUG`) |

Privacy rule: census features are demographic/protected attributes — feature
values are **never** logged at INFO, only at DEBUG (off in production).

Viewing logs: dashboard → Project → Logs (Live), or `npx vercel logs <url>`.
Retention is short (Hobby ~1h, Pro ~1d) — use a Log Drain for long retention.
Set `LOG_LEVEL` under Project → Settings → Environment Variables.

## 7. Test presets (UI and curl)

The `/ui/` page ships 5 one-click presets, verified against the trained model:

| # | Scenario | Expected |
|---|---|---|
| 1 | Rubric low income (25, Private, 11th grade) | `<=50K` |
| 2 | Rubric high income (52, Self-emp-inc, capital-gain 15024) | `>50K` |
| 3 | Typical row (37, Private, HS-grad) | `<=50K` |
| 4 | Senior with unknown (`?`) workclass/occupation, 12h/week | `<=50K` |
| 5 | Immigrant professional (45, Doctorate, India, capital-gain 5178) | `>50K` |

Equivalent curls are in the README; `python starter/query_live_api.py <url>`
runs presets 1–2 against any live deployment.

## 8. Troubleshooting

- **First request takes 2–6 s**: cold start (pandas+sklearn import dominates).
  The cold-start INFO stamp in the logs shows the exact cost. Subsequent
  requests are warm (Fluid compute reuses instances).
- **Preview URL returns 401**: Deployment Protection (default on) protects
  preview and per-deployment URLs. The **production alias is public**. Open
  previews in a browser logged into Vercel, or use a Protection Bypass for
  Automation header, or disable protection in Project Settings.
- **Framework preset not detected**: requires `fastapi` in the ROOT
  `requirements.txt`, a top-level `app` in root `app.py`, and CLI ≥ 48.1.8.
  Set Framework Preset to "FastAPI" manually in project settings if needed.
- **WARNING: value outside training vocabulary**: the request contained a
  category string the encoder never saw (typo/case/whitespace mismatch). The
  prediction still returns but is degraded — send byte-exact category values
  (see the dropdowns in `/ui/` for the full vocabulary).
- **InconsistentVersionWarning in logs**: the scikit-learn version no longer
  matches the one that trained the pickles — retrain or restore the
  `scikit-learn==1.7.2` pin.
- **413 on /predict**: request body exceeded Vercel's 4.5 MB limit (a normal
  payload is ~1 KB — this indicates a client bug).

## 9. Rollback

- **Instant rollback**: dashboard → Project → Deployments → previous
  production deployment → ⋯ → *Promote to Production*
  (or `npx vercel rollback`).
- **Git revert**: revert the bad commit on `master`; CI+CD redeploys the
  previous state once green.
- **Fallback**: the Render deployment
  (`https://census-income-api-l4cf.onrender.com`) is independent and
  unaffected by Vercel incidents.
