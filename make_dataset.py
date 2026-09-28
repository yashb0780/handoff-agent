from dotenv import load_dotenv
from langsmith import Client

load_dotenv()
client = Client()

dataset = client.create_dataset(
    dataset_name="handoff-agent-tests",
    description="Real ways a CSM might ask for a handoff doc",
)

examples = [
    {"inputs": {"request": "Build the handoff doc for acme.com"},
     "outputs": {"expected": "acme corp"}},
    {"inputs": {"request": "Build the handoff doc for tryacme.com"},
     "outputs": {"expected": "acme inc"}},
    {"inputs": {"request": "Build the handoff doc for Acme Corp"},
     "outputs": {"expected": "acme corp"}},
    {"inputs": {"request": "Build the handoff doc for ACME CORP."},
     "outputs": {"expected": "acme corp"}},
    {"inputs": {"request": "Build the handoff doc for acme"},
     "outputs": {"expected": "ambiguous"}},
    {"inputs": {"request": "Build the handoff doc for Globex Inc"},
     "outputs": {"expected": "not_found"}},
]

client.create_examples(dataset_id=dataset.id, examples=examples)
print("Done. Created dataset with", len(examples), "examples.")
