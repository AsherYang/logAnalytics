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
import re
import json
from MultiProcessFile import MultiProcessFile
from EncodeUtil import _translateUtf8
from analyticslog.BaseAttrBean import BaseAttrBean


def process_wrapper(fname, chunkStart, chunkSize, keyword="base attribute info"):
    # print '----- process_wrapper PID:%s , chunkSize:%d ' % (os.getpid(), chunkSize)
    with open(fname) as f:
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        baseAttrBeanList = []
        for line in lines:
            # print '---> line: %s, keyword: %s ' % (line, keyword)
            textLine = str(_translateUtf8(line))
            # print '--> textLine: ', textLine
            textLineLower = textLine.lower()
            keywordIndex = textLineLower.find(str(_translateUtf8(keyword)).lower())
            if keywordIndex != -1:
                baseAttrJson = filterBaseAttr2Json(textLine)
                # print '==> baseAttrJsonDict: ', baseAttrJson
                if baseAttrJson:
                    baseAttr = BaseAttrBean()
                    baseAttr.binderNumber = baseAttrJson['mId']
                    baseAttr.machineMode = baseAttrJson['devName']
                    baseAttr.osVersion = baseAttrJson['osVer']
                    # print 'baseAttr: ', baseAttr
                    baseAttrBeanList.append(baseAttr)
        return baseAttrBeanList


# 找出有效的基础信息，进行json 转换
def filterBaseAttr2Json(searchedBaseAttr):
    if not searchedBaseAttr:
        return None
    baseAttrJson = None
    baseAttrList = re.findall(r'BaseAttr(\{.+})', searchedBaseAttr)
    # print '---> baseAttrList: ', baseAttrList
    if baseAttrList:
        for baseAttrStr in baseAttrList:
            baseAttrJson = convertStr2JsonStr(baseAttrStr)
            # print '==> baseAttrJson: ', baseAttrJson
            if baseAttrJson:
                return baseAttrJson
    return baseAttrJson


# 将字符串转换为json 格式
# http://www.runoob.com/python/python-reg-expressions.html
def convertStr2JsonStr(string):
    if not string:
        return None
    string = string.replace("\'", "\"")
    strList = re.findall(r'([A-Za-z0-9]+=)', string)
    for strTmp in strList:
        strTmp = strTmp.replace("=", "")
        string = string.replace(strTmp, "\"" + strTmp + "\"")
    string = string.replace("=", ":")
    # print '---> string: ', string
    # print '---> strList: ', strList
    jsonStr = None
    try:
        jsonStr = json.loads(string)
    except Exception as e:
        pass
    # print "json >>> ", jsonStr
    return jsonStr


class SearchBaseAttrByMultiProcess(MultiProcessFile):
    def __init__(self, fname, cls_instance, status_call_back, keyword="base attribute info"):
        MultiProcessFile.__init__(self, fname, cls_instance, status_call_back, process_wrapper, keyword)
