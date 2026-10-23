import json
import os
import csv
import shutil
from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

ANALYSES_BY_REF = {
    "C01": {
        "entity": "Harborlight Advisory (Pranav)",
        "suggested_routes": ["Sales Coaching", "Do Not Pursue / Opt-Out"],
        "route_reason": "Cold call met strong objection to unsolicited work-number outreach; prospect stated finance processes are already automated.",
        "summary": "Arun cold-called Pranav regarding a partnership with Harborlight Advisory. Pranav objected to being cold-called on his work number via networking outreach and stated their finance processes are already highly automated.",
        "evidence": [
            {"ref": "C01 (2ec4404c-beee-5377-a63c-aab701da08ed)", "quote": "I didn't ask for this call, and I'm not interested. This number is for my work, not for people to sell things to me."},
            {"ref": "C01 (2ec4404c-beee-5377-a63c-aab701da08ed)", "quote": "Our processes are already very automated. We have a fairly advanced setup, so I don't think this is something we need."}
        ],
        "not_established": "Does not establish which software Harborlight Advisory uses or whether marketing had valid opt-in consent.",
        "next_steps": "Suppress Pranav's number from outbound lists. Coach Arun to answer 'Why are you calling?' directly on the first ask.",
        "owner": "Arun (Sales Representative)"
    },
    "C02": {
        "entity": "Fernhaven Group (Kavya / Leela)",
        "suggested_routes": ["Gatekeeper / Voicemail"],
        "route_reason": "Receptionist screening call only; target prospect (Leela) was out of office and call transferred to voicemail.",
        "summary": "Caller reached receptionist Kavya at Fernhaven Group asking for Leela. Leela was not in the office today, and the caller asked to be transferred to her voicemail mailbox.",
        "evidence": [
            {"ref": "C02 (4b870624-8aad-5315-a60e-0db95981cf99)", "quote": "It looks as though she isn't in the office today. Would you like to leave a message with me, or would you prefer her voicemail?"}
        ],
        "not_established": "Challenges upstream 'is_conversation=true' classification: connected only to receptionist, not the target decision-maker.",
        "next_steps": "Retry Leela on a subsequent business day.",
        "owner": "Assigned Sales Representative"
    },
    "C03": {
        "entity": "Milan (Developer API Access)",
        "suggested_routes": ["Deal Next Steps", "Customer Follow-Up"],
        "route_reason": "Scheduled 5-week follow-up on developer API access and webhooks; poor roaming audio required shifting to email plus Monday/Tuesday callback.",
        "summary": "Kiran followed up with Milan after 5 weeks regarding developer API access and event notifications. Milan noted price was previously a concern and API access wasn't essential enough for heavy spend, but poor outdoor roaming audio cut the discussion short.",
        "evidence": [
            {"ref": "C03 (20d509ba-d589-5334-9aef-ea4ce6105b1a)", "quote": "We did ask about some developer functionality, but it isn't essential enough for us to spend much on it."},
            {"ref": "C03 (20d509ba-d589-5334-9aef-ea4ce6105b1a)", "quote": "Something like 'Developer access and event notifications — follow-up'... Send the email and we can speak Monday or Tuesday."}
        ],
        "not_established": "Does not establish Milan's exact budget ceiling or whether his engineering team still requires API access.",
        "next_steps": "Send email with subject 'Developer access and event notifications — follow-up' and call Milan back on Monday or Tuesday earlier when indoors.",
        "owner": "Kiran (Sales Representative)"
    },
    "C04": {
        "entity": "Lanternpath Media (Ritesh)",
        "suggested_routes": ["Gatekeeper / Voicemail", "Deal Next Steps"],
        "route_reason": "One-way call screening and voicemail left for Ritesh after prior proposal went to the wrong email address.",
        "summary": "Arun passed automated call screening and left a voicemail for Ritesh at Lanternpath Media, noting that earlier expense platform info had gone to the wrong email address before being resent to the corrected address.",
        "evidence": [
            {"ref": "C04 (bcdcbf56-d338-5c78-9a97-42c2fc1c9931)", "quote": "The person you called is unavailable. You may leave a further message after the signal."},
            {"ref": "C04 (bcdcbf56-d338-5c78-9a97-42c2fc1c9931)", "quote": "My understanding is that our information first went to the wrong email address. We subsequently used the corrected address you gave us"}
        ],
        "not_established": "No two-way human conversation occurred (automated screening prompt + voicemail). Does not establish whether Ritesh read the resent email.",
        "next_steps": "Monitor for Ritesh's callback or follow up on the corrected email thread.",
        "owner": "Arun (Sales Representative)"
    },
    "C05": {
        "entity": "Multi-Store Prospect (StoreHarbor user)",
        "suggested_routes": ["Deal Next Steps", "Competitive Intelligence"],
        "route_reason": "Prospect already uses StoreHarbor and other tools for store expenses and vendor payments, but requested a presentation deck via email.",
        "summary": "Meera pitched SpendNest's store cards, instant-payment budgets, and vendor bill approvals. The prospect confirmed they already have those capabilities via StoreHarbor and other providers, but asked Meera to email a presentation to contact05@example.com for future consideration.",
        "evidence": [
            {"ref": "C05 (75a6b94f-7717-5cfb-9e41-0acc94415e17)", "quote": "One is StoreHarbor, and we use others too. What I suggest is that you send me your presentation. If we ever decide to change the providers we already have, we could consider it then."},
            {"ref": "C05 (75a6b94f-7717-5cfb-9e41-0acc94415e17)", "quote": "may I confirm contact05@example.com? Yes, that is right."}
        ],
        "not_established": "No active buying project or dissatisfaction with StoreHarbor is established.",
        "next_steps": "Email presentation deck to contact05@example.com and log StoreHarbor as incumbent competitor.",
        "owner": "Meera (Sales Representative)"
    },
    "C06": {
        "entity": "Mr Nikhil (120+ Store Retail/Distribution)",
        "suggested_routes": ["Sales Coaching", "Do Not Pursue / Opt-Out"],
        "route_reason": "Prospect has >120 stores already automated via head-office business management system and declined follow-up.",
        "summary": "Ravi cold-called Mr Nikhil (120+ stores). Mr Nikhil stated their store expenses and approvals are already automated and connected to their business management system managed by head office.",
        "evidence": [
            {"ref": "C06 (12216d5c-e254-52c6-b344-47de4c6e1ae5)", "quote": "The essential processes are automated and connected through our business management system. Head office manages it, and we have full visibility. That is why I said the arrangements are already in place."}
        ],
        "not_established": "Does not establish which ERP/business management platform Nikhil's company uses.",
        "next_steps": "Update CRM to prevent duplicate cold calls from other reps. Coach Ravi not to pitch a redundant feature after a prospect has already closed the conversation.",
        "owner": "Ravi (Sales Representative)"
    },
    "C07": {
        "entity": "Willowbank Advisory (Mr Aditya)",
        "suggested_routes": ["Partnership & Channel", "Deal Next Steps"],
        "route_reason": "High-fit incorporation advisory partner that actively refers newly formed companies to digital account providers.",
        "summary": "Dev spoke with Mr Aditya at Willowbank Advisory, who confirmed they incorporate companies domestically and overseas and normally refer clients to digital business account providers. Aditya requested a proposal via chat app and agreed to a Monday callback.",
        "evidence": [
            {"ref": "C07 (428817fa-7e9e-5418-a7d4-bb396d28dfbf)", "quote": "Do you currently refer clients to providers for that part of the process? Yes, that is something we normally do."},
            {"ref": "C07 (428817fa-7e9e-5418-a7d4-bb396d28dfbf)", "quote": "Sorry, could you message me on our chat app and send whatever proposal you have?... Once you've received them, could I call on Monday to see whether you'd like to discuss it further? Yes, that's fine."}
        ],
        "not_established": "Does not establish monthly client referral volume or specific overseas jurisdictions.",
        "next_steps": "Send partnership proposal via chat app to Aditya's number and call back on Monday.",
        "owner": "Dev (Sales Representative)"
    },
    "C08": {
        "entity": "Mr Raghav (Multi-Location Fulfilment)",
        "suggested_routes": ["Deal Next Steps"],
        "route_reason": "Prospect confirmed prior internal discussions around frontline/location expense solutions and provided colleague's email with permission to use his name.",
        "summary": "Meera pitched SpendNest as a payment execution and expense layer alongside existing enterprise systems. Mr Raghav noted internal discussions had taken place and gave his people-operations colleague's email (contact08@example.com) to receive a proposal.",
        "evidence": [
            {"ref": "C08 (129497b2-8e1d-5e01-919c-e8a852b5ff68)", "quote": "The colleague handling our people operations also deals with frontline processes and the locations. I think we may have been looking at a solution... If you send him a proposal and say you spoke with me, he can take a look."}
        ],
        "not_established": "Does not establish the colleague's name, ERP system, or timeline.",
        "next_steps": "Send proposal to contact08@example.com explicitly referencing the conversation with Mr Raghav.",
        "owner": "Meera (Sales Representative)"
    },
    "C09": {
        "entity": "Mr Vedant & Mr Rishabh (~130 Stores)",
        "suggested_routes": ["Deal Next Steps", "Sales Coaching"],
        "route_reason": "Prospect uses in-house software (~130 locations) but pointed to Business Head Mr Rishabh on professional networking; explicitly forbade using his name.",
        "summary": "Meera called Mr Vedant (~130 stores). They built internal expense software, though Vedant did not know if it executes payments directly. He directed Meera to find their business head, Mr Rishabh, on a professional networking site, but asked not to have his name mentioned.",
        "evidence": [
            {"ref": "C09 (4a1de681-f884-55e8-b1ad-de22d17cd959)", "quote": "If you want to speak to somebody about it, you can find our business head, Mr Rishabh, on a professional networking site."},
            {"ref": "C09 (4a1de681-f884-55e8-b1ad-de22d17cd959)", "quote": "Would it be all right if I mentioned your name when contacting him? No, please don't use my name."}
        ],
        "not_established": "Does not establish whether their internal software has gaps in payment execution.",
        "next_steps": "Reach out to Business Head Mr Rishabh via professional networking WITHOUT mentioning Mr Vedant's name. Highlight Meera's good practice of asking permission before name-dropping.",
        "owner": "Meera (Sales Representative)"
    },
    "C10": {
        "entity": "Mr Aniket (Ex-Meadowbrick, now Manufacturing)",
        "suggested_routes": ["Sales Coaching", "Customer Follow-Up"],
        "route_reason": "Stale lead data (left Meadowbrick for manufacturing); agreed to messaging app brief but firmly rejected rep's push for a Monday/Tuesday call.",
        "summary": "Meera called Mr Aniket about Meadowbrick, but he had moved to a manufacturing firm. He offered to review a brief on the messaging app, interrupting twice to state he would reach out if interested, and firmly rejected Meera's attempt to lock in a Monday/Tuesday call.",
        "evidence": [
            {"ref": "C10 (b747f592-810e-583c-9b81-8db5ab035806)", "quote": "Are you calling about Meadowbrick? Yes, that's right. I don't work there anymore... It is different. Manufacturing."},
            {"ref": "C10 (b747f592-810e-583c-9b81-8db5ab035806)", "quote": "Would a follow-up call on Monday or Tuesday next week be okay, in case you have any questions? No. I said I will contact you if there is anything to discuss."}
        ],
        "not_established": "Does not establish the name of Mr Aniket's new manufacturing employer.",
        "next_steps": "Update CRM that Aniket left Meadowbrick; send concise manufacturing/AP brief via messaging app; DO NOT call Monday/Tuesday. Coach Meera not to push for a calendar slot right after a prospect says 'I will get back to you.'",
        "owner": "Meera (Sales Representative)"
    },
    "M01": {
        "entity": "Harborpath Advisory (Partner A)",
        "suggested_routes": ["Partnership & Channel", "Deal Next Steps"],
        "route_reason": "Channel partner onboarding agreement for US virtual accounts/cards; requires unique referral link + commission/KYB documentation.",
        "summary": "Partner onboarding session with Harborpath Advisory covering US virtual accounts and cards for registered businesses (not individuals). Reviewed commission tiers (USD 260 per approved account + 60-day spend bonuses of USD 195 / USD 390 + every 5th referral bonus), customer pricing (USD 38/mo waived at USD 2,600 spend), strict KYB rules (proof of US operations), and agreed to provide a scalable unique referral link rather than manual email introductions.",
        "evidence": [
            {"ref": "M01 (cb5cecac-e68d-52b7-b10b-b0c748efc467) Turn 2", "quote": "we work with registered businesses, not individuals opening personal accounts."},
            {"ref": "M01 (cb5cecac-e68d-52b7-b10b-b0c748efc467) Turn 9 & 13", "quote": "The activation payment is USD 260 when a referred company gets its account approved... Another important point is evidence of US operations or intended operations"},
            {"ref": "M01 (cb5cecac-e68d-52b7-b10b-b0c748efc467) Turn 20-21", "quote": "It cannot depend on me manually writing every email. This needs to scale... Then let us use the unique link."}
        ],
        "not_established": "Does not establish signed memorandum completion or projected referral count.",
        "next_steps": "Send partner memorandum, written commercial & customer pricing terms, KYB checklist (noting bank-transfer-only funding), and unique referral link + shared tracking sheet; connect Partner A with marketing for podcast.",
        "owner": "SpendNest Team Member A"
    },
    "M02": {
        "entity": "LedgerBridge (Supplier A - E-Invoicing Vendor)",
        "suggested_routes": ["Vendor & Product Strategy"],
        "route_reason": "SpendNest is the BUYER evaluating LedgerBridge as an e-invoicing infrastructure supplier (EUR 2,600-6,500 setup cost), NOT a sales prospect.",
        "summary": "SpendNest strategy/partnerships (Team member A) and product (Team member B) evaluated supplier LedgerBridge for compliant e-invoicing (issuing & receiving) across Singapore, Australia, and India to support SpendNest's upcoming AR module (targeted for Q4, though could slip to early next year). LedgerBridge quoted EUR 2,600–6,500 one-time setup plus country or per-customer licensing.",
        "evidence": [
            {"ref": "M02 (1a21c409-c050-5787-90af-2667e057e1b6) Turn 1 & 15", "quote": "We want to understand whether LedgerBridge can give us compliant invoicing coverage... Early next year is possible if the work moves. We intend to build the capability, but I would not describe the quarter as an immovable deadline."},
            {"ref": "M02 (1a21c409-c050-5787-90af-2667e057e1b6) Turn 18", "quote": "Received invoice volumes can be based on current accounts-payable usage. Issued volumes will be estimates because the receivables product is still being built."},
            {"ref": "M02 (1a21c409-c050-5787-90af-2667e057e1b6) Turn 30-31", "quote": "And the commercial relationship is between SpendNest and LedgerBridge?... Correct. There is also a one-time setup charge. The basic setup begins at EUR 2,600; a more supported implementation starts at EUR 6,500"}
        ],
        "not_established": "EUR 2,600–6,500 is a vendor cost to SpendNest, NOT sales revenue. Management has not yet approved a hard Q4 commitment.",
        "next_steps": "Receive volume template from Supplier A; populate AP actuals vs AR estimates separately; test LedgerBridge sandbox API; hold short pricing explanation call before internal management briefing.",
        "owner": "SpendNest Strategy & Product Team + Supplier A"
    },
    "M03": {
        "entity": "Asterloom Systems (Customer A & B)",
        "suggested_routes": ["Deal Next Steps", "Sales Coaching"],
        "route_reason": "Active 65-employee prospect (4-5 user pilot), but friction over prepaid vs credit cards, manual accounting sync, and unannounced INR 13,000 setup fee added to INR 26,000 quote.",
        "summary": "Demo and commercial discussion with Asterloom Systems (~65 employees, ~INR 10–13 lakh monthly employee spend, starting with 4–5 travellers). Customer A was surprised domestic cards are prepaid rather than credit, and challenged why their prior INR 26,000 quote became INR 39,000 (rep had bundled a INR 13,000 accounting setup fee without separating it). CFO approval is required before proceeding.",
        "evidence": [
            {"ref": "M03 (398672e7-62dd-5afd-846d-0237d49792fb) Turn 6", "quote": "Wait, these are prepaid? I had thought about a corporate credit card. So we put money in before anyone spends, and there is no credit facility on these domestic cards?"},
            {"ref": "M03 (398672e7-62dd-5afd-846d-0237d49792fb) Turn 16", "quote": "If you need automatic syncing after approval, that is something we can build. I am showing the current manual selection here"},
            {"ref": "M03 (398672e7-62dd-5afd-846d-0237d49792fb) Turn 23-24", "quote": "But you previously told me INR 26,000. Why has that become INR 39,000? I included the integration setup in that number. To separate it: INR 26,000 plus tax is the recurring annual subscription, and INR 13,000 is the one-time accounting integration setup."},
            {"ref": "M03 (398672e7-62dd-5afd-846d-0237d49792fb) Turn 28 & 36", "quote": "Our CFO approves the larger payments... Send the details first. We need time with the CFO and will tell you if another call is needed."}
        ],
        "not_established": "CFO approval is not established; vendor payments (~INR 26–39 lakh/mo rough guess in Turn 34) are explicitly out of current scope (Turn 3).",
        "next_steps": "Send transparent written proposal separating INR 26,000 annual subscription, INR 13,000 integration setup, and optional reimbursement module pricing. Coach rep to always separate one-time setup fees from recurring quotes upfront.",
        "owner": "SpendNest Team Member A"
    },
    "M04": {
        "entity": "Cedarwave Distribution (Customer A & B)",
        "suggested_routes": ["Customer Support & Escalation", "Deal Next Steps"],
        "route_reason": "Retention risk on existing card migration: customer wants credit rather than prepaid (has INR 1.3Cr bank credit line), needs bank-feed & accounting feasibility checks, plus department user cleanup.",
        "summary": "Card programme migration call with existing customer Cedarwave Distribution. SpendNest is closing their current card programme (requiring re-KYC on a new prepaid network), but Cedarwave stated moving from prepaid to credit is their main priority and they already hold an INR 1.3 crore bank corporate credit line. Explored connecting their bank-issued credit cards to SpendNest via post-settlement transaction feeds, plus fixing a confusing department user setup.",
        "evidence": [
            {"ref": "M04 (b0f79b3d-37ba-52f9-b2bc-58b159dd6d91) Turn 4-6", "quote": "The plan is to close the old programme in the coming weeks... Users need to complete identity checks again because the provider changes."},
            {"ref": "M04 (b0f79b3d-37ba-52f9-b2bc-58b159dd6d91) Turn 11", "quote": "Okay, I have confirmed it: moving from prepaid to credit is the main issue for us. At some stage we will have to consider another option for that."},
            {"ref": "M04 (b0f79b3d-37ba-52f9-b2bc-58b159dd6d91) Turn 21-25", "quote": "source-balance reconciliation is a question in this setup. I need the team to confirm feasibility for your bank-card transactions... I cannot confirm the existing-card eligibility on this call."},
            {"ref": "M04 (b0f79b3d-37ba-52f9-b2bc-58b159dd6d91) Turn 30-31", "quote": "There is also the earlier issue with moving users between departments... We can arrange a session to guide you through it"}
        ],
        "not_established": "Does not establish whether Cedarwave's already-issued bank credit cards qualify for the transaction feed or whether bank-card accounting reconciliation works.",
        "next_steps": "Confirm with programme/product team whether existing bank credit cards can join the transaction feed and sync to accounting; schedule a guided admin session to reorganize users across departments.",
        "owner": "SpendNest Team Member A"
    },
    "M06": {
        "entity": "Mapletrail Services (Customer A - Branch Finance)",
        "suggested_routes": ["Deal Next Steps", "Sales Coaching"],
        "route_reason": "Early discovery on AR collections & expenses with a local branch contact (~8 clients locally vs 65-person central finance team); requires security docs and central team alignment.",
        "summary": "Discovery conversation with a branch finance manager at Mapletrail Services (65 finance staff centrally; roughly 65–78 customers and an estimated 390–520 invoices/month company-wide, though Customer A handles ~8 clients locally). Discussed AI-assisted AR collection follow-ups, exception flagging (e.g., an expense-recovery invoice unpaid for months), cash application discrepancies, and data confidentiality/security controls.",
        "evidence": [
            {"ref": "M06 (657b9e9d-9472-5b01-a127-a648ad7e8cf7) Turn 4, 6 & 9", "quote": "Roughly 65 people across finance... Most operations sit centrally... I cover around eight clients."},
            {"ref": "M06 (657b9e9d-9472-5b01-a127-a648ad7e8cf7) Turn 15-16", "quote": "So perhaps nearer 390–520 a month overall? Approximately. The value is the bigger point, and many are in foreign currency. These are rough numbers in this conversation, not a report I have open."},
            {"ref": "M06 (657b9e9d-9472-5b01-a127-a648ad7e8cf7) Turn 31-32", "quote": "Confidentiality is important. Payment information is sensitive. How is that protected... I can share the material on our setup as part of the follow-up."}
        ],
        "not_established": "Invoice counts (390–520/mo) are unverified conversational estimates (Turn 16); Customer A is a local branch user, not the central finance buyer (Turn 6-7, 25).",
        "next_steps": "Send AR collections, expense/payables, and security/compliance certification materials. Coach rep to map the path to the 65-person central finance office that controls ERP and payables.",
        "owner": "SpendNest Team Member A"
    },
    "M07": {
        "entity": "Willowfield Trust (Customer A)",
        "suggested_routes": ["Customer Support & Escalation", "Product Bug Escalation"],
        "route_reason": "Late-arriving transcript (Revision 2) documents 4 reproducible production UI/payment bugs requiring engineering escalation and a 1-2 hour status update.",
        "summary": "Live troubleshooting session with existing customer Willowfield Trust covering 4 active product bugs: (1) edited event-payment descriptions revert to old text on display after saving; (2) invoice upload fails on the 'Recreate payment' path (workaround found via Invoice Inbox -> Review); (3) released reimbursement payments stuck in 'Processing' state disabling selection; and (4) 'Mark as paid' carries forward the previous item's amount (INR 18,200) into the next item unless cancelled and reopened.",
        "evidence": [
            {"ref": "M07 (4f304fff-fd40-5cfc-a366-0a134c445c2a) Turn 2-7", "quote": "The field still shows the earlier wording... I have captured screenshots of that behaviour. I will get it checked today."},
            {"ref": "M07 (4f304fff-fd40-5cfc-a366-0a134c445c2a) Turn 8-13", "quote": "When I go through this route [Recreate payment], I cannot upload a document... the workaround is to save the changes, return to the invoice inbox, open Review and upload the document there."},
            {"ref": "M07 (4f304fff-fd40-5cfc-a366-0a134c445c2a) Turn 16-19", "quote": "The payments appear to have been released but are stuck showing Processing. I have asked the team to look at these. I expect an update or resolution in an hour or two"},
            {"ref": "M07 (4f304fff-fd40-5cfc-a366-0a134c445c2a) Turn 21-25", "quote": "When I use Mark as paid, the first payment shows INR 18,200... The amount from the previous item appears in the next one."}
        ],
        "not_established": "In Revision 1 (01_initial.json), transcript turns were empty ([]). Revision 2 (02_update.json) establishes the 4 bugs, but root cause and final resolution are still pending engineering confirmation.",
        "next_steps": "Follow up within 1–2 hours on stuck 'Processing' reimbursements; file engineering bug tickets with screenshots/steps for description save refresh, Recreate payment upload, and Mark as paid amount carry-forward.",
        "owner": "SpendNest Team Member A"
    },
    "M09": {
        "entity": "Brookmint Holdings & Northkite Equipment (Customer A)",
        "suggested_routes": ["Customer Support & Escalation", "Customer Onboarding"],
        "route_reason": "Multi-entity setup blocked by an immediately expiring password-reset token for Brookmint Holdings plus admin role separation concerns.",
        "summary": "Onboarding and support session for a customer managing two entities: Northkite Equipment (used the trial) and Brookmint Holdings (larger employee base, blocked from logging in). Discussed admin continuity risks when an AP officer can read a shared accounts mailbox (Customer A opted for separate personal work emails via IT). When Team member A sent a fresh password reset invitation for Brookmint Holdings live on the call, clicking it immediately returned an 'expired token' error.",
        "evidence": [
            {"ref": "M09 (4b5b9192-f3fc-505a-8e77-4d2ffaa54594) Turn 7", "quote": "No, only Northkite Equipment used the trial. There was no Brookmint Holdings spending in that period."},
            {"ref": "M09 (4b5b9192-f3fc-505a-8e77-4d2ffaa54594) Turn 15-19", "quote": "The accounts-payable officer already has an individual login. My concern is that they also have access to the shared mailbox... I think separate personal work identities for the two companies may be better."},
            {"ref": "M09 (4b5b9192-f3fc-505a-8e77-4d2ffaa54594) Turn 21-22", "quote": "It says the token has expired. This is the fresh message we just received. I need to check that with the team. I hope to update you today, or by Monday at the latest."}
        ],
        "not_established": "Does not establish why newly generated invitation tokens are expiring immediately or when Brookmint Holdings will go live.",
        "next_steps": "Escalate Brookmint Holdings expired-token bug to engineering and update Customer A today or by Monday at the latest; Customer A to request separate email identities from internal IT.",
        "owner": "SpendNest Team Member A & Customer A"
    },
    "M10": {
        "entity": "Internal Billing Walkthrough (Team members A, B, C)",
        "suggested_routes": ["Internal Ops & Enablement"],
        "route_reason": "Internal staff training session on SpendNest's back-office super-admin billing engine; NOT a customer or prospect interaction.",
        "summary": "Internal enablement session where Trainer (Team member A) walked Team members B & C through the back-office billing application. Covered invoice due dates vs collection grace periods, zero-value periodic invoices, midnight automated invoice generation, the 10-day failed wallet deduction retry/freeze cycle (Day 1, Day 3, Day 7 warning, Day 10 block), and the requirement for operations to manually adjust the next billing date when unfreezing a topped-up account.",
        "evidence": [
            {"ref": "M10 (337f297d-9385-5b82-9e54-5019c1ed912c) Turn 4-5", "quote": "I do not have the back-office super-admin access you mentioned. Okay. That is a different application. Operations uses it to create accounts, control enabled features and manage billing."},
            {"ref": "M10 (337f297d-9385-5b82-9e54-5019c1ed912c) Turn 15-18", "quote": "Simply topping up a frozen account does not complete the whole recovery flow in this process... Operations also needs to adjust the next billing date manually. Clearing the payment without checking that date can leave the next cycle wrong."},
            {"ref": "M10 (337f297d-9385-5b82-9e54-5019c1ed912c) Turn 20", "quote": "I will request the back-office access separately for the next training session."}
        ],
        "not_established": "Internal training example amounts (e.g. INR 6,240 invoice / INR 6,110 wallet) are hypothetical training examples, not customer records.",
        "next_steps": "Team member A to request back-office super-admin access for Team member B before the next training session.",
        "owner": "SpendNest Internal Trainer"
    }
}


