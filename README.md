# UniFinds — AI-Powered Campus Lost & Found System

UniFinds is a full-featured campus Lost and Found matching platform featuring a web frontend and an intelligent multi-modal matching engine (text semantics, CLIP image embeddings, attribute matching, and spatio-temporal scoring).

## Project Overview

- **`lost_found_matching/`**: Core system module containing the backend engine, SQLite persistence, matching algorithms, REST services, and frontend interface.
  - **`frontend/`**: Interactive web application for submitting reports, viewing ledgers, verifying ownership, and seeing ranked matches.
  - **`matching/`**: Multi-modal scoring pipeline combining CLIP visual similarity, sentence transformer semantic text similarity, geographic proximity, and temporal decay.
  - **`database/`**: SQLite persistence layer with parameterized schema and migrations.
  - **`services/`**: High-level report and match management APIs.
  - **`tests/`**: Unit and integration test suite.

## Getting Started

### 1. Install Dependencies

```bash
python -m pip install -r lost_found_matching/requirements.txt
```

### 2. Run Demo & Matching Verification

```bash
python -m lost_found_matching.demo
```

### 3. Run Tests

```bash
python -m pytest lost_found_matching/tests -q
```
