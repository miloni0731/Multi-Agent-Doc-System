from memory.memory_manager import MemoryManager
from utils.hf_llm import query_llm
import json

class EmailAgent:
    def __init__(self, memory: MemoryManager):
        self.memory = memory

    def process_email(self, content: str, source_name: str):
        prompt = f"""
You are an intelligent email processor.

Given the email content:
\"\"\"
{content}
\"\"\"

Extract the following:
- Sender
- Urgency (High/Medium/Low)
- Intent (Invoice, RFQ, Complaint, Regulation, Unknown)

Respond strictly in JSON:
{{
  "sender": "...",
  "urgency": "...",
  "intent": "..."
}}
        """

        response = query_llm(prompt)

        # Optional debug print
        print("===== RAW EMAIL AGENT LLM RESPONSE =====")
        print(response)

        try:
            result = json.loads(
                response.strip().split("```")[-1] if "```" in response else response
            )
            # Optional: Normalize fields
            result["sender"] = result.get("sender", "Unknown").strip()
            result["urgency"] = result.get("urgency", "Unknown").strip()
            result["intent"] = result.get("intent", "Unknown").strip()
        except Exception:
            result = {"sender": "Unknown", "urgency": "Unknown", "intent": "Unknown"}

        self.memory.log({
            "source": source_name,
            "email_meta": result
        })

        return result
