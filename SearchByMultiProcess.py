#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/12/8
Desc  : 利用多进程在文件中搜索关键字

本类是传递 line 数据出去，但是发现会出现 QWinEventNotifier cannot have more than 62 enabled at one time 的问题
故，先拆分为 SearchKeywordByMultiProcess.py 和 SearchBaseAttrByMultiProcess.py 分别处理完line 再进行回调结果
"""
import os
from MultiProcessFile import MultiProcessFile
from EncodeUtil import _translateUtf8


def process_wrapper(fname, chunkStart, chunkSize, keyword):
    # print '----- process_wrapper PID:%s , chunkSize:%d ' % (os.getpid(), chunkSize)
    with open(fname) as f:
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        filterLines = ""
        for line in lines:
            # print '---> line: %s, keyword: %s ' % (line, keyword)
            textLine = str(_translateUtf8(line))
            # print '--> textLine: ', textLine
            textLineLower = textLine.lower()
            keywordIndex = textLineLower.find(str(_translateUtf8(keyword)).lower())
            if keywordIndex != -1:
                filterLines += textLine + "\n"
        if filterLines:
            return filterLines


class SearchByMultiProcess(MultiProcessFile):

    def __init__(self, fname, keyword, cls_instance, status_call_back):
        MultiProcessFile.__init__(self, fname, cls_instance, status_call_back, process_wrapper, keyword)

