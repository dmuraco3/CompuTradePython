import pandas as pd
from pandas_datareader import data as pdr
class main():
    def __init__(self):
        self.backtest()

    def algo(self,place, weiner):
        print("this will show if it worked")
        print("this will ALSOSOSOSOSO show if it worked")
    

    def backtest(self):
        data = pdr.get_data_yahoo(
            tickers = 'SPY AAPL MSFT',

            period = 'max',

            interval = '1d'
        )
if __name__ == "__main__":
    main = main()
    main