from chaquopy import chaquopy_java_init
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

# Register the ActivityLifecycleCallbacks
application = Application.getApplication()
callbacks = MyActivityLifecycleCallbacks()
application.registerActivityLifecycleCallbacks(callbacks)

# Define a function to periodically check the lifecycle status
def check_lifecycle_status():
    while True:
        time.sleep(5)  # Sleep for 5 seconds
        print("Current Activity Lifecycle Status:", current_lifecycle_status)

# Start the thread to periodically check the lifecycle status
thread = threading.Thread(target=check_lifecycle_status)
thread.start()

def hello_world():
    return 'Hello from Flask!'

# @app.route('/location')
def location():
    return 'This is your location!'

def call_java_function():
    result = DemoActivity.fromPython()
    return result

def get_activity_lifecycle():
    
