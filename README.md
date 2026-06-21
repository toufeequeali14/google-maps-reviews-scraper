# Google Maps Reviews Scraper

Scrape Google Maps reviews — ratings, text, owner replies, and dining details (food/service/atmosphere, noise level, group size) — for any business, just by entering its name and city.

## Requirements

```bash
pip install requests
```

## Setup

Google session cookies are required since this uses Google's internal endpoint, not a public API.

1. Open [Google Maps](https://www.google.com/maps), log in, and run any search.
2. In DevTools → Network, find a `google.com/search` request and copy its **Cookie** header.
3. Paste the relevant cookies into the `COOKIES` dict in the script.

Cookies expire periodically — refresh them if you start getting empty results.

## Usage

```bash
python google_maps_reviews_scraper.py
```

```
Restaurant name : Dishoom
City / country  : London
```

## Output

- `reviews_<query>.csv` — reviewer name, URL, rating, review text, reply, timestamps, food/service/atmosphere ratings, noise level, group size, etc.
- `place_<query>.json` — place name, address, overall rating, price range, website
- `raw_<query>.json` — full raw response, kept for debugging
