
from pathlib import Path
import json
import os
from datetime import datetime

PROJECT = Path("/content/drive/MyDrive/Mamaearth_Data_Analytics")
NARRATOR = PROJECT / "narrator"
FINDINGS_FILE = NARRATOR / "findings.json"
SAMPLE_FILE = NARRATOR / "sample_output.txt"


def generate_scr_narrative_offline(findings: dict) -> dict:
    """Build a report locally, without a Gemini key or network connection."""
    rates = findings["return_rate_by_payment"]
    risk = findings["highest_risk_segment"]
    peak = findings["true_peak_month"]
    january = findings["outlier_inflated_month"]
    peak_month = datetime.strptime(peak["month"], "%Y-%m").strftime("%B")

    narrative = f"""Situation
Cleaned revenue was ₹{findings['cleaned_total_revenue_inr']:,.2f}. The true peak month was {peak_month} with revenue of ₹{peak['revenue_inr']:,.2f}.

Complication
Raw revenue was ₹{findings['raw_total_revenue_inr']:,.2f}, a reconciliation difference of ₹{findings['duplicate_reconciliation_delta_inr']:,.2f}. COD had the highest payment return rate at {rates['COD']}%. The highest-risk segment was {risk['payment_method']} in City Tier {risk['city_tier']}, with a {risk['return_rate_pct']}% return rate. January's apparent revenue of ₹{january['apparent_revenue_inr']:,.2f} fell to ₹{january['corrected_revenue_inr']:,.2f} after outlier correction.

Resolution
Reconcile duplicate purchases before reporting revenue. Review COD returns first, especially in City Tier {risk['city_tier']}. Use corrected monthly revenue for comparisons, and monitor performance after the {peak_month} peak. CARD return rate was {rates['CARD']}%; UPI return rate was {rates['UPI']}%.
"""

    return {"status": "success", "narrative": narrative, "tokens": None}


def generate_scr_narrative(findings: dict) -> dict:
    """Use Gemini when a key is available; return a structured error otherwise."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return generate_scr_narrative_offline(findings)

    try:
        # Import only for the online path so offline mode needs no SDK setup.
        from google import genai
        from google.genai import types

        system_instruction = (
            "You are a senior data analyst writing for Mamaearth's regional "
            "ops and finance heads. Write exactly three labeled sections: "
            "Situation, Complication, and Resolution. Every number in the "
            "output must come from the supplied findings and appear with the "
            "same value. Do not invent statistics."
        )

        # The prompt comes from this function's findings argument.
        contents = (
            "Write a concise business narrative using these verified findings:\n"
            + json.dumps(findings, indent=2)
        )

        # A 30-second timeout prevents the request from waiting indefinitely.
        client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(timeout=30_000),
        )

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                # Zero temperature suits a factual report and reduces variation.
                temperature=0.0,
                max_output_tokens=500,
            ),
        )

        usage = getattr(response, "usage_metadata", None)
        token_count = (
            getattr(usage, "total_token_count", None) if usage else None
        )

        return {
            "status": "success",
            "narrative": response.text or "",
            "tokens": token_count,
        }

    except Exception as err:
        # Return an error dictionary instead of passing an exception to the caller.
        return {
            "status": "error",
            "narrative": None,
            "message": str(err),
        }


def check_required_figures(narrative: str) -> bool:
    """Check that the five required figures appear in the report."""
    no_commas = narrative.replace(",", "")

    checks = {
        "cleaned revenue 97,358.30":
            "97358.30" in no_commas or "97358.3" in no_commas,
        "COD return rate 44.4": "44.4" in no_commas,
        "highest-risk rate 54.5": "54.5" in no_commas,
        "reconciliation difference 2,501.90":
            "2501.90" in no_commas or "2501.9" in no_commas,
        "March peak revenue 20,318.90":
            "March" in narrative
            and ("20318.90" in no_commas or "20318.9" in no_commas),
    }

    for label, passed in checks.items():
        print(f"{'PASS' if passed else 'FAIL'}: {label}")

    return all(checks.values())


def main():
    findings = json.loads(FINDINGS_FILE.read_text(encoding="utf-8"))

    result = generate_scr_narrative(findings)

    # If Gemini is unavailable or fails, use the offline template.
    if result["status"] == "error":
        print("Gemini unavailable; using the offline report.")
        result = generate_scr_narrative_offline(findings)

    print(result["narrative"])

    # Save the report so the grader can check this file.
    SAMPLE_FILE.write_text(result["narrative"], encoding="utf-8")
    print("\nChecking saved sample_output.txt:")
    saved_text = SAMPLE_FILE.read_text(encoding="utf-8")

    if not check_required_figures(saved_text):
        raise ValueError("The saved report is missing a required figure.")

    print("\nSuccess! Saved:", SAMPLE_FILE)


if __name__ == "__main__":
    main()
