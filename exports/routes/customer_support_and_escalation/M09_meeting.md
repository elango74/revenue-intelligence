# M09 — Brookmint Holdings & Northkite Equipment (Customer A) (Customer Support & Escalation)
- **Identity**: `(meeting, 4b5b9192-f3fc-505a-8e77-4d2ffaa54594)` | **Applied Revision**: `1`
- **Review State**: `Ready for Review` | **Analysis Freshness**: `Fresh (Rev 1)`
- **Manual Route Override**: `False`
- **All Assigned Routes**: Customer Support & Escalation, Customer Onboarding
- **Sibling Route Outputs**: Customer Onboarding
- **Canonical Source Dossier**: `exports/records/M09_meeting_4b5b9192.json`

## 1. What Happened & Why It Matters
Onboarding and support session for a customer managing two entities: Northkite Equipment (used the trial) and Brookmint Holdings (larger employee base, blocked from logging in). Discussed admin continuity risks when an AP officer can read a shared accounts mailbox (Customer A opted for separate personal work emails via IT). When Team member A sent a fresh password reset invitation for Brookmint Holdings live on the call, clicking it immediately returned an 'expired token' error.

## 2. Supporting Transcript Evidence
- **M09 (4b5b9192-f3fc-505a-8e77-4d2ffaa54594) Turn 7**: "No, only Northkite Equipment used the trial. There was no Brookmint Holdings spending in that period."
- **M09 (4b5b9192-f3fc-505a-8e77-4d2ffaa54594) Turn 15-19**: "The accounts-payable officer already has an individual login. My concern is that they also have access to the shared mailbox... I think separate personal work identities for the two companies may be better."
- **M09 (4b5b9192-f3fc-505a-8e77-4d2ffaa54594) Turn 21-22**: "It says the token has expired. This is the fresh message we just received. I need to check that with the team. I hope to update you today, or by Monday at the latest."

## 3. What the Evidence Does Not Establish & Label Audit
- **Uncertainty / Boundaries**: Does not establish why newly generated invitation tokens are expiring immediately or when Brookmint Holdings will go live.
- **Upstream Label Audit**: Source recording_status='recorded', summary_status='stored' (upstream summary withheld by assessment).

## 4. Recommended Next Action & Stated Owner
- **Next Step**: Escalate Brookmint Holdings expired-token bug to engineering and update Customer A today or by Monday at the latest; Customer A to request separate email identities from internal IT.
- **Stated Owner**: Team member A (SpendNest) & Customer A
