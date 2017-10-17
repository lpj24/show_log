# -*- coding: utf-8 -*-
from flask import Flask, request, copy_current_request_context
from flask import render_template, redirect, url_for
from libs import coroutine
import threading
import Queue
from flask_socketio import SocketIO, emit, disconnect
import subprocess
app = Flask(__name__)
app.debug = True

socket_io = SocketIO(app)
SHELL_PROCESS = None
STREAM = None


@app.route('/')
def hello_world():
    return render_template('index.html')


@socket_io.on('connect', namespace='/log')
def show_log():
    print 'socket io connect'
    try:
        global SHELL_PROCESS, STREAM
        SHELL_PROCESS = subprocess.Popen("tail -f ~/Downloads/error.log", stdout=subprocess.PIPE, shell=True)
        # t = threading.Thread(target=tail_file, args=(r, ))
        STREAM = SHELL_PROCESS.stdout
        t = ThreadExecuteJob(STREAM)
        # STREAM.readlines()
        t.setDaemon(True)
        t.start()
    except Exception as e:
        print 'error: ' + str(e.message)


@socket_io.on('disconnect')
def socket_close():
    print 'web close'
    if STREAM is not None:
        STREAM.close()

    if SHELL_PROCESS is not None:
        SHELL_PROCESS.terminate()
    # disconnect()


# def tail_file(stream):
#     line = stream.readline()
#     while line:
#         socket_io.emit('show_file_line', line + '<br/>', namespace='/log')
#         line = stream.readline()


class ThreadExecuteJob(threading.Thread):
    """Threaded Url Grab"""

    def __init__(self, stream):
        threading.Thread.__init__(self)
        self.stream = stream

    def run(self):
        line = self.stream.readline()
        while 1:
            line = self.stream.readline()
            if line:
                socket_io.emit('show_file_line', line + '<br/>', namespace='/log')


if __name__ == '__main__':
    socket_io.run(app, host='127.0.0.1', port=5000)
    # f = open('C:\\Users\\Administrator\\Desktop\\error.log')
    # gen_calling_obj = printer()
    # monitor_file(f, gen_calling_obj)
