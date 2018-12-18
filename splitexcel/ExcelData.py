#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/12/18
Desc  : excel 数据类
"""


class ExcelData:
    def __init__(self):
        self._lineNo = None
        self._columnNo = None
        self._value = None

    @property
    def lineNo(self):
        return self._lineNo

    @lineNo.setter
    def lineNo(self, line_no):
        self._lineNo = line_no

    @property
    def columnNo(self):
        return self._columnNo

    @columnNo.setter
    def columnNo(self, column_no):
        self._columnNo = column_no

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    # toString
    def __str__(self):
        return '_lineNo: %s, _colNo: %s, value: %s' % (self.lineNo, self.columnNo, self.value)

