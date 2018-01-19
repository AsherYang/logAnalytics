#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/1/3
Desc  : 运行系统 cmd 命令
"""

import subprocess

copyXtcSystemLogPath = r"D:\xtc_resource\4g\XTCLog_TOOL\Logs-CopyToPC.bat"
copyXtcLauncherLogPath = r'D:\xtc_resource\4g\XTCLog_TOOL\Logs-CopyToPC_Launcher.bat'


class RunCopyXTCLogCmd:
    def __init__(self):
        pass

    # 这种方法直接调用，不输出结果
    # def run(self, path):
    #     return subprocess.call(path, shell=True)

    # 该种方法可以获取到终端输出结果
    # 通过 callback 把 msg 传递出去。
    def run(self, path, callback):
        process = subprocess.Popen(path, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        while process.poll() is None:
            line = process.stdout.readline()
            line = line.strip()
            if line:
                # print "out put = ", format(line)
                callback(format(line))
        if process.returncode == 0:
            # print 'sub process success.'
            callback('copy log success.')
        else:
            # print 'sub process fail.'
            callback('copy log fail.')
        return process
