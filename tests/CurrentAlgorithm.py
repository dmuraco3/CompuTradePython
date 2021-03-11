from TestCompuTrade import CompuTradeEngine
import random

CompuTradeEngine = CompuTradeEngine()

CompuTradeEngine.config()


@CompuTradeEngine.algorithm
def algo():
    self.cci()
    self.emv()
    self.roc()
    if self.ema(20) > self.ema(100) and self.ema(50) > self.ema(100):
        self.buy()
    else:
        self.sell()
    # print(self.sma(10))
    


