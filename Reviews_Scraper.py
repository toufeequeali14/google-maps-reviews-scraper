"""
Google Maps Reviews Scraper
Usage: python google_maps_reviews_scraper.py
Enter restaurant name and city/location when prompted.
"""

import requests
import re
import csv
import json
from urllib.parse import quote


# ─────────────────────────────────────────────
#  HTTP helpers
# ─────────────────────────────────────────────

COOKIES = {
    '__Secure-BUCKET': 'CJME',
    'AEC': 'AaJma5vp-G6hybgy-LoiXkKgVZgqOe-jM08l1EXCvWLWo21ZebkpRDUg4g',
    'NID': '532=t1DzEfzDgufGhHKkNfjdGfE-DC2muiyVULj-YDn5PUN9pQL5qUPGNQGDaaE9GZ8VOWqNwifHtbrMkSKOOlj6QavpuEkoWKqDLfCTVxPqocVHz7KdZYGWaFiDrdRO5XdyTLmp9vDAnLH7_1eQZZQqdVNDOGcsBkYBv82fI3PajF6Xwv-Pic8bFWLscWDcyiDsAOguD60f9smMknH6H1U9v9P8_YfFda3JXQaFfXj2VYdUJgXXQvEZpj2DzoKce4oguZnEfCQzw1rVt_MViHTXjmoIs3INqwKJL86SZkMgPNrJcnN5LSro6FmuEzC9_DoV7K9xPlGrf5OvyTLyyolY6Ra1SP1NwX9EMwJXLfks3T2O5xtMH4otBoZ2ntK5gfUXqCltPZt1d04SiQuHvdktBK4sskCziYsMieNBqgmt1ltHbLevrSMJsg',
    '__Secure-STRP': 'ANmZwa31Jp2zhHXp_J7t0GkZoUUNXIpocmnjMCf2IZIkgVoEls3pK4umMQU-ioDGEoH-HHzMqbXkSi5HB4qVheeGkUHX1eX-50JX',
}

HEADERS = {
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control': 'no-cache',
    'pragma': 'no-cache',
    'referer': 'https://www.google.com/',
    'user-agent': (
        'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/149.0.0.0 Safari/537.36'
    ),
}

PB_BLOB = (
    '!4m12!1m3!1d8178.7176775376565!2d73.0300416!3d33.68559355'
    '!2m3!1f0!2f0!3f0!3m2!1i1850!2i473!4f13.1!7i20!10b1'
    '!12m25!1m5!18b1!30b1!31m1!1b1!34e1!2m4!5m1!6e2!20e3!39b1'
    '!10b1!12b1!13b1!16b1!17m1!3e1!20m3!5e2!6b1!14b1!46m1!1b0'
    '!96b1!99b1!19m4!2m3!1i360!2i120!4i8'
    '!20m65!2m2!1i203!2i100!3m2!2i4!5b1!6m6!1m2!1i86!2i86'
    '!1m2!1i408!2i240!7m33!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2'
    '!1m3!1e2!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e10!2b0!3e3'
    '!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!1m3!1e9!2b1!3e2!2b1!9b0'
    '!15m16!1m7!1m2!1m1!1e2!2m2!1i195!2i195!3i20'
    '!1m7!1m2!1m1!1e2!2m2!1i195!2i195!3i20'
    '!22m6!1sJ-Inase2BpqRkdUP4PG0yQE%3A3'
    '!2s1i%3A0%2Ct%3A11886%2Cp%3AJ-Inase2BpqRkdUP4PG0yQE%3A3'
    '!7e81!12e5!17sJ-Inase2BpqRkdUP4PG0yQE%3A33!18e15'
    '!24m109!1m27!13m9!2b1!3b1!4b1!6i1!8b1!9b1!14b1!20b1!25b1'
    '!18m16!3b1!4b1!5b1!6b1!9b1!13b1!14b1!17b1!20b1!21b1!22b1'
    '!32b1!33m1!1b1!34b1!36e2!10m1!8e3!11m1!3e1!17b1'
    '!20m2!1e3!1e6!24b1!25b1!26b1!27b1!29b1!30m1!2b1!36b1!37b1'
    '!39m3!2m2!2i1!3i1!43b1!52b1!54m1!1b1!55b1!56m1!1b1'
    '!61m2!1m1!1e1!65m5!3m4!1m3!1m2!1i224!2i298'
    '!72m22!1m8!2b1!5b1!7b1!12m4!1b1!2b1!4m1!1e1!4b1'
    '!8m10!1m6!4m1!1e1!4m1!1e3!4m1!1e4'
    '!3sother_user_google_review_posts__and__hotel_and_vr_partner_review_posts'
    '!6m1!1e1!9b1!89b1!90m2!1m1!1e2!98m3!1b1!2b1!3b1'
    '!103b1!113b1!114m3!1b1!2m1!1b1!117b1!122m1!1b1'
    '!126b1!127b1!128m1!1b0!26m4!2m3!1i80!2i92!4i8'
    '!30m28!1m6!1m2!1i0!2i0!2m2!1i530!2i473'
    '!1m6!1m2!1i1800!2i0!2m2!1i1850!2i473'
    '!1m6!1m2!1i0!2i0!2m2!1i1850!2i20'
    '!1m6!1m2!1i0!2i453!2m2!1i1850!2i473'
    '!34m19!2b1!3b1!4b1!6b1!8m6!1b1!3b1!4b1!5b1!6b1!7b1'
    '!9b1!12b1!14b1!20b1!23b1!25b1!26b1!31b1!37m1!1e81'
    '!42b1!47m0!49m10!3b1!6m2!1b1!2b1!7m2!1e3!2b1!8b1!9b1!10e2'
    '!50m4!2e2!3m2!1b1!3b1!67m5!7b1!10b1!14b1!15m1!1b0!69i782!77b1'
)


