from java import jclass as autoclass

Application = autoclass('android.app.Application')
Activity = autoclass('android.app.Activity')
Bundle = autoclass('android.os.Bundle')
Log = autoclass('android.util.Log')

class ApplicationLifecycleCallbacksWrapper:
    def __init__(self):
        self.application = Application.getApplication()
        self.lifecycle_callbacks = ApplicationLifecycleCallbacks()

    def initialize(self):
        self.application.registerActivityLifecycleCallbacks(self.lifecycle_callbacks)

    def on_activity_created(self, activity, bundle):
        try:
            activity_instance = cast(Activity, activity)
            bundle_instance = cast(Bundle, bundle)
            self.lifecycle_callbacks.onActivityCreated(activity_instance, bundle_instance)
        except Exception as e:
            Log.e("ApplicationLifecycle", "Error in on_activity_created: " + str(e))