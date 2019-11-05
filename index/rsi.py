#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Author: zero
Email: 13256937698@163.com
Date: 2018-09-29
"""
from Technical.util.base import RSEventWindow
from Technical.util.common import DataSeries


class RSI(DataSeries):
    def __init__(self, data, R6=6, R12=12, R24=24, maxLen=None):
        super(RSI, self).__init__()
        self.__R6Even = RSEventWindow(R6)
        self.__R12Even = RSEventWindow(R12)
        self.__R24Even = RSEventWindow(R24)
        self.data = []
        data.event.register(self.__oneNewValue)

    def __oneNewValue(self, DataSeries, datetime, value):
        self.__R6Even.oneNewValue(value)
        self.__R12Even.oneNewValue(value)
        self.__R24Even.oneNewValue(value)
        RSI6, avgGain6, avgLoss6 = self.__R6Even.getValue()
        RSI12,avgGain12, avgLoss12 = self.__R12Even.getValue()
        RSI24,avgGain24, avgLoss24 = self.__R24Even.getValue()
        rsi_dict = {'RSI6': RSI6, 'RSI12': RSI12, 'RSI24': RSI24,
                    'avgGain6': avgGain6, 'avgGain12': avgGain12, 'avgGain24': avgGain24,
                    'avgLoss6': avgLoss6, 'avgLoss12': avgLoss12, 'avgLoss24': avgLoss24,
                    'date': datetime}

        self.data.append(rsi_dict)

    def oneLastValue(self, rsi_dict):
        last_dict = rsi_dict['last_dict']
        close_list = rsi_dict['close']
        self.__R6Even.oneLastValue(last_dict['avgGain6'], last_dict['avgLoss6'], close_list[-6:])
        self.__R12Even.oneLastValue(last_dict['avgGain12'], last_dict['avgLoss12'], close_list[-12:])
        self.__R24Even.oneLastValue(last_dict['avgGain24'], last_dict['avgLoss24'], close_list)

