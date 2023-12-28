# background_service.py
from chaquo.python.android import Android

android = Android()

def run_background_service():
    # Call the Android method from Python
    android.callAttr("com.example.myapplication.ExampleJavaClass.androidMethod")

def call_android():
    return "fromPython"
