#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2017/12/1
Desc  : pyqt4 study
"""

from PyQt4 import QtGui
from PyQt4 import QtCore

import sys

class Icon(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.resize(500, 250)
        self.setWindowTitle('Icon')
        self.setWindowIcon(QtGui.QIcon('img/icon.png'))

class ToolTip(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.resize(500, 250)
        self.setWindowTitle('ToolTip')
        self.setToolTip('This is a <b> QWidget by oyf </b> widget')
        QtGui.QToolTip.setFont(QtGui.QFont('OldEnglish', 10))

class QuitButton(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.resize(500, 250)
        self.setWindowTitle('QuitButton')

        quitBtn = QtGui.QPushButton('Close', self)
        # quitBtn 大小自适应
        quitBtn.resize(quitBtn.sizeHint())
        # 按钮位置
        quitBtn.move(10, 10)
        # 信号槽
        self.connect(quitBtn, QtCore.SIGNAL('clicked()'), QtGui.qApp, QtCore.SLOT('quit()'))

class MessageBox(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.resize(500, 250)
        self.setWindowTitle('MessageBox')

    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message', 'Are you sure to quit?', QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

class Center(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)

        self.resize(500, 250)
        self.setWindowTitle('center')
        self.center()

    def center(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        print 'screen = %s , size = %s' %(screen, size)
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

class StatusBar(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)

        self.resize(500, 250)
        self.setWindowTitle('statusbar')
        self.statusBar().showMessage('Ready')

class MenuBar(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)

        self.resize(500, 250)
        self.setWindowTitle('MenuBar')

        exitAction = QtGui.QAction(QtGui.QIcon('img/icon.png'), 'Exit this', self)
        exitAction.setShortcut('Ctrl+Q')
        # 结合 statusBar ，在statusBar 上显示提示 'Exit application'
        exitAction.setStatusTip('Exit application')
        exitAction.connect(exitAction, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))

        exitAction2 = QtGui.QAction(QtGui.QIcon('img/icon.png'), 'Exit this22', self)
        exitAction2.setShortcut('Ctrl+Q')
        # 结合 statusBar ，在statusBar 上显示提示 'Exit application'
        exitAction2.setStatusTip('Exit application22')
        exitAction2.connect(exitAction2, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))

        self.statusBar()
        mBar = self.menuBar()
        file = mBar.addMenu('&File')
        file.addAction(exitAction)
        file.addAction(exitAction2)

class ToolBar(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)

        self.resize(500, 250)
        self.setWindowTitle('toolBar')

        exitAction = QtGui.QAction(QtGui.QIcon('img/icon.png'), 'Exit go', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.connect(exitAction, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))

        toolBar = self.addToolBar('Go Exit')
        toolBar.addAction(exitAction)

class ChapterOne(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self)

        self.resize(500, 250)
        self.setWindowTitle('ChapterOne')

        self.setStatusTip('First chapter')
        self.statusBar()

        textEdit = QtGui.QTextEdit()
        self.setCentralWidget(textEdit)

        exitAction = QtGui.QAction(QtGui.QIcon('img/icon.png'), 'Exit Action', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('exit status tip')

        self.connect(exitAction, QtCore.SIGNAL('triggered()'), QtGui.qApp, QtCore.SLOT('quit()'))

        menuB = self.menuBar()
        file = menuB.addMenu('&File')
        file.addAction(exitAction)

        clearTxtAction = QtGui.QAction(QtGui.QIcon('img/icon.png'), 'clear txt', self)
        clearTxtAction.setShortcut('Ctrl+C')
        clearTxtAction.setStatusTip('clear text tip')

        self.connect(clearTxtAction, QtCore.SIGNAL('triggered()'), textEdit, QtCore.SLOT('clear()'))

        toolBar = self.addToolBar('clear ToolBar')
        toolBar.addAction(clearTxtAction)


class Absolute(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)

        self.resize(500, 250)
        self.setWindowTitle('absolute')
        label = QtGui.QLabel('Couldn\`t', self)
        label.move(15, 10)
        label = QtGui.QLabel('care', self)
        label.move(35, 40)
        label = QtGui.QLabel('less', self)
        label.move(55, 65)
        label = QtGui.QLabel('And', self)
        label.move(115, 65)
        label = QtGui.QLabel('then', self)
        label.move(135, 45)
        label = QtGui.QLabel('you', self)
        label.move(115, 25)
        label = QtGui.QLabel('kissed', self)
        label.move(145, 10)
        label = QtGui.QLabel('me', self)
        label.move(215, 10)

class BoxLayout(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)

        self.resize(500, 250)
        self.setWindowTitle('BoxLayout')

        ok = QtGui.QPushButton('OK')
        cancel = QtGui.QPushButton('cancel')

        hbox = QtGui.QHBoxLayout()
        # 伸缩间隔元素
        hbox.addStretch(1)
        hbox.addWidget(ok)
        hbox.addWidget(cancel)

        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        # 设置窗口主布局
        self.setLayout(vbox)


class GridLayout(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)

        self.resize(500, 250)
        self.setWindowTitle('GridLayout')

        names = ['Cls', 'Bck', ' ' , 'Close', '7', '8', '9', '/', '4', '5', '6', '*', '1', '2', '3', '-', '0', '.', '=', '+']
        grid = QtGui.QGridLayout()
        j = 0
        pos = [(0,0), (0,1), (0,2), (0,3),
               (1, 0), (1, 1), (1, 2), (1, 3),
               (2, 0), (2, 1), (2, 2), (2, 3),
               (3, 0), (3, 1), (3, 2), (3, 3),
               (4, 0), (4, 1), (4, 2), (4, 3)]
        for i in names:
            button = QtGui.QPushButton(i)
            if j == 2:
                grid.addWidget(QtGui.QLabel(''), 0, 2)
            else:
                # pos[j][0] 行号， pos[j][1] 列号. pos[j] 表示选择pos的元素，比如： pos[1] = (0, 1).
                #  然后 pos[j][1] 表示选择内部集合(0, 1)的第2位。 如 pos[3][1] = 3
                # print 'name = %s , x = %s , y = %s' %(i, pos[j][0], pos[j][1])
                grid.addWidget(button, pos[j][0], pos[j][1])
            j = j + 1

        self.setLayout(grid)


class GridLayout2(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)

        self.resize(500, 250)
        self.setWindowTitle('gridLayout2')

        title = QtGui.QLabel('title')
        author = QtGui.QLabel('author')
        review = QtGui.QLabel('review')

        titleEdit = QtGui.QLineEdit()
        authorEdit = QtGui.QLineEdit()
        reviewEdit = QtGui.QLineEdit()

        grid = QtGui.QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)

        grid.addWidget(author, 2, 0)
        grid.addWidget(authorEdit, 2, 1)

        grid.addWidget(review, 3, 0)
        # 设置行列跨度，行跨度：5； 列跨度：10
        grid.addWidget(reviewEdit, 3, 1, 5, 10)

        self.setLayout(grid)


class SigSlot(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)

        self.resize(500, 250)
        self.setWindowTitle('SigSlot')

        lcd = QtGui.QLCDNumber(self)
        slider = QtGui.QSlider(QtCore.Qt.Horizontal, self)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(lcd)
        vbox.addWidget(slider)

        self.setLayout(vbox)
        # connect 参数： 信号的发送者对象， 要发射的信号(valueChange 信号)， 信号的接收者对象， 对信号做出响应的槽函数(display 方法)
        self.connect(slider, QtCore.SIGNAL('valueChanged(int)'), lcd, QtCore.SLOT('display(int)'))


class Escape(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)

        self.resize(500, 250)
        self.setWindowTitle('Escape')

        self.connect(self, QtCore.SIGNAL('closeEmitApp()'), QtCore.SLOT('close()'))

    # 重写事件处理函数
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()


class Emit(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)

        self.resize(500, 250)
        self.setWindowTitle('emit')

        # 创建一个 closeEmitApp 信号
        self.connect(self, QtCore.SIGNAL('closeEmitApp()'), QtCore.SLOT('close()'))

    def mousePressEvent(self, event):
        # 点击鼠标将发送该信号
        self.emit(QtCore.SIGNAL('closeEmitApp()'))


class InputDialog(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)

        self.resize(500, 250)
        self.setWindowTitle('InputDialog')

        self.button = QtGui.QPushButton('Dialog', self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.button.move(20, 20)
        # 这里的槽函数为 self.dialog. (信号槽简写版)，请注意这里这里没有括号()。 否则会出错(直接调出showDialog函数了，导致异常)
        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.showDialog)
        self.setFocus()

        self.label = QtGui.QLineEdit(self)
        self.label.move(130, 22)

    def showDialog(self):
        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter your name:')
        if ok:
            self.label.setText(unicode(text))


class ColorDialog(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)

        self.resize(500, 250)
        self.setWindowTitle('ColorDialog')

        color = QtGui.QColor(0, 0, 0)

        self.button = QtGui.QPushButton('Dialog', self)
        self.button.setFocusPolicy(QtCore.Qt.NoFocus)
        self.move(20, 20)

        self.connect(self.button, QtCore.SIGNAL('clicked()'), self.showDialog)
        self.setFocus()

        self.widget = QtGui.QWidget(self)
        self.widget.setStyleSheet('QWidget {background-color: %s}' %color.name())
        self.widget.setGeometry(130, 22, 100, 100)

    def showDialog(self):
        col = QtGui.QColorDialog.getColor()
        if col.isValid():
            self.widget.setStyleSheet('QWidget {background-color: %s}' %col.name())


class FontDialog(QtGui.QWidget):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self.resize(500, 250)
        self.setWindowTitle('FontDialog')

        hbox = QtGui.QHBoxLayout()
        button = QtGui.QPushButton('Dialog', self)
        button.setFocusPolicy(QtCore.Qt.NoFocus)
        button.move(20, 20)

        hbox.addWidget(button)
        self.connect(button, QtCore.SIGNAL('clicked()'), self.showDialog)

        self.label = QtGui.QLabel('Knowledge only matters', self)
        self.label.move(130, 20)

        hbox.addWidget(self.label, 1)
        self.setLayout(hbox)

    def showDialog(self):
        font, ok = QtGui.QFontDialog.getFont()
        if ok:
            self.label.setFont(font)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    # label = QtGui.QLabel("<center>Hello World with PyQt5!</center>")
    # label.resize(200, 50)
    # label.show()
    # sys.exit(app.exec_())
    # app = QtGui.QApplication(sys.argv)
    # widget = QtGui.QWidget()
    # widget.resize(500, 250)
    # icon = QtGui.QIcon('img/icon.png')
    # widget.setWindowIcon(icon)
    # widget.setGeometry(500, 200, 250, 250)
    # widget.setWindowTitle('Hello')
    # widget.show()

    # 加载 Icon
    # icon = Icon()
    # icon.show()

    # 显示toolTip 提示语
    # toolTip = ToolTip()
    # toolTip.show()

    # 信号槽
    # qb = QuitButton()
    # qb.show()

    # MessageBox 提示窗
    # mb = MessageBox()
    # mb.show()

    # 定位桌面中间
    # center = Center()
    # center.show()

    # statusBar
    # statusBar = StatusBar()
    # statusBar.show()

    # menuBar
    # menuBar = MenuBar()
    # menuBar.show()

    # toolBar
    # toolBar = ToolBar()
    # toolBar.show()

    # 第一章综合
    # chapterOne = ChapterOne()
    # chapterOne.show()

    # 绝对布局
    # ab = Absolute()
    # ab.show()

    # Box 布局
    # boxLayout = BoxLayout()
    # boxLayout.show()

    # 网格布局
    # gridLayout = GridLayout()
    # gridLayout.show()

    # gridLayout2 = GridLayout2()
    # gridLayout2.show()

    # 信号槽
    # sigSlot = SigSlot()
    # sigSlot.show()

    # 重写事件处理函数
    # escape = Escape()
    # escape.show()

    # 手动发射信号
    # emit = Emit()
    # emit.show()

    # input dialog
    # inputDialog = InputDialog()
    # inputDialog.show()

    # color dialog
    # colorDialog = ColorDialog()
    # colorDialog.show()

    # font dialog
    fontDialog = FontDialog()
    fontDialog.show()

    sys.exit(app.exec_())