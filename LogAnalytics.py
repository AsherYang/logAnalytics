# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LogAnalytics.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import sys

from PyQt4 import QtCore, QtGui

import StringUtil

# import pickle

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

class Ui_MainWidget(object):
    def setupUi(self, mainWindow):
        self.mainwindow = mainWindow
        mainWindow.setObjectName(_fromUtf8("MainWindow"))
        # MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.statusBar = QtGui.QStatusBar(mainWindow)
        self.menubar = QtGui.QMenuBar(mainWindow)
        file = self.menubar.addMenu(' &File')
        openFileAction = QtGui.QAction('Open file', mainWindow)
        openFileAction.setStatusTip(_fromUtf8('选择日志文件'))
        openFileAction.setShortcut('Ctrl+O')
        openFileAction.connect(openFileAction, QtCore.SIGNAL('triggered()'), self.openFile)

        saveLogFileAction = QtGui.QAction('Save Analytics', mainWindow)
        saveLogFileAction.setStatusTip(_fromUtf8('保存日志分析文件'))
        saveLogFileAction.setShortcut('Ctrl+Alt+S')
        saveLogFileAction.connect(saveLogFileAction, QtCore.SIGNAL('triggered()'), self.saveLogFile)

        loadLogFileAction = QtGui.QAction('Load Analytics', mainWindow)
        loadLogFileAction.setStatusTip(_fromUtf8('加载日志分析文件'))
        loadLogFileAction.setShortcut('Ctrl+Alt+O')
        loadLogFileAction.connect(loadLogFileAction, QtCore.SIGNAL('triggered()'), self.loadLogFile)

        file.addAction(openFileAction)
        file.addAction(loadLogFileAction)
        file.addAction(saveLogFileAction)

        setting = self.menubar.addMenu('&Setting')
        tools = self.menubar.addMenu('&Tools')

        # 添加到 mainWindow
        mainWindow.setMenuBar(self.menubar)
        mainWindow.setStatusBar(self.statusBar)

        # vBoxLayout 和 hBoxLayout 的选择依据是：根据2个控件的排列方向，上下排(vBoxLayout)还是左右排(hBoxLayout)
        vBoxLayout = QtGui.QVBoxLayout()
        hBboxLayout = QtGui.QHBoxLayout()

        # 需要设置添加到 self.centralwidget
        self.logAnalyticsEdit = QtGui.QTextEdit()
        self.logAnalyticsEdit.setFont(self.getFont('Monospace'))

        self.filterLineEdit = QtGui.QLineEdit()
        self.filterLineEdit.setFont(self.getFont('Monospace'))
        self.filterBtn = QtGui.QPushButton()
        self.filterBtn.setText(u'Filter')
        self.saveKeyWordBtn = QtGui.QPushButton()
        self.saveKeyWordBtn.setText(u'Save')
        self.LoadKeyWorkBtn = QtGui.QPushButton()
        self.LoadKeyWorkBtn.setText(u'Load')
        self.filterBtn.setFixedWidth(60)
        self.saveKeyWordBtn.setFixedWidth(60)
        self.LoadKeyWorkBtn.setFixedWidth(60)
        self.filterBtn.setFont(self.getFont('Consolas'))
        self.saveKeyWordBtn.setFont(self.getFont('Consolas'))
        self.LoadKeyWorkBtn.setFont(self.getFont('Consolas'))

        self.tabWidget = QtGui.QTabWidget()
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.setMovable(True)
        self.tabWidget.connect(self.tabWidget, QtCore.SIGNAL('tabCloseRequested(int)'), self.tabClose)
        self.tabWidget.connect(mainWindow, QtCore.SIGNAL('closeCurrentTabSignal()'), self.currentTabCloseSlot)

        self.filterLineEdit.setMaximumHeight(28)
        self.filterLineEdit.setMinimumHeight(28)
        hFilterSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        hFilterSplitter.addWidget(self.filterLineEdit)
        hFilterSplitter.addWidget(self.filterBtn)
        hFilterSplitter.addWidget(self.saveKeyWordBtn)
        hFilterSplitter.addWidget(self.LoadKeyWorkBtn)

        vSplitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        vSplitter.addWidget(hFilterSplitter)
        vSplitter.addWidget(self.tabWidget)

        hSplitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        hSplitter.addWidget(vSplitter)
        hSplitter.addWidget(self.logAnalyticsEdit)
        # 按比例分配 5:3
        hSplitter.setStretchFactor(0, 5)
        hSplitter.setStretchFactor(1, 3)

        hBboxLayout.addWidget(hSplitter)
        vBoxLayout.addLayout(hBboxLayout)

        self.centralwidget.setLayout(vBoxLayout)

        mainWindow.setCentralWidget(self.centralwidget)

    def getFont(self, fontStr):
        font = QtGui.QFont()
        font.setFamily(fontStr)
        font.setPointSize(10)
        font.setFixedPitch(True)
        return font

    def openFile(self):
        fileName = unicode(QtGui.QFileDialog.getOpenFileName(None, 'Open file', './', 'log files(*.log *.md *.txt)'))
        if not fileName:
            return
        file = open(fileName)
        data = file.read()
        file.close()
        loadTextEdit = QtGui.QTextEdit()
        loadTextEdit.setFont(self.getFont('Monospace'))
        loadTextEdit.setText(_translate('', data, None))
        self.tabWidget.addTab(loadTextEdit, fileName[(StringUtil.findLast(fileName, '/') + 1): ])

    def saveLogFile(self):
        text = str(self.logAnalyticsEdit.toPlainText())
        logTxtName = ''
        if text:
            logTxtName = text.split('\n')[0]
            if logTxtName.find('#') >= 0:
                # 字符串切片
                logTxtName = logTxtName[(logTxtName.find('#') + 1): ] + '.md'
            else:
                logTxtName += '.txt'
        # print logTxtName
        logTxtName = _translate('', logTxtName, None)
        fileName = unicode(QtGui.QFileDialog.getSaveFileName(None, 'save File', './' + logTxtName))
        print fileName
        if not fileName:
            fileName = 'logAnalytics.md'
            fileName = unicode(QtGui.QFileDialog.getSaveFileName(None, 'save File', './' + fileName))

        try:
            out_file = open(str(fileName), 'wb')
        except IOError:
            print u'未能保存Log分析文件'
            return
        # pickle.dump(text, out_file)
        out_file.write(text)
        out_file.close()
        # print text
        print fileName

    def loadLogFile(self):
        fileName = unicode(QtGui.QFileDialog.getOpenFileName(None, 'Open file', './', 'log files(*.log *.md *.txt)'))
        if not fileName:
            return
        file = open(fileName)
        data = file.read()
        file.close()
        self.logAnalyticsEdit.setText(_translate('', data, None))

    def currentTabCloseSlot(self):
        tabIndex = self.tabWidget.currentIndex()
        if tabIndex < 0:
            return
        self.tabClose(tabIndex)

    def tabClose(self, index):
        self.tabWidget.removeTab(index)


class LogMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)

        screen = QtGui.QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 4 * 3, screen.height() / 4 * 3)
        self.setWindowTitle('LogAnalytics')

    def keyPressEvent(self, event):
        # 设置 "Ctrl+w" 快捷键，用于关闭 tab
        if event.key() == QtCore.Qt.Key_W and event.modifiers() == QtCore.Qt.ControlModifier:
            self.emit(QtCore.SIGNAL('closeCurrentTabSignal()'))

    def closeCurrentTabSignal(self):
        return


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    logMainWin = LogMainWindow()
    uiMainWidget = Ui_MainWidget()
    uiMainWidget.setupUi(logMainWin)
    logMainWin.show()
    sys.exit(app.exec_())
