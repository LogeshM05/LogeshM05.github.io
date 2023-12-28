from com.example.pythondemo import DemoActivity

# Initialize the Python interpreter
AndroidPlatform.start_dir = None

def hello_world():
    return 'Hello from Flask!'

# @app.route('/location')
def location():
    return 'This is your location!'

def call_java_function():
    result = DemoActivity.fromPython()
    print(result)
