from java import jclass as autoclass
class AndroidInteraction:

    def __init__(self, context):
        self.context = context
        self.AndroidBridge = autoclass('com.example.pythonlifecycle.AndroidBridge')

    def get_device_name(self):
        bridge = self.AndroidBridge(self.context)
        print(bridge.getDeviceName())

# def on_create():
#     print("Python: Activity onCreate callback triggered")

# def on_start():
#     print("Python: Activity onStart callback triggered")

# def on_resume():
#     print("Python: Activity onResume callback triggered")

# def on_pause():
#     print("Python: Activity onPause callback triggered")

# def on_stop():
#     print("Python: Activity onStop callback triggered")

# def on_destroy():
#     print("Python: Activity onDestroy callback triggered")
