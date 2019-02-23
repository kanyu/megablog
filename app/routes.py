from app import myApp


@myApp.route('/')
@myApp.route('/index')
def index():
    return "Hello, World!"