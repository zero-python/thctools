#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Author: zero
Email: 13256937698@163.com
Date: 2018-09-29
"""
from TechnicalIndex.base import EMAEventWindow
from TechnicalIndex.common import DataSeries


class MACD(DataSeries):

    def __init__(self, data,  fastEMA, slowEMA, signalEMA, maxLen=None):
        assert (fastEMA > 0)
        assert (slowEMA-fastEMA > 0)
        assert (signalEMA > 0)
        super(MACD, self).__init__()
        self.__EMAskip = slowEMA-fastEMA
        self.__fastEMAValue = EMAEventWindow(fastEMA)
        self.__slowEMAValue = EMAEventWindow(slowEMA)
        self.__signalEMAValue = EMAEventWindow(signalEMA)
        self.maxLen = maxLen
        self.data = []
        data.event.register(self.__oneNewValue)

    def __oneNewValue(self, DataSeries, datetime, value):

        macd = {}
        self.__slowEMAValue.oneNewValue(value)
        self.__fastEMAValue.oneNewValue(value)
        macd['EMA12'] = self.__fastEMAValue.getValue()
        macd['EMA26'] = self.__slowEMAValue.getValue()
        macd['DIF'] = macd['EMA12'] - macd['EMA26']
        self.__signalEMAValue.oneNewValue(macd['DIF'])
        macd['DEA'] = self.__signalEMAValue.getValue()
        macd['MACD'] = (macd['DIF'] - macd['DEA'])*2
        macd['date'] = datetime
        self.data.append(macd)

    def oneLastValue(self, macd_dict):

        self.__fastEMAValue.onLastValue(macd_dict['EMA12'])
        self.__slowEMAValue.onLastValue(macd_dict['EMA26'])
        self.__signalEMAValue.onLastValue(macd_dict['DEA'])

class MacdManger:

    def __init__(self, close_value, last_macd=None, fastEMA=12, slowEMA=26, signalEMA=9):
        self.__last_macd = last_macd
        self.__close_value = close_value
        self.__fastEMA = fastEMA
        self.__slowEMA = slowEMA
        self.__signalEMA = signalEMA

    def main(self):
        data = DataSeries()
        macds = MACD(data, fastEMA=self.__fastEMA, slowEMA=self.__slowEMA, signalEMA=self.__signalEMA)
        if self.__last_macd:
            macds.oneLastValue(self.__last_macd)
        for key, value in self.__close_value:
            data.appendWithDateTime(key, float(value))
        return macds.data