# -*- coding: utf-8 -*-
from flask import Flask, request, copy_current_request_context
from flask import render_template, redirect, url_for
from libs import coroutine
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
    r = subprocess.Popen("tail -f ~/Downloads/error.log", stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE, shell=True)
    # t = threading.Thread(target=tail_file, args=(r, ))
    t = ThreadExecuteJob(r)
    t.start()


def tail_file(r):
    while r.stdout.readline():
        socket_io.emit('show_file_line', r.stdout.readline() + '<br/>', namespace='/log')


class ThreadExecuteJob(threading.Thread):
    """Threaded Url Grab"""

    def __init__(self, r):
        threading.Thread.__init__(self)
        self.r = r

    def run(self):
        while self.r.stdout.readline():
            socket_io.emit('show_file_line', self.r.stdout.readline(), namespace='/log')




if __name__ == '__main__':
    socket_io.run(app, host='127.0.0.1', port=5000)
    # f = open('C:\\Users\\Administrator\\Desktop\\error.log')
    # gen_calling_obj = printer()
    # monitor_file(f, gen_calling_obj)
hahahhahahah
hahahhahahalpwjkewjh
hahahhahahalpwjkewjhhhhhhhhhhhhhh