def fetch_maps_data(query: str) -> str | None:
    """Fire the Google Maps search request and return raw response text."""
    encoded = quote(query)
    url = (
        f'https://www.google.com/search?tbm=map&authuser=0&hl=en'
        f'&pb={PB_BLOB}'
        f'&q={encoded}&oq={encoded}'
        f'&gs_l=maps.3..38i426k1.2204.4415.1.5757.2.2.....293.507.2-2.2.....0....1..maps..0.1.302.0.'
        f'&tch=1&ech=1&psi=J-Inase2BpqRkdUP4PG0yQE.1780998696175.1'
    )
    try:
        resp = requests.get(url, cookies=COOKIES, headers=HEADERS, timeout=20)
        if resp.status_code == 200:
            return resp.text
        print(f'  [!] HTTP {resp.status_code}')
    except requests.RequestException as exc:
        print(f'  [!] Request error: {exc}')
    return None


# ─────────────────────────────────────────────
#  Place-level metadata parser
# ─────────────────────────────────────────────

def parse_place_info(raw: str) -> dict:
    """Extract high-level place info from the response."""
    info = {
        'place_name': '', 'address': '', 'overall_rating': '',
        'total_reviews': '', 'price_range': '', 'website': '',
        'place_id': '', 'categories': '',
    }

    # Parse the wrapper to get inner data
    data = _parse_response(raw)
    if data is None:
        return info

    # Overall rating and total review count
    rating_match = re.search(r',null,(\d+\.\d+),(\d+),\[', raw)
    if rating_match:
        info['overall_rating'] = rating_match.group(1)
        info['total_reviews'] = rating_match.group(2)

    # Place name
    name_match = re.search(r'\[\[\"([^"]{3,80})\",\[\[null,null,null', raw)
    if name_match:
        info['place_name'] = name_match.group(1)

    # Address
    addr_match = re.search(
        r'"(\d+[^"]{5,80}(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Drive|Dr|Way|Gardens?|Garden|Square|Sq)[^"]{0,60})"',
        raw
    )
    if addr_match:
        info['address'] = addr_match.group(1)

    # Price range
    price_match = re.search(r'"(£\d+[–-]\d+)"', raw)
    if price_match:
        info['price_range'] = price_match.group(1)

    # Website
    web_match = re.search(
        r'"(https?://(?!(?:lh3|streetview|www\.google|maps\.google))[^"]{5,100})"',
        raw
    )
    if web_match:
        info['website'] = web_match.group(1)

    # Place ID
    pid_match = re.search(r'"(ChIJ[A-Za-z0-9_-]{10,})"', raw)
    if pid_match:
        info['place_id'] = pid_match.group(1)

    # Categories
    cat_matches = re.findall(
        r'"(Steak house|Restaurant|Cafe|Bar|Bakery|Pizza|Sushi|Indian|Chinese|'
        r'Italian|Thai|Mexican|French|Japanese|Korean|Halal|Vegan|Vegetarian|'
        r'Fast food|Burger|Coffee shop)"', raw
    )
    info['categories'] = ', '.join(dict.fromkeys(cat_matches))

    return info


# ─────────────────────────────────────────────
#  JSON response parser
# ─────────────────────────────────────────────

def _parse_response(raw: str):
    """Parse the Google Maps JSON response and return the inner data array."""
    # Find the first complete JSON object (handles trailing comments like /*""*/)
    depth = 0
    in_string = False
    escape_next = False
    end_pos = len(raw)
    
    for i, ch in enumerate(raw):
        if escape_next:
            escape_next = False
            continue
        if ch == '\\':
            escape_next = True
            continue
        if ch == '"' and not escape_next:
            in_string = not in_string
            continue
        if not in_string:
            if ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    end_pos = i + 1
                    break
    
    try:
        wrapper = json.loads(raw[:end_pos])
    except json.JSONDecodeError:
        return None
    
    d = wrapper.get('d', '')
    if d.startswith(")]}'"):
        d = d[4:].lstrip('\n')
    
    try:
        return json.loads(d)
    except json.JSONDecodeError:
        return None


