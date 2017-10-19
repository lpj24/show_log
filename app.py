#!./env/bin/python
# -*- coding: utf-8 -*-
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import threading
from libs import get_ip
import subprocess
import os


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        ip = get_ip()
        self.render('index.html', domain=ip, port=port)


class LogHandler(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        return True

    def open(self):
        print "client is connection"
        try:
            shell_process = subprocess.Popen("tail -f " + log_path, stdout=subprocess.PIPE,shell=True)
            stream = shell_process.stdout
        except OSError as e:
            print e.args[1]

        t = ThreadExecuteJob(self, stream)
        t.setDaemon(True)
        t.start()

    def on_message(self, message):
        self.write_message(u"Your message was: "+message)

    def on_close(self):
        print "client lost connection"


class ThreadExecuteJob(threading.Thread):
    def __init__(self, ws_client, stream):
        threading.Thread.__init__(self)
        self.stream = stream
        self.ws_client = ws_client

    def run(self):
        while 1:
            try:
                line = self.stream.readline()
                if line:
                    self.ws_client.write_message(line + '<br/>')
            except Exception:
                break


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexHandler),
            (r'/log', LogHandler)
        ]

        settings = {
            "template_path": "templates",
            "debug": False,
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(usage='./env/bin/python app.py -path /home/lpj/error.log', description='start server and give log path')
    parser.add_argument('-path', required=True, type=str, help=u'日志文件的具体路径')
    parser.add_argument('-port', required=False, type=int, help=u'啓動端口')
    args = parser.parse_args()
    log_path = args.path
    port = args.port

    if not port:
        port = 5500
    if not os.path.exists(log_path):
        print log_path + " no such file"
        exit(0)

    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(port)
    print "server is listening " + str(port)
    print "http://" + get_ip() + ":" + str(port)
    tornado.ioloop.IOLoop.instance().start()


