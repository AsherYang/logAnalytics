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

"""
文件路径是否包含某一str字符串
该方法的好处是：
1.可以灵活统一去除包含某一关键字的文件路径
2.可以统一去除某一文件夹下的文件
**当然，输入的pathKey 关键字需要特殊一点，防止误判断**
"""
def hasContainsPath(filePath, *pathKey):
    if not filePath or not pathKey:
        return False
    for path in pathKey:
        if filePath.find(path) != -1:
            return True
    return False
