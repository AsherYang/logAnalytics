#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/11/19
Desc  : encode util
"""

from PyQt4 import QtCore, QtGui
import sys
import chardet

reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')
# print sys.getdefaultencoding()

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


def _translateUtf8(text):
    text_detect = chardet.detect(str(text))['encoding']
    # print type(text_detect)
    # print text_detect
    if text_detect == 'utf-8':
        return text
    elif text_detect == 'ascii':
        return _translate('', text, None)
    elif text_detect == 'GB2312' or text_detect == 'gbk':
        utf8Text = text.decode('gbk').encode('utf8')
        return _translate('', utf8Text, None)
    else:
        return _translate('', text, None)

