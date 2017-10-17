# -*- coding: utf-8 -*-
from flask import Flask
from flask import render_template, redirect, url_for
from libs import coroutine
from celery import Celery
import threading
import Queue
from flask_socketio import SocketIO, emit, send
import subprocess
app = Flask(__name__)
app.debug = True

socket_io = SocketIO(app)


@app.route('/')
def hello_world():
    return render_template('index.html')


@socket_io.on('show_log', namespace='/log')
def show_log(msg):
    print msg
    r = subprocess.Popen("tail -f /home/huolibi/local/hbgj_statistics/log/error.log", stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, shell=True)
    t = threading.Thread(target=tail_file, args=r)
    t.start()


def tail_file(r):
    line = r.readline()
    while line:
        emit('show_file_line', line, namespace='/log')





if __name__ == '__main__':
    socket_io.run(app, host='127.0.0.1', port=5000)
    # f = open('C:\\Users\\Administrator\\Desktop\\error.log')
    # gen_calling_obj = printer()
    # monitor_file(f, gen_calling_obj)