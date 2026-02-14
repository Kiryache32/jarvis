from app.brain import llm_think
from app.swarm import swarm_analyze
from app.agents.soc import soc_agent
from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def planner(cmd):
    cmd = cmd.lower()
    if "миссия" in cmd:
        return swarm_analyze(cmd)
    if "soc" in cmd:
        return soc_agent()
    return llm_think(cmd)

def planner(text: str) -> str:
    if not text.strip():
        return "⚠️ Команда пуста"
    return f"🤖 JARVIS получил: {text}"
