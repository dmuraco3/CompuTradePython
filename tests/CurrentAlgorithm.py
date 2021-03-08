from TestCompuTrade import CompuTradeEngine
import random

CompuTradeEngine = CompuTradeEngine()

CompuTradeEngine.config()


@CompuTradeEngine.algorithm
def algo():
    self.sma(10)
    self.sma(30)
    self.ema(10)
    # print(self.sma(10))
    


