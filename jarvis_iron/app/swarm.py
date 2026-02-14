from app.agents.soc import soc_agent
from app.agents.network import network_agent
from app.agents.logs import logs_agent
from app.agents.code import code_agent
from app.agents.ctf import ctf_agent
from app.brain import llm_think

def swarm_analyze(task):
    data = {
        "SOC": soc_agent(),
        "NETWORK": network_agent(),
        "LOGS": logs_agent(),
        "CODE": code_agent(),
        "CTF": ctf_agent()
    }
    return llm_think(f"Задача: {task}\nДанные агентов: {data}")
