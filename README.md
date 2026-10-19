# CalFresh RMP Restaurant Finder

Enter any California ZIP code → get the hot-meal restaurants near it that accept EBT
through California's **Restaurant Meals Program (RMP)**, each with its popular orders
and typical prices.

## How it works

- **Vendor data (live):** the USDA Food and Nutrition Service's public SNAP retailer
  API — the same dataset behind the USDA retailer locator and the restaurant set the
  state points to. Filtered to `Store_Type = 'Restaurant Meals Program'`, `State = 'CA'`,
  searched in a radius around the ZIP via ArcGIS geometry query. No key, no sign-in.
- **ZIP → coordinates:** api.zippopotam.us (free, keyless). Falls back to an exact
  ZIP match against the USDA data if the geocoder is unreachable.
- **Menus & prices:** `data/chain_menus.json` — popular orders and *typical* California
  menu prices (compiled Oct 2026) for the chains that dominate the RMP vendor list
  (Subway, McDonald's, El Pollo Loco, Del Taco, Yoshinoya, WaBa Grill, … — 21 chains).
  Independent restaurants get a "check in store" note instead of made-up data.

## Run it

Just open `frontend/index.html` in a browser — it calls the public APIs directly.
If the browser blocks the cross-origin calls, run the bundled proxy instead:

```
python backend/proxy.py
# open http://localhost:5000/
```

The frontend automatically retries failed API calls through `/api/proxy`.

## Notes

- **Eligibility:** RMP hot meals on EBT are for CalFresh households where *every*
  member is 60+, disabled, or experiencing homelessness (spouses included).
- Vendor participation is per-location, not per-chain — a nearby McDonald's may
  participate while another doesn't. The USDA data is the authority; the state also
  publishes a [statewide spreadsheet](https://www.cdss.ca.gov/Portals/9/CalFresh/RMP/restaurant-list.xlsx).
- Prices are typical advertised prices at CA locations and change over time —
  always verify in store.
