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


# 从文件路径中提取文件名(包括后缀拓展名)
def getFileName(filePath):
    fileName = 'UnKnownFile'
    if not filePath:
        return fileName
    return os.path.basename(filePath)


# 返回文件拓展名(不包含点".")
def getFileExt(filePath):
    fileExt = 'UnknownFileExt'
    if not filePath:
        return fileExt
    return os.path.splitext(filePath)[1][1:].lower()


# 返回文件名(包括文件目录, 但不包含扩展名)
def getFilePathWithName(filePath):
    if not filePath:
        return './'
    return os.path.splitext(filePath)[0]


# 返回文件父目录
def getFileDir(filePath):
    if not filePath:
        return './'
    return os.path.dirname(filePath)


# 获取指定目录及其子目录下，指定文件名的文件
def getAllFilesByExt(dir, fileExt):
    fileList = []
    if not fileExt:
        return fileList
    for root, dirs, files in os.walk(dir):
        for file in files:
            if fileExt == getFileExt(file):
                fileList.append(os.path.join(root, file))
    return fileList


# 当文件目录不存在时，创建一个文件目录(创建多层目录)
def mkdirNotExist(directory):
    # 防止创建文件目录时乱码
    directory = directory.decode('utf-8')
    if not os.path.exists(directory):
        os.makedirs(directory)
