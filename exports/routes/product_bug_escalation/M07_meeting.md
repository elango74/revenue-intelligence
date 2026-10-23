# M07 — Willowfield Trust (Customer A) (Product Bug Escalation)
- **Identity**: `(meeting, 4f304fff-fd40-5cfc-a366-0a134c445c2a)` | **Applied Revision**: `2`
- **Review State**: `Updated Transcript — Needs Review` | **Analysis Freshness**: `Updated in Rev 2 (Late Transcript Inspected)`
- **Manual Route Override**: `True`
- **All Assigned Routes**: Customer Support & Escalation, Product Bug Escalation
- **Sibling Route Outputs**: Customer Support & Escalation
- **Canonical Source Dossier**: `exports/records/M07_meeting_4f304fff.json`

## 1. What Happened & Why It Matters
Live troubleshooting session with existing customer Willowfield Trust covering 4 active product bugs: (1) edited event-payment descriptions revert to old text on display after saving; (2) invoice upload fails on the 'Recreate payment' path (workaround found via Invoice Inbox -> Review); (3) released reimbursement payments stuck in 'Processing' state disabling selection; and (4) 'Mark as paid' carries forward the previous item's amount (INR 18,200) into the next item unless cancelled and reopened.

## 2. Supporting Transcript Evidence
- **M07 (4f304fff-fd40-5cfc-a366-0a134c445c2a) Turn 2-7**: "The field still shows the earlier wording... I have captured screenshots of that behaviour. I will get it checked today."
- **M07 (4f304fff-fd40-5cfc-a366-0a134c445c2a) Turn 8-13**: "When I go through this route [Recreate payment], I cannot upload a document... the workaround is to save the changes, return to the invoice inbox, open Review and upload the document there."
- **M07 (4f304fff-fd40-5cfc-a366-0a134c445c2a) Turn 16-19**: "The payments appear to have been released but are stuck showing Processing. I have asked the team to look at these. I expect an update or resolution in an hour or two"
- **M07 (4f304fff-fd40-5cfc-a366-0a134c445c2a) Turn 21-25**: "When I use Mark as paid, the first payment shows INR 18,200... The amount from the previous item appears in the next one."

## 3. What the Evidence Does Not Establish & Label Audit
- **Uncertainty / Boundaries**: In Revision 1 (01_initial.json), transcript turns were empty ([]). Revision 2 (02_update.json) establishes the 4 bugs, but root cause and final resolution are still pending engineering confirmation.
- **Upstream Label Audit**: Source recording_status='recorded', summary_status='stored' (upstream summary withheld by assessment).

## 4. Recommended Next Action & Stated Owner
- **Next Step**: Follow up within 1–2 hours on stuck 'Processing' reimbursements; file engineering bug tickets with screenshots/steps for description save refresh, Recreate payment upload, and Mark as paid amount carry-forward.
- **Stated Owner**: SpendNest Team Member A
