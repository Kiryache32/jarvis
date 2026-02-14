import json
MEMORY_FILE = "data/memory.json"

def save_memory(entry):
    try:
        with open(MEMORY_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []
    data.append(entry)
    with open(MEMORY_FILE, "w") as f:
        json.dump(data, f, indent=2)
