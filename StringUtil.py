#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2017/12/5
Desc  : String util
"""

def findLast(string, str):
    lastPos = -1
    while True:
        position = string.find(str, lastPos + 1)
        if position == -1:
            return lastPos
        lastPos = position