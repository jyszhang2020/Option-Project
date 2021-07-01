from enum import Enum
import math
from scipy.stats import norm
from typing import Optional
from utils import calculate_maturity_time


class OptionType(Enum):
    CALL = 1
    PUT = 2

    def __repr__(self):
        return 'CALL' if self == OptionType.CALL else 'PUT'

class Option:
    """
    This class will group the different black-shcoles calculations for an option
    """
    def __init__(self,
                 option_type: OptionType,
                 stock_price: float,
                 strike_price: float,
                 evaluation_date: str,
                 expiration_date: str,
                 option_price: Optional[float] = None,
                 risk_free_rate: float = 0.01,
                 volatility: float = 0.3,
                 dividend: float = 0):
        assert option_type == OptionType.CALL or option_type == OptionType.PUT
        self.strike_price = float(strike_price)
        self.stock_price = float(stock_price)
        self.risk_free_rate = float(risk_free_rate)
        self.volatility = float(volatility)
        self.maturity_time = calculate_maturity_time(evaluation_date, expiration_date)
        self.real_option_price = option_price
        self.option_type = option_type   # Call or Put
        self.dividend = dividend

    def get_calculated_option_price(self) -> float:
        d1 = self.get_d1()
        d2 = self.get_d2(d1)
        if self.option_type == OptionType.CALL:
            return (norm.cdf(d1) * self.stock_price * math.exp(-self.dividend * self.maturity_time) - norm.cdf(d2) *
                    self.strike_price * math.exp(-self.risk_free_rate * self.maturity_time))
        else:
            return (-norm.cdf(-d1) * self.stock_price * math.exp(-self.dividend * self.maturity_time) + norm.cdf(
                -d2) *
                    self.strike_price * math.exp(-self.risk_free_rate * self.maturity_time))

    def get_delta(self) -> float:
        d1 = self.get_d1()
        if self.option_type == OptionType.CALL:
            return norm.cdf(d1)
        else:
            return -norm.cdf(-d1)

    def get_theta(self, offset: float = 0.0027777) -> float:
        # change rate of price when expiration time changes
        self.maturity_time += offset
        after_price = self.get_calculated_option_price()
        self.maturity_time -= offset
        orig_price = self.get_calculated_option_price()
        return (after_price - orig_price) * (-1)

    def get_gamma(self, offset: float = 0.001) -> float:
        # change rate of delta when stock price changes
        self.stock_price += offset
        after_delta = self.get_delta()
        self.stock_price -= offset
        orig_delta = self.get_delta()
        return (after_delta - orig_delta) / offset

    def get_vega(self, offset: float = 0.01) -> float:
        # change rate of delta when stock volatility changes
        self.volatility += offset
        after_price = self.get_calculated_option_price()
        self.volatility -= offset
        orig_price = self.get_calculated_option_price()
        return (after_price - orig_price) / (offset * 100)  # Vega is measured by percent

    def get_rho(self, dr=0.01):
        # Change rate of delta when risk-free rate changes
        orig_price = self.get_calculated_option_price()
        self.risk_free_rate += dr
        after_price = self.get_calculated_option_price()
        self.risk_free_rate -= dr
        return (after_price - orig_price) / (dr * 100)  # Rho is measured by percent

    def get_d1(self) -> float:
        return (math.log(self.stock_price / self.strike_price) + (
                    self.risk_free_rate + self.volatility ** 2 / 2) * self.maturity_time) \
               / (self.volatility * math.sqrt(self.maturity_time))

    def get_d2(self, d1) -> float:
        return d1 - self.volatility * math.sqrt(self.maturity_time)

    def get_impl_vol(self) -> float:
        """
        This function will iterate until finding the implied volatility
        """
        ITERATIONS = 100
        ACCURACY = 0.05
        low_vol = 0
        high_vol = 1
        self.volatility = 0.5  ## It will try mid point and then choose new interval
        for i in range(ITERATIONS):
            if self.get_calculated_option_price() > self.real_option_price + ACCURACY:
                high_vol = self.volatility
            elif self.get_calculated_option_price() < self.real_option_price - ACCURACY:
                low_vol = self.volatility
            else:
                break
            self.volatility = low_vol + (high_vol - low_vol) / 2.0

        return self.volatility

    def __repr__(self):
        option_info = {
            "delta": self.get_delta(),
            "theta": self.get_theta(),
            "gamma": self.get_gamma(),
            "vega": self.get_vega(),
            "rho": self.get_rho(),
            "option": self.get_calculated_option_price(),
        }
        return '====================================\n' + \
               '\n'.join('%r: %r' % i for i in option_info.items()) + \
               '\n===================================='

    def get_basic_info(self):
        option_info = {
            "option_type": self.option_type,
            "stock_price": self.stock_price,
            "strike_price": self.strike_price,
            "volatility": self.volatility,
        }
        return '====================================\n' + \
               '\n'.join('%r: %r' % i for i in option_info.items()) + \
               '\n===================================='