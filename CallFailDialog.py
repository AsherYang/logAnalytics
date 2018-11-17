#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/11/17
Desc  : 掉话自动分析对话框
"""

from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QSizePolicy
import QSettingsUtil
from QtFontUtil import QtFontUtil
import os
import sys


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

class CallFailDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle(u'掉话分析')
        self.resize(500, 400)
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.mainLayout.setContentsMargins(5, 2, 5, 2)
        # select directory
        self.selectDirectoryLayout = QtGui.QHBoxLayout()
        self.selectDirectoryLineEdit = QtGui.QLineEdit()
        self.selectDirectoryLineEdit.setTextMargins(10, 0, 10, 0)
        self.selectDirectoryLineEdit.setMinimumHeight(25)
        self.selectDirectoryLineEdit.setFont(QtFontUtil().getFont('Monospace', 12))
        self.selectDirectoryBtn = QtGui.QPushButton(u'选择文件夹')
        self.selectDirectoryBtn.connect(self.selectDirectoryBtn, QtCore.SIGNAL('clicked()'), self.selectDirectoryMethod)
        self.selectDirectoryLayout.addWidget(self.selectDirectoryBtn)
        self.selectDirectoryLayout.addWidget(self.selectDirectoryLineEdit)
        # analytics key word
        self.keywordLayout = QtGui.QHBoxLayout()
        self.keywordLineEdit = QtGui.QLineEdit()
        self.keywordLineEdit.setTextMargins(10, 0, 10, 0)
        self.keywordLineEdit.setMinimumHeight(25)
        self.keywordLineEdit.setFont(QtFontUtil().getFont('Monospace', 12))
        self.keywordBtn = QtGui.QPushButton(u'输入关键字')
        self.keywordBtn.setDisabled(True)
        self.keywordLayout.addWidget(self.keywordBtn)
        self.keywordLayout.addWidget(self.keywordLineEdit)
        # operate buttons
        self.btnsLayout = QtGui.QHBoxLayout()
        self.unzipBtn = QtGui.QPushButton(u'解压日志')
        self.analyticsBtn = QtGui.QPushButton(u'开始分析')
        self.generateDocumentBtn = QtGui.QPushButton(u'生成文档')
        self.unzipBtn.setMinimumHeight(25)
        self.analyticsBtn.setMinimumHeight(25)
        self.generateDocumentBtn.setMinimumHeight(25)
        self.unzipBtn.connect(self.unzipBtn,  QtCore.SIGNAL('clicked()'), self.unZipMethod)
        self.analyticsBtn.connect(self.analyticsBtn,  QtCore.SIGNAL('clicked()'), self.analyticsMethod)
        self.generateDocumentBtn.connect(self.generateDocumentBtn,  QtCore.SIGNAL('clicked()'), self.genDocMethod)
        self.btnsLayout.addWidget(self.unzipBtn)
        self.btnsLayout.addWidget(self.analyticsBtn)
        self.btnsLayout.addWidget(self.generateDocumentBtn)
        # show log
        self.LogTextEdit = QtGui.QTextEdit()
        self.LogTextEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.LogTextEdit.setFont(QtFontUtil().getFont('Monospace', 12))
        # addLayout
        self.mainLayout.addLayout(self.selectDirectoryLayout)
        self.mainLayout.addLayout(self.keywordLayout)
        self.mainLayout.addLayout(self.btnsLayout)
        self.mainLayout.addWidget(self.LogTextEdit)
        self.setLayout(self.mainLayout)

    # 选择文件夹
    def selectDirectoryMethod(self):
        lastDir = self.getLastOpenDir()
        dirPath = unicode(QtGui.QFileDialog.getExistingDirectory(None, u'选择文件夹', lastDir))
        if not dirPath or not os.path.exists(dirPath):
            self.LogTextEdit.append(u'您尚未选择日志文件路径! 请先选择日志路径。')
            return
        logStr = u'日志路径为: ' + str(dirPath)
        self.LogTextEdit.append(logStr)
        self.selectDirectoryLineEdit.setText(dirPath)

    # 获取QFileDialog 上次打开的路径
    def getLastOpenDir(self):
        lastDir = self.selectDirectoryLineEdit.text()
        if lastDir:
            return str(lastDir)
        # open last remember directory
        lastDir = QSettingsUtil.getLastDir()
        if not QtCore.QDir(lastDir).exists():
            lastDir = 'd://'
        return str(lastDir)

    def unZipMethod(self):
        if not self.selectDirectoryLineEdit.text():
            self.LogTextEdit.append(u'您尚未选择日志文件路径! 请先选择日志路径。')
            return
        pass

    def analyticsMethod(self):
        if not self.selectDirectoryLineEdit.text():
            self.LogTextEdit.append(u'您尚未选择日志文件路径! 请先选择日志路径。')
            return
        pass

    def genDocMethod(self):
        if not self.selectDirectoryLineEdit.text():
            self.LogTextEdit.append(u'您尚未选择日志文件路径! 请先选择日志路径。')
            return
        pass

    def show(self):
        self.exec_()
