from gevent import monkey
monkey.patch_all()

import time
from threading import Thread

from flask import Flask, render_template, session, request, jsonify
from flask.ext.socketio import SocketIO, emit

from netem import Netem
from netstats import Netstats

nm = Netem()
ns = Netstats(nm.list_ifaces())

# Initialize the Flask application
app = Flask(__name__)
app.debug = True
socketio = SocketIO(app)
stats_thread = None

def stats_thread_run():
   count = 0
   while True:
      time.sleep(0.1)
      count += 1
      stats = ns.get_stats()
      socketio.emit('stats',
                    {'data': stats, 'count': count},
                    namespace='/statsNS')


@socketio.on('connect', namespace='/statsNS')
def stats_connect():
   print('Client Connected')
   global stats_thread
   if stats_thread is None:
      stats_thread = Thread(target=stats_thread_run)
      stats_thread.start()
   emit('response', {'data': 'Connected', 'count': 0})


@app.route('/')
def netem():
    return render_template('netem.html')


@app.route('/_list_ifaces')
def get_ifaces():
    iflist = nm.list_ifaces()
    print iflist
    return jsonify(ifaces=iflist)

@app.route('/_get_netem')
def get_netem():
    dev = request.args.get('dev', 0, type=str)
    conf = nm.get_netem(dev)
    return jsonify(netem_config=conf['conf'], delay=conf['delay'],
                   d_var=conf['d_var'], loss=conf['loss'])


@app.route('/_set_delay')
def set_delay():
    dev = request.args.get('dev', 0, type=str)
    delay = request.args.get('delay', 0, type=str)
    d_var = request.args.get('d_var', 0, type=str)
    loss = request.args.get('loss', 0, type=str)
    conf = nm.set_delay(dev, delay, d_var, loss)

    return jsonify(netem_config=conf['conf'], delay=conf['delay'],
                   d_var=conf['d_var'], loss=conf['loss'])


if __name__ == '__main__':
    socketio.run(
        app,
        host="0.0.0.0",
        port=int("8080"),
    )

