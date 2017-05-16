# Creating and Testing out our first Flask application

from flask import Flask
# Create an instance of this class with __name__ as the running argument
app = Flask(__name__)

# python decorator - when browser uses URL, the function specific to that URL gets executed
@app.route('/')
@app.route('/hello')


def HelloWorld():
    return "Hello World"

# if executed via python interpreter run this function
if __name__ == '__main__':
    # reload server when code change detected and run debug in browser
    app.debug = True
    # use to run local server with our application
    # special config for vagrant machine by making our host publicly available
    app.run(host='0.0.0.0', port=5000)

