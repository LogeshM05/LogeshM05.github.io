from java import jclass as autoclass

PythonLifecyclePythonWrapper = autoclass('com.example.pythonlifecycle.PythonLifecyclePythonWrapper')

def onActivityCreated(activity, savedInstanceState):
    # Called when an activity is created
    pass

def onActivityStarted(activity):
    # Called when an activity is started
    pass

def onActivityResumed(activity):
    # Called when an activity is resumed
    pass

def onActivityPaused(activity):
    # Called when an activity is paused
    pass

def onActivityStopped(activity):
    # Called when an activity is stopped
    pass

def onActivitySaveInstanceState(activity, outState):
    # Called when an activity's state is saved
    pass

def onActivityDestroyed(activity):
    # Called when an activity is destroyed
    pass

def attach(application):
    PythonLifecyclePythonWrapper.attach(application)
