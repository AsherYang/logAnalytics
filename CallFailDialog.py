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
from PyQt4.QtCore import QFile
import QSettingsUtil
from QtFontUtil import QtFontUtil
import os
import sys
import zipfile
import FileUtil
import SupportFiles
from EncodeUtil import _translate, _fromUtf8, _translateUtf8
import StringIO
from ThreadUtil import ThreadUtil


reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')
# print sys.getdefaultencoding()


class CallFailDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle(u'掉话分析')
        self.resize(600, 400)
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
        self.keywordLineEdit.setPlaceholderText(u'reportCallFailLD =')
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
        self.LogTextEdit.connect(self.LogTextEdit, QtCore.SIGNAL('appendLogSignal(QString)'), self.appendLog)
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
            self.appendLog(u'您尚未选择日志文件路径! 请先选择日志路径。')
            return
        logStr = u'日志路径为: ' + str(dirPath)
        self.appendLog(logStr)
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

    # 点击解压日志按钮
    def unZipMethod(self):
        selectDir = str(self.selectDirectoryLineEdit.text())
        if not selectDir:
            self.appendLog(u'您尚未选择日志文件路径! 请先选择日志路径。')
            return
        # self.appendLog(u'正在解压文件..')
        # selectDir = "D:\\111111"
        allZipFileList = FileUtil.getAllFilesByExt(selectDir, 'zip')
        if not allZipFileList:
            logStr = u'在目录 ' + _translateUtf8(selectDir) + u' 及子目录下未找到 zip 文件'
            self.appendLog(logStr)
            return
        for fileList in allZipFileList:
            # print '>>> fileList: ' + str(_translateUtf8(fileList))
            self.doUnzipFile(fileList)
        self.appendLog(u'解压完成')
        pass

    # 解压文件
    def doUnzipFile(self, file_path):
        log_txt = u'正在解压文件: ' + _translateUtf8(file_path)
        self.appendLog(log_txt)
        # print str(_translateUtf8(file_path))
        dest_dir = _translateUtf8(FileUtil.getFilePathWithName(file_path))
        zip_ref = zipfile.ZipFile(str(file_path), 'r')
        # FileUtil.mkdirNotExist(str(dest_dir)) # zipfile 会自动创建
        zip_ref.extractall(str(dest_dir))
        zip_ref.close()

    # 点击分析日志按钮
    def analyticsMethod(self):
        self.analyticsBtn.setDisabled(True)
        # self.doAnalytics()
        threadUtil = ThreadUtil(funcName=self.doAnalytics, log_call_back=self.emitAppendLogSignal)
        threadUtil.setDaemon(True)
        threadUtil.start()

    # 开始分析
    def doAnalytics(self, log_call_back):
        selectDir = str(self.selectDirectoryLineEdit.text())
        if not selectDir:
            logMsg = u'您尚未选择日志文件路径! 请先选择日志路径。'
            log_call_back(logMsg)
            self.analyticsBtn.setEnabled(True)
            return
        analyKey = str(self.keywordLineEdit.text()) if str(
            self.keywordLineEdit.text()).strip() else u'reportCallFailLD ='
        filePaths = FileUtil.getAllFiles(selectDir)
        for filePath in filePaths:
            if SupportFiles.hasSupportFile(filePath):
                # print _translateUtf8(filePath)
                self.searchWordInFile(analyKey, filePath, log_call_back)
            # else:
            #     logMsg = u'暂不支持文件：' + _translateUtf8(filePath)
            #     print logMsg
        self.analyticsBtn.setEnabled(True)
        logMsg = u'---------- 日志分析完毕 -----------'
        log_call_back(logMsg)

    # 在文件中，搜索关键字，并返回该关键字所在的行数据
    def searchWordInFile(self, keyword, file_path, log_call_back):
        if not file_path or not keyword.strip():
            return
        filePath = _translate('', file_path, None)
        file = QFile(filePath)
        if not file.open(QtCore.QIODevice.ReadOnly):
            logMsg = u'无法打开文件：' + _translateUtf8(file_path)
            log_call_back(logMsg)
            file.close()
            return
        stream = QtCore.QTextStream(file)
        stream.setCodec('UTF-8')
        data = stream.readAll()
        file.close()
        dataTmp = StringIO.StringIO(data)
        searchedText = ''
        logMsg = u'正在分析文件：' + _translateUtf8(file_path)
        log_call_back(logMsg)
        while True:
            textLine = str(_translateUtf8(dataTmp.readline()))
            if textLine == '':
                # logMsg = u'已分析完文件：' + _translateUtf8(file_path)
                # log_call_back(logMsg)
                break
            textLineLower = textLine.lower()
            keywordIndex = textLineLower.find(keyword.lower())
            if keywordIndex != -1:
                searchedText += textLine
        return searchedText

    # 点击生成文档按钮
    def genDocMethod(self):
        selectDir = self.selectDirectoryLineEdit.text()
        if not selectDir:
            logMsg = u'您尚未选择日志文件路径! 请先选择日志路径。'
            self.appendLog(logMsg)
            return
        pass

    def appendLog(self, logTxt):
        self.LogTextEdit.append(_translateUtf8(logTxt))

    # 解决在子线程中刷新UI 的问题。' QWidget::repaint: Recursive repaint detected '
    def appendLogSignal(self, logTxt):
        pass

    def emitAppendLogSignal(self, logTxt):
        self.LogTextEdit.emit(QtCore.SIGNAL('appendLogSignal(QString)'), logTxt)
        pass

    def show(self):
        self.exec_()
