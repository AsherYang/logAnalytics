#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/11/22
Desc  : 日志分析实体 bean

self._keyword          # 搜索log的关键字
self._logTxt           # 搜索到的log信息
self._logTime          # 搜索到log 行数时间
self._filePath         # 搜索到log的文件路径
"""


class AnalyticsLogBean:
    def __init__(self):
        self._keyword = None
        self._logTxt = None
        self._logTime = None
        self._filePath = None

    @property
    def keyword(self):
        return self._keyword

    @keyword.setter
    def keyword(self, value):
        self._keyword = value

    @property
    def logTxt(self):
        return self._logTxt

    @logTxt.setter
    def logTxt(self, value):
        self._logTxt = value

    @property
    def logTime(self):
        return self._logTime

    @logTime.setter
    def logTime(self, value):
        self._logTime = value

    @property
    def filePath(self):
        return self._filePath

    @filePath.setter
    def filePath(self, value):
        self._filePath = value

    # toString
    def __str__(self):
        return '_logTxt: %s' % self.logTxt
