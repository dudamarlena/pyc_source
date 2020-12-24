# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hm/GIT/yahoostats/yahoostats/requests_stats.py
# Compiled at: 2020-05-07 08:02:57
# Size of source mod 2**32: 7947 bytes
import requests
from bs4 import BeautifulSoup as soup
from time import sleep
import json
from pprint import pprint as pp
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
logger = logging.getLogger(__name__)

def get_page_content--- This code section failed: ---

 L.  16         0  LOAD_GLOBAL              requests
                2  LOAD_METHOD              Session
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               's'

 L.  17         8  LOAD_GLOBAL              Retry
               10  LOAD_CONST               5

 L.  18        12  LOAD_CONST               0.3

 L.  19        14  LOAD_CONST               500
               16  LOAD_CONST               502
               18  LOAD_CONST               503
               20  LOAD_CONST               504
               22  BUILD_LIST_4          4 

 L.  17        24  LOAD_CONST               ('total', 'backoff_factor', 'status_forcelist')
               26  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               28  STORE_FAST               'retries'

 L.  20        30  LOAD_FAST                's'
               32  LOAD_METHOD              mount
               34  LOAD_STR                 'http://'
               36  LOAD_GLOBAL              HTTPAdapter
               38  LOAD_FAST                'retries'
               40  LOAD_CONST               ('max_retries',)
               42  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               44  CALL_METHOD_2         2  ''
               46  POP_TOP          

 L.  21        48  LOAD_FAST                's'
               50  LOAD_METHOD              mount
               52  LOAD_STR                 'https://'
               54  LOAD_GLOBAL              HTTPAdapter
               56  LOAD_FAST                'retries'
               58  LOAD_CONST               ('max_retries',)
               60  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               62  CALL_METHOD_2         2  ''
               64  POP_TOP          

 L.  22        66  LOAD_GLOBAL              logger
               68  LOAD_METHOD              debug
               70  LOAD_STR                 'Fetching url: '
               72  LOAD_FAST                'url'
               74  FORMAT_VALUE          0  ''
               76  BUILD_STRING_2        2 
               78  CALL_METHOD_1         1  ''
               80  POP_TOP          

 L.  23        82  SETUP_FINALLY       136  'to 136'

 L.  24        84  LOAD_GLOBAL              sleep
               86  LOAD_CONST               0.01
               88  CALL_FUNCTION_1       1  ''
               90  POP_TOP          

 L.  25        92  LOAD_FAST                's'
               94  LOAD_ATTR                get
               96  LOAD_FAST                'url'
               98  LOAD_STR                 'User-Agent'
              100  LOAD_STR                 'Mozilla/5.0'
              102  BUILD_MAP_1           1 
              104  LOAD_CONST               ('headers',)
              106  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              108  STORE_FAST               'res'

 L.  26       110  LOAD_FAST                'res'
              112  LOAD_ATTR                status_code
              114  LOAD_GLOBAL              requests
              116  LOAD_ATTR                codes
              118  LOAD_STR                 'ok'
              120  BINARY_SUBSCR    
              122  COMPARE_OP               ==
              124  POP_JUMP_IF_FALSE   132  'to 132'

 L.  27       126  LOAD_FAST                'res'
              128  POP_BLOCK        
              130  RETURN_VALUE     
            132_0  COME_FROM           124  '124'
              132  POP_BLOCK        
              134  JUMP_FORWARD        192  'to 192'
            136_0  COME_FROM_FINALLY    82  '82'

 L.  28       136  DUP_TOP          
              138  LOAD_GLOBAL              Exception
              140  COMPARE_OP               exception-match
              142  POP_JUMP_IF_FALSE   190  'to 190'
              144  POP_TOP          
              146  STORE_FAST               'exe'
              148  POP_TOP          
              150  SETUP_FINALLY       178  'to 178'

 L.  29       152  LOAD_GLOBAL              logger
              154  LOAD_METHOD              error
              156  LOAD_STR                 'Unable to load the url '
              158  LOAD_FAST                'exe'
              160  FORMAT_VALUE          0  ''
              162  BUILD_STRING_2        2 
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          

 L.  30       168  POP_BLOCK        
              170  POP_EXCEPT       
              172  CALL_FINALLY        178  'to 178'
              174  LOAD_CONST               None
              176  RETURN_VALUE     
            178_0  COME_FROM           172  '172'
            178_1  COME_FROM_FINALLY   150  '150'
              178  LOAD_CONST               None
              180  STORE_FAST               'exe'
              182  DELETE_FAST              'exe'
              184  END_FINALLY      
              186  POP_EXCEPT       
              188  JUMP_FORWARD        192  'to 192'
            190_0  COME_FROM           142  '142'
              190  END_FINALLY      
            192_0  COME_FROM           188  '188'
            192_1  COME_FROM           134  '134'

