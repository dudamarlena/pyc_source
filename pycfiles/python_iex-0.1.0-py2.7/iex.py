# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/iex/iex.py
# Compiled at: 2018-10-14 19:54:51
import requests
from urllib.parse import urljoin

class IEX(object):
    base_url = 'https://ws-api.iextrading.com/1.0/'

    def __init__(self):
        self.uris = {'statistics': 'stock/{}/stats', 
           'financials': 'stock/{}/financials', 
           'book': 'stock/{}/book', 
           'chart': 'stock/{}/chart/{}', 
           'company': 'stock/{}/company', 
           'delayed_quote': 'stock/{}/delayed-quote', 
           'dividends': 'stock/{}/dividends/{}', 
           'earnings': 'stock/{}/earnings', 
           'threshold_securities': 'stock/market/threshold-securities', 
           'short_interest_list': 'stock/ziext/short-interest', 
           'largest_trades': 'stock/{}/largest-trades', 
           'most_active': 'stock/market/list/mostactive', 
           'gainers': 'stock/market/list/gainers', 
           'losers': 'stock/market/list/losers', 
           'iexvolume': 'stock/market/list/iexvolume', 
           'iexpercent': 'stock/market/list/iexpercent', 
           'logo': 'stock/{}/logo', 
           'news': 'stock/{}/news', 
           'news_range': 'stock/{}/news/last/{}', 
           'market_news': 'stock/market/news/last/{}', 
           'ohlc': 'stock/{}/ohlc', 
           'market_ohlc': 'stock/market/ohlc', 
           'peers': 'stock/{}/peers', 
           'previous': 'stock/{}/previous', 
           'market_previous': 'stock/market/previous', 
           'price': 'stock/{}/price', 
           'quote': 'stock/{}/quote', 
           'relevant_stocks': 'stock/{}/relevant', 
           'splits': 'stock/{}/splits/{}y', 
           'time_series': 'stock/{}/time-series', 
           'volume_by_venue': 'stock/{}/volume-by-venue', 
           'symbols': 'ref-data/symbols', 
           'corporate_actions': 'ref-data/daily-list/corporate-actions/{}', 
           'daily_dividends': 'ref-data/daily-list/dividends', 
           'next_day_ex_date': 'ref-data/daily-list/next-day-ex-date', 
           'symbol_directory': 'ref-data/daily-list/symbol-directory'}

    def get_request(self, uri):
        response = requests.get(urljoin(IEX.base_url, uri))
        resp_json = response.json()
        return resp_json

    def statistics(self, ticker):
        uri = self.uris['statistics'].format(ticker)
        return self.get_request(uri)

    def financials(self, ticker):
        uri = self.uris['financials'].format(ticker)
        return self.get_request(uri)

    def book(self, ticker):
        uri = self.uris['book'].format(ticker)
        return self.get_request(uri)

    def chart(self, ticker, time):
        uri = self.uris['chart'].format(ticker, time)
        return self.get_request(uri)

    def company(self, ticker):
        uri = self.uris['company'].format(ticker)
        return self.get_request(uri)

    def delayed_quote(self, ticker):
        uri = self.uris['delayed_quote'].format(ticker)
        return self.get_request(uri)

    def dividends(self, ticker, time):
        uri = self.uris['dividends'].format(ticker, time)
        return self.get_request(uri)

    def earnings(self, ticker):
        uri = self.uris['earnings'].format(ticker)
        return self.get_request(uri)

    def threshold_securities(self):
        uri = self.uris['threshold_securities']
        return self.get_request(uri)

    def short_interest_list(self):
        uri = self.uris['short_interest_list']
        return self.get_request(uri)

    def largest_trades(self, ticker):
        uri = self.uris['largest_trades'].format(ticker)
        return self.get_request(uri)

    def most_active(self):
        uri = self.uris['most_active']
        return self.get_request(uri)

    def gainers(self):
        uri = self.uris['gainers']
        return self.get_request(uri)

    def losers(self):
        uri = self.uris['losers']
        return self.get_request(uri)

    def iexvolume(self):
        uri = self.uris['iexvolume']
        return self.get_request(uri)

    def iexpercent(self):
        uri = self.uris['iexpercent']
        return self.get_request(uri)

    def logo(self, ticker):
        uri = self.uris['logo'].format(ticker)
        return self.get_request(uri)

    def news(self, ticker):
        uri = self.uris['news'].format(ticker)
        return self.get_request(uri)

    def news_range(self, ticker, time):
        uri = self.uris['news'].format(ticker, time)
        return self.get_request(uri)

    def market_news(self, time):
        uri = self.uris['market_news'].format(time)
        return self.get_request(uri)

    def ohlc(self, ticker):
        uri = self.uris['ohlc'].format(ticker)
        return self.get_request(uri)

    def market_ohlc(self):
        uri = self.uris['market_ohlc']
        return self.get_request(uri)

    def peers(self, ticker):
        uri = self.uris['peers'].format(ticker)
        return self.get_request(uri)

    def previous(self, ticker):
        uri = self.uris['previous'].format(ticker)
        return self.get_request(uri)

    def market_previous(self):
        uri = self.uris['market_previous']
        return self.get_request(uri)

    def price(self, ticker):
        uri = self.uris['price'].format(ticker)
        return self.get_request(uri)

    def quote(self, ticker):
        uri = self.uris['quote'].format(ticker)
        return self.get_request(uri)

    def relevant_stocks(self, ticker):
        uri = self.uris['relevant_stocks'].format(ticker)
        return self.get_request(uri)

    def splits(self, ticker, time):
        uri = self.uris['splits'].format(ticker, time)
        return self.get_request(uri)

    def time_series(self, ticker):
        uri = self.uris['time_series'].format(ticker)
        return self.get_request(uri)

    def volume_by_venue(self, ticker):
        uri = self.uris['volume_by_venue'].format(ticker)
        return self.get_request(uri)

    def symbols(self):
        uri = self.uris['symbols']
        return self.get_request(uri)

    def corporate_actions(self, date):
        uri = self.uris['corporate_actions'].format(date)
        return self.get_request(uri)

    def daily_dividends(self):
        uri = self.uris['daily_dividends']
        return self.get_request(uri)

    def next_day_ex_date(self):
        uri = self.uris['next_day_ex_date']
        return self.get_request(uri)

    def symbol_directory(self):
        uri = self.uris['symbol_directory']
        return self.get_request(uri)