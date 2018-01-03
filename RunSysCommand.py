#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/1/3
Desc  : 运行系统 cmd 命令
"""

import subprocess

copyXtcLogPath = r"D:\xtc_resource\4g\XTCLog_TOOL\Logs-CopyToPC.bat"


class RunCopyXTCLogCmd:
    def __init__(self):
        pass

    def run(self, path):
        return subprocess.call(path, shell=True)
