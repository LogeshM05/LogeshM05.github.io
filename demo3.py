from chaquopy import chaquopy_java_init

chaquopy_java_init()

from com.example.pythondemo import DemoActivity
from android.app import ActivityLifecycleCallbacks, Application
import threading
import time

chaquopy_java_init()

current_lifecycle_status = None

class MyActivityLifecycleCallbacks(ActivityLifecycleCallbacks):
    def onActivityResumed(self, activity):
        global current_lifecycle_status
        current_lifecycle_status = "Resumed"

    def onActivityPaused(self, activity):
        global current_lifecycle_status
        current_lifecycle_status = "Paused"

def hello_world():
    return 'Hello from Flask!'

# @app.route('/location')
def location():
    return 'This is your location!'

def call_java_function():
    result = DemoActivity.fromPython()
    return result
    