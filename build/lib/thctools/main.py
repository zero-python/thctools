# -*- coding: utf-8 -*-
"""
Author: zero
Email: 13256937698@163.com
Date: 2019-11-01
"""

from thctools.index.kdj import KDJManger
from thctools.index.ma import MAManger
from thctools.index.macd import MacdManger
import pandas

class Technical:
    """
    基于事件驱动设计模式，实现macd，kdj，rsi，ma等常见股票技术指标的算法。
    为了方便后人便捷使用，减少再造轮子，这里简单分装接口。
    >>> import tushare as ts
    >>> from thctools.main import Technical
    >>> import pandas as pd
    >>> ts.set_token('24c7a5d5b40cd5db779cbc888ba4516d4be3384c0cf897caeaf2415b')
    >>> pro = ts.pro_api()
    >>> df = pro.query('daily', ts_code='603019.SH')
    >>> df = df.rename(columns={'trade_date': 'date'})[['date', 'open', 'high', 'low', 'close']]
    >>> isinstance(df,pd.DataFrame)
    True
    >>> tech_obj = Technical(df)
    >>> ma = tech_obj.ma
    >>> isinstance(ma,pd.DataFrame)
    True
    >>> macd = tech_obj.macd
    >>> isinstance(macd,pd.DataFrame)
    True
    >>> kdj = tech_obj.kdj
    >>> isinstance(kdj, pd.DataFrame)
    True
    """
    def __init__(self, data):
        assert isinstance(data, pandas.DataFrame)
        self.df = data

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


if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)