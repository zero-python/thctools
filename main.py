# -*- coding: utf-8 -*-
"""
Author: zero
Email: 13256937698@163.com
Date: 2019-11-01
"""

import pandas as pd

from TechnicalIndex.kdj import KDJManger
from TechnicalIndex.ma import MAManger
from TechnicalIndex.macd import MacdManger


class Technical:

    def __init__(self, values):

        self.values = values

    @property
    def macd(self):
        return MacdManger(self.values).main()

    @property
    def ma(self):
        return MAManger(self.values).main()

    @property
    def kdj(self):
        return KDJManger(self.values).main()


