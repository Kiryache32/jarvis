import psutil
def soc_agent():
    return f"SOC → CPU {psutil.cpu_percent()}% | RAM {psutil.virtual_memory().percent}%"