# def _find_review_batches(data):
#     """Recursively search for review batch arrays in the parsed data."""
#     if isinstance(data, list):
#         # Check if this looks like review batches
#         if len(data) > 0 and isinstance(data[0], list):
#             if len(data[0]) > 0 and isinstance(data[0][0], list):
#                 if len(data[0][0]) > 0:
#                     first = data[0][0][0] if isinstance(data[0][0], list) else None
#                     if isinstance(first, list) and len(first) >= 2:
#                         if isinstance(first[1], list) and len(first[1]) >= 10:
#                             return data
#         # Recurse into sublists
#         for item in data:
#             result = _find_review_batches(item)
#             if result:
#                 return result
#     elif isinstance(data, dict):
#         for v in data.values():
#             result = _find_review_batches(v)
#             if result:
#                 return result
#     return None

def _find_review_batches(data):
    """Find review batch arrays in the parsed data."""
    # Try the known path first: data[0][1][0][14][175][9][0][0]
    try:
        batches = data[0][1][0][14][175][9][0][0]
        if isinstance(batches, list) and len(batches) > 0:
            # Verify it contains valid review data
            first_batch = batches[0]
            if first_batch and isinstance(first_batch, list) and len(first_batch) > 0:
                first_review = first_batch[0]
                if first_review and isinstance(first_review, list) and len(first_review) >= 2:
                    rdata = first_review[1]
                    if isinstance(rdata, list) and len(rdata) >= 10:
                        return batches
    except (IndexError, TypeError):
        pass
    
    # Fallback: recursive search
    def search(obj, depth=0):
        if depth > 15:
            return None
        if isinstance(obj, list) and len(obj) > 0:
            if isinstance(obj[0], list) and len(obj[0]) > 0:
                first = obj[0][0] if isinstance(obj[0], list) else None
                if isinstance(first, list) and len(first) >= 2:
                    rdata = first[1]
                    if isinstance(rdata, list) and len(rdata) >= 10:
                        return obj
            for item in obj:
                result = search(item, depth + 1)
                if result:
                    return result
        return None
    
    return search(data)


# ─────────────────────────────────────────────
#  Review parser (JSON-based)
# ─────────────────────────────────────────────

def parse_reviews(raw: str) -> list[dict]:
    """Extract all reviews using JSON parsing."""
    data = _parse_response(raw)
    if data is None:
        return []
    
    # Find the review batches
    batches = _find_review_batches(data)
    if batches is None:
        print('  ⚠️  Could not find review batches in response')
        return []
    
    reviews = []
    
    for batch in batches:
        if not batch:
            continue
        for review in batch:
            # Skip None, non-lists, and invalid structures
            if not review:
                continue
            if not isinstance(review, list) or len(review) < 2:
                continue
            rdata = review[1]
            if not isinstance(rdata, list) or len(rdata) < 10:
                continue
            
            r = {
                'reviewer_name': '', 'reviewer_url': '', 'reviewer_reviews': '',
                'rating': '', 'relative_time': '', 'timestamp_ms': '',
                'review_text': '', 'language': 'en',
                'reply_text': '', 'reply_time': '',
                'price_range': '', 'food_rating': '', 'service_rating': '',
                'atmosphere_rating': '', 'noise_level': '',
                'group_size': '', 'special_events': '', 'vegetarian_friendly': ''
            }
            
            # Rating: rdata[13][4]
            if len(rdata) > 13 and isinstance(rdata[13], list) and len(rdata[13]) > 4:
                r['rating'] = rdata[13][4]
            
            # Time: rdata[6]
            if len(rdata) > 6 and rdata[6]:
                r['relative_time'] = rdata[6]
            
            # Timestamp: rdata[2]
            if len(rdata) > 2 and rdata[2]:
                r['timestamp_ms'] = rdata[2]
            
            # Reviewer info
            if len(rdata) > 4 and rdata[4] and isinstance(rdata[4], list):
                # URL: rdata[4][2][0]
                if len(rdata[4]) > 2 and rdata[4][2] and isinstance(rdata[4][2], list) and rdata[4][2]:
                    r['reviewer_url'] = str(rdata[4][2][0])
                # Name & count: rdata[4][5]
                if len(rdata[4]) > 5 and rdata[4][5] and isinstance(rdata[4][5], list):
                    ri = rdata[4][5]
                    if len(ri) > 0 and ri[0]:
                        r['reviewer_name'] = str(ri[0])
                    if len(ri) > 5 and ri[5]:
                        r['reviewer_reviews'] = ri[5]
            
            # Review text via JSON dump + regex
            review_str = json.dumps(review)
            match = re.search(r'\["en"\],\s*\[\["((?:[^"\\]|\\.)*)"', review_str)
            if match:
                text = match.group(1)
                text = text.replace('\\n', '\n').replace('\\"', '"').replace('\\u003d', '=')
                text = text.replace('\\u200b', '').replace('\\u2014', '—').replace('\\u2019', "'")
                r['review_text'] = text
            
            # Reply text (second match)
            matches = list(re.finditer(r'\["en"\],\s*\[\["((?:[^"\\]|\\.)*)"', review_str))
            if len(matches) > 1:
                reply = matches[1].group(1).replace('\\n', '\n').replace('\\"', '"')
                r['reply_text'] = reply
            
            reviews.append(r)
    
    return reviews


