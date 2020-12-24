# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vanilla_option_pricing\option.py
# Compiled at: 2018-09-15 07:42:28
# Size of source mod 2**32: 2975 bytes
import pandas as pd
from py_lets_be_rational.exceptions import BelowIntrinsicException
from py_vollib.black import implied_volatility as iv

def option_list_to_pandas_dataframe(options):
    """
    A utility function to convert a list of :class:`~option.VanillaOption` to a pandas dataframe

    :param options: a list of :class:`~option.VanillaOption`
    :return: a pandas dataframe, containing option data
    """
    return pd.DataFrame.from_records([o.to_dict() for o in options])


def pandas_dataframe_to_option_list(data_frame: pd.DataFrame):
    """
    A utility function to convert a pandas dataframe to a list of :class:`~option.VanillaOption`.
    For this function to work, the dataframe columns should be names as the parameters of
    :class:`~option.VanillaOption`'s constructor

    :param data_frame: a pandas dataframe, containing option data
    :return: a list of :class:`~option.VanillaOption`
    """
    return [VanillaOption(**o) for o in data_frame.to_dict(orient='record')]


class VanillaOption:
    __doc__ = '\n    A European vanilla option. All the prices must have consistent unit of measure\n\n    :param instrument: name of the undelying\n    :param option_type: type of the option (c for call, p for put)\n    :param date: the date when the option is traded\n    :param price: option price\n    :param strike: option strike price\n    :param spot: spot price of the underlying\n    :param maturity: the maturity date\n    :param dividend: underlying dividend - if any, expressed as a decimal number\n    '
    DAYS_IN_YEAR = 365.2425

    def __init__(self, instrument: str, option_type: str, date, price: float, strike: float, spot: float, maturity, dividend=0):
        self.instrument = instrument
        self.option_type = option_type.lower()
        self.date = date
        self.price = price
        self.strike = strike
        self.spot = spot
        self.maturity = maturity
        self.dividend = dividend

    @property
    def years_to_maturity(self) -> float:
        """
        The years remaining to option maturity, as a decimal number
        """
        return (self.maturity - self.date).days / self.DAYS_IN_YEAR

    @property
    def implied_volatility_of_undiscounted_price(self):
        """
        The implied volatility of the option, considering an undisconted price.
        """
        try:
            return iv.implied_volatility_of_undiscounted_option_price(self.price, self.spot, self.strike, self.years_to_maturity, self.option_type)
        except BelowIntrinsicException:
            return 0

    def to_dict(self):
        """
        :return: all the fields of the object in a dictionary
        """
        return {k:v for k, v in vars(self).items() if not k.startswith('_') if not k.startswith('_')}