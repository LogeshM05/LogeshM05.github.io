from java import jclass as autoclass

Activity = autoclass('android.app.Activity')
Bundle = autoclass('android.os.Bundle')

# class PythonLifecyclePythonWrapper:

    # @staticmethod
    def onActivityCreated(activity, savedInstanceState):
        # Called when an activity is created
        print("onActivityCreated:", activity)

    # @staticmethod
    def onActivityStarted(activity):
        # Called when an activity is started
        print("onActivityStarted:", activity)

    # @staticmethod
    def onActivityResumed(activity):
        # Called when an activity is resumed
        print("onActivityResumed:", activity)

    # @staticmethod
    def onActivityPaused(activity):
        # Called when an activity is paused
        print("onActivityPaused:", activity)

    # @staticmethod
    def onActivityStopped(activity):
        # Called when an activity is stopped
        print("onActivityStopped:", activity)

    # @staticmethod
    def onActivitySaveInstanceState(activity, outState):
        # Called when an activity's state is saved
        print("onActivitySaveInstanceState:", activity)

    # @staticmethod
    def onActivityDestroyed(activity):
        # Called when an activity is destroyed
        print("onActivityDestroyed:", activity)

    # @staticmethod
    def attach(application):        
        print("onAttach successfully called)

        # callback = PythonLifecyclePythonWrapper()
        # application.registerActivityLifecycleCallbacks(callback)
