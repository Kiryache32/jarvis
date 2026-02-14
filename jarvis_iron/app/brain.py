import requests

def llm_think(prompt):
    r = requests.post(
        "http://ollama:11434/api/generate",
        json={"model": "llama3", "prompt": prompt, "stream": False},
        timeout=120
    )
    return r.json().get("response", "LLM error")
