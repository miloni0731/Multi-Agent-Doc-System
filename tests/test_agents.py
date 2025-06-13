import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
from agents.classifier_agent import ClassifierAgent
from agents.json_agent import JSONAgent
from agents.email_agent import EmailAgent
from memory.memory_manager import MemoryManager

def test_classifier():
    print("\n--- Testing Classifier Agent ---")
    memory = MemoryManager(path="memory/test_memory_classifier.json")
    agent = ClassifierAgent(memory)
    sample_text = "Please send us a quotation for air conditioners."
    format_type, intent = agent.classify_and_route(sample_text, "txt", "test_email.txt")

    assert format_type in ["Email", "PDF", "JSON"], f"Invalid format detected: {format_type}"
    assert intent in ["Invoice", "RFQ", "Complaint", "Regulation", "Unknown"], f"Unexpected intent: {intent}"

    logs = memory.get_memory()
    assert any(log["type"] == format_type for log in logs), "Format not logged"
    assert any(log["intent"] == intent for log in logs), "Intent not logged"

    print(" ClassifierAgent test passed.")
    os.remove("memory/test_memory_classifier.json")


def test_email_agent():
    print("\n--- Testing Email Agent ---")
    memory = MemoryManager(path="memory/test_memory_email.json")
    agent = EmailAgent(memory)
    email_text = "From: alice@example.com\nSubject: Complaint\n\nThis is unacceptable service. Fix this immediately!"
    result = agent.process_email(email_text, "test_email.txt")

    assert "sender" in result, "Sender missing in result"
    assert result["urgency"] in ["High", "Medium", "Low", "Unknown"], f"Invalid urgency: {result['urgency']}"
    assert result["intent"] in ["Invoice", "RFQ", "Complaint", "Regulation", "Unknown"], f"Invalid intent: {result['intent']}"

    logs = memory.get_memory()
    assert any("email_meta" in log for log in logs), "Email metadata not logged"

    print(" EmailAgent test passed.")
    os.remove("memory/test_memory_email.json")


def test_json_agent():
    print("\n--- Testing JSON Agent ---")
    memory = MemoryManager(path="memory/test_memory_json.json")
    agent = JSONAgent(memory)
    json_text = json.dumps({
        "id": "INV-001",
        "amount": 2500,
        "sender": "XYZ Corp"
        # 'date' is missing intentionally
    })
    result = agent.process_json(json_text, "test_invoice.json")

    assert "standardized" in result, "Standardized field missing"
    assert isinstance(result.get("missing_fields", []), list), "Missing fields should be a list"
    assert "date" in result["missing_fields"], "'date' should be flagged as missing"

    logs = memory.get_memory()
    assert any("json_data" in log for log in logs), "JSON data not logged"

    print(" JSONAgent test passed.")
    os.remove("memory/test_memory_json.json")


if __name__ == "__main__":
    print("Choose a test to run:")
    print("1. ClassifierAgent")
    print("2. EmailAgent")
    print("3. JSONAgent")
    print("4. All")

    choice = input("Enter choice (1/2/3/4): ").strip()

    if choice == "1":
        test_classifier()
    elif choice == "2":
        test_email_agent()
    elif choice == "3":
        test_json_agent()
    elif choice == "4":
        test_classifier()
        test_email_agent()
        test_json_agent()
    else:
        print("Invalid choice.")
