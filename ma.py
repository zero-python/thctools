#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Author: zero
Email: 13256937698@163.com
Date: 2018-09-24
"""
from TechnicalIndex.base import SMAEventWindow
from TechnicalIndex.common import DataSeries
import pandas as pd

class MA(DataSeries):
    def __init__(self, data, M5=5, M10=10, M20=20,M60=60, maxLen=None):

        super(MA, self).__init__()
        self.__MA5Value = SMAEventWindow(M5)
        self.__MA10Value = SMAEventWindow(M10)
        self.__MA20Value = SMAEventWindow(M20)
        self.__MA60Value = SMAEventWindow(M60)
        self.maxLen = maxLen
        self.data = []
        data.event.register(self.__oneNewValue)

    def __oneNewValue(self, DataSeries, datetime, value):
        m5 = 0
        m10 = 0
        m20 = 0
        m60 = 0
        self.__MA5Value.oneNewValue(value)
        self.__MA10Value.oneNewValue(value)
        self.__MA20Value.oneNewValue(value)
        self.__MA60Value.oneNewValue(value)

        if self.__MA5Value.windowfull():
            m5 = self.__MA5Value.getValue()
        if self.__MA10Value.windowfull():
            m10 = self.__MA10Value.getValue()
        if self.__MA20Value.windowfull():
            m20 = self.__MA20Value.getValue()
        if self.__MA60Value.windowfull():
            m60 = self.__MA60Value.getValue()
        ma_dict = {'MA5': m5, 'MA10': m10, 'MA20': m20, 'MA60': m60, 'date': datetime,}
        self.data.append(ma_dict)

    def oneLastValue(self, ma_dict):

        self.__MA5Value.onLastValue(ma_dict['MA5'], ma_dict['close'][-5:])
        self.__MA10Value.onLastValue(ma_dict['MA10'], ma_dict['close'][-10:])
        self.__MA20Value.onLastValue(ma_dict['MA20'], ma_dict['close'][-20:])
        self.__MA60Value.onLastValue(ma_dict['MA60'], ma_dict['close'])


class MAManger:

    def __init__(self, close_value, last_ma=None, M5=5, M10=10, M20=20, M60=60):
        self.__last_ma = last_ma
        self.__close_value = close_value
        self.__M5 = M5
        self.__M10 = M10
        self.__M20 = M20
        self.__M60 = M60

    def main(self):

        data = DataSeries()
        ma_obj = MA(data, M5=5, M10=10, M20=20, M60=60)
        if self.__last_ma:
            ma_obj.oneLastValue(self.__last_ma)
        for key, value in self.__close_value:
            data.appendWithDateTime(key, float(value))

        return pd.DataFrame(ma_obj.data)

