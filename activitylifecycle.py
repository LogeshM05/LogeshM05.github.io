# lifecycle_listener.py
from jnius import autoclass, PythonJavaClass, java_method

Activity = autoclass('android.app.Activity')
LifecycleObserver = autoclass('androidx.lifecycle.LifecycleObserver')
Lifecycle = autoclass('androidx.lifecycle.Lifecycle')
OnLifecycleEvent = autoclass('androidx.lifecycle.OnLifecycleEvent')

class MyLifecycleObserver(PythonJavaClass, LifecycleObserver):
    __javainterfaces__ = ['androidx/lifecycle/LifecycleObserver']

    def __init__(self, callback):
        super().__init__()
        self.callback = callback

    @java_method('()V')
    def on_create(self):
        self.callback('on_create')

# Add other lifecycle event methods here

def add_lifecycle_observer(activity, callback):
    lifecycle = activity.getLifecycle()
    observer = MyLifecycleObserver(callback)
    lifecycle.addObserver(observer)
