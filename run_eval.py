from dotenv import load_dotenv
from langsmith import Client
from agent import agent

load_dotenv()
client = Client()

FOUND = ["acme corp", "acme inc"]  # answer keys where a real doc should be built


# How to run the agent on one test request
def run_agent(inputs: dict) -> dict:
    result = agent.invoke(
        {"messages": [{"role": "user", "content": inputs["request"]}]}
    )
    return {"answer": result["messages"][-1].content}


# Grader 1: right account (exact values)
def right_account(outputs: dict, reference_outputs: dict) -> bool:
    answer = outputs["answer"].lower()
    expected = reference_outputs["expected"]

    has_priya = "priya" in answer
    has_daniel = "daniel" in answer
    mentions_tryacme = "tryacme.com" in answer
    mentions_acme = "acme.com" in answer.replace("tryacme.com", "")

    if expected == "acme corp":
        return has_priya and not has_daniel
    if expected == "acme inc":
        return has_daniel and not has_priya and "audit" not in answer
    if expected == "ambiguous":
        return mentions_acme and mentions_tryacme and not has_priya and not has_daniel
    if expected == "not_found":
        return not has_priya and not has_daniel
    return False


# Grader 2: no invented sponsor (exact phrase)
def no_invented_sponsor(outputs: dict, reference_outputs: dict) -> bool:
    if reference_outputs["expected"] not in FOUND:
        return True  # no doc expected, nothing to check
    answer = outputs["answer"].lower()
    sponsor_lines = [line for line in answer.split("\n") if "sponsor" in line]
    return any("not found" in line for line in sponsor_lines)


# Grader 3: sources tagged (pattern)
def sources_tagged(outputs: dict, reference_outputs: dict) -> bool:
    if reference_outputs["expected"] not in FOUND:
        return True  # no doc expected, nothing to check
    return "(source:" in outputs["answer"].lower()


# Run all tests through the agent and grade them
client.evaluate(
    run_agent,
    data="handoff-agent-tests",
    evaluators=[right_account, no_invented_sponsor, sources_tagged],
    experiment_prefix="after-fix",
    max_concurrency=1,
)

