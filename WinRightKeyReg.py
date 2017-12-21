#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2017/12/20
Desc  : 为程序添加 window 右键快捷键打开方式
参考资料： http://www.cnblogs.com/russellluo/archive/2011/11/25/2263881.html
http://www.jb51.net/article/102474.htm (主要)
同时可以对照 cmd-> regedit 查看注册表情况
"""

import _winreg
import os

from _winreg import KEY_ALL_ACCESS

prog_name = u'LogAnalytics'
# prog_path = r'D:\python_demo\qt5\logAnalytics\dist\LogAnalytics.exe'
print os.path.realpath(__file__)
print os.path.dirname(os.path.realpath(__file__))

class registerKey():
    def __init__(self, programPath):
        self.prog_path = programPath

    def register(self):
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Classes\*\shell')
        print key

        newKey = _winreg.CreateKeyEx(key, 'LogAnalytics', 0, KEY_ALL_ACCESS)
        subKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Classes\*\shell\LogAnalytics')
        newSubKey = _winreg.CreateKey(subKey, "command")

        # _winreg.SetValue(newSubKey, "(Default)", 1, '"' + prog_path + '"' + ' "%1"')
        _winreg.SetValue(subKey, 'command', _winreg.REG_SZ, '"' + self.prog_path + '"' + ' "%1"')

        _winreg.CloseKey(key)
        _winreg.CloseKey(subKey)