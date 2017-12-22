#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2017/12/21
Desc  : 支持的文件类型
"""

import FileUtil


def files():
    return 'md', 'log', 'txt'


def hasSupportFileExt(fileExt):
    if not files():
        return False
    if not fileExt:
        return False
    fileExt = str(fileExt).lower()
    # print fileExt
    if fileExt in files():
        return True
    else:
        return False


def hasSupportFile(filePath):
    fileExt = FileUtil.getFileExt(filePath)
    return hasSupportFileExt(fileExt)
