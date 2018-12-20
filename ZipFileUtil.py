#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/12/20
Desc  : 文件压缩工具
"""

import zipfile
import tarfile
import FileUtil
from EncodeUtil import _translate, _translateUtf8


class ZipFileUtil:

    def __init__(self, call_back=None):
        self.call_back = call_back

    """
    解压缩
    """
    def recursiveUnZipFile(self, src_dir):
        if not src_dir:
            self.doCallBack(u'请输入需要解压缩的路径')
            return
        allZipFileList = FileUtil.getAllFilesByExt(src_dir, 'zip')
        allGzFileList = FileUtil.getAllFilesByExt(src_dir, 'gz')
        # print '--->src_dir:%s allGzFileList:%s ' % (src_dir, allGzFileList)
        if not allZipFileList and not allGzFileList:
            logStr = u'在目录 ' + _translateUtf8(src_dir) + u' 及子目录下未找到 zip 文件'
            self.doCallBack(logStr)
            return
        for file_path in allZipFileList:
            log_txt = u'正在解压文件: ' + _translateUtf8(file_path)
            self.doCallBack(log_txt)
            # print str(_translateUtf8(file_path))
            dest_dir = _translateUtf8(FileUtil.getFilePathWithName(file_path))
            zip_ref = zipfile.ZipFile(str(file_path), 'r')
            # FileUtil.mkdirNotExist(str(dest_dir)) # zipfile 会自动创建
            zip_ref.extractall(unicode(dest_dir))
            zip_ref.close()
            self.recursiveUnZipFile(dest_dir)
        for file_path in allGzFileList:
            log_txt = u'正在解压文件: ' + _translateUtf8(file_path)
            self.doCallBack(log_txt)
            dest_dir = str(_translateUtf8(FileUtil.getFilePathWithName(file_path)))
            if FileUtil.getFileExt(dest_dir).find('tar') != -1:
                dest_dir = str(_translateUtf8(FileUtil.getFilePathWithName(dest_dir)))
                # print '----dest_dir: ', dest_dir
            tarf = tarfile.open(file_path)
            tarf.extractall(unicode(dest_dir))
            tarf.close()
            self.recursiveUnZipFile(dest_dir)

    def doCallBack(self, msg):
        if self.call_back:
            self.call_back(msg)
