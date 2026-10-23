# M14 — CRM demonstration (M14) (Pending Transcript / Uncaptured Meeting)
- **Identity**: `(meeting, 93f4867d-65cd-5236-bc55-7bd57df8ac24)` | **Applied Revision**: `1`
- **Review State**: `Metadata Only (No Text)` | **Analysis Freshness**: `Fresh (Rev 1)`
- **Manual Route Override**: `False`
- **All Assigned Routes**: Pending Transcript / Uncaptured Meeting
- **Sibling Route Outputs**: None (Single destination)
- **Canonical Source Dossier**: `exports/records/M14_meeting_93f4867d.json`

## 1. What Happened & Why It Matters
Calendar meeting 'CRM demonstration' organised by team14@example.com (duration_seconds=3600). Supplied turns array is empty (unavailable_reason: The notetaker was cancelled before the meeting started.).

## 2. Supporting Transcript Evidence
- **M14 (93f4867d-65cd-5236-bc55-7bd57df8ac24)**: "[0 usable turns supplied. recording_status=cancelled, recording_detail=The notetaker was cancelled before the meeting started., unavailable_reason=The notetaker was cancelled before the meeting started.]"

## 3. What the Evidence Does Not Establish & Label Audit
- **Uncertainty / Boundaries**: A cancelled notetaker bot or missing transcript does not prove the meeting itself was cancelled or who attended. Refusing to fabricate meeting notes.
- **Upstream Label Audit**: has_transcript=False with 0 turns; recording_status='cancelled' (The notetaker was cancelled before the meeting started.).

## 4. Recommended Next Action & Stated Owner
- **Next Step**: Await late transcript delivery (if has_transcript=true) or request manual notes from meeting participants.
- **Stated Owner**: team14@example.com
