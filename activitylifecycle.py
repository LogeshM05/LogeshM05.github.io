import android

class MyLifecycleCallbacks:
    def __init__(self, application):
        self.application = application

    def onCreate(self):
        android.makeToast("App: onCreate called")

    def onStart(self):
        android.makeToast("App: onStart called")

    def onResume(self):
        android.makeToast("App: onResume called")

    def onPause(self):
        android.makeToast("App: onPause called")

    def onStop(self):
        android.makeToast("App: onStop called")

    def onDestroy(self):
        android.makeToast("App: onDestroy called")

    def registerLifecycleCallbacks(self):
        self.application.registerActivityLifecycleCallbacks(self)
