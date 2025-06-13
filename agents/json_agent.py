from memory.memory_manager import MemoryManager
from utils.hf_llm import query_llm
import json

class JSONAgent:
    def __init__(self, memory: MemoryManager):
        self.memory = memory

    def process_json(self, content: str, source_name: str):
        prompt = f"""
You are a JSON document agent.

Given this structured JSON content:
\"\"\"
{content}
\"\"\"

Do the following:
1. Reformat into a standard schema with fields: id, date, amount, sender
2. List missing or null fields from this schema
3. Report everything in JSON format as:
{{
  "standardized": {{...}},
  "missing_fields": [...]
}}

Respond only in JSON.
        """

        response = query_llm(prompt)

        # Optional: Debug print
        print("===== RAW JSON AGENT LLM RESPONSE =====")
        print(response)

        try:
            result = json.loads(
                response.strip().split("```")[-1] if "```" in response else response
            )
            result["standardized"] = result.get("standardized", {})
            result["missing_fields"] = result.get("missing_fields", [])
        except Exception:
            result = {
                "standardized": {},
                "missing_fields": ["Unknown"]
            }

        self.memory.log({
            "source": source_name,
            "json_data": result
        })

        return result