# ─────────────────────────────────────────────
#  CSV output
# ─────────────────────────────────────────────

REVIEW_FIELDS = [
    'reviewer_name', 'reviewer_url', 'reviewer_reviews',
    'rating', 'relative_time', 'timestamp_ms', 'review_text', 'language',
    'reply_text', 'reply_time',
    'price_range', 'food_rating', 'service_rating', 'atmosphere_rating',
    'noise_level', 'group_size', 'special_events', 'vegetarian_friendly'
]


def save_reviews_csv(reviews: list[dict], path: str) -> None:
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=REVIEW_FIELDS, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(reviews)
    print(f'  💾 Saved {len(reviews)} reviews → {path}')


def save_place_json(info: dict, path: str) -> None:
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(info, f, indent=2, ensure_ascii=False)
    print(f'  💾 Place info → {path}')


# ─────────────────────────────────────────────
#  Main
# ─────────────────────────────────────────────

def scrape(restaurant_name: str, location: str) -> list[dict]:
    query = f'{restaurant_name} {location}'
    safe = re.sub(r'[^\w\s-]', '', query).strip().replace(' ', '_')

    print(f'\n🔍  Searching: "{query}"')

    raw = fetch_maps_data(query)
    if not raw:
        print('❌  Failed to fetch data.')
        return []

    print('✅  Data fetched.')

    # Save raw response for debugging
    raw_path = f'raw_{safe}.json'
    with open(raw_path, 'w', encoding='utf-8') as f:
        f.write(raw)
    print(f'  📄 Raw response → {raw_path}')

    # Parse place info
    place = parse_place_info(raw)
    if place['place_name']:
        print(f'\n📍 Place: {place["place_name"]}')
        print(f'   Address : {place["address"] or "—"}')
        print(f'   Rating  : {place["overall_rating"]} ({place["total_reviews"]} reviews)')
        print(f'   Price   : {place["price_range"] or "—"}')
        print(f'   Website : {place["website"] or "—"}')
        save_place_json(place, f'place_{safe}.json')

    # Parse reviews
    print('\n📊  Parsing reviews…')
    reviews = parse_reviews(raw)

    if not reviews:
        print('⚠️   No reviews found. Cookies may have expired or place not resolved.')
        return []

    print(f'  ✅  {len(reviews)} reviews extracted.')

    # Preview first 5
    for i, r in enumerate(reviews[:5], 1):
        stars = '★' * (r['rating'] or 0) + '☆' * (5 - (r['rating'] or 0))
        print(f'\n  ── Review {i} ──')
        print(f'  Name   : {r["reviewer_name"]} ({r["reviewer_reviews"]} reviews)')
        print(f'  Rating : {stars}  ({r["relative_time"]})')
        preview = (r['review_text'] or '').replace('\n', ' ')[:200]
        print(f'  Text   : {preview}…')
        if r['reply_text']:
            rp = r['reply_text'][:100].replace('\n', ' ')
            print(f'  Reply  : {rp}…')

    # Save CSV
    csv_path = f'reviews_{safe}.csv'
    save_reviews_csv(reviews, csv_path)

    return reviews


def main():
    print('=' * 50)
    print('   Google Maps Reviews Scraper')
    print('=' * 50)
    restaurant = input('\nRestaurant name : ').strip()
    location = input('City / country  : ').strip()

    if not restaurant or not location:
        print('❌  Both fields are required.')
        return

    reviews = scrape(restaurant, location)
    if reviews:
        print(f'\n🎉  Done — {len(reviews)} reviews scraped.')
    else:
        print('\n💡  Tip: if you got 0 reviews, refresh the cookies in COOKIES dict.')


if __name__ == '__main__':
    main()



















# """
# Google Maps Reviews Scraper - Updated Parser
# Key patterns identified:
# - Review blocks start with: ["Ci..." or ["Ch...", ["0x...
# - Reviewer name: after "https://lh3.googleusercontent.com/a..." pattern
# - Review text: in ["en"], [["TEXT HERE" pattern
# """

# import requests
# import re
# import csv
# import json
# from urllib.parse import quote


# # ─────────────────────────────────────────────
# #  HTTP helpers
# # ─────────────────────────────────────────────

