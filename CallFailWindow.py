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
import re
import json

from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QFile
from PyQt4.QtGui import QSizePolicy, QWidget

import FileUtil
import QSettingsUtil
import SupportFiles
from EncodeUtil import _translate, _translateUtf8
from QtFontUtil import QtFontUtil
from TrayIcon import TrayIcon
from ThreadUtil import ThreadUtil
from ZipFileUtil import ZipFileUtil
from analyticslog.CallFailBean import CallFailBean
from SearchKeywordByMultiProcess import SearchKeywordByMultiProcess
from SearchBaseAttrByMultiProcess import SearchBaseAttrByMultiProcess
from IconResourceUtil import resource_path
from DownloadLogByWeb import DownloadLogByWeb
from SearchByMultiProcess import SearchByMultiProcess
import xlrd
import threading

reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')
# print sys.getdefaultencoding()


class CallFailWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowTitle(u'掉话分析')
        self.setWindowIcon(QtGui.QIcon(resource_path('img/log.png')))
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
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
        # download the log [from http://172.28.199.58/watch/index_prod.html#/watchda_web/logCollection]
        self.downloadLogLayout = QtGui.QHBoxLayout()
        self.dlBinderNumberLineEdit = QtGui.QLineEdit()
        self.dlBinderNumberLineEdit.setTextMargins(10, 0, 10, 0)
        self.dlBinderNumberLineEdit.setMinimumHeight(25)
        self.dlBinderNumberLineEdit.setFont(QtFontUtil().getFont('Monospace', 12))
        self.dlImportBinderNumberBtn = QtGui.QPushButton(u'导入绑定号')
        self.dlImportBinderNumberBtn.connect(self.dlImportBinderNumberBtn, QtCore.SIGNAL('clicked()'),
                                             self.dlImportBinderNumberMethod)
        self.downloadLogLayout.addWidget(self.dlImportBinderNumberBtn)
        self.downloadLogLayout.addWidget(self.dlBinderNumberLineEdit)
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
        self.downloadLogBtn = QtGui.QPushButton(u'下载日志')
        self.unzipBtn = QtGui.QPushButton(u'解压日志')
        self.analyticsBtn = QtGui.QPushButton(u'开始分析')
        self.generateDocumentBtn = QtGui.QPushButton(u'生成文档')
        self.openDirBtn = QtGui.QPushButton(u'打开文件夹')
        self.unzipBtn.setMinimumHeight(25)
        self.analyticsBtn.setMinimumHeight(25)
        self.generateDocumentBtn.setMinimumHeight(25)
        self.openDirBtn.setMinimumHeight(25)
        self.downloadLogBtn.connect(self.downloadLogBtn,  QtCore.SIGNAL('clicked()'), self.downloadLogMethod)
        self.unzipBtn.connect(self.unzipBtn,  QtCore.SIGNAL('clicked()'), self.unZipMethod)
        self.analyticsBtn.connect(self.analyticsBtn,  QtCore.SIGNAL('clicked()'), self.analyticsMethod)
        self.analyticsBtn.connect(self.analyticsBtn, QtCore.SIGNAL('combineLogSignal(QString)'), self.combineLogWithAttr)
        self.generateDocumentBtn.connect(self.generateDocumentBtn,  QtCore.SIGNAL('clicked()'), self.genDocMethod)
        self.openDirBtn.connect(self.openDirBtn,  QtCore.SIGNAL('clicked()'), self.openDirMethod)
        self.btnsLayout.addWidget(self.downloadLogBtn)
        self.btnsLayout.addWidget(self.unzipBtn)
        self.btnsLayout.addWidget(self.analyticsBtn)
        self.btnsLayout.addWidget(self.generateDocumentBtn)
        self.btnsLayout.addWidget(self.openDirBtn)
        # show log
        self.LogTextEdit = QtGui.QTextEdit()
        self.LogTextEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.LogTextEdit.setFont(QtFontUtil().getFont('Monospace', 12))
        self.LogTextEdit.connect(self.LogTextEdit, QtCore.SIGNAL('appendLogSignal(QString)'), self.appendLog)
        # addLayout
        self.mainLayout.addLayout(self.selectDirectoryLayout)
        self.mainLayout.addLayout(self.downloadLogLayout)
        self.mainLayout.addLayout(self.keywordLayout)
        self.mainLayout.addLayout(self.btnsLayout)
        self.mainLayout.addWidget(self.LogTextEdit)
        self.centralwidget.setLayout(self.mainLayout)
        # 优化文件数据分析性能，已分组形式进行, 这两个变量记录总共需要分析的分组数量，以及已经分析的组数
        # self.analyticsGroupTotalSize = 0
        # self.processedGroupSize = 0
        # self.processedGroupLock = threading.Lock()
        # 接收 keywordLineEdit 中输入的关键字
        self.analyKeyword = None
        # 接收基础信息 baseAttr 的关键字
        self.baseAttrKeyword = None
        # # 搜索keyword 时，返回包含keyword的行数据
        # self.searchedKeywordLines = ""
        # # 搜索基础信息baseAttr时, 返回包含baseAttr的行数据
        # self.searchedBaseAttrLines = ""
        # 保存分析的日志信息集合
        self.analyticsLogList = []
        # 保存基本信息的集合
        self.baseAttrList = []
        # 多线程中进行集合过滤的锁
        self.filterLogLock = threading.Lock()
        self.filterAttrLock = threading.Lock()
        # 保存最后分析结果 CallFailBean 的集合
        self.callFailList = []
        # 保存从excel 导入的绑定号集合
        self.binderNumberList = []
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

    # download log. load binder number(下载日志时，需要提前导入绑定号)
    # 操作excel 数据 https://www.cnblogs.com/lhj588/archive/2012/01/06/2314181.html
    def dlImportBinderNumberMethod(self):
        filePath = unicode(QtGui.QFileDialog.getOpenFileName(
            None, 'Select file', self.getLastOpenDir(), 'binder_number(*.xls *.xlsx)'))
        if not filePath:
            return
        # print 'binderNumberFilePath: ', filePath
        binderNumberListStr = ''
        try:
            data = xlrd.open_workbook(unicode(filePath))
            binderNumberTable = data.sheets()[0]
            # print 'table row: ', binderNumberTable.nrows
            # print 'table col: ', binderNumberTable.ncols
            for i in range(binderNumberTable.ncols):
                binderNumberColList = binderNumberTable.col_values(i)
                for binderNumber in binderNumberColList:
                    if binderNumber not in self.binderNumberList:
                        self.binderNumberList.append(binderNumber)
                        binderNumberListStr += (binderNumber + '|')
                # print 'table col: ', binderNumberTable.col_values(i)
                # print 'table row: ', binderNumberTable.row_values(i)
        except Exception as e:
            self.binderNumberList = []
            raise e
        print 'binderNumberList: ', self.binderNumberList
        self.dlBinderNumberLineEdit.setText(binderNumberListStr)

    # 点击下载日志按钮，从服务器[http://172.28.199.58/watch/index_prod.html#/watchda_web/logCollection]下载日志
    def downloadLogMethod(self):
        selectDir = str(self.selectDirectoryLineEdit.text())
        if not selectDir:
            self.appendLog(u'您尚未选择日志文件路径! 请先选择日志路径。')
            return
        importedBinderNumbers = str(self.dlBinderNumberLineEdit.text())
        if not importedBinderNumbers:
            self.appendLog(u'请导入需要下载日志的绑定号!')
            return
        # self.doDownloadLog(log_call_back=self.emitAppendLogSignal)
        threadUtil = ThreadUtil(funcName=self.doDownloadLog, log_call_back=self.emitAppendLogSignal)
        threadUtil.setDaemon(True)
        threadUtil.start()

    # 开始下载日志
    def doDownloadLog(self, log_call_back):
        dlLogByWeb = DownloadLogByWeb()
        dlLogByWeb.setCallBack(log_call_back)
        dlLogByWeb.login()
        dlLogByWeb.setBinderNumberList(self.binderNumberList)
        dlLogByWeb.downloadLog()

    # 点击解压日志按钮
    def unZipMethod(self):
        # self.doUnzipFile(log_call_back=self.emitAppendLogSignal)
        threadUtil = ThreadUtil(funcName=self.doUnzipFile, log_call_back=self.emitAppendLogSignal)
        threadUtil.setDaemon(True)
        threadUtil.start()

    # 解压文件
    def doUnzipFile(self, log_call_back):
        selectDir = str(self.selectDirectoryLineEdit.text())
        if not selectDir:
            log_call_back(u'您尚未选择日志文件路径! 请先选择日志路径。')
            return
        zipFileUtil = ZipFileUtil(log_call_back)
        zipFileUtil.recursiveUnZipFile(selectDir)
        log_call_back(u'解压完成')

    # 点击分析日志按钮
    def analyticsMethod(self):
        self.analyticsBtn.setDisabled(True)
        self.generateDocumentBtn.setDisabled(True)
        self.doAnalyticsWithGroup()

    """
    开始分析， 分析步骤：
    # 1. 先将文件进行分组；利用线程分组策略，每一线程处理多个文件 (!!多进程操作文件的情况下，已去除!!)
    2. 先分析给定的关键字，在单个数据文件中进行搜索；利用多进程读取策略读取单个文件(提升速度)
    3. 再搜索基础信息，同样在分组数据中进行搜索；(基本信息BaseAttrBean: binderNumber, machineMode, osVersion 等)
    4. 组合数据，则将 AnalyticsLogBean 内容与 baseAttr 基本信息进行整合，保存进 CallFailBeanList 中。便于后面生成文档。
    """
    def doAnalyticsWithGroup(self):
        selectDir = str(self.selectDirectoryLineEdit.text())
        if not selectDir:
            logMsg = u'您尚未选择日志文件路径! 请先选择日志路径。'
            self.appendLog(logMsg)
            self.analyticsBtn.setEnabled(True)
            self.generateDocumentBtn.setEnabled(True)
            return
        allFilePaths = FileUtil.getAllFiles(selectDir)
        print 'len(allFilePaths): ', len(allFilePaths)
        supportFilePaths = []
        for filePath in allFilePaths:
            if SupportFiles.hasSupportFile(filePath) and \
                    not SupportFiles.hasContainsPath(filePath, *self.removeThePathKeys()):
                supportFilePaths.append(filePath)
        if not supportFilePaths:
            return
        # self.analyticsGroupTotalSize = len([supportFilePaths[i:i+10] for i in xrange(0, len(supportFilePaths), 10)])
        print 'len(supportFilePaths): ', len(supportFilePaths)
        # print 'len(analyticsGroupTotalSize): ', self.analyticsGroupTotalSize
        # 1. 数组分组，以10个一组
        # for i in xrange(0, len(supportFilePaths), 10):
        #     filePathList = supportFilePaths[i:i+10]
        #     # print 'filePathList: ', filePathList
        #     # 2,3 进行分组数据搜索
        #     # 无线程版
        #     # self.doSearchFile(filePathList)
        #     threadUtil = ThreadUtil(funcName=self.doSearchFile, filePaths=filePathList)
        #     threadUtil.setDaemon(True)
        #     threadUtil.start()
        # self.doSearchFile(supportFilePaths)
        # 去除多线程分组，默认采用多进程分析文件，避免同时使用多线程的情况下使用多进程，否则电脑会被冲爆
        threadUtil = ThreadUtil(funcName=self.doSearchFile, filePaths=supportFilePaths)
        threadUtil.setDaemon(True)
        threadUtil.start()

    # 2,3 进行分组数据搜索
    def doSearchFile(self, filePaths):
        if not filePaths:
            return
        # 进行搜索前，确认本次搜索关键字
        self.analyKeyword = str(self.keywordLineEdit.text()) if str(
            self.keywordLineEdit.text()).strip() else str("reportCallFailLD =")
        self.baseAttrKeyword = str("base attribute info")
        # 搜索关键字信息
        for filePath in filePaths:
            # print "filePath---> : %s --> currentThread: %s" % (_translateUtf8(filePath), threading.currentThread().getName())
            self.searchkeywordByMultiProcess(filePath)
        # 再搜索基本信息
        for filePath in filePaths:
            self.searchBaseAttrByMultiProcess(filePath)
        # 4. 组合数据，去主线程组装数据
        self.emitCombineLogSignal(threading.currentThread().getName())

    def combineLogSignal(self, thread_name):
        pass

    def emitCombineLogSignal(self, thread_name):
        self.analyticsBtn.emit(QtCore.SIGNAL('combineLogSignal(QString)'), thread_name)

    # 4. 组合数据,主线程组装数据(提高优先级)
    def combineLogWithAttr(self, thread_name):
        print u'----线程%s已完成工作, 正在使用线程%s开始组装数据-----' % (thread_name, threading.currentThread().getName())
        # self.processedGroupSize += 1
        # logMsg = u'一共需要分析:' + str(self.analyticsGroupTotalSize) + u'组，已经分析:' + str(self.processedGroupSize) \
        #          + u'组，剩余:' + str(self.analyticsGroupTotalSize - self.processedGroupSize) + u'组。'
        logMsg = u'已分析完文件，正在开始组装数据'
        self.appendLog(logMsg)
        print logMsg
        # if self.analyticsGroupTotalSize == self.processedGroupSize:
        for analyLog in self.analyticsLogList:
            analyLogTxt = analyLog.logTxt
            analyLogFilePath = analyLog.filePath
            analyLogStr = re.search(r'ReportCallFailLD\s(\{.+})', analyLogTxt).group(1)
            analyLogJson = self.convertStr2JsonStr(analyLogStr)
            if not analyLogJson:
                continue
            for baseAttr in self.baseAttrList:
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
                          ' logFilePath: %s) ' \
                          % (callFail.binderNumber, callFail.machineMode, callFail.osVersion, callFail.failTime,
                             callFail.voiceNetworkType, callFail.dialMode, callFail.causeCode,
                             callFail.vendorCauseCode, callFail.logText, callFail.logFilePath)
                    self.callFailList.append(callFail)
        self.analyticsBtn.setEnabled(True)
        self.generateDocumentBtn.setEnabled(True)
        logMsg = u'---------- 日志分析完毕 -----------'
        self.appendLog(logMsg)
        self.emitTrayMsgSignal(u'日志分析完毕')
        print '------------- over ---------------'
        # end if self.analyticsGroupTotalSize == self.processedGroupSize: (此处只做一个end if 语句记号)

    # 多进程操作文件，搜索输入关键字
    def searchkeywordByMultiProcess(self, file_path):
        searchKeywordMultiProcess = SearchKeywordByMultiProcess(file_path, self, self.searchKeywordCallBack, self.analyKeyword)
        searchKeywordMultiProcess.createAndDoJobs()

    # 多进程操作文件，用于状态回调
    @staticmethod
    def searchKeywordCallBack(self, status, file_path, searchedLogJobs):
        # print '-0---searchKeywordCallBack keyword:%s == lines: %s, status: %s' % (self.analyKeyword, searchedLogList, status)
        if not self.analyKeyword:
            return
        if status == SearchByMultiProcess.STATUS_PROCESSING:
            logMsg = u'正在分析文件：' + _translateUtf8(file_path)
            self.dologCallBack(self.emitAppendLogSignal, logMsg)
            return
        if not searchedLogJobs:
            return
        for searchedLogJob in searchedLogJobs:
            if not searchedLogJob:
                continue
            for searchedLog in searchedLogJob:
                if not searchedLog:
                    continue
                self.filterAnalyLog2List(self.analyticsLogList, searchedLog)

    # 多进程操作文件，搜索基础信息
    def searchBaseAttrByMultiProcess(self, file_path):
        searchBaseAttrMultiProcess = SearchBaseAttrByMultiProcess(file_path, self, self.searchBaseAttrCallBack, self.baseAttrKeyword)
        searchBaseAttrMultiProcess.createAndDoJobs()

    # 多进程操作文件，用于状态回调
    @staticmethod
    def searchBaseAttrCallBack(self, status, file_path, searchedBaseAttrJobs):
        if not self.baseAttrKeyword:
            return
        if status == SearchByMultiProcess.STATUS_PROCESSING:
            return
        if not searchedBaseAttrJobs:
            return
        for searchedBaseAttrJob in searchedBaseAttrJobs:
            if not searchedBaseAttrJob:
                continue
            for searchedBaseAttr in searchedBaseAttrJob:
                if not searchedBaseAttr:
                    continue
                self.filterBaseAttr2List(self.baseAttrList, searchedBaseAttr)

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
        logMsg = u'正在分析文件：' + _translateUtf8(file_path)
        self.dologCallBack(log_call_back, logMsg)
        # stream = QtCore.QTextStream(file)
        # stream.setCodec('UTF-8')
        # data = stream.readAll()
        # file.close()
        # stream.flush()
        # dataTmp = StringIO.StringIO(data)
        searchedText = ''
        # while True:
        with open(filePath) as f:
            print 'len(file): ', len(f.readlines())
            for line in f:
                textLine = str(_translateUtf8(line))
                if textLine == '':
                    # logMsg = u'已分析完文件：' + _translateUtf8(file_path)
                    # log_call_back(logMsg)
                    # print logMsg
                    break
                textLineLower = textLine.lower()
                keywordIndex = textLineLower.find(keyword.lower())
                if keywordIndex != -1:
                    searchedText += textLine
        # release StringIO memory
        # dataTmp.close()
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

    # 过滤日志信息, 去重后添加进集合
    def filterAnalyLog2List(self, analyticsLogList, analyLogBean):
        with self.filterLogLock:
            if not analyLogBean:
                return
            if len(analyticsLogList) == 0:
                analyticsLogList.append(analyLogBean)
                return
            if not self.hasListContainLog(analyticsLogList, analyLogBean):
                # print '>>>> append analyticsLogList: %s ---> analyLogBean:%s' % (analyticsLogList, analyLogBean)
                analyticsLogList.append(analyLogBean)

    # 集合中是否已经包含了重复LOG
    def hasListContainLog(self, analyticsLogList, analyLogBean):
        for analyLog in analyticsLogList:
            if analyLog.logTxt == analyLogBean.logTxt:
                return True
            elif analyLogBean in analyticsLogList:
                return True
        return False

    # 过滤 baseAttr 信息， 去重后添加进集合
    def filterBaseAttr2List(self, baseAttrList, baseAttr):
        with self.filterAttrLock:
            if not baseAttr:
                return
            if len(baseAttrList) == 0:
                baseAttrList.append(baseAttr)
                return
            if not self.hasListContainAttr(baseAttrList, baseAttr):
                # print '>>>> append baseAttrList: %s ---> baseAttr:%s' % (baseAttrList, baseAttr)
                baseAttrList.append(baseAttr)

    # 集合中是否已经包含了重复attr属性
    def hasListContainAttr(self, baseAttrList, baseAttr):
        for baseAttrTmp in baseAttrList:
            if baseAttrTmp.binderNumber == baseAttr.binderNumber:
                return True
            elif baseAttr in baseAttrList:
                return True
        return False

    # 找出有效的基础信息，进行json 转换
    def filterBaseAttr2Json(self, searchedBaseAttr):
        if not searchedBaseAttr:
            return None
        baseAttrJson = None
        baseAttrList = re.findall(r'BaseAttr(\{.+})', searchedBaseAttr)
        # print '---> baseAttrList: ', baseAttrList
        if baseAttrList:
            for baseAttrStr in baseAttrList:
                baseAttrJson = self.convertStr2JsonStr(baseAttrStr)
                # print '==> baseAttrJson: ', baseAttrJson
                if baseAttrJson:
                    return baseAttrJson
        return baseAttrJson

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
            fileName = binderNumber + u'_问题分析.txt'
            filePath = os.path.join(fileDirPath, fileName)
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
        self.release()
        logMsg = u'---------- 文档生成完毕 -----------'
        log_call_back(logMsg)
        self.emitTrayMsgSignal(u'文档生成完毕')

    # 打开文件夹
    def openDirMethod(self):
        selectDir = self.selectDirectoryLineEdit.text()
        if not selectDir:
            logMsg = u'您尚未选择日志文件路径! 请先选择日志路径。'
            self.appendLog(logMsg)
            return
        os.startfile(unicode(selectDir))

    # 需要去除包含以下关键字的路径
    def removeThePathKeys(self):
        return ["traces", "bugreport", "diag_logs"]

    # release
    def release(self):
        # 清空本次数据
        self.analyKeyword = None
        self.baseAttrKeyword = None
        self.analyticsLogList = []
        self.baseAttrList = []
        self.callFailList = []
        # self.analyticsGroupTotalSize = 0
        # self.processedGroupSize = 0

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

    def keyPressEvent(self, event):
        # 设置 "Ctrl+w" 快捷键，用于关闭 tab
        if event.key() == QtCore.Qt.Key_W and event.modifiers() == QtCore.Qt.ControlModifier:
            self.close()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    callFailWin = CallFailWindow()
    callFailWin.show()
    sys.exit(app.exec_())
