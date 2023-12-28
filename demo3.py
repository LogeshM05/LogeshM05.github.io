from chaquopy import chaquopy_java_init
from com.example.pythondemo import DemoActivity

chaquopy_java_init()

def hello_world():
    return 'Hello from Flask!'

# @app.route('/location')
def location():
    return 'This is your location!'

def call_java_function():
    result = DemoActivity.fromPython()
    return result
