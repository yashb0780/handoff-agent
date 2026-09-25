from dotenv import load_dotenv
from langchain.agents import create_agent
from tools import get_salesforce_deal, get_gong_calls

load_dotenv()

SYSTEM_PROMPT = """You are a handoff agent for a Customer Success team.
When given a customer account name, use your tools to pull the closed deal
from Salesforce and the call insights from Gong. Then fill in this handoff doc:

1. Account basics (industry, ARR, products, close date)
2. Stakeholders (champion, economic buyer, executive sponsor)
3. Business goals
4. Pain points
5. Promises made during sales
6. Risks and red flags
7. Timeline expectations

Rules:
- Only use facts from your tools. Never guess or invent.
- If something is missing, write "Not found in Salesforce or Gong".
- After each fact, note its source, e.g. (Source: Salesforce) or (Source: Gong, 2026-08-20).
"""

agent = create_agent(
    model="anthropic:claude-haiku-4-5",
    tools=[get_salesforce_deal, get_gong_calls],
    system_prompt=SYSTEM_PROMPT,
)

