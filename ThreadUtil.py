#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/9/13
Desc  : 线程工具类， 将线程的异常信息上报传递给主线程。
        主线程可检测线程异常

https://blog.csdn.net/linchere/article/details/49587479
"""

import threading, traceback, sys


class ThreadUtil(threading.Thread):
    def __init__(self, funcName, **args):
        threading.Thread.__init__(self)
        self.exitCode = 0
        self.exception = None
        self.exc_traceback = ''
        self.funcName = funcName
        self.args = args

    def run(self):
        try:
            self._run()
        except Exception as e:
            self.exitCode = 1
            self.exception = e
            self.exc_traceback = ''.join(traceback.format_exception(*sys.exc_info()))

    def _run(self):
        try:
            self.funcName(**(self.args))
        except Exception as e:
            raise e