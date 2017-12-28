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

# prog_path = r'D:\python_demo\qt5\logAnalytics\dist\LogAnalytics.exe'
# print os.path.realpath(__file__)
# print os.path.dirname(os.path.realpath(__file__))
prog_name = 'LogAnalytics.exe'


# 注册LogAnalytics 程序到注册表，用于右键运行方式
class RegisterLogAnalyticsWinKey:
    def __init__(self, programPath):
        self.prog_path = programPath

    def register(self):
        key = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Classes\*\shell')
        # print key

        newKey = _winreg.CreateKeyEx(key, 'LogAnalytics', 0, KEY_ALL_ACCESS)
        subKey = _winreg.OpenKey(_winreg.HKEY_LOCAL_MACHINE, r'SOFTWARE\Classes\*\shell\LogAnalytics')
        # newSubKey = _winreg.CreateKey(subKey, "command")

        # _winreg.SetValue(newSubKey, "(Default)", 1, '"' + prog_path + '"' + ' "%1"')
        _winreg.SetValue(subKey, 'command', _winreg.REG_SZ, '"' + self.prog_path + '"' + ' "%1"')

        # value = _winreg.QueryValue(subKey, 'command').split('"')[1]
        # value2 = _winreg.QueryInfoKey(subKey)

        _winreg.CloseKey(key)
        _winreg.CloseKey(subKey)


# 注册cmd 命令行到注册表，用于右键运行方式，不用cd 到对应文件夹
# http://blog.csdn.net/rchm8519/article/details/47991419
class RegisterCmdWinKey:
    def __init__(self):
        pass

    # 只在 Folder 上面才会出现的右键选项。不同于LogAnalytics 右键
    def register(self):
        key = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, r'Folder\shell')
        newKey = _winreg.CreateKeyEx(key, 'cmdPrompt', 0, KEY_ALL_ACCESS)
        subKey = _winreg.OpenKey(_winreg.HKEY_CLASSES_ROOT, r'Folder\shell\cmdPrompt')
        _winreg.SetValue(subKey, 'command', _winreg.REG_SZ, 'C:\Windows\system32\cmd.exe cd' + ' "%1"')
        _winreg.CloseKey(key)
        _winreg.CloseKey(subKey)


if __name__ == "__main__":
    programPath = os.path.join(os.path.dirname(os.path.realpath(__file__)), prog_name)
    regWinKey = RegisterLogAnalyticsWinKey(programPath)
    regWinKey.register()
