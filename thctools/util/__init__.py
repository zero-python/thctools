#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Author: zero
Email: 13256937698@163.com
Date: 2018-09-19
"""


class WindowEvent(object):
    """作为移动的列表窗口，控制计算的列表溢出"""
    def __init__(self, maxLen):
        self.windowSize = maxLen
        self.__values = NumData(maxLen)
        self.skip = True

    def oneNewValue(self, value):
        """
        添加新增值
        :param value:新增值
        :return:
        """
        if value is not None or not self.skip:
            self.__values.append(value)

    def getValues(self):
        """
        获取所有值
        :return:
        """
        return self.__values.data()

    def windowfull(self):
        """
        判断缓存列表是否塞满
        :return:
        """
        return self.windowSize == len(self.__values)

    def getValueLen(self):
        """
        获取列表长度
        :return:
        """
        return len(self.__values)

    def setValues(self, values):
        """
        列表添加值
        :param values:
        :return:
        """
        for value in values:
            self.__values.append(value)

class NumData(object):
    """列表数据控制"""
    def __init__(self, maxLen, dtype=float):
        self.__values = [None for i in range(maxLen)]
        self.__maxLen = maxLen
        self.__nextPar = 0

    def append(self, value):

        if self.__nextPar < self.__maxLen:

            self.__values[self.__nextPar] = value
            self.__nextPar += 1
        else:
            self.__values[0:-1] = self.__values[1:]
            self.__values[self.__nextPar-1] = value

    def data(self):

        if self.__nextPar < self.__maxLen:
            ret = self.__values[0:self.__nextPar]
        else:
            ret = self.__values
        return ret

    def __len__(self):
        return self.__nextPar

    def __getitem__(self, item):
        return self.data()[item]


