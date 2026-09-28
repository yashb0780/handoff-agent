from langchain.tools import tool

# Fake Salesforce data (pretend this came from a real CRM)
# Two different customers both named "Acme". The website tells them apart.
SALESFORCE = {
    "acme corp": {
        "account": "Acme Corp",
        "website": "acme.com",
        "industry": "Healthcare",
        "arr": 120000,
        "products": ["Service Desk", "Asset Management"],
        "close_date": "2026-09-15",
        "contacts": [
            {"name": "Priya Shah", "role": "IT Director", "type": "Champion"},
            {"name": "Mark Lee", "role": "CFO", "type": "Economic buyer"},
        ],
        "rep_notes": "Replacing legacy ticketing tool. Wants go-live before Q1 audit.",
    },
    "acme inc": {
        "account": "Acme Inc",
        "website": "tryacme.com",
        "industry": "Retail",
        "arr": 45000,
        "products": ["Service Desk"],
        "close_date": "2026-09-10",
        "contacts": [
            {"name": "Daniel Kim", "role": "Head of IT Ops", "type": "Champion"},
        ],
        "rep_notes": "Small IT team. Wants self-serve onboarding, light touch.",
    },
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
    ],
    "acme inc": [
        {
            "date": "2026-08-28",
            "title": "Demo call",
            "pain_points": ["Store managers email IT directly", "No ticket tracking"],
            "goals": ["One place for all store IT requests"],
            "promises_made": ["Onboarding videos for store managers"],
        }
    ],
}


def clean(text: str) -> str:
    """Tidy up what the CSM typed: 'https://www.Acme.com/' becomes 'acme.com'."""
    text = text.strip().lower()
    for prefix in ["https://", "http://", "www."]:
        if text.startswith(prefix):
            text = text[len(prefix):]
    return text.strip("/. ")


def find_accounts(query: str) -> list:
    """Return every account that matches a website or a name."""
    q = clean(query)
    # 1. Website: must match the WHOLE domain (so acme.co never matches acme.com)
    by_website = [key for key, acct in SALESFORCE.items() if acct["website"] == q]
    if by_website:
        return by_website
    # 2. Exact name
    if q in SALESFORCE:
        return [q]
    # 3. First word of the name, e.g. "acme" matches "acme corp" AND "acme inc"
    return [key for key in SALESFORCE if key.startswith(q + " ")]


def matches_or_error(query: str, system: str):
    """Shared answer for both tools: one match, several, or none."""
    keys = find_accounts(query)
    if len(keys) == 0:
        return None, {"error": f"No account found in {system} for '{query}'"}
    if len(keys) > 1:
        options = [
            {"account": SALESFORCE[k]["account"], "website": SALESFORCE[k]["website"]}
            for k in keys
        ]
        return None, {"multiple_matches": options, "note": "Ask the CSM which one they mean."}
    return keys[0], None


@tool
def get_salesforce_deal(account: str) -> dict:
    """Look up the closed deal in Salesforce: ARR, products, contacts, and sales rep notes.
    'account' can be an account name (e.g. 'Acme Corp') or a website (e.g. 'acme.com'
    or 'https://www.acme.com'). If the CSM gave a website, pass the website."""
    key, problem = matches_or_error(account, "Salesforce")
    return problem if problem else SALESFORCE[key]


@tool
def get_gong_calls(account: str) -> list:
    """Look up Gong call insights: pain points, goals, and promises made during sales.
    'account' can be an account name or a website. Pass the same website Salesforce
    returned, so both tools describe the same customer."""
    key, problem = matches_or_error(account, "Gong")
    return [problem] if problem else GONG[key]
