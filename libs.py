# -*- coding: utf-8 -*-
import functools
import socket


class coroutine(object):
    def __init__(self, fun):
        self.fun = fun
        functools.update_wrapper(self, fun)

    def __call__(self, *args, **kwargs):
        gen = self.fun(*args, **kwargs)
        next(gen)
        return gen


def get_ip():
    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(('8.8.8.8', 80))
        (addr, port) = csock.getsockname()
        csock.close()
        return addr
    except socket.error:
        return "127.0.0.1"




