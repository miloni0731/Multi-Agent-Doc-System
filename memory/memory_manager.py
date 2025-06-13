import os
import json
import threading
from datetime import datetime, timezone

class MemoryManager:
    def __init__(self, path: str = "memory/memory_log.json"):
        self.path = path
        self.memory = []
        self.lock = threading.Lock()

        # Load existing memory if available
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as f:
                try:
                    self.memory = json.load(f)
                except json.JSONDecodeError:
                    self.memory = []

    def log(self, entry: dict):
        """
        Log a new entry to shared memory with timestamp and optional agent tag.
        """
        entry["timestamp"] = datetime.now(timezone.utc).isoformat()
        entry.setdefault("agent", "unknown")

        # Ensure memory directory exists
        os.makedirs(os.path.dirname(self.path), exist_ok=True)

        with self.lock:
            self.memory.append(entry)
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.memory, f, indent=4)

    def get_memory(self):
        """
        Return all memory as list of dicts.
        """
        return self.memory

    def get_memory_df(self):
        """
        Return memory as pandas DataFrame for analysis.
        """
        import pandas as pd
        return pd.DataFrame(self.memory)

    def export_csv(self, csv_path: str = "memory/memory_export.csv"):
        """
        Export memory to CSV format.
        """
        import pandas as pd
        df = pd.DataFrame(self.memory)
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        df.to_csv(csv_path, index=False)
