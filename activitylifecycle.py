from java import jclass as autoclass

Activity = autoclass('android.app.Activity')
Bundle = autoclass('android.os.Bundle')
Application = autoclass('android.app.Application')
Application_ActivityLifecycleCallbacks = autoclass('android.app.Application$ActivityLifecycleCallbacks')

class PythonLifecyclePythonWrapper(Application_ActivityLifecycleCallbacks):

    def __init__(self):
        self.application = None

    def onActivityCreated(self, activity, savedInstanceState):
        print("onActivityCreated:", activity)
        
    def onActivityStarted(self, activity):
        print("onActivityStarted:", activity)

    def onActivityResumed(self, activity):
        print("onActivityResumed:", activity)

    def onActivityPaused(self, activity):
        print("onActivityPaused:", activity)

    def onActivityStopped(self, activity):
        print("onActivityStopped:", activity)

    def onActivitySaveInstanceState(self, activity, outState):
        print("onActivitySaveInstanceState:", activity)

    def onActivityDestroyed(self, activity):
        print("onActivityDestroyed:", activity)

    @staticmethod
    def attach(self, application):        
        print("onAttach successfully called")
        application.registerActivityLifecycleCallbacks(self)

        if self.application is not None:
            self.application.registerActivityLifecycleCallbacks(self)

# Create an instance of PythonLifecyclePythonWrapper
lifecycle_wrapper = PythonLifecyclePythonWrapper()