# COOKIES = {
#     '__Secure-BUCKET': 'CJME',
#     'AEC': 'AaJma5vp-G6hybgy-LoiXkKgVZgqOe-jM08l1EXCvWLWo21ZebkpRDUg4g',
#     'NID': '532=t1DzEfzDgufGhHKkNfjdGfE-DC2muiyVULj-YDn5PUN9pQL5qUPGNQGDaaE9GZ8VOWqNwifHtbrMkSKOOlj6QavpuEkoWKqDLfCTVxPqocVHz7KdZYGWaFiDrdRO5XdyTLmp9vDAnLH7_1eQZZQqdVNDOGcsBkYBv82fI3PajF6Xwv-Pic8bFWLscWDcyiDsAOguD60f9smMknH6H1U9v9P8_YfFda3JXQaFfXj2VYdUJgXXQvEZpj2DzoKce4oguZnEfCQzw1rVt_MViHTXjmoIs3INqwKJL86SZkMgPNrJcnN5LSro6FmuEzC9_DoV7K9xPlGrf5OvyTLyyolY6Ra1SP1NwX9EMwJXLfks3T2O5xtMH4otBoZ2ntK5gfUXqCltPZt1d04SiQuHvdktBK4sskCziYsMieNBqgmt1ltHbLevrSMJsg',
#     '__Secure-STRP': 'ANmZwa31Jp2zhHXp_J7t0GkZoUUNXIpocmnjMCf2IZIkgVoEls3pK4umMQU-ioDGEoH-HHzMqbXkSi5HB4qVheeGkUHX1eX-50JX',
# }

# HEADERS = {
#     'accept': '*/*',
#     'accept-language': 'en-US,en;q=0.9',
#     'cache-control': 'no-cache',
#     'pragma': 'no-cache',
#     'referer': 'https://www.google.com/',
#     'user-agent': (
#         'Mozilla/5.0 (X11; Ubuntu; Linux x86_64) '
#         'AppleWebKit/537.36 (KHTML, like Gecko) '
#         'Chrome/149.0.0.0 Safari/537.36'
#     ),
# }

# PB_BLOB = (
#     '!4m12!1m3!1d8178.7176775376565!2d73.0300416!3d33.68559355'
#     '!2m3!1f0!2f0!3f0!3m2!1i1850!2i473!4f13.1!7i20!10b1'
#     '!12m25!1m5!18b1!30b1!31m1!1b1!34e1!2m4!5m1!6e2!20e3!39b1'
#     '!10b1!12b1!13b1!16b1!17m1!3e1!20m3!5e2!6b1!14b1!46m1!1b0'
#     '!96b1!99b1!19m4!2m3!1i360!2i120!4i8'
#     '!20m65!2m2!1i203!2i100!3m2!2i4!5b1!6m6!1m2!1i86!2i86'
#     '!1m2!1i408!2i240!7m33!1m3!1e1!2b0!3e3!1m3!1e2!2b1!3e2'
#     '!1m3!1e2!2b0!3e3!1m3!1e8!2b0!3e3!1m3!1e10!2b0!3e3'
#     '!1m3!1e10!2b1!3e2!1m3!1e10!2b0!3e4!1m3!1e9!2b1!3e2!2b1!9b0'
#     '!15m16!1m7!1m2!1m1!1e2!2m2!1i195!2i195!3i20'
#     '!1m7!1m2!1m1!1e2!2m2!1i195!2i195!3i20'
#     '!22m6!1sJ-Inase2BpqRkdUP4PG0yQE%3A3'
#     '!2s1i%3A0%2Ct%3A11886%2Cp%3AJ-Inase2BpqRkdUP4PG0yQE%3A3'
#     '!7e81!12e5!17sJ-Inase2BpqRkdUP4PG0yQE%3A33!18e15'
#     '!24m109!1m27!13m9!2b1!3b1!4b1!6i1!8b1!9b1!14b1!20b1!25b1'
#     '!18m16!3b1!4b1!5b1!6b1!9b1!13b1!14b1!17b1!20b1!21b1!22b1'
#     '!32b1!33m1!1b1!34b1!36e2!10m1!8e3!11m1!3e1!17b1'
#     '!20m2!1e3!1e6!24b1!25b1!26b1!27b1!29b1!30m1!2b1!36b1!37b1'
#     '!39m3!2m2!2i1!3i1!43b1!52b1!54m1!1b1!55b1!56m1!1b1'
#     '!61m2!1m1!1e1!65m5!3m4!1m3!1m2!1i224!2i298'
#     '!72m22!1m8!2b1!5b1!7b1!12m4!1b1!2b1!4m1!1e1!4b1'
#     '!8m10!1m6!4m1!1e1!4m1!1e3!4m1!1e4'
#     '!3sother_user_google_review_posts__and__hotel_and_vr_partner_review_posts'
#     '!6m1!1e1!9b1!89b1!90m2!1m1!1e2!98m3!1b1!2b1!3b1'
#     '!103b1!113b1!114m3!1b1!2m1!1b1!117b1!122m1!1b1'
#     '!126b1!127b1!128m1!1b0!26m4!2m3!1i80!2i92!4i8'
#     '!30m28!1m6!1m2!1i0!2i0!2m2!1i530!2i473'
#     '!1m6!1m2!1i1800!2i0!2m2!1i1850!2i473'
#     '!1m6!1m2!1i0!2i0!2m2!1i1850!2i20'
#     '!1m6!1m2!1i0!2i453!2m2!1i1850!2i473'
#     '!34m19!2b1!3b1!4b1!6b1!8m6!1b1!3b1!4b1!5b1!6b1!7b1'
#     '!9b1!12b1!14b1!20b1!23b1!25b1!26b1!31b1!37m1!1e81'
#     '!42b1!47m0!49m10!3b1!6m2!1b1!2b1!7m2!1e3!2b1!8b1!9b1!10e2'
#     '!50m4!2e2!3m2!1b1!3b1!67m5!7b1!10b1!14b1!15m1!1b0!69i782!77b1'
# )


