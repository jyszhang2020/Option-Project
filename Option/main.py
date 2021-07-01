"""
This module contains black-scholes calculations of prices and greeks for options
"""
from historical_volatility import (
    get_close_price,
    get_historical_volatility,
)
from data_types import (
    Option,
    OptionType,
)
from pprint import pprint

if __name__ == '__main__':
    symbol = 'IBM'
    evaluation_date = '2021-06-30'
    expiration_date = '2022-01-21'
    close_price = get_close_price(symbol)
    strike_price = 150
    historical_volatility = get_historical_volatility(symbol)
    # historical_volatility = 0.2735
    option_type = OptionType.CALL
    option = Option(
        option_type,
        close_price,
        strike_price,
        evaluation_date,
        expiration_date,
        volatility=historical_volatility
    )

    # option_info = {
    #     "delta": option.get_delta(),
    #     "theta": option.get_theta(),
    #     "gamma": option.get_gamma(),
    #     "vega": option.get_vega(),
    #     "rho": option.get_rho(),
    #     "option_price": option.get_calculated_option_price(),
    # }
    print(option)
    print(option.get_basic_info())