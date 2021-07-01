from datetime import date, timedelta
import numpy as np
import pandas_datareader.data as web


def get_historical_volatility(stock_symbol) -> float:

    # set date range for historical prices
    end_time = date.today()
    start_time = end_time - timedelta(days=30)

    # reformat date range
    end = end_time.strftime('%Y-%m-%d')
    start = start_time.strftime('%Y-%m-%d')

    # get daily stock prices over date range
    prices = web.DataReader(stock_symbol, 'yahoo', start, end)

    # sort dates in descending order
    # prices.sort_index(ascending=False, inplace=True)

    # calculate daily logarithmic return
    prices['returns'] = (np.log(prices.Close /
                                prices.Close.shift(-1)))

    # calculate daily standard deviation of returns
    daily_std = np.std(prices.returns)

    # annualized daily standard deviation
    std = daily_std * 252 ** 0.5
    return std


def get_close_price(stock_symbol: str) -> float:
    today = date.today()
    prices = web.DataReader(stock_symbol, 'yahoo', today, today)
    return prices.Close[0]
