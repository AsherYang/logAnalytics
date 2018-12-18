#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/11/17
Desc  : Excel 拆分类，主要用于选取 Excel 中数据。
目前用于切分Excel 绑定号数据，用于大数据平台批量导入功能。(平台的限制批量只有100 一次)

操作excel 数据 https://www.cnblogs.com/lhj588/archive/2012/01/06/2314181.html
"""

import os
import sys

import xlwt
import xlrd
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QSizePolicy, QWidget, QSplitter

import QSettingsUtil
from EncodeUtil import _translateUtf8
from IconResourceUtil import resource_path
from QtFontUtil import QtFontUtil
from TrayIcon import TrayIcon
import FileUtil
from splitexcel.ExcelData import ExcelData
from ThreadUtil import ThreadUtil

reload(sys)
# print sys.getdefaultencoding()
sys.setdefaultencoding('utf8')


# print sys.getdefaultencoding()


class SplitExcelWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setWindowTitle(u'拆分Excel数据')
        self.setWindowIcon(QtGui.QIcon(resource_path('img/log.png')))
        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.resize(650, 500)
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignTop)
        self.mainLayout.setContentsMargins(5, 10, 5, 2)
        # 选取excel文件
        self.excelFileLayout = QtGui.QHBoxLayout()
        self.selectExcelFileBtn = QtGui.QPushButton(u'选择Excel文件')
        self.selectExcelFileBtn.connect(self.selectExcelFileBtn, QtCore.SIGNAL('clicked()'), self.selectExcelFileMethod)
        self.selectExcelFileLineEdit = QtGui.QLineEdit()
        self.selectExcelFileLineEdit.setTextMargins(10, 0, 10, 0)
        self.selectExcelFileLineEdit.setMinimumHeight(25)
        self.selectExcelFileLineEdit.setFont(QtFontUtil().getFont('Monospace', 12))
        self.excelFileLayout.addWidget(self.selectExcelFileBtn)
        self.excelFileLayout.addWidget(self.selectExcelFileLineEdit)
        # excel 行限制条件 directory
        self.LineConditionLayout = QtGui.QHBoxLayout()
        self.LineConditionStartLineEdit = QtGui.QLineEdit()
        self.LineConditionStartLineEdit.setTextMargins(10, 0, 10, 0)
        self.LineConditionStartLineEdit.setMinimumHeight(25)
        self.LineConditionStartLineEdit.setPlaceholderText(u'开始行号')
        self.LineConditionStartLineEdit.setFont(QtFontUtil().getFont('Monospace', 12))
        self.LineConditionEndLineEdit = QtGui.QLineEdit()
        self.LineConditionEndLineEdit.setTextMargins(10, 0, 10, 0)
        self.LineConditionEndLineEdit.setMinimumHeight(25)
        self.LineConditionEndLineEdit.setPlaceholderText(u'结束行号')
        self.LineConditionEndLineEdit.setFont(QtFontUtil().getFont('Monospace', 12))
        self.LineConditionIntervalTitle = QtGui.QLabel()
        self.LineConditionIntervalTitle.setText(u'行拆分间隔条数:')
        self.LineConditionIntervalTitle.setFont(QtFontUtil().getFont('微软雅黑', 14))
        self.LineConditionIntervalEdit = QtGui.QLineEdit()
        self.LineConditionIntervalEdit.setTextMargins(10, 0, 10, 0)
        self.LineConditionIntervalEdit.setMinimumHeight(25)
        self.LineConditionIntervalEdit.setPlaceholderText('0')
        self.LineConditionIntervalEdit.setFont(QtFontUtil().getFont('Monospace', 12))
        self.LineConditionTitle = QtGui.QLabel()
        self.LineConditionTitle.setText(u' 行数据: ')
        self.LineConditionTitle.setFont(QtFontUtil().getFont('微软雅黑', 14))
        self.LineConditionLabel = QtGui.QLabel()
        self.LineConditionLabel.setText(u'-->')
        self.LineConditionLabel.setFont(QtFontUtil().getFont('Monospace', 12))
        self.LineConditionLayout.addWidget(self.LineConditionTitle)
        self.LineConditionLayout.addWidget(self.LineConditionStartLineEdit)
        self.LineConditionLayout.addWidget(self.LineConditionLabel)
        self.LineConditionLayout.addWidget(self.LineConditionEndLineEdit)
        self.LineConditionLayout.addStretch()
        self.LineConditionLayout.addWidget(self.LineConditionIntervalTitle)
        self.LineConditionLayout.addWidget(self.LineConditionIntervalEdit)
        # excel 列限制条件 directory
        self.ColumnConditionLayout = QtGui.QHBoxLayout()
        self.ColumnConditionStartLineEdit = QtGui.QLineEdit()
        self.ColumnConditionStartLineEdit.setTextMargins(10, 0, 10, 0)
        self.ColumnConditionStartLineEdit.setMinimumHeight(25)
        self.ColumnConditionStartLineEdit.setPlaceholderText(u'开始列号')
        self.ColumnConditionStartLineEdit.setFont(QtFontUtil().getFont('Monospace', 12))
        self.ColumnConditionEndLineEdit = QtGui.QLineEdit()
        self.ColumnConditionEndLineEdit.setTextMargins(10, 0, 10, 0)
        self.ColumnConditionEndLineEdit.setMinimumHeight(25)
        self.ColumnConditionEndLineEdit.setPlaceholderText(u'结束列号')
        self.ColumnConditionEndLineEdit.setFont(QtFontUtil().getFont('Monospace', 12))
        self.ColumnConditionIntervalTitle = QtGui.QLabel()
        self.ColumnConditionIntervalTitle.setText(u'列拆分间隔条数:')
        self.ColumnConditionIntervalTitle.setFont(QtFontUtil().getFont('微软雅黑', 14))
        self.ColumnConditionIntervalEdit = QtGui.QLineEdit()
        self.ColumnConditionIntervalEdit.setTextMargins(10, 0, 10, 0)
        self.ColumnConditionIntervalEdit.setMinimumHeight(25)
        self.ColumnConditionIntervalEdit.setPlaceholderText('0')
        self.ColumnConditionIntervalEdit.setFont(QtFontUtil().getFont('Monospace', 12))
        self.ColumnConditionTitle = QtGui.QLabel()
        self.ColumnConditionTitle.setText(u' 列数据: ')
        self.ColumnConditionTitle.setFont(QtFontUtil().getFont('微软雅黑', 14))
        self.ColumnConditionLabel = QtGui.QLabel()
        self.ColumnConditionLabel.setText(u'-->')
        self.ColumnConditionLabel.setFont(QtFontUtil().getFont('Monospace', 12))
        self.ColumnConditionLayout.addWidget(self.ColumnConditionTitle)
        self.ColumnConditionLayout.addWidget(self.ColumnConditionStartLineEdit)
        self.ColumnConditionLayout.addWidget(self.ColumnConditionLabel)
        self.ColumnConditionLayout.addWidget(self.ColumnConditionEndLineEdit)
        self.ColumnConditionLayout.addStretch()
        self.ColumnConditionLayout.addWidget(self.ColumnConditionIntervalTitle)
        self.ColumnConditionLayout.addWidget(self.ColumnConditionIntervalEdit)
        # operate buttons
        self.btnsLayout = QtGui.QHBoxLayout()
        self.splitExcelBtn = QtGui.QPushButton(u'开始拆分')
        self.splitExcelBtn.setMinimumHeight(25)
        self.splitExcelBtn.connect(self.splitExcelBtn, QtCore.SIGNAL('clicked()'), self.splitExcelDataMethod)
        self.openDirBtn = QtGui.QPushButton(u'打开文件夹')
        self.openDirBtn.setMinimumHeight(25)
        self.openDirBtn.connect(self.openDirBtn, QtCore.SIGNAL('clicked()'), self.openDirMethod)
        self.btnsLayout.addWidget(self.splitExcelBtn)
        self.btnsLayout.addWidget(self.openDirBtn)
        # show log
        self.LogTextEdit = QtGui.QTextEdit()
        self.LogTextEdit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.LogTextEdit.setFont(QtFontUtil().getFont('Monospace', 12))
        self.LogTextEdit.connect(self.LogTextEdit, QtCore.SIGNAL('appendLogSignal(QString)'), self.appendLog)
        # addLayout
        self.mainLayout.addLayout(self.excelFileLayout)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.LineConditionLayout)
        self.mainLayout.addLayout(self.ColumnConditionLayout)
        self.mainLayout.addSpacing(10)
        self.mainLayout.addLayout(self.btnsLayout)
        self.centralwidget.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.LogTextEdit)
        # excelFileDataList 为新生成的每一个新excel 数据集合的集合
        self.excelFileDataList = []
        # 显示托盘
        self.tray = TrayIcon(parent=self, clickEnable=False)
        self.tray.connect(self.tray, QtCore.SIGNAL('showTrayMsgSignal(QString)'), self.showTrayMsg)

    # 选取Excel 文件
    def selectExcelFileMethod(self):
        filePath = unicode(QtGui.QFileDialog.getOpenFileName(
            None, 'Select excel', self.getLastOpenDir(), 'binder_number(*.xls *.xlsx)'))
        if not filePath:
            return
        self.selectExcelFileLineEdit.setText(filePath)

    # 获取QFileDialog 上次打开的路径
    def getLastOpenDir(self):
        lastDir = self.selectExcelFileLineEdit.text()
        if lastDir:
            return str(lastDir)
        # open last remember directory
        lastDir = QSettingsUtil.getLastDir()
        if not QtCore.QDir(lastDir).exists():
            lastDir = 'd://'
        return str(lastDir)

    def splitExcelDataMethod(self):
        # self.doSplitExcelData(log_call_back=self.emitAppendLogSignal)
        threadUtil = ThreadUtil(funcName=self.doSplitExcelData, log_call_back=self.emitAppendLogSignal)
        threadUtil.setDaemon(True)
        threadUtil.start()

    def doSplitExcelData(self, log_call_back):
        # 先进行清空操作
        self.excelFileDataList = []
        filePath = str(self.selectExcelFileLineEdit.text())
        if not filePath:
            log_call_back(u'请先选择Excel文件')
        log_call_back(u'行拆分和列拆分，是互斥操作，优先行拆分.')
        startLineStr = str(self.LineConditionStartLineEdit.text())
        endLineStr = str(self.LineConditionEndLineEdit.text())
        lineIntervalStr = str(self.LineConditionIntervalEdit.text())
        startColumnStr = str(self.ColumnConditionStartLineEdit.text())
        endColumnStr = str(self.ColumnConditionEndLineEdit.text())
        columnIntervalStr = str(self.ColumnConditionIntervalEdit.text())
        try:
            data = xlrd.open_workbook(unicode(filePath))
            dataTable = data.sheets()[0]
            tableRow = dataTable.nrows
            tableColumn = dataTable.ncols
            # print 'table row: ', tableRow
            # print 'table col: ', tableColumn
            # 配合 xrange ()的方式
            excelStartLine = int(startLineStr) - 1 if startLineStr else 0
            excelEndLine = int(endLineStr) if endLineStr else tableRow
            excelLineInterval = int(lineIntervalStr) if lineIntervalStr else -1
            excelStartColumn = int(startColumnStr) - 1 if startColumnStr else 0
            excelEndColumn = int(endColumnStr) if endColumnStr else tableColumn
            excelColumnInterval = int(columnIntervalStr) if columnIntervalStr else -1
            if excelLineInterval < 0 and excelColumnInterval < 0:
                log_call_back(u'必须要有一个行或者列拆分间隔!')
                return
            if excelStartLine < 0 or excelStartLine > tableRow or excelStartLine > excelEndLine or excelEndLine < 0 \
                    or excelStartColumn < 0 or excelStartColumn > tableColumn or excelStartColumn > excelEndColumn \
                    or excelEndColumn < 0:
                log_call_back(u'参数不合法，请重新输入!')
                return
            cellDataList = []
            newLineNo = 0
            newColumnNo = 0
            # 先准备数据
            for i in xrange(excelStartLine, excelEndLine):
                for j in xrange(excelStartColumn, excelEndColumn):
                    # print 'i = %d, j= %d ' % (i, j)
                    # rowDataList = dataTable.row_values(i)
                    # columnDataList = dataTable.col_values(j)
                    # cellData = dataTable.cell(i, j).value
                    # print 'rowDataList: ', rowDataList
                    # print 'columnDataList: ', columnDataList
                    # print 'cellData: ', cellData
                    # print 'i = %d , interval = %d , sp = %d ' % (i, excelLineInterval, i % excelLineInterval)
                    if i != 0 and excelLineInterval > 0 and i % excelLineInterval == 0:
                        newLineNo = 0
                    elif j != 0 and excelColumnInterval > 0 and j % excelColumnInterval == 0:
                        newColumnNo = 0
                    else:
                        pass
                    excelData = ExcelData()
                    excelData.lineNo = newLineNo
                    excelData.columnNo = newColumnNo
                    excelData.value = dataTable.cell(i, j).value
                    cellDataList.append(excelData)
                    newColumnNo += 1
                newLineNo += 1
                newColumnNo = 0
            # 拆分数据，到各个excel文件中去
            tempList = []
            for i in xrange(len(cellDataList)):
                if tempList and cellDataList[i].lineNo == 0 and cellDataList[i].columnNo == 0:
                    self.excelFileDataList.append(tempList)
                    tempList = []
                tempList.append(cellDataList[i])
                if i == len(cellDataList) - 1:
                    self.excelFileDataList.append(tempList)
            # print 'excelFileDataList: ', self.excelFileDataList
            # for excelList in self.excelFileDataList:
            #     print '-------------------------------'
            #     for cellData in excelList:
            #         print 'cellData: ', cellData
            interval = excelLineInterval if excelLineInterval > 0 else \
                (excelColumnInterval if excelColumnInterval > 0 else -1)
            self.genExcelData(self.excelFileDataList, interval, log_call_back)
        except Exception as e:
            raise e

    def genExcelData(self, allExcelDataList, interval, log_call_back):
        if not allExcelDataList:
            log_call_back(u'未生成相关数据!')
            return
        if interval == -1:
            log_call_back(u'拆分间隔未设置，不做数据拆分!')
            return
        selectExcelFileName = FileUtil.getFilePathWithName(str(self.selectExcelFileLineEdit.text()))
        for i in xrange(len(allExcelDataList)):
            excelFileName = str(selectExcelFileName) + str("_") + str((i+1)*interval) + str(".xls")
            # print 'excelFileName: ', excelFileName
            workbook = xlwt.Workbook(encoding='utf-8')
            sheetData = workbook.add_sheet("split_data")
            for cellData in allExcelDataList[i]:
                # print 'cellData===', cellData
                sheetData.write(cellData.lineNo, cellData.columnNo, cellData.value)
            workbook.save(unicode(excelFileName))
        log_call_back(u'excel文件拆分完毕!')

    # 打开文件夹
    def openDirMethod(self):
        excelFilePath = str(self.selectExcelFileLineEdit.text())
        if not excelFilePath:
            logMsg = u'请先选择Excel 文件'
            self.appendLog(logMsg)
            return
        parentPath = unicode(FileUtil.getFileDir(excelFilePath))
        # print 'parentPath: %s' % parentPath
        os.startfile(parentPath)

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


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    splitExcelWin = SplitExcelWindow()
    splitExcelWin.show()
    sys.exit(app.exec_())
