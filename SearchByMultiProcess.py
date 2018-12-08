#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/12/8
Desc  : 利用多进程在文件中搜索关键字
"""
import os
from MultiProcessFile import MultiProcessFile


def process_wrapper(fname, chunkStart, chunkSize, keyword):
    print '----- process_wrapper PID: ', os.getpid()
    keyword = keyword(0)
    with open(fname) as f:
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        filterLines = []
        for line in lines:
            textLine = line.decode('utf-8')
            textLineLower = textLine.lower()
            keywordIndex = textLineLower.find(keyword.lower())
            if keywordIndex != -1:
                filterLines += textLine
        if filterLines:
            return filterLines


class SearchByMultiProcess(MultiProcessFile):

    def __init__(self, fname, keyword, status_call_back):
        MultiProcessFile.__init__(self, fname, status_call_back, process_wrapper, keyword)

