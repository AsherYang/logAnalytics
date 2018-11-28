#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/11/27
Desc  : 通过LOG 日志接口下载日志
"""
import cookielib
import urllib2
import urllib
import json
import HttpUtil


LOGIN_URL = r'http://admin.eebbk.com/webadmin-cas/login'
GET_BY_USER_DO_URL = r'http://172.28.199.58/watchda2/log/getByUser.do'
GET_USER_INFO_BY_IDS_URL = r'http://admin.eebbk.com/webadmin-authority/authority/openapi/getUserInfoByIds'
GET_CHILD_DO_URL = r'http://172.28.199.58/watchda2/log/getChild.do'
USER_NAME = r'20251572'
USER_PWD = r'123456'


class DownloadLogHttp:
    def __init__(self):
        self.cj = cookielib.CookieJar()
        self.handler = urllib2.HTTPCookieProcessor(self.cj)
        self.opener = urllib2.build_opener(self.handler)
        self.userName = USER_NAME
        self.password = USER_PWD
        self.binder_number_list = []
        pass

    def setLoginInfo(self, user_name, password):
        self.userName = user_name
        self.password = password

    def login(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Connection': 'keep-alive',
            'Origin': 'http://admin.eebbk.com',
            'Referer': 'http://admin.eebbk.com/webadmin-cas/login?service=http://172.28.199.58/watchda2/common/index.do',
            'Accept-Language': 'zh-CN,zh;q=0.8',
        }
        values = {
            'service': r'http://172.28.199.58/watchda2/common/index.do'
        }
        # data = urllib.urlencode(values)
        # request = urllib2.Request(url=LOGIN_URL, data=data, headers=headers)
        # response = urllib2.urlopen(request)
        body = HttpUtil.http_post(LOGIN_URL, params=values, header=headers)
        print 'response : ', body
        # response = json.loads(body)
        # print 'response : ', response.code
        pass

    def setBinderNumberList(self, binder_number_list):
        self.binder_number_list = binder_number_list

    # 开始下载LOG
    def downloadLog(self):
        if not self.binder_number_list:
            return
        for binderNumber in self.binder_number_list:
            self.doDownloadSingleLog(binderNumber)

    # 单个LOG下载
    def doDownloadSingleLog(self, binder_number):
        pass

    def getByUserDo(self):
        # 访问getByUserDo 接口
        headers = {
            'Accept': r'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': r'gzip, deflate',
            'Accept-Language': r'zh-CN,zh;q=0.8',
            'Connection': r'keep-alive',
            'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
            'Content-Length': '77',
            'Cookie': 'JSESSIONID=D43445E866934FFA31556F38C614D315; userName=%E6%AC%A7%E9%98%B3%E5%B8%86',
            'Host': r'172.28.199.58',
            'Origin': r'http://172.28.199.58',
            'Referer': r'http://172.28.199.58/watch/index_prod.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        values = {
            'bindNumber': r'amegylwphqjbjiuu',
            'index': 1,
            'size': 15,
            'order': 'desc',
            'orderField': 'create_time'
        }
        # opener = self.opener
        # opener.addheaders = headers
        # data = urllib.urlencode(values)
        # resp = opener.open(GET_BY_USER_DO_URL, data)
        # print '--> resp : ', resp
        body = HttpUtil.http_post(GET_BY_USER_DO_URL, params=values, header=headers)
        print 'response : ', body
        # body = json.loads(body)
        # print 'response message : ', body['message']
        # print 'response data: ', json.loads(body['data'])
        # print 'response code: ', body['code']
        # print 'response : ', response
        # print 'response : ', json.loads(response)
        pass

    def getChildDo(self):
        # 访问getByUserDo 接口
        headers = {
            'Accept': r'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': r'gzip, deflate',
            'Accept-Language': r'zh-CN,zh;q=0.8',
            'Connection': r'keep-alive',
            'Content-Type': r'application/x-www-form-urlencoded; charset=UTF-8',
            'Content-Length': '77',
            'Cookie': 'JSESSIONID=D43445E866934FFA31556F38C614D315; userName=%E6%AC%A7%E9%98%B3%E5%B8%86',
            'Host': r'172.28.199.58',
            'Origin': r'http://172.28.199.58',
            'Referer': r'http://172.28.199.58/watch/index_prod.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        values = {
            'bindNumber': r'amegylwphqjbjiuu',
            'index': 1,
            'size': 15,
            'order': 'desc',
            'orderField': 'create_time'
        }
        # data = urllib.urlencode(values)
        # request = urllib2.Request(url=GET_BY_USER_DO_URL, data=data, headers=headers)
        # response = urllib2.urlopen(request)
        body = HttpUtil.http_post(GET_CHILD_DO_URL, params=values, header=headers)
        print 'response : ', body
        body = json.loads(body)
        print 'response message : ', body['message']
        # print 'response data: ', json.loads(body['data'])
        print 'response code: ', body['code']
        # print 'response : ', response
        # print 'response : ', json.loads(response)
        pass

if __name__ == '__main__':
    dlHttp = DownloadLogHttp()
    # dlHttp.getChildDo()
    # dlHttp.getByUserDo()
    dlHttp.login()
    dlHttp.getByUserDo()
    pass
