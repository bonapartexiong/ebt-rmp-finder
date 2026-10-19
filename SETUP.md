# Setup Guide — EBT RMP Finder (local)

Get the app running on your own computer in a few minutes. No accounts, API keys,
or installs beyond what you already have.

## What you need

- **Git** ([git-scm.com](https://git-scm.com/downloads)) to download the code
- **Python 3** (only needed for the optional local server — check with `python3 --version`)
- A web browser

## 1. Download the code

```bash
git clone https://github.com/bonapartexiong/ebt-rmp-finder.git
cd ebt-rmp-finder
```

No dependencies to install — the app is a single HTML page plus a small JSON
menu file, and it calls public data APIs directly from your browser.

## 2. Run it (pick one)

**Option A — just open the file (easiest).**
Open `frontend/index.html` in your browser (double-click it, or
File → Open File). Enter a California ZIP code and hit Search.

**Option B — local server (use this if searches fail to load).**
Some browsers block the app's direct calls to the data APIs when the page is
opened as a file. The bundled server proxies those calls:

```bash
python3 backend/proxy.py
```

Then open <http://localhost:5000/> in your browser. Stop the server with
Ctrl+C when you're done.

## 3. Try it

1. Type a California ZIP code, e.g. `91006` (Arcadia).
2. Pick a radius (default 5 miles) and click **Search**.
3. Each result shows the restaurant name, address, distance, a directions link,
   and its popular orders with typical prices.

## Troubleshooting

| Problem | Fix |
|---|---|
| "Enter a 5-digit ZIP code" | ZIP must be exactly 5 digits, e.g. `91006` not `91006-1234`. |
| "covers California only" | This finder uses California's Restaurant Meals Program data. |
| Search spins then errors (Option A) | Your browser blocked the API calls — use Option B. |
| No restaurants found | Try a larger radius. Rural areas may genuinely have none nearby. |
| Prices look off | Prices are *typical* California menu prices compiled Oct 2026 — they vary by location. Verify in store. |

## Notes

- Vendor data is queried **live** from the USDA Food and Nutrition Service's
  public SNAP retailer API (the approved RMP vendor set), geocoded by ZIP via
  api.zippopotam.us. Nothing is stored or cached on your machine.
- RMP hot meals on EBT are for CalFresh households where **every** member is
  60+, disabled, or experiencing homelessness (spouses included).
- Participation is per restaurant location, not per chain — always look for the
  official RMP decal in the window.
