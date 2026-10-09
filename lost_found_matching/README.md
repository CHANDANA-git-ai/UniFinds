# AI Lost & Found — Person 3 Module

A standalone Python backend for persisting LOST/FOUND reports and ranking likely matches. It is deliberately UI-independent: a future Streamlit form can call `create_report(**fields)`, then its results page can call `find_matches(report_id, top_k=5)`.

## Pipeline

`SQLite → active opposite-type reports → CLIP image similarity + MiniLM semantic text similarity + attributes + Haversine location + event time → normalized weighted score → confidence/explanation → ranked results`

The database contains `reports` (LOST/FOUND and ACTIVE/MATCHED/CLOSED) and `matches` (per-feature scores plus final result). SQL parameters are used for all data values.

## Scores

Default weights: image 40%, text 25%, attributes 15%, location 15%, time 5%. Scores are 0–100 and are reweighted across available features; missing image, coordinates, date, or time does not count as a zero. Confidence is HIGH at 80+, MEDIUM at 60+, otherwise LOW.

Text uses `sentence-transformers/all-MiniLM-L6-v2`, cached after first use. If unavailable it safely falls back to TF-IDF cosine similarity. Images use cached `openai/clip-vit-base-patch32`; unavailable/missing/corrupt images are omitted from scoring rather than invented. Location uses Haversine distance (linear falloff to zero at 50 km, configurable). Time falls off linearly to zero at 168 hours.

## Run

```bash
python -m pip install -r requirements.txt
python -m lost_found_matching.demo
python -m pytest lost_found_matching/tests -q
```

The first semantic/image comparison may download pretrained model weights. The seeded demo covers close and far wallets, different objects, missing coordinates/images, and multiple candidates. The `database/lost_found.db` file is created automatically.

## Layout

- `database/`: schema and parameterized SQLite repository
- `services/`: frontend-friendly report operations
- `matching/`: isolated feature matchers, scoring, ranker, and orchestration
- `models/`: report contract
- `seed_demo_data.py`, `demo.py`, `tests/`: demonstration and verification

## Limitations

CLIP compares overall visual appearance and cannot reliably prove ownership. Location-name fallback only checks normalized exact names; integrate geocoding later if desired. Model downloads require network/cache availability, while structured matching remains functional offline.
