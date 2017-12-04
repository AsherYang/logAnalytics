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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        # MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 121, 21))
        self.label.setObjectName(_fromUtf8("label"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu = QtGui.QMenu(self.menubar)
        self.menu.setObjectName(_fromUtf8("menu"))
        self.menu_2 = QtGui.QMenu(self.menubar)
        self.menu_2.setObjectName(_fromUtf8("menu_2"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.label.setText(_translate("MainWindow", "TextLabel", None))
        self.menu.setTitle(_translate("MainWindow", "选择文件", None))
        self.menu_2.setTitle(_translate("MainWindow", "设置", None))


class LogMainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)

        screen = QtGui.QDesktopWidget().screenGeometry()
        self.resize(screen.width() / 4 * 3, screen.height() / 4 * 3)
        self.setWindowTitle('LogAnalytics')

        self.statusBar()

        menuBar = self.menuBar()
        file = menuBar.addMenu(' &File')
        openFile1Action = QtGui.QAction('Open file 1', self)
        openFile1Action.setStatusTip(_fromUtf8('选择文件1'))
        openFile1Action.connect(openFile1Action, QtCore.SIGNAL('triggered()'), self.openFile1)

        openFile2Action = QtGui.QAction('Open file 2', self)
        openFile2Action.setStatusTip(_fromUtf8('选择文件2'))
        openFile2Action.connect(openFile2Action, QtCore.SIGNAL('triggered()'), self.openFile2)

        saveLogFileAction = QtGui.QAction('Save file', self)
        saveLogFileAction.setStatusTip(_fromUtf8('保存日志分析文件'))
        saveLogFileAction.setShortcut('Ctrl+Alt+S')
        saveLogFileAction.connect(saveLogFileAction, QtCore.SIGNAL('triggered()'), self.saveLogFile)

        file.addAction(openFile1Action)
        file.addAction(openFile2Action)
        file.addAction(saveLogFileAction)

        setting = menuBar.addMenu('&Setting')
        tools = menuBar.addMenu('Tools')

        self.textEdit = QtGui.QTextEdit()
        self.textEdit.setFont(self.getFont('Monospace'))
        self.setCentralWidget(self.textEdit)

    def getFont(self, fontStr):
        font = QtGui.QFont()
        font.setFamily(fontStr)
        font.setPointSize(10)
        font.setFixedPitch(True)
        return font

    def openFile1(self):
        fileName = unicode(QtGui.QFileDialog.getOpenFileName(self, 'Open file 1', './', 'log files(*.log *.md *.txt)'))
        if not fileName:
            return
        file = open(fileName)
        data = file.read()
        file.close()
        self.textEdit.setText(_translate('', data, None))

    def openFile2(self):
        fileName = unicode(QtGui.QFileDialog.getOpenFileName(self, 'Open file 2', './', 'log files(*.log *.md *.txt)'))
        if not fileName:
            return
        file = open(fileName)
        data = file.read()
        file.close()
        self.textEdit.setText(_translate('', data, None))

    def saveLogFile(self):
        fileName = unicode(QtGui.QFileDialog.getSaveFileName(self, 'save File', './'))
        if not fileName:
            return

        try:
            out_file = open(str(fileName), 'wb')
        except IOError:
            QtGui.QMessageBox.information(self, "Unable to open file",
                                          "There was an error opening \"%s\"" % fileName)
            return
        text = str(self.textEdit.toPlainText())
        # pickle.dump(text, out_file)
        out_file.write(text)
        out_file.close()
        # print text
        print fileName


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    # label = QtGui.QLabel("<center>Hello World with PyQt4!</center>")
    # label.resize(500, 400)
    # label.show()
    # mainWin = QtGui.QMainWindow()
    logMainWin = LogMainWindow()
    # uiMainWin = Ui_MainWindow()
    # uiMainWin.setupUi(logMainWin)
    logMainWin.show()
    sys.exit(app.exec_())
