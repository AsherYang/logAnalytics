#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/12/8
Desc  : 利用多进程在文件中搜索关键字

1. 将数据处理完成之后，再进行回调，
   而不是回调大量 line 数据，让上层继续处理，
2.这样做的好处是，封装处理完毕再反馈结果给上层；同时避免了
QWinEventNotifier cannot have more than 62 enabled at one time 的问题
"""
import os
import re
from MultiProcessFile import MultiProcessFile
from EncodeUtil import _translateUtf8
from analyticslog.AnalyticsLogBean import AnalyticsLogBean


def process_wrapper(fname, chunkStart, chunkSize, keyword="reportCallFailLD ="):
    # print '----- process_wrapper PID:%s , chunkSize:%d ' % (os.getpid(), chunkSize)
    with open(fname) as f:
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        analyLogBeanList = []
        for line in lines:
            # print '---> line: %s, keyword: %s ' % (line, keyword)
            textLine = str(_translateUtf8(line))
            # print '--> textLine: ', textLine
            textLineLower = textLine.lower()
            keywordIndex = textLineLower.find(str(_translateUtf8(keyword)).lower())
            if keywordIndex != -1:
                # 匹配以时间开头，除换行符"\n"之外的任意字符
                reLogStr = r'(\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}.\d{3}.*)'
                # 匹配时间
                reTimeStr = r'(\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}.\d{3})'
                # 一个文件中可能有多个异常Log打印信息
                searchedLogList = re.findall(reLogStr, textLine)
                if not searchedLogList:
                    continue
                # print 'searchedLogList: %s --> filePath: %s ' % (searchedLogList, file_path)
                for searchedLog in searchedLogList:
                    if not searchedLog:
                        continue
                    # print 'searchedLog: %s --> filePath: %s ' % (searchedLog, file_path)
                    logTime = re.search(reTimeStr, str(searchedLog)).group(1)
                    analyLogBean = AnalyticsLogBean()
                    analyLogBean.keyword = keyword
                    analyLogBean.logTxt = searchedLog
                    analyLogBean.filePath = fname
                    analyLogBean.logTime = logTime
                    analyLogBeanList.append(analyLogBean)
        return analyLogBeanList


class SearchKeywordByMultiProcess(MultiProcessFile):

    def __init__(self, fname, cls_instance, status_call_back, keyword="reportCallFailLD ="):
        MultiProcessFile.__init__(self, fname, cls_instance, status_call_back, process_wrapper, keyword)

