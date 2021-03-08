
import inspect
import os
import pandas as pd
from pandas_datareader import data as pdr
import random
import matplotlib.pyplot as plt
class CompuTradeEngine():
    """
    CompuTradeEngine helps you reliabley backtest your trading algorithms faster than ever.
    
        Parameters:
            backtest (bool): CompuTradeEngine will backtest your algorithm.
            build    (bool): CompuTradeEngine will build you algorithm in python and output it to a build directory in your current working directory.

    """
    from ._buildPython import BuildPythonFile

    from ._algorithm import algorithm

    from ._sma import sma

    from ._ema import ema

    def __init__(self, backtest=True, build=False):
        self.constuctors()

        # next block gets the callee's working directory
        frame_info = inspect.stack()[1]
        filepath = frame_info[1]
        filename=filepath
        del frame_info
        filepath = os.path.abspath(filepath)
        filepath = filepath.replace(f'/{filename}', '')
        self.path = filepath

        self.backtest = backtest
        self.build = build

    def constuctors(self):
        self.algorithmFunc = None
        self.interval = 'd'
        self.position = False
        self.MAXperiod = 0

    def backtest_algorithm(self):
        symbols = ['AAPL', 'SPY']
        for symbol in symbols:
            self.index=0
            self.data = pdr.get_data_yahoo(symbols=symbol, interval=self.interval) # iterates over symbols by symbol to backtest algorithm on symbol data
            self.close = self.data['Close']
            for index, rows in self.data.iterrows():
                self.algo(self)


                self.index+=1
            print(self.data.head())
            print(self.data['ema_10'][-20: -1])
            plt.plot(self.data['Close'])
            plt.plot(self.data['sma_10'])
            plt.plot(self.data['ema_10'])
            plt.show()
            # print(self.data.loc[:, 'Close'].rolling(window=10).mean())
            # print(self.data.iloc[:, 1].rolling(window=4).mean())
            # print(self.data['Close'][-4:-1].max())

    def buy(self):
        if not self.position:
            self.position = True
            print('buy')
    def sell(self):
        if self.position:
            self.position = False

    def config(self, period='15min'):
        self.period = period

