#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Author: AsherYang
Email : ouyangfan1991@gmail.com
Date  : 2018/11/22
Desc  : 基本信息实体 bean
"""


class BaseAttrBean:
    def __init__(self):
        self._binderNumber = None
        self._machineMode = None
        self._osVersion = None

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

    # toString
    def __str__(self):
        return 'binderNumber: %s' % self.binderNumber