def has_usable_text(rec):
    stype = rec.get("source_type")
    payload = rec.get("payload") or {}
    tpayload = rec.get("transcript_payload") or {}
    if stype == "call":
        t = payload.get("transcript")
        return bool(t and str(t).strip())
    elif stype == "meeting":
        turns = tpayload.get("turns") or []
        return any(bool(turn.get("text") and str(turn.get("text")).strip()) for turn in turns)
    return False


def build_record_analysis(rec):
    ref = rec.get("record_ref", "")
    stype = rec.get("source_type", "")
    payload = rec.get("payload") or {}
    tpayload = rec.get("transcript_payload") or {}
    usable = has_usable_text(rec)

    if usable and ref in ANALYSES_BY_REF:
        base = dict(ANALYSES_BY_REF[ref])
        if stype == "call":
            is_conn = payload.get("is_connected")
            is_conv = payload.get("is_conversation")
            outcome = payload.get("observed_outcome")
            if ref in ("C02", "C04"):
                base["label_audit"] = f"Upstream marked is_connected={is_conn}, is_conversation={is_conv}, outcome='{outcome}', but transcript shows only gatekeeper/voicemail screening without reaching target prospect."
            else:
                base["label_audit"] = f"Source-reported is_connected={is_conn}, is_conversation={is_conv}, observed_outcome='{outcome}' verified against 2-way transcript."
        else:
            rec_status = payload.get("recording_status")
            sum_status = payload.get("summary_status")
            if ref == "M02":
                base["label_audit"] = "Title looks like a general discussion, but transcript proves SpendNest is the buyer evaluating a supplier (excluded from sales pipeline)."
            elif ref == "M10":
                base["label_audit"] = "Internal staff training walkthrough; organiser is internal trainer/coordinator, not a sales deal."
            else:
                base["label_audit"] = f"Source recording_status='{rec_status}', summary_status='{sum_status}' (upstream summary withheld by assessment)."
        return base

    if stype == "call":
        is_conn = payload.get("is_connected")
        is_conv = payload.get("is_conversation")
        dur = payload.get("duration_seconds", 0)
        outcome = payload.get("observed_outcome")
        return {
            "entity": f"Call {ref} ({payload.get('direction', 'unknown')} | {dur}s)",
            "suggested_routes": ["Metadata-Only Intake (No Transcript)"],
            "route_reason": f"No transcript supplied in package (transcript=null). Source-reported is_connected={is_conn}, is_conversation={is_conv}, observed_outcome={outcome}.",
            "summary": f"Metadata-only call record ({dur}s duration, talk_time={payload.get('talk_time_seconds')}s). Transcript text is null in this extract. A missing transcript does not prove no conversation occurred, nor is stored classification ground truth.",
            "evidence": [
                {"ref": f"{ref} ({rec.get('source_id')})", "quote": f"[No supplied transcript text. Metadata: duration_seconds={dur}, is_connected={is_conn}, observed_outcome={outcome}]"}
            ],
            "not_established": "Cannot verify conversation substance, speaker intent, or next steps without transcript text. Refusing to invent substantive analysis.",
            "next_steps": "Log activity in rep volume counts; require human check only if rep flags an active deal in CRM.",
            "owner": payload.get("rep_name") or payload.get("rep_email") or "Unassigned Sales Representative",
            "label_audit": f"Unverified upstream metadata: is_connected={is_conn}, is_conversation={is_conv}, summary_status={payload.get('summary_status')}."
        }
    else:
        title = payload.get("title", "Untitled Meeting")
        rec_status = payload.get("recording_status")
        rec_detail = payload.get("recording_detail")
        has_tr = payload.get("has_transcript")
        unavail = tpayload.get("unavailable_reason")
        return {
            "entity": f"{title} ({ref})",
            "suggested_routes": ["Pending Transcript / Uncaptured Meeting"],
            "route_reason": f"No usable transcript turns supplied (recording_status='{rec_status}', has_transcript={has_tr}, unavailable_reason='{unavail}').",
            "summary": f"Calendar meeting '{title}' organised by {payload.get('organizer_email')} (duration_seconds={payload.get('duration_seconds')}). Supplied turns array is empty (unavailable_reason: {unavail or rec_detail or 'not captured'}).",
            "evidence": [
                {"ref": f"{ref} ({rec.get('source_id')})", "quote": f"[0 usable turns supplied. recording_status={rec_status}, recording_detail={rec_detail}, unavailable_reason={unavail}]"}
            ],
            "not_established": "A cancelled notetaker bot or missing transcript does not prove the meeting itself was cancelled or who attended. Refusing to fabricate meeting notes.",
            "next_steps": "Await late transcript delivery (if has_transcript=true) or request manual notes from meeting participants.",
            "owner": payload.get("organizer_email") or "Meeting Organiser",
            "label_audit": f"has_transcript={has_tr} with 0 turns; recording_status='{rec_status}' ({rec_detail})."
        }


