# CalFresh RMP Restaurant Finder

Enter any California ZIP code → get the hot-meal restaurants near it that accept EBT

**Live site:** https://bonapartexiong.github.io/ebt-rmp-finder/ (after enabling
GitHub Pages — see below).

## How it works

- **Vendor data (live):** the USDA Food and Nutrition Service's public SNAP retailer
  API — the same dataset behind the USDA retailer locator and the restaurant set the
  state points to. Filtered to `Store_Type = 'Restaurant Meals Program'`, `State = 'CA'`,
  searched in a radius around the ZIP via ArcGIS geometry query. No key, no sign-in.
- **ZIP → coordinates:** api.zippopotam.us (free, keyless). Falls back to an exact
  ZIP match against the USDA data if the geocoder is unreachable.
- **Map:** Leaflet + OpenStreetMap tiles (no API key). Markers show name/address/distance on hover; tap for details and a directions link. Business hours are not published in the public vendor dataset.

## Run it

Just open `index.html` in a browser — it calls the public APIs directly.
If the browser blocks the cross-origin calls, run the bundled proxy instead:

```
python backend/proxy.py
# open http://localhost:5000/
```

The frontend automatically retries failed API calls through `/api/proxy`.

## Publishing (GitHub Pages)

The app is a static site, so it can be published free with GitHub Pages —
`index.html` already sits at the repo root for this:

1. On GitHub, open the repo → **Settings** → **Pages**.
2. Under "Build and deployment", set Source to **Deploy from a branch**,
   Branch to **main**, folder to **/(root)** → Save.
3. After a minute or two the site is live at
   https://bonapartexiong.github.io/ebt-rmp-finder/

No backend needed — the page calls the USDA and Zippopotam APIs directly from
the visitor's browser (both allow cross-origin requests).

## Notes

- **Eligibility:** RMP hot meals on EBT are for CalFresh households where *every*
  member is 60+, disabled, or experiencing homelessness (spouses included).
- Vendor participation is per-location, not per-chain — a nearby McDonald's may
  participate while another doesn't. The USDA data is the authority; the state also
  publishes a [statewide spreadsheet](https://www.cdss.ca.gov/Portals/9/CalFresh/RMP/restaurant-list.xlsx).
