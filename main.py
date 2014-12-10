from netem import Netem
nm = Netem()

# We'll render HTML templates and access data sent by GET
# using the request object from flask. jsonigy is required
# to send JSON as a response of a request
from flask import Flask, render_template, request, jsonify
# Initialize the Flask application
app = Flask(__name__)


@app.route('/')
def netem():
    return render_template('netem.html')


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
    app.run(
        host="0.0.0.0",
        port=int("8080"),
        debug=True
    )

