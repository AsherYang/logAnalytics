#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/11/21
Desc  : 保存 call fail 信息实体bean

self._binderNumber          # 绑定号
self._machineMode           # 机器型号
self._osVersion             # 系统版本
self._failTime              # 异常时间
self._voiceNetworkType      # 通话类型
self._dialMode              # 通话方向
self._causeCode             # 掉话code
self._vendorCauseCode       # 掉话vendor code
self._logText               # 详细 log 信息(信息文本行全部信息)

"""


class CallFailBean:
    def __init__(self):
        self._binderNumber = None
        self._machineMode = None
        self._osVersion = None
        self._failTime = None
        self._voiceNetworkType = None
        self._dialMode = None
        self._causeCode = None
        self._vendorCauseCode = None
        self._logText = None
        pass

    @property
    def binderNumber(self):
        return self._binderNumber

    @binderNumber.setter
    def binderNumber(self, value):
        self._binderNumber = value

    @property
    def machineMode(self):
        return self._machineMode

    @machineMode.setter
    def machineMode(self, value):
        self._machineMode = value

    @property
    def osVersion(self):
        return self._osVersion

    @osVersion.setter
    def osVersion(self, value):
        self._osVersion = value

    @property
    def failTime(self):
        return self._failTime

    @failTime.setter
    def failTime(self, value):
        self._failTime = value

    @property
    def voiceNetworkType(self):
        return self._voiceNetworkType

    @voiceNetworkType.setter
    def voiceNetworkType(self, value):
        self._voiceNetworkType = value

    @property
    def dialMode(self):
        return self._dialMode

    @dialMode.setter
    def dialMode(self, value):
        self._dialMode = value

    @property
    def causeCode(self):
        return self._causeCode

    @causeCode.setter
    def causeCode(self, value):
        self._causeCode = value

    @property
    def vendorCauseCode(self):
        return self._vendorCauseCode

    @vendorCauseCode.setter
    def vendorCauseCode(self, value):
        self._vendorCauseCode = value

    @property
    def logText(self):
        return self._logText

    @logText.setter
    def logText(self, value):
        self._logText = value






