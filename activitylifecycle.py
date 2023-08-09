# my_script.py

from jnius import autoclass

# Get the Java classes
PythonActivity = autoclass('org.kivy.android.PythonActivity')

def main():
    # Get the Context of the current Android application
    activity = PythonActivity.mActivity
    context = activity.getApplicationContext()
    
    # Get the package name of the Context
    package_name = context.getPackageName()
    print("Package Name:", package_name)
    
