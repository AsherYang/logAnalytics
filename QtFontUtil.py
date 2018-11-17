#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/7/11
Desc  : 字体设置工具类
"""
from PyQt4.QtGui import QFont
from PyQt4 import QtCore

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s


class QtFontUtil:
    def __init__(self):
        pass

    """
    font_family: 字体样式
    font_size: 字体大小(以像素为单位)
    bold: 是否加粗
    italic: 是否斜体
    Underline: 是否有下划线
    """
    def getFont(self, font_family, font_size=10, bold=False, italic=False, Underline=False):
        font = QFont()
        font.setFamily(_fromUtf8(font_family))
        font.setPixelSize(font_size)
        font.setFixedPitch(True)
        font.setBold(bold)
        font.setItalic(italic)
        font.setUnderline(Underline)
        return font