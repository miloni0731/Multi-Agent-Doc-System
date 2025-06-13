from agents.classifier_agent import ClassifierAgent
from agents.json_agent import JSONAgent
from agents.email_agent import EmailAgent
from memory.memory_manager import MemoryManager
from utils.file_loader import load_file
import os
import json

def main(file_path: str):
    if not os.path.exists(file_path):
        print(f"[❌] File not found: {file_path}")
        return

    file_extension = file_path.split(".")[-1].lower()
    try:
        content = load_file(file_path)
    except Exception as e:
        print(f"[❌] Error loading file: {e}")
        return

    memory = MemoryManager()
    classifier = ClassifierAgent(memory)
    email_agent = EmailAgent(memory)
    json_agent = JSONAgent(memory)

    print(f"\n Processing File: {file_path}")
    doc_format, intent = classifier.classify_and_route(content, file_extension, file_path)
    print(f" Detected Format: {doc_format}")
    print(f" Detected Intent: {intent}")

    result = None
    if doc_format == "Email":
        result = email_agent.process_email(content, file_path)
        print(" Email Metadata:", json.dumps(result, indent=2))
    elif doc_format == "JSON":
        result = json_agent.process_json(content, file_path)
        print(" JSON Parse Result:", json.dumps(result, indent=2))
    else:
        print(" No specialized processing for this document format.")

    # Save to output (optional)
    os.makedirs("data/output", exist_ok=True)
    base_name = os.path.basename(file_path)
    out_path = os.path.join("data/output", f"{base_name}.out.json")
    if result:
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)
        print(f" Output saved to {out_path}")
    else:
        print(" No output data to save.")

if __name__ == "__main__":
    # Default example file path
    test_file = "examples/sample_email.txt"  # Or sample_invoice.json, sample_complaint.pdf
    main(test_file)
