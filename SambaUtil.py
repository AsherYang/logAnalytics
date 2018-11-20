#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/11/20
Desc  : 访问 samba 服务器，操作共享文件
"""

from smb.SMBConnection import SMBConnection

REMOTE_SMB_IP = "172.28.1.99"
REMOTE_SMB_PORT = 139
USER_NAME = "oyf"
USER_PWD = "oyf"

MY_NAME = "anyname"
REMOTE_SMB_NAME = ""

OYF_SMB_DIR = '\\新共享盘（文件中转，不长期保存）\\oyf欧阳帆'


class SambaUtil:
    def __init__(self, smb_ip, smb_port, user_name, user_pwd):
        self.smb_ip = smb_ip
        self.smb_port = smb_port
        self.user_name = user_name
        self.user_pwd = user_pwd
        self.my_name = MY_NAME
        self.remote_name = REMOTE_SMB_NAME
        self.conn = SMBConnection(self.user_name, self.user_pwd, self.my_name, self.remote_name, use_ntlm_v2=True)

    def connect(self):
        assert self.conn.connect(self.smb_ip, self.smb_port)

    def close(self):
        self.conn.close()

    def listDir(self, service_name='oyf', path='/work_src/gitlab'):
        shareList = self.conn.listShares()
        for list in shareList:
            print list.name
        files = self.conn.listPath(service_name, path)
        for file in files:
            print file.filename


if __name__ == '__main__':
    sambaUtil = SambaUtil(REMOTE_SMB_IP, REMOTE_SMB_PORT, USER_NAME, USER_PWD)
    sambaUtil.connect()
    sambaUtil.listDir(service_name='oyf', path='/work_src/gitlab')
    sambaUtil.close()
