from flask import Flask, request, render_template, Response, json
app = Flask(__name__)
import gevent
from gevent.pywsgi import WSGIServer
from gevent import monkey
from numpy import random
monkey.patch_all()

@app.route('/')
def index():
    return render_template('index.html')

def event():
    """For something more intelligent, take a look at Redis pub/sub
    stuff. A great example can be found here__.
    __ https://github.com/jakubroztocil/chat
    """
    while True:
        yield 'data: ' + json.dumps(random.rand(2).tolist()) + '\n\n'
        gevent.sleep(0.2)

@app.route('/status', methods=['POST'])
def handlestatus():
    status = request.form.get('status', None)
    if not status:
        return ('Missing status value', 400)
    print "Got some status: " + status
    return ('', 200)

@app.route('/status', methods=['GET'])
def getstatus():
    return "Status is alive!"

@app.route('/stream/', methods=['GET', 'POST'])
def stream():
    print 'Something is connected!'
    return Response(event(), mimetype="text/event-stream")

# if __name__ == "__main__":
#     app.run(host="192.168.20.61", debug=True, port=80)
#     raw_input()
#
if __name__ == "__main__":
    WSGIServer(('192.168.60.118', 80), app).serve_forever()
