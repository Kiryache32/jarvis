from threading import Thread
from app.gui import JarvisGUI
from app.siem import autonomous_monitor

def start_app():
    Thread(target=autonomous_monitor, daemon=True).start()
    JarvisGUI().run()
