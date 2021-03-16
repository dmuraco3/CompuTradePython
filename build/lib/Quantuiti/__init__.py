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
        self.shares = 0
        self.balance = 1000
        self.trades = []

    def backtest_algorithm(self):
        symbols = ['AAPL', 'GME']
        for symbol in symbols:
            self.index=0
            self.data = pdr.get_data_yahoo(symbols=symbol, interval=self.interval, start='JAN-01-2020' end='DEC-28-2020') # iterates over symbols by symbol to backtest algorithm on symbol data
            self.close = self.data['Close']
            for index, rows in self.data.iterrows():
                self.algo(self)


                self.index+=1

            profit = ( self.data['Close'][-1]*self.shares ) - ( self.trades[-1][1] * self.shares )
            self.balance = profit + ( self.trades[-1][1] * self.shares )
            self.shares = 0

            print(self.data.head())
            plt.plot(self.data['Close'])
            plt.plot(self.data['ema_20'])
            plt.plot(self.data['ema_100'])
            plt.title(symbol)
            print(self.balance, self.shares)
            self.balance = 1000
            self.shares = 0
            plt.show()
            # print(self.data.loc[:, 'Close'].rolling(window=10).mean())
            # print(self.data.iloc[:, 1].rolling(window=4).mean())
            # print(self.data['Close'][-4:-1].max())

    def buy(self):
        if self.shares == 0 and self.balance > 0 :
            print('buy')
            self.shares = self.balance / self.data['Close'][self.index]
            self.balance = 0
            self.trades.append(tuple([self.shares, self.data['Close'][self.index]])) 
    def sell(self):
        if self.shares != 0:
            print('sell', ( self.trades[-1][1] ))
            profit = ( self.data['Close'][self.index]*self.shares ) - ( self.trades[-1][1] * self.shares )
            self.balance = profit + ( self.trades[-1][1] * self.shares )
            self.shares = 0
    def config(self, period='15min'):
        self.period = period