# def fetch_maps_data(query: str) -> str | None:
#     """Fetch Google Maps search data for a given query."""
#     encoded = quote(query)
#     url = (
#         f'https://www.google.com/search?tbm=map&authuser=0&hl=en'
#         f'&pb={PB_BLOB}'
#         f'&q={encoded}&oq={encoded}'
#         f'&gs_l=maps.3..38i426k1.2204.4415.1.5757.2.2.....293.507.2-2.2.....0....1..maps..0.1.302.0.'
#         f'&tch=1&ech=1&psi=J-Inase2BpqRkdUP4PG0yQE.1780998696175.1'
#     )
#     try:
#         resp = requests.get(url, cookies=COOKIES, headers=HEADERS, timeout=20)
#         if resp.status_code == 200:
#             return resp.text
#         print(f'  [!] HTTP {resp.status_code}')
#     except requests.RequestException as exc:
#         print(f'  [!] Request error: {exc}')
#     return None


# # ─────────────────────────────────────────────
# #  Place-level metadata parser
# # ─────────────────────────────────────────────

# def parse_place_info(raw: str) -> dict:
#     """Extract restaurant metadata from the response."""
#     info = {
#         'place_name': '',
#         'address': '',
#         'overall_rating': '',
#         'total_reviews': '',
#         'price_range': '',
#         'website': '',
#         'place_id': '',
#         'categories': '',
#     }

#     # Overall rating and total review count
#     rating_match = re.search(r',null,(\d+\.\d+),(\d+),\[', raw)
#     if rating_match:
#         info['overall_rating'] = rating_match.group(1)
#         info['total_reviews'] = rating_match.group(2)

#     # Place name
#     name_match = re.search(r'\[\[\"([^"]{3,80})\",\[\[null,null,null', raw)
#     if name_match:
#         info['place_name'] = name_match.group(1)

#     # Address - look for UK-style addresses
#     addr_match = re.search(r'"(\d+[^"]{10,80}(?:Street|St|Road|Rd|Avenue|Ave|Lane|Ln|Drive|Dr|Way|Gardens?|Square|Sq|London)[^"]{0,60})"', raw)
#     if addr_match:
#         info['address'] = addr_match.group(1)

#     # Price range
#     price_match = re.search(r'"(£\d+[–-]\d+)"', raw)
#     if price_match:
#         info['price_range'] = price_match.group(1)

#     # Website (exclude Google domains)
#     web_match = re.search(r'"(https?://(?!(?:lh3|streetview|www\.google|maps\.google))[^"]{5,100})"', raw)
#     if web_match:
#         info['website'] = web_match.group(1)

#     # Place ID
#     pid_match = re.search(r'"(ChIJ[A-Za-z0-9_-]{10,})"', raw)
#     if pid_match:
#         info['place_id'] = pid_match.group(1)

#     # Categories
#     cat_matches = re.findall(
#         r'"(Steak house|Restaurant|Cafe|Bar|Bakery|Pizza|Sushi|Indian|Chinese|Italian|Thai|Mexican|French|Japanese|Korean|Halal|Vegan|Vegetarian|Fast food|Burger|Coffee shop)"',
#         raw
#     )
#     info['categories'] = ', '.join(dict.fromkeys(cat_matches))

#     return info


# # ─────────────────────────────────────────────
# #  Individual review parser
# # ─────────────────────────────────────────────

# def extract_review(block: str) -> dict | None:
#     """Parse a single review block into a structured dict."""
#     review = {
#         'reviewer_name': '',
#         'reviewer_url': '',
#         'reviewer_reviews': '',
#         'rating': '',
#         'relative_time': '',
#         'timestamp_ms': '',
#         'review_text': '',
#         'language': 'en',
#         'reply_text': '',
#         'reply_time': '',
#         'price_range': '',
#         'food_rating': '',
#         'service_rating': '',
#         'atmosphere_rating': '',
#         'noise_level': '',
#         'group_size': '',
#         'special_events': '',
#         'vegetarian_friendly': ''
#     }

#     try:
#         # Reviewer name (after Google photo URL pattern)
#         name_match = re.search(
#             r'\["([^"]+)",\s*"https://lh3\.googleusercontent\.com/a[^"]*"', block
#         )
#         if name_match:
#             review['reviewer_name'] = name_match.group(1)

