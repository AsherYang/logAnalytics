#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/12/6
Desc  : 多进程操作文件
@see https://www.blopig.com/blog/2016/08/processing-large-files-using-python/
"""

import multiprocessing as mp
import os
from EncodeUtil import _translateUtf8


"""
file_name:  操作的文件
process_method：传递该函数，用于回调行数据处理，为空时，表示不进行行数据Job处理
process_call_back：传递该函数，用于接收处理的状态。为空时，表示不关心是否处理完Job任务
"""


class MultiProcessFile:

    STATUS_PROCESSING = 0
    STATUS_PROCESSED = 1

    def __init__(self, fname, cls_instance, status_call_back, process_func, keyword):
        self.fname = fname
        self.clsInstance = cls_instance
        self.statusCallBack = status_call_back
        self.processFunc = process_func
        self.keyword = keyword

    def chunkify(self, size=1024 * 1024):
        fileEnd = os.path.getsize(self.fname)
        with open(self.fname, 'r') as f:
            chunkEnd = f.tell()
            while True:
                chunkStart = chunkEnd
                f.seek(size, 1)
                f.readline()
                chunkEnd = f.tell()
                # print 'chunkStart: %d , chunkEnd - chunkStart: %d ' % (chunkStart, chunkEnd - chunkStart)
                yield chunkStart, chunkEnd - chunkStart
                if chunkEnd > fileEnd:
                    break
            f.close()

    def createAndDoJobs(self):
        if self.statusCallBack:
            self.statusCallBack(self.clsInstance, MultiProcessFile.STATUS_PROCESSING, self.fname, None)
        cpu = mp.cpu_count()-1 if mp.cpu_count() > 1 else 1
        pool = mp.Pool(processes=cpu)
        jobs = []
        for chunkStart, chunkSize in self.chunkify():
            # print '====> chunkStart: %d , chunkSize: %d' % (chunkStart,  chunkSize)
            # self.jobs.append(self.pool.apply_async(self.process_wrapper(chunkStart, chunkSize)))
            # print '---type(process): ', type(cls.process_wrapper)
            # print '---type(process): ', self.processFunc
            # 需要注意传递的格式类型：函数和参数
            jobs.append(pool.apply_async(self.processFunc, (self.fname, chunkStart, chunkSize, self.keyword, )))
        # wait for all jobs to finish
        pool.close()
        pool.join()
        self.doJobsCallBack(jobs)

    def doJobsCallBack(self, jobs):
        if not jobs:
            return
        tasks = []
        for job in jobs:
            if not job:
                continue
            # print '----> job.get(): ', job.get()
            if job.get():
                tasks.append(job.get())
        if tasks and self.statusCallBack:
            self.statusCallBack(self.clsInstance, MultiProcessFile.STATUS_PROCESSED, self.fname, tasks)


# ==============下面方法不属于MultiProcessFile类，否则就无法在多进程中运行(方法与函数的区别) 用于测试=========================

def process_wrapper(fname, chunkStart, chunkSize, *args):
    print '----- process_wrapper PID: ', os.getpid()
    for arg in args:
        print arg
        # for x in arg:
        #     print 'args : ', x
    with open(fname) as f:
        f.seek(chunkStart)
        lines = f.read(chunkSize).splitlines()
        funckLines = []
        for line in lines:
            x = process(line, fname)
            if x:
                funckLines.append(x)
            # # todo
            # if processFunc:
            #     processFunc(line, fname)
        if funckLines:
            return funckLines


# 另外提供子类覆写方法：
# 具体操作，子类通过覆写该方法进行处理行数
# 子类覆写该方法时，可将回调函数process_method 置为None
def process(line, fname):
    filterLines = ""
    textLine = str(_translateUtf8(line))
    print '--> textLine: ', textLine
    textLineLower = textLine.lower()
    keywordIndex = textLineLower.find("reportCallFailLD =")
    if keywordIndex != -1:
        filterLines += textLine
    return filterLines


def doCallBack(cls_instance, status, file, jobs):
    print '----------- doCallBack status: ', status
    # print '----------- doCallBack file: ', file
    print 'jobs: ', jobs
    if jobs:
        for job in jobs:
            if job:
                print 'type(job): ', type(job)

if __name__ == '__main__':
    multiProcessFile = MultiProcessFile("Log.main_sys_2018-11-30 00-00-17.log", None, doCallBack, process_wrapper, '11')
    multiProcessFile.createAndDoJobs()
