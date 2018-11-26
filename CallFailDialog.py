#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/11/17
Desc  : 掉话自动分析对话框
"""

import StringIO
import os
import sys
import zipfile
import re
import json

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QFile
from PyQt4.QtGui import QSizePolicy

import FileUtil
import QSettingsUtil
import SupportFiles
from EncodeUtil import _translate, _translateUtf8
from QtFontUtil import QtFontUtil
from TrayIcon import TrayIcon
from ThreadUtil import ThreadUtil
from analyticslog.CallFailBean import CallFailBean
from analyticslog.AnalyticsLogBean import AnalyticsLogBean
from analyticslog.BaseAttrBean import BaseAttrBean
from IconResourceUtil import resource_path

reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')
# print sys.getdefaultencoding()


class CallFailDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle(u'掉话分析')
        self.setWindowIcon(QtGui.QIcon(resource_path('img/log.png')))
        self.resize(1000, 500)
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
        # 保存最后分析结果 CallFailBean 的集合
        self.callFailList = []
        # 显示托盘
        self.tray = TrayIcon(parent=self, clickEnable=False)
        self.tray.connect(self.tray, QtCore.SIGNAL('showTrayMsgSignal(QString)'), self.showTrayMsg)

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
        self.generateDocumentBtn.setDisabled(True)
        # self.doAnalytics(log_call_back=self.emitAppendLogSignal)
        threadUtil = ThreadUtil(funcName=self.doAnalytics, log_call_back=self.emitAppendLogSignal)
        threadUtil.setDaemon(True)
        threadUtil.start()

    """
    开始分析， 分析步骤：
    1. 先分析给定的关键字，进行搜索。
    2. 若搜索到关键字相关文本行，则进行关键log 信息保存，保存进 AnalyticsLogBeanList 集合
    3. 若第2步搜索到内容，则进行基本信息搜索, 基本信息BaseAttrBean: binderNumber, machineMode, osVersion 等
    4. 若第3步搜索到基本信息，则将 AnalyticsLogBean 内容与 baseAttr 基本信息进行整合，保存进 CallFailBeanList 中。便于后面生成文档。
    """
    def doAnalytics(self, log_call_back):
        selectDir = str(self.selectDirectoryLineEdit.text())
        if not selectDir:
            logMsg = u'您尚未选择日志文件路径! 请先选择日志路径。'
            log_call_back(logMsg)
            self.analyticsBtn.setEnabled(True)
            self.generateDocumentBtn.setEnabled(True)
            return
        analyKey = str(self.keywordLineEdit.text()) if str(
            self.keywordLineEdit.text()).strip() else u'reportCallFailLD ='
        baseAttrKeyword = u'base attribute info'
        filePaths = FileUtil.getAllFiles(selectDir)
        # 保存分析的日志信息集合
        analyticsLogList = []
        # 搜索关键字信息
        for filePath in filePaths:
            if SupportFiles.hasSupportFile(filePath):
                # print _translateUtf8(filePath)
                searchedlogInFile = self.searchWordInFile(analyKey, filePath, log_call_back)
                if not searchedlogInFile:
                    continue
                # print '----> ', searchedlogInFile
                # 匹配时间
                reTimeStr = r'(\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}.\d{3})'
                # 匹配以时间开头，除换行符"\n"之外的任意字符
                reLogStr = r'(\d{2}-\d{2}\s\d{2}:\d{2}:\d{2}.\d{3}.*)'
                # 一个文件中可能有多个异常Log打印信息
                searchedLogList = re.findall(reLogStr, searchedlogInFile)
                print '===> searchedLogList: ', searchedLogList
                for searchedLog in searchedLogList:
                    logTime = re.search(reTimeStr, str(searchedLog)).group(1)
                    analyLogBean = AnalyticsLogBean()
                    analyLogBean.keyword = analyKey
                    analyLogBean.logTxt = searchedLog
                    analyLogBean.filePath = filePath
                    analyLogBean.logTime = logTime
                    self.filterAnalyLog2List(analyticsLogList, analyLogBean)
                    # analyticsLogList.append(analyLogBean)
                    # print 'searchedlogInFile == ', searchedlogInFile
            # else:
            #     logMsg = u'暂不支持文件：' + _translateUtf8(filePath)
            #     print logMsg
        # 保存基本信息的集合
        baseAttrList = []
        # 再搜索基本信息
        # print 'len(analyticsLogList): ', len(analyticsLogList)
        if analyticsLogList:
            # 先搜索基础信息
            for filePath in filePaths:
                if SupportFiles.hasSupportFile(filePath):
                    searchedBaseAttr = self.searchWordInFile(baseAttrKeyword, filePath)
                    print searchedBaseAttr
                    if searchedBaseAttr:
                        baseAttrStr = re.search(r'BaseAttr(\{.+})', searchedBaseAttr).group(1)
                        # print '==> baseAttrJsonStr: ', baseAttrStr
                        baseAttrJson = self.convertStr2JsonStr(baseAttrStr)
                        # print '==> baseAttrJsonDict: ', baseAttrJson
                        baseAttr = BaseAttrBean()
                        baseAttr.binderNumber = baseAttrJson['mId']
                        baseAttr.machineMode = baseAttrJson['devName']
                        baseAttr.osVersion = baseAttrJson['osVer']
                        self.filterBaseAttr2List(baseAttrList, baseAttr)
                        # baseAttrList.append(baseAttr)
            # 再组合数据
            for analyLog in analyticsLogList:
                analyLogTxt = analyLog.logTxt
                analyLogFilePath = analyLog.filePath
                analyLogStr = re.search(r'ReportCallFailLD\s(\{.+})', analyLogTxt).group(1)
                analyLogJson = self.convertStr2JsonStr(analyLogStr)
                for baseAttr in baseAttrList:
                    binderNumber = baseAttr.binderNumber
                    # 组合同一个绑定号数据
                    if analyLogStr.find(binderNumber) != -1 or analyLogFilePath.find(binderNumber) != -1:
                        callFail = CallFailBean()
                        callFail.binderNumber = binderNumber
                        callFail.machineMode = baseAttr.machineMode
                        callFail.osVersion = baseAttr.osVersion
                        callFail.failTime = analyLog.logTime
                        callFail.voiceNetworkType = analyLogJson['voiceNetWorkTypeLD']
                        callFail.dialMode = analyLogJson['selfDialModeLD']
                        callFail.causeCode = analyLogJson['callFailCauseCodeLD']
                        callFail.vendorCauseCode = analyLogJson['callFailVendorCauseLD']
                        callFail.logText = analyLogTxt
                        callFail.logFilePath = analyLogFilePath
                        print '----> callFail (bindNumber: %s,  machineMode: %s, osVersion: %s, failTime: %s, ' \
                              'voiceNetworkType: %s, dailMode: %s, causeCode: %s, vendorCause: %s, logText: %s,' \
                              ' logFilePath: %s) '\
                              % (callFail.binderNumber, callFail.machineMode, callFail.osVersion, callFail.failTime,
                                 callFail.voiceNetworkType, callFail.dialMode, callFail.causeCode,
                                 callFail.vendorCauseCode, callFail.logText, callFail.logFilePath)
                        self.callFailList.append(callFail)
        self.analyticsBtn.setEnabled(True)
        self.generateDocumentBtn.setEnabled(True)
        logMsg = u'---------- 日志分析完毕 -----------'
        log_call_back(logMsg)
        self.emitTrayMsgSignal(u'日志分析完毕')
        print '------------- over ---------------'

    # 在文件中，搜索关键字，并返回该关键字所在的行数据
    def searchWordInFile(self, keyword, file_path, log_call_back=None):
        if not file_path or not keyword.strip():
            return
        filePath = _translate('', file_path, None)
        file = QFile(filePath)
        if not file.open(QtCore.QIODevice.ReadOnly):
            logMsg = u'无法打开文件：' + _translateUtf8(file_path)
            self.dologCallBack(log_call_back, logMsg)
            file.close()
            return
        stream = QtCore.QTextStream(file)
        stream.setCodec('UTF-8')
        data = stream.readAll()
        file.close()
        stream.flush()
        dataTmp = StringIO.StringIO(data)
        searchedText = ''
        logMsg = u'正在分析文件：' + _translateUtf8(file_path)
        self.dologCallBack(log_call_back, logMsg)
        while True:
            textLine = str(_translateUtf8(dataTmp.readline()))
            if textLine == '':
                # logMsg = u'已分析完文件：' + _translateUtf8(file_path)
                # log_call_back(logMsg)
                # print logMsg
                break
            textLineLower = textLine.lower()
            keywordIndex = textLineLower.find(keyword.lower())
            if keywordIndex != -1:
                searchedText += textLine
        return searchedText

    # 处理 log_call_back 函数，去除None空回调和返回信息的问题
    def dologCallBack(self, log_call_back=None, msg=None):
        if not log_call_back or not msg:
            return
        log_call_back(msg)

    # 将字符串转换为json 格式
    # http://www.runoob.com/python/python-reg-expressions.html
    def convertStr2JsonStr(self, string):
        if not string:
            return
        string = string.replace("\'", "\"")
        strList = re.findall(r'([A-Za-z0-9]+=)', string)
        for strTmp in strList:
            strTmp = strTmp.replace("=", "")
            string = string.replace(strTmp, "\"" + strTmp + "\"")
        string = string.replace("=", ":")
        # print '---> string: ', string
        # print '---> strList: ', strList
        jsonStr = json.loads(string)
        # print "json >>> ", jsonStr
        return jsonStr

    # 过滤日志信息, 去重后添加进集合
    def filterAnalyLog2List(self, analyticsLogList, analyLogBean):
        if not analyLogBean:
            return
        if len(analyticsLogList) == 0:
            analyticsLogList.append(analyLogBean)
        for analyLog in analyticsLogList:
            # logTxt 包含了整条log 信息，包括时间
            if analyLog.logTxt == analyLogBean.logTxt:
                continue
            else:
                analyticsLogList.append(analyLogBean)


    # 过滤 baseAttr 信息， 去重后添加进集合
    def filterBaseAttr2List(self, baseAttrList, baseAttr):
        if not baseAttr:
            return
        if len(baseAttrList) == 0:
            baseAttrList.append(baseAttr)
        for baseAttrTmp in baseAttrList:
            if baseAttrTmp.binderNumber == baseAttr.binderNumber:
                continue
            else:
                baseAttrList.append(baseAttr)

    # 点击生成文档按钮
    def genDocMethod(self):
        selectDir = self.selectDirectoryLineEdit.text()
        if not selectDir:
            logMsg = u'您尚未选择日志文件路径! 请先选择日志路径。'
            self.appendLog(logMsg)
            return
        if not self.callFailList:
            logMsg = u'请先分析LOG, 再生成文档!'
            self.appendLog(logMsg)
            return
        # self.doGenDocFile(self.emitAppendLogSignal)
        threadUtil = ThreadUtil(funcName=self.doGenDocFile, log_call_back=self.emitAppendLogSignal)
        threadUtil.setDaemon(True)
        threadUtil.start()

    def doGenDocFile(self, log_call_back):
        docTitle = u'# 问题分析'
        docSecondTitle = u'## 上层分析'
        docTempleteBinder = u'绑定号: '
        docTempleteMachine = u'+ 机型 ： '
        docTempleteTime = u'+ 时间点: '
        docTempleteNetworkType = u'+ 通话类型：'
        docTempleteDialMode = u'+ 通话方向：'
        docTempleteCause = u'+ 掉话code: '
        docTempleteDetail = u'+ 详情：'
        print 'callFailList len: ', len(self.callFailList)
        for callFail in self.callFailList:
            docFilePath = callFail.logFilePath
            binderNumber = callFail.binderNumber
            docFilePathTmp = re.findall(r'([A-Za-z0-9_.]+)', docFilePath)
            docFilePath.rfind(binderNumber)
            fileDirPath = ''
            for fileDirPathTmp in docFilePathTmp:
                if fileDirPathTmp == binderNumber:
                    fileDirPathIndex = docFilePath.find(binderNumber)
                    fileDirPath = docFilePath[:fileDirPathIndex + len(binderNumber) + 1]
                    break
                elif fileDirPathTmp.find(binderNumber) != -1:
                    fileDirPathIndex = docFilePath.find(binderNumber)
                    fileDirPath = docFilePath[:fileDirPathIndex]
                else:
                    fileDirPath = os.path.join(str(self.selectDirectoryLineEdit.text()), binderNumber)
            FileUtil.mkdirNotExist(fileDirPath)
            print 'docFilePath: ', fileDirPath
            filePath = os.path.join(fileDirPath, u'问题分析.txt')
            hasFileExists = os.path.exists(filePath)
            docFile = open(filePath, 'a+')
            docContentBinderNumber = str(docTempleteBinder + binderNumber).encode('utf-8')
            docContentMachine = str(docTempleteMachine + callFail.machineMode + "\t" + callFail.osVersion).encode('utf-8')
            docContentTime = str(docTempleteTime + callFail.failTime).encode('utf-8')
            docContentNetworkType = str(docTempleteNetworkType + callFail.voiceNetworkType).encode('utf-8')
            docContentDialMode = str(docTempleteDialMode + callFail.dialMode).encode('utf-8')
            docContentCause = str(docTempleteCause + callFail.vendorCauseCode).encode('utf-8')
            docContentDetail = str(docTempleteDetail + callFail.logText).encode('utf-8')
            if not hasFileExists:
                docFile.write('\n' + docTitle + '\n')
                docFile.write('\n' + docContentBinderNumber + '\n')
                docFile.write('\n' + docSecondTitle + '\n')
                docFile.write('\n' + docContentMachine + '\n')
            else:
                docFile.write('\n\n\n')
            docFile.write(docContentTime + '\n')
            docFile.write(docContentNetworkType + '\n')
            docFile.write(docContentDialMode + '\n')
            docFile.write(docContentCause + '\n')
            docFile.write(docContentDetail + '\n')
            docFile.flush()
            docFile.close()
            logMsg = u'已生成文档：' + _translateUtf8(filePath)
            log_call_back(logMsg)
            print logMsg
        logMsg = u'---------- 文档生成完毕 -----------'
        log_call_back(logMsg)
        self.emitTrayMsgSignal(u'文档生成完毕')

    # 显示操作日志
    def appendLog(self, logTxt):
        self.LogTextEdit.append(_translateUtf8(logTxt))

    # 解决在子线程中刷新UI 的问题。' QWidget::repaint: Recursive repaint detected '
    def appendLogSignal(self, logTxt):
        pass

    def emitAppendLogSignal(self, logTxt):
        self.LogTextEdit.emit(QtCore.SIGNAL('appendLogSignal(QString)'), logTxt)

    # 托盘消息
    def showTrayMsg(self, trayMsg):
        self.tray.show()
        # show 5 min
        self.tray.showMsg(trayMsg)

    def showTrayMsgSignal(self, trayMsg):
        pass

    def emitTrayMsgSignal(self, trayMsg):
        self.tray.emit(QtCore.SIGNAL('showTrayMsgSignal(QString)'), trayMsg)

    def show(self):
        self.exec_()
