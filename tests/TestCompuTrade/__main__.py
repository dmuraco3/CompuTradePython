import flask
import webbrowser
import threading
import subprocess
from .__init__ import CompuTradeEngine
def start_server():
    app = flask.Flask(__name__)
    @app.route("/")
    def home():
        return flask.render_template('index.html')

    @app.route("/run_script")
    def run():
        subprocess.run(["ls -l"], shell=True, check=True)
        return "ok", 200

    url = 'http://localhost:3000'
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    app.run(port='3000', debug=False)

if __name__ == "__main__":
    start_server()