# -*- coding: utf-8 -*-
"""
Author: zero
Email: 13256937698@163.com
Date: 2019-11-01
"""
import tushare as ts

from thctools import Technical

ts.set_token('24c7a5d5b40cd5db779cbc888ba4516d4be3384c0cf897caeaf2415b')
pro = ts.pro_api()
df = pro.query('daily', ts_code='603019.SH')
df = df.rename(columns={'trade_date': 'date'})[['date', 'open', 'high', 'low', 'close']]
print(df.head(10))
tech_obj = Technical(df)
print(tech_obj.ma.head(10))
print(tech_obj.macd.head(10))
print(tech_obj.kdj.head(10))
