from memory.memory_manager import MemoryManager
from utils.hf_llm import query_llm
import json

class ClassifierAgent:
    def __init__(self, memory: MemoryManager):
        self.memory = memory

    def classify_and_route(self, content: str, ext: str, source_name: str):
        prompt = f"""
You are a document classifier agent.

Document Content:
\"\"\"
{content}
\"\"\"

Classify:
- Format: One of [PDF, JSON, Email]
- Intent: One of [Invoice, RFQ, Complaint, Regulation, Unknown]

Respond strictly in JSON:
{{
  "format": "...",
  "intent": "..."
}}
        """

        response = query_llm(prompt)

        # Debug raw LLM output (optional)
        print("===== RAW LLM RESPONSE =====")
        print(response)

        try:
            parsed = json.loads(
                response.strip().split("```")[-1] if "```" in response else response
            )
            fmt = parsed.get("format", "Unknown").strip()
            intent = parsed.get("intent", "Unknown").strip()
        except Exception:
            fmt, intent = "Unknown", "Unknown"

        self.memory.log({
            "source": source_name,
            "type": fmt,
            "intent": intent
        })

        return fmt, intent
