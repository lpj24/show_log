# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template
from flask_sse import sse
from libs import coroutine
import threading
import time
app = Flask(__name__)
app.debug = False
app.config['REDIS_URL'] = "redis://localhost"
app.register_blueprint(sse, url_prefix='/stream')


@app.route('/')
def hello_world():
    f = open('C:\\Users\\Administrator\\Desktop\\error.log')
    gen_calling_obj = printer()
    monitor_file(f, gen_calling_obj)
    # t = threading.Thread(target=log_file)
    # t.start()
    # t.join()

    return render_template('index.html')


@coroutine
def printer():
    while 1:
        line = yield
        print line
        sse.publish({'message': line}, type='greeting')


def monitor_file(logfile, target):
    logfile.seek(0, 2)
    while 1:
        line = logfile.readline()
        if not line:
            time.sleep(1)
            continue
        target.send(line)


def log_file():
    f = open('C:\\Users\\Administrator\\Desktop\\error.log')
    gen_calling_obj = printer()
    monitor_file(f, gen_calling_obj)


@app.route('/send')
def send_file_line():
    print 'send'
    # f = open('error.log')
    # gen_calling_obj = printer()
    # monitor_file(f, gen_calling_obj)
    # sse.publish({'message': 'lpj24'}, type='greeting')
    return 'file msg send'

if __name__ == '__main__':
    app.run(port=8100, debug=app.debug, threaded=True)