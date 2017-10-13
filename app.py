# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask_sse import sse
from libs import coroutine
import time
app = Flask(__name__)
app.debug = True
app.config['REDIS_URL'] = 'redis://127.0.0.1'
app.register_blueprint(sse, url_prefix='/stream')


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/send')
def send_file_line():
    sse.publish({'file_line': 'dsadasdsad'}, type='greeting')
    return 'file msg send'


def monitor_file(logfile, target):
    logfile.seek(0, 2)
    while 1:
        line = logfile.readline()
        if not line:
            time.sleep(1)
            continue
        target.send(line)

if __name__ == '__main__':
    app.run()