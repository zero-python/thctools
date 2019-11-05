# -*- coding: utf-8 -*-
"""
Author: zero
Email: 13256937698@163.com
Date: 2019-11-01
"""

from Technical.index.kdj import KDJManger
from Technical.index.ma import MAManger
from Technical.index.macd import MacdManger


class Technical:

    def __init__(self, df):
        self.df = df

    @property
    def macd(self):
        df = self.df.set_index('date')
        close_dict = df['close'].dropna(axis=0).to_dict()
        close_values = sorted(close_dict.items(), key=lambda k: k[0])
        return MacdManger(close_values).main()

    @property
    def ma(self):
        df = self.df.set_index('date')
        close_dict = df['close'].dropna(axis=0).to_dict()
        close_values = sorted(close_dict.items(), key=lambda k: k[0])
        return MAManger(close_values).main()

    @property
    def kdj(self):
        need_columns = ['close', 'low', 'high', 'date']
        pd_list = self.df[need_columns].to_dict(orient='records')
        pd_list = sorted(pd_list, key=lambda k: k['date'], reverse=False)
        return KDJManger(pd_list).main()


