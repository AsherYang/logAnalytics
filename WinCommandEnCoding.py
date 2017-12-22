#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2017/12/21
Desc  : 处理 window 在python 2.7 时，传递的参数 sys.argv 的编码问题

https://github.com/pallets/click/blob/acc1e170b79ad4be8986dce183ff327922c126db/click/_compat.py
https://stackoverflow.com/questions/34821806/python-sys-argv-special-symbol-%E2%82%AC-%C2%A2-%E2%82%AA-etc
"""

import os
import sys

PY2 = sys.version_info[0] == 2
WIN = sys.platform.startswith('win')


def getOsArgv():
    # On Python 3 or non windows environments, we just return the args
    #  as they are.
    if not PY2 or os.name != 'nt':
        return sys.argv

    from ctypes import WINFUNCTYPE, windll, POINTER, byref, c_int
    from ctypes.wintypes import LPWSTR, LPCWSTR

    GetCommandLineW = WINFUNCTYPE(LPWSTR)(('GetCommandLineW', windll.kernel32))
    CommandLineToArgvW = WINFUNCTYPE(POINTER(LPWSTR), LPCWSTR, POINTER(c_int))(("CommandLineToArgvW", windll.shell32))

    argc = c_int(0)
    argv_unicode = CommandLineToArgvW(GetCommandLineW(), byref(argc))
    argv = [argv_unicode[i] for i in range(0, argc.value)]

    return argv
