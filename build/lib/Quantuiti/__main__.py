from flask import Flask
import logging
import webbrowser
import threading
import subprocess
from .__init__ import CompuTradeEngine
def start_server():
    log = logging.getLogger('werkzeug')
    log.disabled = False


    app = Flask(__name__, static_folder='./build', static_url_path='/')
    
    @app.route('/', defaults={'path': ''})
    @app.route('/<path>')
    def index(path):
        return app.send_static_file('index.html')

    @app.route('/api')
    def api():
        print('ACCESS')
        return 'ok', 200

    @app.route("/run_script")
    def run():
        subprocess.run(["ls -l"], shell=True, check=True)
        return "ok", 200

    url = 'http://localhost:3000'
    threading.Timer(1.25, lambda: webbrowser.open(url)).start()
    app.run(port='3000', debug=False)

if __name__ == "__main__":
    start_server()