Parse error at or near `CALL_FINALLY' instruction at offset 172


def reuters_stats(ticker):
    """
    Function to get data from Thompson Reuters"
    https://www.reuters.com/finance/stocks/lookup?searchType=any&comSortBy=marketcap&search="COMPANY"
    https://www.reuters.com/companies/GOOGL.O/key-metrics
    https://www.reuters.com/companies/IBM/key-metrics
    O - NASDAQ
    OQ - NASDAQ Stock Exchange Global Select Market
    N - NEWYORK Stock Exchange
    ""or without specified exchange - NEWYORK CONSOLIDATED
    """
    exchanges = [
     '', '.OQ', '.O', '.N']
    try:
        for exchange in exchanges:
            url = f"https://www.reuters.com/companies/{ticker}{exchange}/key-metrics"
            used_exchange = ''
            html = soup(get_page_content(url).text, 'html.parser')
            title = html.title.text
            logger.info('-----Reuters-----')
            logger.info(f"Trying with {ticker} on {exchange} -> {title}")
            if 'Page Not Found' in title:
                continue
        else:
            if ticker in title:
                soup1 = soup(get_page_content(url).content, 'html.parser')
                used_exchange = exchange
                break
            data_dict = {}
            data_dict.update({'exchange': used_exchange})
            for table in soup1.findAll'div'{'class': 'KeyMetrics-table-container-3wVZN'}:
                for row in table.findAll('tr'):
                    keys = row.findAll('th')
                    values = row.findAll('td')
                    row = []
                    if keys and values and keys[0].text:
                        data_dict.update({keys[0].text: values[0].text})

    except Exception as exe:
        try:
            logger.warning(exe)
            logger.warning(f"Wetsite {url} changed need to edit the function.")
            data_dict = {}
        finally:
            exe = None
            del exe

    else:
        return data_dict


def filter_reuters(data):
    """
    Filter the data from reuters.
    """
    r_beta = None
    r_eps_gr3 = None
    r_eps_gr5 = None
    r_div_gr3 = None
    r_roi_ttm = None
    r_roi_5 = None
    r_current_ratio = None
    r_mar_cap = None
    r_net_income = None
    r_net_debt = None
    r_div_yield = None
    r_div_yield5 = None
    r_rev_employee = None
    r_eps = None
    try:
        logger.info('-----Reuters data function-----')
        r_beta = data.get('Beta')
        r_eps_gr3 = data.get('EPS Growth Rate (3Y)')
        r_eps_gr5 = data.get('EPS Growth Rate (5Y)')
        r_div_gr3 = data.get('Dividend Growth Rate (3Y)')
        r_roi_ttm = data.get('Return on Investment (TTM)')
        r_roi_5 = data.get('Return on Investment (5Y)')
        r_current_ratio = data.get('Current Ratio (Annual)')
        r_mar_cap = data.get('Market Capitalization')
        r_net_income = data.get('Net Income Available to Common Normalized (Annual)')
        r_net_debt = data.get('Net Debt (Annual)')
        r_div_yield = data.get('Dividend Yield')
        r_div_yield5 = data.get('Dividend Yield (5Y)')
        r_rev_employee = data.get('Revenue/Employee (TTM)')
        r_eps = data.get('EPS Normalized (Annual)')
    except Exception as exe:
        try:
            logger.warning(exe)
        finally:
            exe = None
            del exe

    else:
        filtered = {v:k for k, v in locals().items if not k.startswith('data') if not k.startswith('data')}
        return filtered


def morningstar_stats--- This code section failed: ---

 L. 129         0  LOAD_STR                 'https://financials.morningstar.com/ratios/r.html?t='
                2  LOAD_FAST                'ticker'
                4  FORMAT_VALUE          0  ''
                6  LOAD_STR                 '&culture=en&platform=sal'
                8  BUILD_STRING_3        3 
               10  STORE_FAST               'url'

 L. 130        12  SETUP_FINALLY        90  'to 90'

 L. 131        14  LOAD_GLOBAL              soup
               16  LOAD_GLOBAL              get_page_content
               18  LOAD_FAST                'url'
               20  CALL_FUNCTION_1       1  ''
               22  LOAD_ATTR                content
               24  LOAD_STR                 'html.parser'
               26  CALL_FUNCTION_2       2  ''
               28  STORE_FAST               'soup_ms'

 L. 132        30  LOAD_GLOBAL              logger
               32  LOAD_METHOD              info
               34  LOAD_STR                 '-----Morningstar-----'
               36  CALL_METHOD_1         1  ''
               38  POP_TOP          

 L. 133        40  LOAD_GLOBAL              logger
               42  LOAD_METHOD              info
               44  LOAD_STR                 'Fetching data for '
               46  LOAD_FAST                'ticker'
               48  FORMAT_VALUE          0  ''
               50  BUILD_STRING_2        2 
               52  CALL_METHOD_1         1  ''
               54  POP_TOP          

 L. 134        56  LOAD_FAST                'soup_ms'
               58  LOAD_METHOD              find
               60  LOAD_STR                 'span'
               62  LOAD_STR                 'id'
               64  LOAD_STR                 'star_span'
               66  BUILD_MAP_1           1 
               68  CALL_METHOD_2         2  ''
               70  STORE_FAST               'start_rating'

 L. 135        72  LOAD_STR                 'ms'
               74  LOAD_FAST                'start_rating'
               76  LOAD_STR                 'class'
               78  BINARY_SUBSCR    
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  BUILD_MAP_1           1 
               86  POP_BLOCK        
               88  RETURN_VALUE     
             90_0  COME_FROM_FINALLY    12  '12'

 L. 136        90  DUP_TOP          
               92  LOAD_GLOBAL              Exception
               94  COMPARE_OP               exception-match
               96  POP_JUMP_IF_FALSE   144  'to 144'
               98  POP_TOP          
              100  STORE_FAST               'exe'
              102  POP_TOP          
              104  SETUP_FINALLY       132  'to 132'

 L. 137       106  LOAD_GLOBAL              logger
              108  LOAD_METHOD              warning
              110  LOAD_FAST                'exe'
              112  CALL_METHOD_1         1  ''
              114  POP_TOP          

 L. 138       116  LOAD_STR                 'ms'
              118  LOAD_STR                 '---'
              120  BUILD_MAP_1           1 
              122  ROT_FOUR         
              124  POP_BLOCK        
              126  POP_EXCEPT       
              128  CALL_FINALLY        132  'to 132'
              130  RETURN_VALUE     
            132_0  COME_FROM           128  '128'
            132_1  COME_FROM_FINALLY   104  '104'
              132  LOAD_CONST               None
              134  STORE_FAST               'exe'
              136  DELETE_FAST              'exe'
              138  END_FINALLY      
              140  POP_EXCEPT       
              142  JUMP_FORWARD        146  'to 146'
            144_0  COME_FROM            96  '96'
              144  END_FINALLY      
            146_0  COME_FROM           142  '142'

Parse error at or near `POP_BLOCK' instruction at offset 124


