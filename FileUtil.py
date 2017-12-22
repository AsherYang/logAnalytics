#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2017/12/22
Desc  : 文件操作类
http://blog.csdn.net/ziyuzhao123/article/details/8811496
"""

import os


# 从文件路径中提取文件名
def getFileName(filePath):
    fileName = 'UnKnownFile'
    if not filePath:
        return fileName
    return os.path.basename(filePath)


# 返回文件拓展名
def getFileExt(filePath):
    fileExt = 'UnknownFileExt'
    if not filePath:
        return fileExt
    return os.path.splitext(filePath)[1][1:].lower()
