#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Author: zero
Email: 13256937698@163.com
Date: 2018-09-20
"""

from decimal import Decimal, getcontext
from thctools import WindowEvent


class EMAEventWindow(WindowEvent):
    """
    MA 事件驱动的具体实现过程
    """
    def __init__(self, maxLen):
        super(EMAEventWindow, self).__init__(maxLen)
        self.__value = 0
        self.__close = 0
        self.__multiplier = (2.0 / (maxLen + 1))
        self.__lasterFact = (maxLen - 1) / (maxLen + 1)

    def oneNewValue(self, value):
        """
        新增值的计算
        :param value:
        :return:
        """
        super(EMAEventWindow, self).oneNewValue(value)
        if self.getValueLen() == 1:
            self.__value = value
        else:
            self.__value = (self.__value * self.__lasterFact) + (value * self.__multiplier)

    def onLastValue(self, value):
        """
        填充历史数据，增量计算，需要提前填充历史依赖数据
        :param value:
        :return:
        """
        super(EMAEventWindow, self).oneNewValue(value)
        self.__value = value

    def getValue(self):

        value = float(Decimal(str(self.__value)).quantize(Decimal('0.000')))
        return value


class KDJEvenWindow(WindowEvent):
    """
    kdj 事件驱动的具体实现过程
    """
    def __init__(self, maxLen):
        super(KDJEvenWindow, self).__init__(maxLen)
        self.__value = 50
        self.__multiplier = (maxLen-1) / (maxLen)
        self.__lasterFact = 1 / maxLen

    def oneNewValue(self, value):
        """
        新增值，计算具体实现
        """
        self.__value = (self.__value * self.__multiplier) + (value * self.__lasterFact)

    def oneLastValue(self, value):
        """
        填充历史数据
        """
        self.setValues(value)
        self.__value = value[-1]

    def getValue(self):
        value = float(Decimal(str(self.__value)).quantize(Decimal('0.000')))
        return value


class RSVEvenWindows(WindowEvent):
    """rsv 事件驱动的具体实现过程"""

    def __init__(self, maxLen):
        super(RSVEvenWindows, self).__init__(maxLen)
        self.__value = 0

    def oneNewValue(self, value):
        """
        新增值驱动计算
        """
        super(RSVEvenWindows, self).oneNewValue(value)
        if not self.windowfull():
            self.__value = 0
        else:
            values = self.getValues()
            C = values[-1][0]
            L = min([low_list[1] for low_list in values])
            H = max([low_list[2] for low_list in values])
            self.__value = (C-L)/(H-L)*100

    def oneLastValue(self, value):
        """
        填充历史数据
        """
        self.setValues(value)

    def getValue(self):
        value = float(Decimal(str(self.__value)).quantize(Decimal('0.000')))
        return value


class SMAEventWindow(WindowEvent):
    """
    SMA 事件驱动的具体实现过程
    """
    def __init__(self, period):
        assert(period > 0)
        super(SMAEventWindow, self).__init__(period)
        self.__value = None

    def oneNewValue(self, value):
        """
        新增值驱动计算
        """
        firstValue = None
        if len(self.getValues()) > 0:
            firstValue = self.getValues()[0]
            assert(firstValue is not None)

        super(SMAEventWindow, self).oneNewValue(value)
        if value is not None and self.windowfull():
            if self.__value is None:
                self.__value = sum(self.getValues())/self.getValueLen()
            else:
                self.__value = self.__value + value / float(self.getValueLen()) - firstValue / float(self.getValueLen())

    def onLastValue(self, MA, values):
        """
        填充历史数据
        """
        self.__value = MA
        self.setValues(values)

    def getValue(self):
        return self.__value

    def getFirstValue(self):
        """
        获取第一条数据
        """
        return self.getValues()[0]


class RSEventWindow(WindowEvent):
    """RS 事件驱动的具体实现过程"""
    def __init__(self, period):
        assert(period > 0)
        super(RSEventWindow, self).__init__(period)
        self.__value = 0
        self.__prevGain = None
        self.__prevLoss = None
        self.__period = period

    def oneNewValue(self, value):
        """
        新增值驱动计算
        """
        super(RSEventWindow, self).oneNewValue(value)
        if value is not None and self.windowfull():
            if self.__prevGain is None:
                assert (self.__prevLoss is None)
                avgGain, avgLoss = self.avgGainLoss(self.getValues(), 0, len(self.getValues()))
            else:
                assert (self.__prevLoss is not None)
                prevValue = self.getValues()[-2]
                currValue = self.getValues()[-1]
                currGain, currLoss = self.gainLossOne(prevValue, currValue)
                avgGain = (self.__prevGain * (self.__period - 1) + currGain) / float(self.__period)
                avgLoss = (self.__prevLoss * (self.__period - 1) + currLoss) / float(self.__period)
            if avgLoss == 0:
                self.__value = 100
            else:
                rs = avgGain / avgLoss
                self.__value = 100 - 100 / (1 + rs)
            self.__prevGain = avgGain
            self.__prevLoss = avgLoss

    def oneLastValue(self, avgGain, avgLoss, value):
        """
        填充历史数据
        :return:
        """
        self.setValues(value)
        self.__prevLoss = avgLoss
        self.__prevGain = avgGain

    def avgGainLoss(self, values, begin, end):
        rangeLen = end - begin
        if rangeLen < 2:
            return None
        gain = 0
        loss = 0
        for i in range(begin + 1, end):
            currGain, currLoss = self.gainLossOne(values[i - 1], values[i])
            gain += currGain
            loss += currLoss
        return gain / float(rangeLen), loss / float(rangeLen)

    def gainLossOne(self, prevValue, nextValue):
        change = nextValue - prevValue
        gain, loss = 0, abs(change) if change<0 else change, 0
        return gain, loss

    def getValue(self):
        value = self.changeValue(self.__value)
        avgGain = self.changeValue(self.__prevGain)
        avgLoss = self.changeValue(self.__prevLoss)
        return value, avgGain, avgLoss

    def changeValue(self, value):
        if value is None:
            return 0.0000
        else:
            return float(Decimal(str(value)).quantize(Decimal('0.000000')))