def zacks_stats(ticker):
    """
    Get Zacks start rating for specific stock.
    https://www.zacks.com/stock/chart/GTT/fundamental/peg-ratio-ttm
    https://www.zacks.com/stock/quote/GOOGL/financial-overview
    https://www.zacks.com/stock/quote/TSLA/financial-overview

    <div> class = 'zr_rankbox'
    <p> class = 'rank_view' .text
    added sleep for error code#104 on colab
    https://stackoverflow.com/questions/52051989/requests-exceptions-connectionerror-connection-aborted-connectionreseterro
    """
    logger.info('-----Zacks-----')
    logger.info(f"Fetching data for {ticker}")
    url = f"https://www.zacks.com/stock/quote/{ticker}/financial-overview"
    try:
        sleep(0.01)
        soup_zack = soup(get_page_content(url).content, 'html.parser')
        rating_div = soup_zack.find'div'{'class': 'zr_rankbox'}
        rating_label = rating_div.find('p')
        rating_value = rating_label.text
    except Exception as exe:
        try:
            logger.warning(f"Unable to get data from zacks {exe}")
            rating_value = '---'
        finally:
            exe = None
            del exe

    else:
        return {'zacks': rating_value.split[0]}


def yahoo_api_financials(ticker):
    """
    Get the data from Yahoo API

    """
    logger.info('-----Yahoo Finance API-----')
    logger.info(f"Fetching data for {ticker}")
    url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{ticker}?modules=" + 'financialData%2CdefaultKeyStatistics'
    try:
        resp = get_page_content(url)
        data = resp.json
        fin_data = data['quoteSummary']['result'][0]['financialData']
        current_price = fin_data['currentPrice'].get('raw')
        target_price = fin_data['targetMeanPrice'].get('raw')
        yahoo_rating_val = fin_data['recommendationMean'].get('raw')
        yahoo_rating_str = fin_data['recommendationKey']
        yahoo_valuation = float(target_price) / float(current_price)
        yahoo_current_ratio = fin_data['currentRatio'].get('raw')
        y_return_assets = fin_data['returnOnAssets'].get('raw')
        y_return_equity = fin_data['returnOnEquity'].get('raw')
        bs_data = data['quoteSummary']['result'][0].get('defaultKeyStatistics')
        beta = bs_data.get('beta').get('raw')
    except Exception:
        beta = None
        y_return_equity, yahoo_current_ratio = (None, None)
        y_return_assets, yahoo_valuation = (None, None)
        yahoo_rating_str, yahoo_rating_val = (None, None)
        target_price, current_price = (None, None)
    else:
        result = {'yf_pr_now':current_price, 
         'yf_pr_trg':target_price, 
         'yf_rv':yahoo_rating_val, 
         'yf_rs':yahoo_rating_str, 
         'yf_prof':yahoo_valuation, 
         'yf_cur_ratio':yahoo_current_ratio, 
         'yf_ret_assets':y_return_assets, 
         'yf_ret_equity':y_return_equity, 
         'yf_beta':beta}
        return result