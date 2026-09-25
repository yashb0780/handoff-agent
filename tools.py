from langchain.tools import tool

# Fake Salesforce data (pretend this came from a real CRM)
SALESFORCE = {
    "acme corp": {
        "account": "Acme Corp",
        "industry": "Healthcare",
        "arr": 120000,
        "products": ["Service Desk", "Asset Management"],
        "close_date": "2026-09-15",
        "contacts": [
            {"name": "Priya Shah", "role": "IT Director", "type": "Champion"},
            {"name": "Mark Lee", "role": "CFO", "type": "Economic buyer"},
        ],
        "rep_notes": "Replacing legacy ticketing tool. Wants go-live before Q1 audit.",
    }
}

# Fake Gong call insights (pretend these came from call recordings)
GONG = {
    "acme corp": [
        {
            "date": "2026-08-20",
            "title": "Discovery call",
            "pain_points": ["Tickets lost in email", "No asset visibility"],
            "goals": ["Cut ticket response time in half", "Pass Q1 compliance audit"],
            "promises_made": ["SSO setup in week 1", "Data migration help from our team"],
        }
    ]
}


@tool
def get_salesforce_deal(account_name: str) -> dict:
    """Look up the closed deal in Salesforce: ARR, products, contacts, and sales rep notes."""
    return SALESFORCE.get(account_name.lower(), {"error": "Not found in Salesforce"})


@tool
def get_gong_calls(account_name: str) -> list:
    """Look up Gong call insights: pain points, goals, and promises made during the sales process."""
    return GONG.get(account_name.lower(), [{"error": "No Gong calls found"}])

