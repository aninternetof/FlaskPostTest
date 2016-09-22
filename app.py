from flask import Flask, request, render_template, Response, json
app = Flask(__name__)
import gevent
from gevent.pywsgi import WSGIServer
from gevent import monkey
from numpy import random
from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication
monkey.patch_all

# class OurStatus:
#     def __init__(self, default):
#         self.status = default
#
# current_status = OurStatus("uninited")

current_status = "uninitialized"

@app.route('/')
def index():
    return render_template('index.html')

def event():
    """For something more intelligent, take a look at Redis pub/sub
    stuff. A great example can be found here__.
    __ https://github.com/jakubroztocil/chat
    """
    while True:
        global current_status
        yield 'data: ' + json.dumps(current_status) + '\n\n'
        gevent.sleep(0.2)

@app.route('/status', methods=['POST'])
def handlestatus():
    status = request.form.get('status', None)
    if not status:
        return ('Missing status value', 400)
    print "Got some status: " + status
    # current_status.status = status
    global current_status
    current_status = status
    return ('', 200)

@app.route('/status', methods=['GET'])
def getstatus():
    return "Status is alive!"

@app.route('/stream/', methods=['GET', 'POST'])
def stream():
    print 'Something is connected!'
    return Response(event(), mimetype="text/event-stream")

# if __name__ == "__main__":
#     current_status = OurStatus("uninited")
#     app.run(host="192.168.60.118", debug=True, port=80)
#

@run_with_reloader
def run_server():
    WSGIServer(('192.168.60.118', 80), DebuggedApplication(app)).serve_forever()

if __name__ == "__main__":
    run_server()
