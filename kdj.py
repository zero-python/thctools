#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
Author: zero
Email: 13256937698@163.com
Date: 2018-09-19
"""

from TechnicalIndex.base import KDJEvenWindow, RSVEvenWindows
from TechnicalIndex.common import DataSeries
import pandas as pd


class KDJ(DataSeries):
    def __init__(self, data, N=9, M1=3, M2=3, max_len=None):
        super(KDJ, self).__init__()
        self.skip = N
        self.KValue = KDJEvenWindow(M1)
        self.DValue = KDJEvenWindow(M2)
        self.RsvValue = RSVEvenWindows(N)
        self.data = []
        data.event.register(self.__oneNewValue)

    def __oneNewValue(self, DataSeries, datetime, value):

        K = 0
        D = 0
        J = 0
        RSV = 0
        KDJ = {}
        self.RsvValue.oneNewValue(value)
        RSV = self.RsvValue.getValue()

        if self.RsvValue.windowfull():
            self.KValue.oneNewValue(RSV)
            K = self.KValue.getValue()
            self.DValue.oneNewValue(K)
            D = self.DValue.getValue()
            J = 3*K - 2*D

        KDJ = {'K': K, 'D': D, 'J': J, 'RSV': RSV, 'date': datetime}
        self.data.append(KDJ)

    def oneLastValue(self, kdj_dict):
        self.RsvValue.oneLastValue(kdj_dict['hlc_list'])

        self.KValue.oneLastValue(kdj_dict['k_list'])
        self.DValue.oneLastValue(kdj_dict['d_list'])


class KDJManger:

    def __init__(self, close_value, last_kdj=None, N=9, M1=3, M2=3):
        self.__last_kdj = last_kdj
        self.__close_value = close_value
        self.__N = N
        self.__M1 = M1
        self.__M2 = M2

    def main(self):
        data = DataSeries()
        kdjs = KDJ(data, N=9, M1=3, M2=3)
        if self.__last_kdj:
            kdjs.oneLastValue(self.__last_kdj)
        for info_dict in self.__close_value:
            value_time = info_dict['date']
            value_list = [float(info_dict['close']), float(info_dict['low']), float(info_dict['high'])]
            data.appendWithDateTime(value_time, value_list)
        return pd.DataFrame(kdjs.data)

