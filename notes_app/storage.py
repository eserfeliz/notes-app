import json
import os

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")

def load():
    try:
        with open(DATA_FILE, "r") as f:
            data = json.load(f)
            return {
                "notes": data.get("notes", []),
                "checklists": data.get("checklists", [])
            }
    except (FileNotFoundError, json.JSONDecodeError):
        return {"notes": [], "checklists": []}
    
def save(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)