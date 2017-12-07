# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'LogAnalytics.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

import sys

from PyQt4 import QtCore, QtGui

import StringUtil
import StringIO
import os
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

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Ui_MainWidget(object):
    def setupUi(self, mainWindow):
        self.mainwindow = mainWindow
        self.originalData = None
        self.filterConfigFilePath = '.\\filter_config'
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
        self.filterLineEdit.setFont(self.getFont('Consolas'))
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

        self.filterBtn.setStatusTip(u'请输入过滤字符，多个字符间以 "|" 分割, (Ctrl+F)')
        self.filterBtn.setShortcut('Ctrl+F')
        self.saveKeyWordBtn.setStatusTip(u'保存过滤条件, (Ctrl+B)')
        self.saveKeyWordBtn.setShortcut('Ctrl+B')
        self.LoadKeyWorkBtn.setStatusTip(u'加载过滤条件,(Ctrl+L)')
        self.LoadKeyWorkBtn.setShortcut('Ctrl+L')

        self.filterBtn.connect(self.filterBtn, QtCore.SIGNAL('clicked()'), self.filter)
        self.saveKeyWordBtn.connect(self.saveKeyWordBtn, QtCore.SIGNAL('clicked()'), self.saveKeyWord)
        self.LoadKeyWorkBtn.connect(self.LoadKeyWorkBtn, QtCore.SIGNAL('clicked()'), self.loadKeyWord)

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
        self.originalData = data
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

    def filter(self):
        if not self.originalData:
            return
        if not self.filterLineEdit.text():
            self.tabWidget.currentWidget().setText(_translate('', self.originalData, None))
            return
        filterList = str(self.filterLineEdit.text()).split('|')
        currentTxt = StringIO.StringIO(self.originalData)
        filterTxt = ''
        # print currentTxt.readline()
        while True:
            textLine = str(_translate('', currentTxt.readline(), None))
            if textLine == '':
                print 'read over. '
                break
            for filterWord in filterList:
                if not filterWord.strip():
                    continue
                keywordIndex = textLine.find(filterWord.strip())
                if keywordIndex != -1:
                    # print keywordIndex
                    filterTxt += textLine
        # print filterTxt
        self.tabWidget.currentWidget().setText(_translate('', filterTxt, None))

    def saveKeyWord(self):
        filterStr = self.filterLineEdit.text()
        if not filterStr:
            return
        filterFile = QtCore.QFile(self.filterConfigFilePath)
        if not filterFile.open(QtCore.QFile.ReadWrite):
            filterFile.close()
            return
        oldTxt = QtCore.QTextStream(filterFile)
        oldTxt.setCodec('UTF-8')
        # 注意readAll() 读取一次之后，就不能再重复读了，后面重复读取不到数据
        allFilter = str(oldTxt.readAll())
        if allFilter:
            allFilterList = allFilter.split('#@$')
            for oneFilter in allFilterList:
                if oneFilter == str(filterStr):
                    return
            # 加入分隔符
            oldTxt << '#@$'
        # << 写入操作
        oldTxt << _translate('', filterStr, None)
        oldTxt.flush()
        filterFile.close()

    def loadKeyWord(self):
        filterFile = QtCore.QFile(self.filterConfigFilePath)
        if not filterFile.open(QtCore.QFile.ReadOnly):
            filterFile.close()
            return
        oldTxt = QtCore.QTextStream(filterFile)
        oldTxt.setCodec('UTF-8')
        allFilter = str(oldTxt.readAll())
        allFilterList = allFilter.split('#@$')
        self.showFilterDialog(allFilterList)

    def showFilterDialog(self, filterList):
        if not filterList:
            return
        filterDialog = QtGui.QDialog()
        filterDialog.setWindowTitle(u'过滤条件')
        filterDialog.resize(220, 350)
        filterLayout = QtGui.QGridLayout()
        self.filterListWidget = QtGui.QListWidget()
        listItemIndex = 0
        for filterStr in filterList:
            # listItem = QtGui.QListWidgetItem(_translate('', filterStr, None))
            # listItem.setIcon(QtGui.QIcon('img/delete.png'))
            if not filterStr:
                continue
            listItem = QtGui.QListWidgetItem()
            customListItemWidget = CustomFilterItemWidget()
            customListItemWidget.setItemText(_translate('', filterStr, None))
            customListItemWidget.setItemIcon(resource_path('img/delete.png'))
            customListItemWidget.setItemIndex(listItemIndex)
            listItem.setSizeHint(customListItemWidget.sizeHint())
            listItemIndex += 1
            customListItemWidget.connect(customListItemWidget, QtCore.SIGNAL('deleteItem(int)'), self.filterItemDeleteClick)

            self.filterListWidget.addItem(listItem)
            self.filterListWidget.setItemWidget(listItem, customListItemWidget)

        filterLayout.addWidget(self.filterListWidget)
        filterDialog.setLayout(filterLayout)
        # itemDoubleClicked signal
        self.filterListWidget.connect(self.filterListWidget, QtCore.SIGNAL('itemDoubleClicked(QListWidgetItem *)'),
                                      self.filterItemDoubleClick)
        filterDialog.exec_()

    def filterItemDoubleClick(self, listWidgetItem):
        # 获取到自定义的 widget, 先获取 QListWidget 在获取他的 itemWidget
        customWidget = self.filterListWidget.itemWidget(listWidgetItem)
        # print customWidget.getItemText()
        selectTxt = str(customWidget.getItemText()).strip()
        filterTxt = str(self.filterLineEdit.text()).strip()
        if not filterTxt:
            self.filterLineEdit.setText(_translate('', selectTxt, None))
        else:
            filterList = filterTxt.split('|')
            for onFilter in filterList:
                onFilter = onFilter.strip()
                if onFilter == selectTxt:
                    return
            filterList.append(selectTxt)
            filterStr = "|".join(filterList)
            self.filterLineEdit.setText(_translate('', filterStr, None))

    def filterItemDeleteClick(self, index):
        filterCount = self.filterListWidget.count()
        if index > filterCount:
            return
        customWidget = self.filterListWidget.itemWidget(self.filterListWidget.item(index))
        self.deleteFilterOnFile(customWidget.getItemText())
        self.filterListWidget.takeItem(index)
        # 修正index
        for x in range(0, filterCount):
            x = int(x)
            if x >= index:
                listItem = self.filterListWidget.item(x)
                customWidget = self.filterListWidget.itemWidget(listItem)
                if customWidget:
                    itemIndex = int(customWidget.getItemIndex()) - 1
                    customWidget.setItemIndex(itemIndex)

    def deleteFilterOnFile(self, text):
        if not text:
            return
        filterFile = QtCore.QFile(self.filterConfigFilePath)
        if not filterFile.open(QtCore.QFile.ReadWrite):
            filterFile.close()
            return
        oldTxt = QtCore.QTextStream(filterFile)
        oldTxt.setCodec('UTF-8')
        allFilter = str(oldTxt.readAll())
        allFilterList = allFilter.split('#@$')
        for oneFilter in allFilterList:
            if oneFilter == str(text):
                allFilterList.remove(oneFilter)

        filterFile.resize(0)
        filterStr = '#@$'.join(allFilterList)
        if not filterStr:
            return
        oldTxt << _translate('', filterStr, None)
        oldTxt.flush()
        filterFile.close()


class CustomFilterItemWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        hItemBoxLayout = QtGui.QHBoxLayout()
        self.itemText = QtGui.QLabel()
        self.itemIconBtn = QtGui.QPushButton()
        self.itemIndex = 0
        hItemBoxLayout.addWidget(self.itemText)
        hItemBoxLayout.addWidget(self.itemIconBtn)

        self.itemIconBtn.connect(self.itemIconBtn, QtCore.SIGNAL('clicked()'), self.iconClick)

        self.setLayout(hItemBoxLayout)

    def setItemText(self, text):
        self.itemText.setText(text)

    def getItemText(self):
        return self.itemText.text()

    def setItemIndex(self, index):
        self.itemIndex = index

    def getItemIndex(self):
        return self.itemIndex

    def setItemIcon(self, imgPath):
        iconPixmap = QtGui.QPixmap(imgPath)
        self.itemIconBtn.setIcon(QtGui.QIcon(iconPixmap))
        # setFixedSize
        self.itemIconBtn.setIconSize(iconPixmap.rect().size())
        self.itemIconBtn.setFixedSize(iconPixmap.rect().size())

    def iconClick(self):
        self.emit(QtCore.SIGNAL('deleteItem(int)'), self.getItemIndex())

    def deleteItem(self, itemIndex):
        return


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
