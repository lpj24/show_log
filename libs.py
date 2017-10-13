# -*- coding: utf-8 -*-
import functools


class coroutine(object):
    def __init__(self, fun):
        self.fun = fun
        functools.update_wrapper(self, fun)

    def __call__(self, *args, **kwargs):
        gen = self.fun(*args, **kwargs)
        next(gen)
        return gen



