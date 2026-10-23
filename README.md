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

## 2. Generated Outputs
- `exports/records/`: Canonical source dossiers for each call and meeting.
- `exports/routes/`: Route-specific markdown briefs for each destination team.
- `exports/briefs/`: Daily manager executive brief (Asia/Kolkata).
- `exports/manifest.json` & `exports/manifest.csv`: Machine-readable manifests.
- `data_bundle.js`: Offline data bundle for `app.html`.