#         # Reviewer profile URL
#         url_match = re.search(
#             r'"(https://www\.google\.com/maps/contrib/\d+/reviews\?hl=en)"', block
#         )
#         if url_match:
#             review['reviewer_url'] = url_match.group(1)

#         # Review count
#         reviews_match = re.search(r'"(\d+) reviews?"', block)
#         if reviews_match:
#             review['reviewer_reviews'] = int(reviews_match.group(1))

#         # Star rating
#         rating_match = re.search(r'\[\[(\d)\],\s*null,\s*\[', block)
#         if rating_match:
#             review['rating'] = int(rating_match.group(1))

#         # Timestamp (13-digit, valid range 2020-2030)
#         for ts in re.findall(r'(\d{13})', block):
#             ts_int = int(ts)
#             if 1577836800000 < ts_int < 1893456000000:
#                 review['timestamp_ms'] = ts_int
#                 break

#         # Relative time
#         time_match = re.search(
#             r'"(\d+\s+(?:months?|years?|weeks?|days?|hours?|minutes?)\s+ago)"', block
#         )
#         if time_match:
#             review['relative_time'] = time_match.group(1)

#         # Review text - first ["en"] block
#         text_matches = list(
#             re.finditer(r'\["en"\],\s*\[\["((?:[^"\\]|\\[^"])*)"', block, re.DOTALL)
#         )
#         if text_matches:
#             review['review_text'] = _clean_text(text_matches[0].group(1))

#         # Owner reply - second ["en"] block if present
#         if len(text_matches) > 1:
#             review['reply_text'] = _clean_text(text_matches[1].group(1))
#             # Reply time
#             reply_times = re.findall(
#                 r'"(\d+\s+(?:months?|years?|weeks?|days?)\s+ago)"', block
#             )
#             if len(reply_times) > 1:
#                 review['reply_time'] = reply_times[1]

#         # Price range
#         price_match = re.search(r'"E:GBP_(\d+)_TO_(\d+)"', block)
#         if price_match:
#             review['price_range'] = f'£{price_match.group(1)}–{price_match.group(2)}'

#         # Food rating
#         food_match = re.search(r'"Food",\s*null,\s*null,\s*null,\s*null,\s*\[(\d)\]', block)
#         if food_match:
#             review['food_rating'] = int(food_match.group(1))

#         # Service rating
#         service_match = re.search(r'"Service",\s*null,\s*null,\s*null,\s*null,\s*\[(\d)\]', block)
#         if service_match:
#             review['service_rating'] = int(service_match.group(1))

#         # Atmosphere rating
#         atmosphere_match = re.search(r'"Atmosphere",\s*null,\s*null,\s*null,\s*null,\s*\[(\d)\]', block)
#         if atmosphere_match:
#             review['atmosphere_rating'] = int(atmosphere_match.group(1))

#         # Noise level
#         noise_match = re.search(r'"E:(DINING_NOISE_LEVEL_\w+)"', block)
#         if noise_match:
#             review['noise_level'] = (
#                 noise_match.group(1)
#                 .replace('DINING_NOISE_LEVEL_', '')
#                 .replace('_', ' ')
#                 .title()
#             )

#         # Group size
#         group_match = re.search(r'"E:(DINING_GROUP_SIZE_\w+)"', block)
#         if group_match:
#             review['group_size'] = (
#                 group_match.group(1)
#                 .replace('DINING_GROUP_SIZE_', '')
#                 .replace('_', ' ')
#                 .title()
#             )

#         # Special events
#         events_match = re.search(r'"E:(DINING_SPECIAL_EVENTS_\w+)"', block)
#         if events_match:
#             review['special_events'] = (
#                 events_match.group(1)
#                 .replace('DINING_SPECIAL_EVENTS_', '')
#                 .replace('_', ' ')
#                 .title()
#             )

#         # Vegetarian friendly
#         veg_match = re.search(r'"E:(HIGHLY_RECOMMEND|RECOMMEND|NOT_RECOMMEND)"', block)
#         if veg_match:
#             review['vegetarian_friendly'] = (
#                 veg_match.group(1)
#                 .replace('_', ' ')
#                 .title()
#             )

#         return review if review['reviewer_name'] else None

#     except Exception as exc:
#         print(f'    [!] Error extracting review: {exc}')
#         return None


# def _clean_text(text: str) -> str:
#     """Clean escaped characters in review text."""
#     return (
#         text.replace('\\n', '\n')
#             .replace('\\"', '"')
#             .replace('\\u003d', '=')
#             .replace('\\u0026', '&')
#             .replace('\\u003c', '<')
#             .replace('\\u003e', '>')
#     )


# # ─────────────────────────────────────────────
# #  Review list parser
# # ─────────────────────────────────────────────

