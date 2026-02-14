import time
from app.agents.soc import soc_agent

def autonomous_monitor():
    while True:
        soc_agent()
        time.sleep(30)
