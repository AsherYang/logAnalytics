# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LogAnalytics.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys
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
        openFile1Action = QtGui.QAction('Open file 1', mainWindow)
        openFile1Action.setStatusTip(_fromUtf8('选择文件1'))
        openFile1Action.connect(openFile1Action, QtCore.SIGNAL('triggered()'), self.openFile1)

        openFile2Action = QtGui.QAction('Open file 2', mainWindow)
        openFile2Action.setStatusTip(_fromUtf8('选择文件2'))
        openFile2Action.connect(openFile2Action, QtCore.SIGNAL('triggered()'), self.openFile2)

        saveLogFileAction = QtGui.QAction('Save file', mainWindow)
        saveLogFileAction.setStatusTip(_fromUtf8('保存日志分析文件'))
        saveLogFileAction.setShortcut('Ctrl+Alt+S')
        saveLogFileAction.connect(saveLogFileAction, QtCore.SIGNAL('triggered()'), self.saveLogFile)

        file.addAction(openFile1Action)
        file.addAction(openFile2Action)
        file.addAction(saveLogFileAction)

        setting = self.menubar.addMenu('&Setting')
        tools = self.menubar.addMenu('&Tools')

        # 添加到 mainWindow
        mainWindow.setMenuBar(self.menubar)
        mainWindow.setStatusBar(self.statusBar)

        vBoxLayout = QtGui.QVBoxLayout()
        hBboxLayout = QtGui.QHBoxLayout()

        # 需要设置添加到 self.centralwidget
        self.logAnalyticsEdit = QtGui.QTextEdit()
        self.logAnalyticsEdit.setFont(self.getFont('Monospace'))

        self.tabWidget = QtGui.QTableWidget()

        hBboxLayout.addWidget(self.tabWidget)
        hBboxLayout.addWidget(self.logAnalyticsEdit)
        vBoxLayout.addLayout(hBboxLayout)

        self.centralwidget.setLayout(vBoxLayout)

        mainWindow.setCentralWidget(self.centralwidget)

    def getFont(self, fontStr):
        font = QtGui.QFont()
        font.setFamily(fontStr)
        font.setPointSize(10)
        font.setFixedPitch(True)
        return font

    def openFile1(self):
        fileName = unicode(QtGui.QFileDialog.getOpenFileName(None, 'Open file 1', './', 'log files(*.log *.md *.txt)'))
        if not fileName:
            return
        file = open(fileName)
        data = file.read()
        file.close()
        self.logAnalyticsEdit.setText(_translate('', data, None))

    def openFile2(self):
        fileName = unicode(QtGui.QFileDialog.getOpenFileName(None, 'Open file 2', './', 'log files(*.log *.md *.txt)'))
        if not fileName:
            return
        file = open(fileName)
        data = file.read()
        file.close()
        self.logAnalyticsEdit.setText(_translate('', data, None))

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
        fileName = unicode(QtGui.QFileDialog.getSaveFileName(None, 'save File', './' + logTxtName))
        if not fileName:
            return

        try:
            out_file = open(str(fileName), 'wb')
        except IOError:
            QtGui.QMessageBox.information(None, "Unable to open file",
                                          "There was an error opening \"%s\"" % fileName)
            return
        # pickle.dump(text, out_file)
        out_file.write(text)
        out_file.close()
        # print text
        print fileName

class LogMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)

        screen = QtGui.QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 4 * 3, screen.height() / 4 * 3)
        self.setWindowTitle('LogAnalytics')


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    logMainWin = LogMainWindow()
    uiMainWidget = Ui_MainWidget()
    uiMainWidget.setupUi(logMainWin)
    logMainWin.show()
    sys.exit(app.exec_())
