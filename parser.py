import json
import os
from collections import defaultdict

class RevenueIntelligenceEngine:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.records = {}  # Key: (source_type, source_id) -> record dict
        self.manual_routes = {}  # Key: (source_type, source_id) -> list of routes
        self.review_states = {}  # Key: (source_type, source_id) -> state dict

    def load_batch(self, filepath, batch_revision):
        """Loads a delivery batch and upserts records based on (source_type, source_id) and revision rules."""
        if not os.path.exists(filepath):
            print(f"Notice: {filepath} not found locally. Ensure data files are placed in the 'data/' directory.")
            return
        
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        envelope_rev = data.get("revision", batch_revision)
        for rec in data.get("records", []):
            stype = rec.get("source_type")
            sid = rec.get("source_id") or rec.get("payload", {}).get("id")
            key = (stype, sid)
            
            current = self.records.get(key)
            # Apply update only if record is new or has a higher/equal revision update
            if current is None or envelope_rev >= current.get("applied_revision", 1):
                rec_copy = dict(rec)
                rec_copy["applied_revision"] = envelope_rev
                self.records[key] = rec_copy
                
                # Initialize or update review states
                if key not in self.review_states:
                    self.review_states[key] = {
                        "intake_status": "Intake Complete",
                        "analysis_status": "Fresh",
                        "manual_override": False
                    }
                else:
                    # If source updated and no manual override is active, mark analysis as pending review
                    if envelope_rev > current.get("applied_revision", 1) and not self.review_states[key]["manual_override"]:
                        self.review_states[key]["analysis_status"] = "Pending Review (Stale Transcript)"

    def apply_manual_correction(self, source_type, source_id, new_routes):
        """Manually updates a conversation route, preserving judgment across replays and updates."""
        key = (source_type, source_id)
        if key in self.records:
            self.manual_routes[key] = new_routes
            self.review_states[key]["manual_override"] = True
            self.review_states[key]["analysis_status"] = "Corrected & Verified"

    def compute_metrics(self):
        """Computes strict denominators for dashboard KPIs."""
        total_records = len(self.records)
        calls = [r for r in self.records.values() if r.get("source_type") == "call"]
        meetings = [r for r in self.records.values() if r.get("source_type") == "meeting"]
        
        usable_texts = 0
        for r in self.records.values():
            stype = r.get("source_type")
            payload = r.get("payload", {})
            trans_payload = r.get("transcript_payload", {}) or {}
            
            if stype == "call":
                if payload.get("transcript"):
                    usable_texts += 1
            elif stype == "meeting":
                turns = trans_payload.get("turns", [])
                if turns and len(turns) > 0:
                    usable_texts += 1
                    
        coverage_pct = (usable_texts / total_records) * 100 if total_records > 0 else 0
        
        return {
            "total_records": total_records,
            "total_calls": len(calls),
            "total_meetings": len(meetings),
            "usable_supplied_texts": usable_texts,
            "transcript_coverage_percent": round(coverage_pct, 2)
        }

    def generate_manifest(self, output_dir="exports"):
        """Generates the machine-readable JSON export manifest."""
        os.makedirs(output_dir, exist_ok=True)
        manifest_rows = []
        
        for key, rec in self.records.items():
            stype, sid = key
            ref = rec.get("record_ref", sid[:6])
            rev = rec.get("applied_revision", 1)
            state = self.review_states.get(key, {})
            override = state.get("manual_override", False)
            routes = self.manual_routes.get(key, ["Standard Review"])
            
            manifest_rows.append({
                "source_type": stype,
                "source_id": sid,
                "record_ref": ref,
                "applied_revision": rev,
                "routes": "; ".join(routes),
                "output_path": f"{output_dir}/{stype}_{ref}.json",
                "review_state": state.get("intake_status", "Intake Complete"),
                "analysis_freshness": state.get("analysis_status", "Fresh"),
                "manual_override": override
            })
            
        manifest_path = os.path.join(output_dir, "manifest.json")
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest_rows, f, indent=2)
        return manifest_path

if __name__ == "__main__":
    print("Revenue Intelligence Engine module ready.")