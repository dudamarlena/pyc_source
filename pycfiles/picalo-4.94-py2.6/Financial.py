# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/Financial.py
# Compiled at: 2008-03-17 12:58:08
"""
Encodes financial ratios used for analysis of financial statements.
While most of these ratios are easy to code, this module provides 
a home for their standard coding.

These functions are useful in expressions used throughout Picalo.
"""
from picalo import check_valid_table
import types
__functions__ = [
 'current_ratio',
 'quick_ratio',
 'net_working_capital',
 'return_on_assets',
 'return_on_equity',
 'return_on_common_equity',
 'profit_margin',
 'earnings_per_share',
 'asset_turnover',
 'inventory_turnover',
 'debt_to_equity',
 'price_earnings']

def current_ratio(current_assets, current_liabilities):
    """Returns the current ratio"""
    return float(current_assets) / float(current_liabilities)


def quick_ratio(current_assets, inventory, current_liabilities):
    """Returns the quick ratio"""
    return float(current_assets - inventory) / float(current_liabilities)


def net_working_capital(current_assets, current_liabilities, total_assets):
    """Returns the net working capital ratio"""
    return float(current_assets - current_liabilities) / float(total_assets)


def return_on_assets(net_income, beg_total_assets, end_total_assets):
    """Returns the return on assets"""
    return float(net_income) / (float(beg_total_assets + end_total_assets) / 2.0)


def return_on_equity(net_income, beg_stockholders_equity, end_stockholders_equity):
    """Returns the return on equity"""
    return float(net_income) / (float(beg_stockholders_equity + end_stockholders_equity) / 2.0)


def return_on_common_equity(net_income, beg_common_stockholders_equity, end_common_stockholders_equity):
    """Returns the return on common equity"""
    return float(net_income) / (float(beg_common_stockholders_equity + end_common_stockholders_equity) / 2.0)


def profit_margin(net_income, sales):
    """Returns the profit margin"""
    return float(net_income) / float(sales)


def earnings_per_share(net_income, number_of_shares):
    """Returns the earnings per share"""
    return float(net_income, number_of_shares)


def asset_turnover(sales, beg_total_assets, end_total_assets):
    """Returns the asset turnover ratio"""
    return float(sales) / (float(beg_total_assets + end_total_assets) / 2.0)


def inventory_turnover(cost_of_goods_sold, beg_inventory, end_inventory):
    """Returns the inventory turnover ratio"""
    return float(cost_of_goods_sold) / (float(beg_inventory + end_inventory) / 2.0)


def debt_to_equity(total_liabilities, total_stockholders_equity):
    """Returns the debt to equity ratio"""
    return float(total_liabilities) / float(total_stockholders_equity)


def price_earnings(share_market_price, net_income, number_of_shares):
    """Returns the PE (price earnings) ratio"""
    return float(share_market_price) / earnings_per_share(net_income, number_of_shares)