# def parse_reviews(raw: str) -> list[dict]:
#     """Extract all reviews from the raw response text."""
#     reviews = []

#     # Review blocks start with: ["Ci..." or ["Ch...", ["0x...
#     pattern = re.compile(
#         r'\["(?:Ci|Ch)[A-Za-z0-9_-]+",\s*\["0x[0-9a-f:]+",',
#         re.DOTALL,
#     )

#     starts = [m.start() for m in pattern.finditer(raw)]
#     if not starts:
#         print('  ⚠️  No review blocks found with primary pattern')
#         return reviews

#     for i, start in enumerate(starts):
#         end = starts[i + 1] if i + 1 < len(starts) else len(raw)
#         block = raw[start:end]
#         review = extract_review(block)
#         if review:
#             reviews.append(review)

#     # Deduplicate
#     seen, unique = set(), []
#     for r in reviews:
#         key = r['review_text'][:120] if r['review_text'] else ''
#         if key not in seen:
#             seen.add(key)
#             unique.append(r)

#     return unique


# # ─────────────────────────────────────────────
# #  CSV output
# # ─────────────────────────────────────────────

# REVIEW_FIELDS = [
#     'reviewer_name', 'reviewer_url', 'reviewer_reviews', 'rating',
#     'relative_time', 'timestamp_ms', 'review_text', 'language',
#     'reply_text', 'reply_time', 'price_range', 'food_rating',
#     'service_rating', 'atmosphere_rating', 'noise_level',
#     'group_size', 'special_events', 'vegetarian_friendly'
# ]


# def save_reviews_csv(reviews: list[dict], path: str) -> None:
#     """Save reviews to CSV file."""
#     with open(path, 'w', newline='', encoding='utf-8') as f:
#         writer = csv.DictWriter(f, fieldnames=REVIEW_FIELDS, extrasaction='ignore')
#         writer.writeheader()
#         writer.writerows(reviews)
#     print(f'  💾 Saved {len(reviews)} reviews → {path}')


# def save_place_json(info: dict, path: str) -> None:
#     """Save place info to JSON file."""
#     with open(path, 'w', encoding='utf-8') as f:
#         json.dump(info, f, indent=2, ensure_ascii=False)
#     print(f'  💾 Place info → {path}')


# # ─────────────────────────────────────────────
# #  Main
# # ─────────────────────────────────────────────

# def scrape(restaurant_name: str, location: str) -> list[dict]:
#     """Main scraping function."""
#     query = f'{restaurant_name} {location}'
#     safe = re.sub(r'[^\w\s-]', '', query).strip().replace(' ', '_')

#     print(f'\n🔍  Searching: "{query}"')

#     raw = fetch_maps_data(query)
#     if not raw:
#         print('❌  Failed to fetch data.')
#         return []

#     print('✅  Data fetched.')

#     # Save raw response
#     raw_path = f'raw_{safe}.json'
#     with open(raw_path, 'w', encoding='utf-8') as f:
#         f.write(raw)
#     print(f'  📄 Raw response → {raw_path}')

#     # Parse place info
#     place = parse_place_info(raw)
#     if place['place_name']:
#         print(f'\n📍 Place: {place["place_name"]}')
#         print(f'   Address : {place["address"] or "—"}')
#         print(f'   Rating  : {place["overall_rating"]} ({place["total_reviews"]} reviews)')
#         print(f'   Price   : {place["price_range"] or "—"}')
#         print(f'   Website : {place["website"] or "—"}')
#         save_place_json(place, f'place_{safe}.json')

#     # Parse reviews
#     print('\n📊  Parsing reviews…')
#     reviews = parse_reviews(raw)

#     if not reviews:
#         print('⚠️   No reviews found.')
#         return []

#     print(f'  ✅  {len(reviews)} reviews extracted.')

#     # Preview
#     for i, r in enumerate(reviews[:3], 1):
#         stars = '★' * (r['rating'] or 0) + '☆' * (5 - (r['rating'] or 0))
#         print(f'\n  ── Review {i} ──')
#         print(f'  Name   : {r["reviewer_name"]}')
#         print(f'  Rating : {stars}  ({r["relative_time"]})')
#         preview = (r['review_text'] or '').replace('\n', ' ')[:150]
#         print(f'  Text   : {preview}…')

#     # Save CSV
#     csv_path = f'reviews_{safe}.csv'
#     save_reviews_csv(reviews, csv_path)

#     return reviews


# def main():
#     print('=' * 50)
#     print('   Google Maps Reviews Scraper')
#     print('=' * 50)
#     restaurant = input('\nRestaurant name : ').strip()
#     location = input('City / country  : ').strip()

#     if not restaurant or not location:
#         print('❌  Both fields are required.')
#         return

#     reviews = scrape(restaurant, location)
#     if reviews:
#         print(f'\n🎉  Done — {len(reviews)} reviews scraped.')
#     else:
#         print('\n💡  Tip: If no reviews found, refresh cookies.')


# if __name__ == '__main__':
#     main()