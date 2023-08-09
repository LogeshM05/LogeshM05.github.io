from com.chaquo.python.android import AndroidContext

def on_created(activity_name):
    print(f"Activity created: {activity_name}")
    # Add your Python logic here for when an activity is created

def on_started(activity_name):
    print(f"Activity started: {activity_name}")

def on_resumed(activity_name):
    print(f"Activity resumed: {activity_name}")

def on_paused(activity_name):
    print(f"Activity paused: {activity_name}")

def on_stopped(activity_name):
    print(f"Activity stopped: {activity_name}")

def on_destroyed(activity_name):
    print(f"Activity destroyed: {activity_name}")

def register_android_lifecycle_events(context):
    application = context.getApplicationContext()

    my_lifecycle = context.getModule("androidlifecycle")
    
    class MyLifecycleCallbacks(application.ActivityLifecycleCallbacks):
        def onActivityCreated(self, activity, savedInstanceState):
            my_lifecycle.on_created(activity.getClass().getSimpleName())

        def onActivityStarted(self, activity):
            my_lifecycle.on_started(activity.getClass().getSimpleName())

        def onActivityResumed(self, activity):
            my_lifecycle.on_resumed(activity.getClass().getSimpleName())

        def onActivityPaused(self, activity):
            my_lifecycle.on_paused(activity.getClass().getSimpleName())

        def onActivityStopped(self, activity):
            my_lifecycle.on_stopped(activity.getClass().getSimpleName())

        def onActivityDestroyed(self, activity):
            my_lifecycle.on_destroyed(activity.getClass().getSimpleName())

    callbacks = MyLifecycleCallbacks()
    application.registerActivityLifecycleCallbacks(callbacks)
