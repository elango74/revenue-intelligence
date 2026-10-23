# SpendNest Revenue Intelligence Inbox

## Overview
Automated revenue intelligence and conversation ingestion pipeline with a standalone local review inbox (`app.html`).
Processes multi-source calls and meetings, tracks revisions, preserves manual routing corrections across replay batches, and extracts evidence-backed action items.

## 1. Quick Start & Setup Instructions
1. Ensure Python 3.8+ is installed (no external pip dependencies required).
2. Run the pipeline and export generator from the project root:
   ```bash
   python pipeline.py
   ```
3. Open `app.html` in your browser (or serve via `python -m http.server 8000` and visit `http://localhost:8000/app.html`).

## 2. Interactive Features in `app.html`
- **1. Manager Dashboard**: Live KPI cards, sales rep call volume vs. transcript-verified 2-way substance, calendar organiser breakdown, multi-route assignment breakdown, and review exceptions queue.
- **2. Inbox & Evidence Inspector**: Full filterable list of all 44 records (Calls & Meetings), transcript turns, evidence citations, uncertainty boundaries, and interactive route reassignment with persistent manual override tracking.
- **3. Daily Manager Brief**: Pre-computed executive brief with clickable record links directly into the evidence inspector.
- **4. Replay Contract & Export Manifest**: Complete 5-step data contract test harness (Clean reset, initial batch, repeat shuffle, manual route correction on M07, update batch, and stale re-import verification) with live manifest preview and JSON/CSV download.
- **5. Key Findings & Architecture**: 3 core business findings with exact turn citations and rationale for rejecting aggregated pipeline dollar rollups.

## 3. Generated Outputs
- `exports/records/`: Canonical source dossiers for each call and meeting.
- `exports/routes/`: Route-specific markdown briefs for each destination team.
- `exports/briefs/`: Daily manager executive brief (Asia/Kolkata).
- `exports/manifest.json` & `exports/manifest.csv`: Machine-readable manifests.
- `data_bundle.js`: Offline data bundle for `app.html`.
