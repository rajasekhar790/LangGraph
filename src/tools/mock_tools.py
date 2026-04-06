from langchain_core.tools import tool

@tool
def get_claims_history(member_id: str, last_n_days: int) -> dict:
    """Get the recent claims and billing history for a given member_id."""
    return {"claims": [
        {"claim_id": "CLM-9092", "date": "2026-03-12", "amount": 150.00, "status": "Paid"},
        {"claim_id": "CLM-9124", "date": "2026-03-20", "amount": 850.50, "status": "Pending"}
    ]}

@tool
def get_benefits_eligibility(member_id: str) -> dict:
    """Retrieve benefits coverage, copays, and deductible status for a member."""
    return {
        "plan_type": "PPO High Deductible",
        "in_network_deductible": 2000,
        "deductible_met": 1500,
        "pcp_copay": 25,
        "specialist_copay": 50,
        "status": "Active"
    }

@tool
def get_care_gaps(member_id: str) -> dict:
    """Check clinical records for care gaps, missing wellness visits, etc."""
    return {
        "care_gaps": [
            "Overdue Annual Prevention Visit",
            "Missing Flu Shot for Current Season"
        ],
        "primary_care_physician": "Dr. Sarah Smith"
    }

@tool
def get_recent_interactions(member_id: str) -> dict:
    """Retrieve the recent customer service call or chat logs for the member."""
    return {"interactions": [
        {"date": "2026-03-25", "channel": "Phone", "summary": "Member called to inquire about deductible status."},
        {"date": "2026-04-02", "channel": "Chat", "summary": "Member asked about how to file an appeal."}
    ]}