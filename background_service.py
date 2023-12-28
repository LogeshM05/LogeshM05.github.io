# background_service.py
from chaquo.python.android import Android
import time

android = Android()

def run_background_service():
    while True:
        android.notification('Background Service', 'Running...')
        time.sleep(10)  # Sleep for 10 seconds
