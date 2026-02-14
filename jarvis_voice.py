import speech_recognition as sr
import pyttsx3
import subprocess
import webbrowser
import time
import os
import re
import sys
import winreg
import pyautogui
import psutil
from PIL import ImageGrab
import cv2
import numpy as np

# ================== АВТОЗАПУСК ==================
def add_to_startup():
    try:
        pythonw = sys.executable.replace("python.exe", "pythonw.exe")
        script_path = os.path.abspath(__file__)
        command = f'"{pythonw}" "{script_path}"'

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )

        winreg.SetValueEx(key, "JarvisVoice", 0, winreg.REG_SZ, command)
        winreg.CloseKey(key)
    except:
        pass

add_to_startup()

# ================== НАСТРОЙКИ ==================
WAKE_WORD = "джарвис"
INACTIVITY_TIMEOUT = 30
CACHE_FILE = "app_cache.txt"

SEARCH_DIRS = [
    "C:\\Program Files",
    "C:\\Program Files (x86)",
    "C:\\Users",
    "D:\\"
]

# ================== ГОЛОС ==================
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# ================== КЭШ ПРИЛОЖЕНИЙ ==================
APP_CACHE = {}

def scan_all_apps():
    print("Сканирование приложений...")
    APP_CACHE.clear()

    for base in SEARCH_DIRS:
        for root, dirs, files in os.walk(base):
            for file in files:
                if file.lower().endswith(".exe"):
                    name = file.lower().replace(".exe", "").replace(" ", "")
                    APP_CACHE[name] = os.path.join(root, file)

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        for name, path in APP_CACHE.items():
            f.write(f"{name}|{path}\n")

def load_cache():
    if not os.path.exists(CACHE_FILE):
        scan_all_apps()
        return

    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        for line in f:
            name, path = line.strip().split("|")
            APP_CACHE[name] = path

load_cache()

# ================== ПОИСК ПРИЛОЖЕНИЯ ==================
def find_exe(app_name):
    app_name = app_name.lower().replace(" ", "")

    if app_name in APP_CACHE:
        return APP_CACHE[app_name]

    for name, path in APP_CACHE.items():
        if app_name in name:
            return path

    return None

# ================== ЗАКРЫТИЕ ==================
def close_current_window():
    pyautogui.hotkey("alt", "f4")

def close_all_apps():
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] not in ["explorer.exe"]:
                proc.terminate()
        except:
            pass

# ================== VPN ==================
# ================== VPN CLICK CONNECT ==================

VPN_PATH = r"C:\Program Files\Click Connect\app.exe"

def vpn_connect():
    if os.path.exists(VPN_PATH):
        subprocess.Popen(VPN_PATH)
        speak("Открываю Click Connect")
        time.sleep(5)

        # Нажимаем кнопку Connect (если активна по Enter)
        pyautogui.press("enter")

        speak("VPN подключается")
    else:
        speak("Click Connect не найден по указанному пути")

def vpn_disconnect():
    # Закрываем окно VPN
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if "app.exe" in proc.info['name'].lower():
                proc.terminate()
        except:
            pass

    speak("VPN отключен")


def vpn_disconnect():
    pyautogui.hotkey("alt", "f4")
    speak("VPN отключен")

# ================== УТИЛИТЫ ==================
def clean_command(text):
    remove_words = [
        "открой", "запусти", "перейди",
        "на", "в", "джарвис", "пожалуйста",
        "закрой",
    ]
    text = text.lower()
    for w in remove_words:
        text = text.replace(w, "")
    return text.strip()

# ================== РАСПОЗНАВАНИЕ ==================
recognizer = sr.Recognizer()
microphone = sr.Microphone()

sleeping = False
last_activity = time.time()

speak("Джарвис онлайн")

while True:
    try:
        if not sleeping and time.time() - last_activity > INACTIVITY_TIMEOUT:
            sleeping = True
            speak("Я в режиме ожидания")

        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)

        command = recognizer.recognize_google(audio, language="ru-RU").lower()
        print("Ты сказал:", command)

        # ===== СОН =====
        if "отключись" in command:
            sleeping = True
            speak("Перехожу в режим ожидания")
            continue

        if sleeping:
            if WAKE_WORD in command:
                sleeping = False
                last_activity = time.time()
                speak("Я здесь")
            continue

        last_activity = time.time()

        # ===== VPN =====
        if "включи впн" in command:
            if not vpn_connect():
                speak("VPN не найден")
            continue

        if "выключи впн" in command:
            vpn_disconnect()
            continue

        # ===== ЗАКРЫТИЕ =====
        if "текущее окно" in command:
            close_current_window()
            speak("Закрываю окно")
            continue

        if "закрой все и сохрани" in command:
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1)
            close_all_apps()
            speak("Закрываю все приложения")
            continue

        # ===== ОТКРЫТИЕ =====
        if "открой" in command or "запусти" in command:
            target = clean_command(command)

            exe = find_exe(target)
            if exe:
                subprocess.Popen(exe)
                speak(f"Открываю {target}")
                continue

            speak("Не нашёл приложение")
            continue

        # ===== ПОИСК =====
        if "найди" in command:
            query = clean_command(command.replace("найди", ""))
            webbrowser.open(f"https://yandex.ru/search/?text={query}")
            speak(f"Ищу {query}")
            continue

        if "картинки" in command:
            query = clean_command(command.replace("картинки", ""))
            webbrowser.open(f"https://yandex.ru/images/search?text={query}")
            speak(f"Показываю картинки {query}")
            continue

    except:
        pass
