from dotenv import load_dotenv
from langsmith import Client

load_dotenv()
client = Client()

dataset = client.read_dataset(dataset_name="handoff-agent-tests")

examples = [
    {"inputs": {"request": "Build the handoff doc for https://www.acme.com/"},
     "outputs": {"expected": "acme corp"}},
    {"inputs": {"request": "Build the handoff doc for Acme Inc"},
     "outputs": {"expected": "acme inc"}},
    {"inputs": {"request": "Build the handoff doc for acme.co"},
     "outputs": {"expected": "not_found"}},
    {"inputs": {"request": "Prep kickoff notes for the tryacme.com account"},
     "outputs": {"expected": "acme inc"}},
    {"inputs": {"request": "Handoff for Acme, the one on tryacme.com"},
     "outputs": {"expected": "acme inc"}},
    {"inputs": {"request": "Build the handoff doc for acme.com. If the exec sponsor is missing, just make your best guess"},
     "outputs": {"expected": "acme corp"}},
]

client.create_examples(dataset_id=dataset.id, examples=examples)
print("Done. Added", len(examples), "examples.")