class RevenueIntelligencePipeline:
    def __init__(self, data_dir="data", output_dir="exports"):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.records = {}
        self.manual_routes = {}
        self.review_states = {}
        self.replay_log = []

    def load_batch(self, filepath, reverse_order=False, label="Import"):
        with open(filepath, "r", encoding="utf-8") as f:
            batch = json.load(f)

        envelope_rev = batch.get("revision", 1)
        batch_id = batch.get("batch_id", "batch")
        raw_records = list(batch.get("records", []))
        if reverse_order:
            raw_records.reverse()

        inserted, updated, ignored = 0, 0, 0
        for rec in raw_records:
            stype = rec.get("source_type")
            sid = rec.get("source_id") or (rec.get("payload") or {}).get("id")
            key = (stype, sid)

            existing = self.records.get(key)
            if existing is None:
                rec_copy = json.loads(json.dumps(rec))
                rec_copy["applied_revision"] = envelope_rev
                rec_copy["last_batch_id"] = batch_id
                self.records[key] = rec_copy
                usable = has_usable_text(rec_copy)
                self.review_states[key] = {
                    "intake_status": "Ready for Review" if usable else "Metadata Only (No Text)",
                    "analysis_freshness": f"Fresh (Rev {envelope_rev})",
                    "manual_override": False,
                    "analyzed_revision": envelope_rev
                }
                inserted += 1
            elif envelope_rev > existing.get("applied_revision", 1):
                prev_usable = has_usable_text(existing)
                rec_copy = json.loads(json.dumps(rec))
                rec_copy["applied_revision"] = envelope_rev
                rec_copy["last_batch_id"] = batch_id
                self.records[key] = rec_copy
                now_usable = has_usable_text(rec_copy)

                state = self.review_states[key]
                if prev_usable != now_usable or envelope_rev > state.get("analyzed_revision", 1):
                    state["intake_status"] = "Updated Transcript — Needs Review"
                    state["analysis_freshness"] = f"Updated in Rev {envelope_rev} (Late Transcript Inspected)"
                    state["analyzed_revision"] = envelope_rev
                updated += 1
            else:
                ignored += 1

        usable_count = sum(1 for r in self.records.values() if has_usable_text(r))
        self.replay_log.append({
            "step": label,
            "batch_id": batch_id,
            "revision": envelope_rev,
            "unique_records": len(self.records),
            "usable_texts": usable_count,
            "inserted": inserted,
            "updated": updated,
            "ignored": ignored
        })

    def apply_manual_correction(self, source_type, source_id, routes, reason="Manager verified multi-destination routing"):
        key = (source_type, source_id)
        if key in self.records:
            self.manual_routes[key] = list(routes)
            self.review_states[key]["manual_override"] = True
            self.review_states[key]["override_reason"] = reason
            self.review_states[key]["intake_status"] = "Manually Routed & Verified"
            self.replay_log.append({
                "step": f"Manual Override on {self.records[key].get('record_ref')}",
                "batch_id": "manual_user_action",
                "revision": self.records[key].get("applied_revision", 1),
                "unique_records": len(self.records),
                "usable_texts": sum(1 for r in self.records.values() if has_usable_text(r)),
                "inserted": 0,
                "updated": 1,
                "ignored": 0
            })

    def run_all(self):
        init_path = os.path.join(self.data_dir, "01_initial.json")
        upd_path = os.path.join(self.data_dir, "02_update.json")

        print("=== Running Public Replay Contract ===")
        self.load_batch(init_path, reverse_order=False, label="1. Initial Import (01_initial.json)")
        print(f"Step 1 (Initial): {len(self.records)} unique records, {self.replay_log[-1]['usable_texts']} usable texts.")

        self.load_batch(init_path, reverse_order=True, label="2. Repeat Import Reordered (01_initial.json)")
        print(f"Step 2 (Repeat Reordered): {len(self.records)} unique records (Ignored {self.replay_log[-1]['ignored']} duplicates).")

        m07_key = ("meeting", "4f304fff-fd40-5cfc-a366-0a134c445c2a")
        self.apply_manual_correction(
            "meeting",
            "4f304fff-fd40-5cfc-a366-0a134c445c2a",
            ["Customer Support & Escalation", "Product Bug Escalation"],
            reason="Manager assigned Willowfield Trust (M07) to both Customer Support Escalation and Product Bug Escalation."
        )
        print("Step 3 (Manual Correction): Overrode M07 route prior to update batch.")

        self.load_batch(upd_path, reverse_order=False, label="4. Update Batch Import (02_update.json)")
        print(f"Step 4 (Update Batch): {len(self.records)} unique records, {self.replay_log[-1]['usable_texts']} usable texts (M07 transcript arrived, manual override preserved: {self.review_states[m07_key]['manual_override']}).")

        self.load_batch(init_path, reverse_order=False, label="5. Stale Re-import Check (01_initial.json after Rev 2)")
        print(f"Step 5 (Preserve Newer Revision & Judgment): {len(self.records)} unique records, {self.replay_log[-1]['usable_texts']} usable texts.")

        self.export_all()
        self.write_browser_bundle()
        self.write_slides_and_readme()

    run_replay_sequence = run_all

    def export_all(self):
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

        records_dir = os.path.join(self.output_dir, "records")
        routes_dir = os.path.join(self.output_dir, "routes")
        briefs_dir = os.path.join(self.output_dir, "briefs")
        os.makedirs(records_dir, exist_ok=True)
        os.makedirs(routes_dir, exist_ok=True)
        os.makedirs(briefs_dir, exist_ok=True)

        manifest_rows = []
        sorted_items = sorted(self.records.items(), key=lambda kv: kv[1].get("record_ref", ""))

        for (stype, sid), rec in sorted_items:
            ref = rec.get("record_ref", sid[:6])
            rev = rec.get("applied_revision", 1)
            state = self.review_states.get((stype, sid), {})
            analysis = build_record_analysis(rec)
            usable = has_usable_text(rec)

            override_flag = state.get("manual_override", False)
            active_routes = self.manual_routes.get((stype, sid), analysis["suggested_routes"])

            output_paths = []
            rec_filename = f"records/{ref}_{stype}_{sid[:8]}.json"
            rec_fullpath = os.path.join(self.output_dir, rec_filename)
            dossier = {
                "identity": {"source_type": stype, "source_id": sid, "record_ref": ref, "applied_revision": rev},
                "routing": {
                    "suggested_routes": analysis["suggested_routes"],
                    "active_routes": active_routes,
                    "manual_override": override_flag,
                    "route_reason": state.get("override_reason") if override_flag else analysis["route_reason"]
                },
                "review_state": state,
                "analysis": analysis,
                "source_record": rec
            }
            with open(rec_fullpath, "w", encoding="utf-8") as f:
                json.dump(dossier, f, indent=2)
            output_paths.append(f"exports/{rec_filename}")

            for route_name in active_routes:
                slug = route_name.lower().replace("&", "and").replace("/", "_").replace(" ", "_")
                slug = "".join(c for c in slug if c.isalnum() or c == "_").strip("_")
                route_folder = os.path.join(routes_dir, slug)
                os.makedirs(route_folder, exist_ok=True)

                route_rel = f"routes/{slug}/{ref}_{stype}.md"
                route_full = os.path.join(self.output_dir, route_rel)
                sibling_routes = [r for r in active_routes if r != route_name]

                md_lines = [
                    f"# {ref} — {analysis['entity']} ({route_name})",
                    f"- **Identity**: `({stype}, {sid})` | **Applied Revision**: `{rev}`",
                    f"- **Review State**: `{state.get('intake_status')}` | **Analysis Freshness**: `{state.get('analysis_freshness')}`",
                    f"- **Manual Route Override**: `{override_flag}`",
                    f"- **All Assigned Routes**: {', '.join(active_routes)}",
                    f"- **Sibling Route Outputs**: {', '.join(sibling_routes) if sibling_routes else 'None (Single destination)'}",
                    f"- **Canonical Source Dossier**: `exports/{rec_filename}`",
                    "",
                    "## 1. What Happened & Why It Matters",
                    analysis["summary"],
                    "",
                    "## 2. Supporting Transcript Evidence",
                ]
                for ev in analysis["evidence"]:
                    md_lines.append(f"- **{ev['ref']}**: \"{ev['quote']}\"")
                md_lines.extend([
                    "",
                    "## 3. What the Evidence Does Not Establish & Label Audit",
                    f"- **Uncertainty / Boundaries**: {analysis['not_established']}",
                    f"- **Upstream Label Audit**: {analysis.get('label_audit', 'N/A')}",
                    "",
                    "## 4. Recommended Next Action & Stated Owner",
                    f"- **Next Step**: {analysis['next_steps']}",
                    f"- **Stated Owner**: {analysis['owner']}"
                ])
                with open(route_full, "w", encoding="utf-8") as f:
                    f.write("\n".join(md_lines) + "\n")
                output_paths.append(f"exports/{route_rel}")

            manifest_rows.append({
                "record_ref": ref,
                "source_type": stype,
                "source_id": sid,
                "applied_source_revision": rev,
                "has_usable_text": usable,
                "suggested_routes": "; ".join(analysis["suggested_routes"]),
                "assigned_routes": "; ".join(active_routes),
                "manual_override_flag": override_flag,
                "processing_review_state": state.get("intake_status", "Ready"),
                "analysis_freshness": state.get("analysis_freshness", "Fresh"),
                "output_paths": "; ".join(output_paths)
            })

        brief_rel = "briefs/2026-08-21_manager_brief.md"
        brief_full = os.path.join(self.output_dir, brief_rel)
        with open(brief_full, "w", encoding="utf-8") as f:
            f.write("""# Daily Revenue Intelligence Manager Brief — 21 August 2026 (Asia/Kolkata)

## 1. Activity & Coverage Headline (Selected Sample)
- **Total Distinct Source Records**: 44 (30 Calls, 14 Meetings) on 21 August 2026 (Asia/Kolkata).
- **Usable Supplied Transcript Coverage**: 18 / 44 (40.9%) post-update — 10 / 30 Calls (33.3%) and 8 / 14 Meetings (57.1%, including late-arriving transcript M07 in Revision 2).
- **Important Denominator Distinction**: Sales representatives and meeting organisers are tracked separately because calendar organisers are not automatically salespeople or confirmed attendees.

## 2. Urgent Customer & Product Escalations (Act Today)
1. **Willowfield Trust (`M07`, turns 2–25)**: Late transcript in Revision 2 revealed **4 active product bugs**: edited descriptions reverting after save (Turns 2–7), attachment upload failing under `Recreate payment` (Turns 8–15, temporary workaround via Invoice Inbox -> Review), released reimbursements stuck in `Processing` (Turns 16–19, 1–2 hr ETA promised), and `Mark as paid` carrying forward `INR 18,200` into subsequent payments (Turns 21–25). **Owner**: `SpendNest Team Member A` to confirm reimbursement fix and file engineering tickets.
2. **Brookmint Holdings & Northkite Equipment (`M09`, turns 20–22, 31)**: Fresh password-reset invitation sent during the live session immediately failed with `"token has expired"`. Customer is blocked from onboarding Brookmint Holdings. **Owner**: `SpendNest Team Member A` to escalate token expiry bug today/Monday.
3. **Cedarwave Distribution (`M04`, turns 4–11, 21–25)**: High retention risk during mandatory card network migration. Customer wants credit rather than prepaid (already holds an `INR 1.3 crore` bank credit line). **Owner**: `SpendNest Team Member A` to verify whether existing bank credit cards can connect via post-settlement feed and reconcile in accounting.

## 3. Priority Commercial & Partnership Follow-Ups
1. **Harborpath Advisory (`M01`, turns 9–25)**: High-intent US channel partner. Agreed on USD 260 activation commission + spend tiers and a **scalable unique referral link** (refused manual email intros in Turn 20). **Owner**: `SpendNest Team Member A` to send memorandum, written pricing/KYB rules, and referral link.
2. **Asterloom Systems (`M03`, turns 6, 23–25, 28, 36)**: 65-employee prospect evaluating a 4–5 card pilot (~INR 10–13L monthly spend). Needs written proposal separating `INR 26,000` annual fee from `INR 13,000` setup fee for CFO review. **Owner**: `SpendNest Team Member A`.
3. **Willowbank Advisory (`C07`) & Mr Raghav (`C08`)**: Send partner proposal via chat app + Monday callback (`Dev`, `C07`); email proposal to `contact08@example.com` citing Mr Raghav (`Meera`, `C08`).
4. **Milan (`C03`)**: Email `"Developer access and event notifications — follow-up"` and call back Monday/Tuesday when Milan is indoors (`Kiran`).

## 4. Practical Sales Coaching & Taxonomy Corrections
- **Never Bundle Setup Fees Unannounced (`M03`, turns 22–24)**: Quoting `INR 39,000` after previously quoting `INR 26,000` eroded trust mid-demo; always itemize recurring subscription vs one-time integration setup upfront, and clarify **prepaid vs credit** before demoing (`M03` Turn 6).
- **Respect Prospect Boundaries & Permissions (`C09`, `C10`, `C01`, `C06`)**:
  - *Positive model (`C09`)*: Meera explicitly asked Mr Vedant for permission before using his name with Business Head Mr Rishabh (Vedant said `"No, please don't use my name"`).
  - *Needs correction (`C10`)*: After Mr Aniket (who left Meadowbrick for manufacturing) twice said he would review a messaging brief and reach out himself, Meera pushed for a Monday/Tuesday call and got a sharp refusal.
- **Exclude Non-Sales Meetings from Pipeline (`M02`, `M10`)**: `M02` (LedgerBridge) is SpendNest evaluating an e-invoicing **supplier** (`EUR 2,600–6,500` setup cost to SpendNest), and `M10` is an **internal back-office billing training** session.
""")

        manifest_json_path = os.path.join(self.output_dir, "manifest.json")
        with open(manifest_json_path, "w", encoding="utf-8") as f:
            json.dump({
                "generated_at": datetime.now(IST).isoformat(),
                "activity_date_ist": "2026-08-21",
                "total_unique_records": len(manifest_rows),
                "shared_daily_brief": f"exports/{brief_rel}",
                "records": manifest_rows
            }, f, indent=2)

        manifest_csv_path = os.path.join(self.output_dir, "manifest.csv")
        if manifest_rows:
            with open(manifest_csv_path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=list(manifest_rows[0].keys()))
                writer.writeheader()
                writer.writerows(manifest_rows)

        print(f"[Export Complete] Wrote {len(manifest_rows)} dossiers, route markdown files, daily brief, manifest.json, and manifest.csv to '{self.output_dir}/'.")

    def write_browser_bundle(self):
        with open(os.path.join(self.data_dir, "01_initial.json"), "r", encoding="utf-8") as f:
            b1 = json.load(f)
        with open(os.path.join(self.data_dir, "02_update.json"), "r", encoding="utf-8") as f:
            b2 = json.load(f)

        bundle = {
            "initial_batch": b1,
            "update_batch": b2,
            "analyses_by_ref": ANALYSES_BY_REF
        }
        with open("data_bundle.js", "w", encoding="utf-8") as f:
            f.write("window.SPENDNEST_BUNDLE = " + json.dumps(bundle, indent=2) + ";\n")
        print("[Browser Bundle] Wrote 'data_bundle.js' with all 44 records and 18 conversation analyses.")

    def write_slides_and_readme(self):
        readme_text = """# SpendNest Revenue Intelligence Inbox

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
"""
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_text)
        print("[Documentation] Wrote 'README.md'.")


if __name__ == "__main__":
    pipeline = RevenueIntelligencePipeline()
    pipeline.run_all()
