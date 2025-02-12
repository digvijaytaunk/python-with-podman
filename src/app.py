import os
from flask import Flask
import debugpy

app = Flask(__name__)

# Only enable debugpy in the MAIN process, not in the auto-reloader
if os.environ.get("FLASK_RUN_FROM_CLI") == "true" and not os.environ.get("WERKZEUG_RUN_MAIN"):
    debugpy.listen(("0.0.0.0", 5670))
    print("⚡ Debugger is listening on port 5670. Attach from VS Code!")

@app.route('/')
def hello():
    return 'Hello, World!'

@app.route('/hi')
def hi():
    return '<h1>Hi Page</h1>'

@app.route('/temp')
def temp():
    return '<h1>Temp Page changes</h1>'

@app.route('/hero')
def hero():
    return '<h1>Hello Hero Page</h1>'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

