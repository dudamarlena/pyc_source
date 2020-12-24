# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hm/GIT/yahoostats/yahoostats/selenium_stats.py
# Compiled at: 2020-05-07 12:04:13
# Size of source mod 2**32: 7598 bytes
from selenium import webdriver
import selenium.webdriver.chrome.options as chrome_options
import selenium.webdriver.firefox.options as firefox_options
from bs4 import BeautifulSoup
import pandas as pd, time, configparser
from pprint import pprint as pp
import logging
logger = logging.getLogger(__name__)
config = configparser.ConfigParser()
config.read('config.ini')
print(config.sections())

class Webscraper:

    def __init__(self, browser='Chrome'):
        self._yf_url = 'https://finance.yahoo.com/quote'
        self.browser = browser
        self._Webscraper__driver = None

    def start(self):
        if self.browser == 'Chrome':
            browser_options = chrome_options()
            browser_options.add_argument('--headless')
            browser_options.add_argument('--no-sandbox')
            self._Webscraper__driver = webdriver.Chrome(options=browser_options)
        else:
            if self.browser == 'Firefox':
                browser_options = firefox_options()
                browser_options.add_argument('--headless')
                browser_options.add_argument('--no-sandbox')
                self._Webscraper__driver = webdriver.Firefox(options=browser_options)
            else:
                raise Exception('Please set browser to browser=Firefox or Chrome.')
        logger.info(f"Using {self.browser}")
        time.sleep(1)
        logger.debug('Webdriver Started')

    def accept_yf_cockies(self):
        """Yahoo Finance requires to accept cockies on the fist run."""
        self._Webscraper__driver.get(self._yf_url)
        try:
            cockie_window = self._Webscraper__driver.find_element_by_tag_name('body')
            cockie_window.find_element_by_name('agree').click()
            logger.debug('Yahoo Cockies accepted.')
        except Exception as exe:
            try:
                logger.warning(f"Unable to accept cockies.{exe}")
            finally:
                exe = None
                del exe

    def stop(self):
        try:
            self._Webscraper__driver.close()
            logger.info('Webscraper has finished.Quit.')
        except Exception as exe:
            try:
                logger.warning(f"Unable to stop the Webscraper.{exe}")
            finally:
                exe = None
                del exe

    def get_yahoo_statistics(self, ticker):
        stock_data = {}
        logger.info('----------Yahoo PEG ratio-----')
        logger.info(f"Yahoo webscraping for  {ticker}")
        stock_url = f"{self._yf_url}/{ticker}/key-statistics?p={ticker}"
        logger.info(f"Yahoo url  {stock_url}")
        try:
            self._Webscraper__driver.get(stock_url)
            soup = BeautifulSoup(self._Webscraper__driver.page_source, 'html.parser')
            if 'Symbols Lookup From Yahoo Finance' in self._Webscraper__driver.title:
                logger.warning(f"The {ticker} was not found in Yahoo Finance.")
                print(f"The {ticker} was not found in Yahoo Finance.")
                stock_data.update({'PEG Ratio': '---'})
            else:
                data = soup.find(id='Main')
                tables = data.find_all('table')
                for table in tables:
                    rows = table.find_all('tr')
                    for tr in rows:
                        td = tr.find_all('td')
                        if len(td) > 1 and td[0].text == 'PEG Ratio (5 yr expected) 1':
                            stock_data.update({td[0].text: td[1].text})

        except Exception as exe:
            try:
                logger.warning(f"Unable to get data from Yahoo  {exe}")
            finally:
                exe = None
                del exe

        else:
            return stock_data

    def tipranks_analysis(self, ticker):
        """
        https://www.tipranks.com/stocks/amd/stock-analysis
        """
        url_tr = f"https://www.tipranks.com/stocks/{ticker}/stock-analysis"
        logger.info('-----Tipranks-----')
        logger.info(f"Fetching data for {ticker}")
        logger.debug(f"Using selenium on {url_tr}")
        data = {}
        try:
            self._Webscraper__driver.get(url_tr)
            time.sleep(1)
            soup = BeautifulSoup(self._Webscraper__driver.page_source, 'html.parser')
            div_tr_score = soup.find('div', {'class': 'client-components-ValueChange-shape__Octagon'})
            text_tr_score = div_tr_score.find('tspan').text + '/10'
            data.update({'tr_score': text_tr_score})
            div_boxes = soup.find_all('div', {'class': 'client-components-stock-research-smart-score-Factor-Factor__Factor'})
            for box in div_boxes[:8]:
                k = 'tr_' + box.find('header').text
                v = box.find_all('div')[0].find_all('div')[0].text
                data.update({k: v})

        except Exception as exe:
            try:
                logger.warning(exe)
            finally:
                exe = None
                del exe

        else:
            return data

    def tipranks_price(self, ticker):
        """
        Webscrape price prediction for the next 12 months.
        https://www.tipranks.com/stocks/amd/price-target
        http://theautomatic.net/2019/01/19/scraping-data-from-javascript-webpage-python/
        price - target value
        <div class="client-components-stock-research-analysts-price-target-style__actualMoney">

        <div class="client-components-stock-research-analysts-price-target-style__change">
        """
        url_tr = f"https://www.tipranks.com/stocks/{ticker}/price-target"
        logger.info('-----tipranks_price-----')
        logger.info(f"Fetching data for {ticker}")
        logger.debug(f"Using selenium on {url_tr}")
        target_pr, target_change = (None, None)
        try:
            self._Webscraper__driver.get(url_tr)
            time.sleep(2)
            soup = BeautifulSoup(self._Webscraper__driver.page_source, 'html.parser')
            div_target_pr = soup.find('div', {'class': 'client-components-stock-research-analysts-price-target-style__actualMoney'})
            target_pr = div_target_pr.find('span')['title']
            div_target_prof = soup.find('div', {'class': 'client-components-stock-research-analysts-price-target-style__change'})
            target_change = div_target_prof.find('span').text
        except Exception as exe:
            try:
                logger.warning(f"Website changed {exe}")
            finally:
                exe = None
                del exe

        else:
            return {'tr_target_pr':target_pr, 
             'tr_change':target_change}

    def simplywall(self, ticker):
        """
        https://simplywall.st/stocks/us/media/nasdaq-goog.l/alphabet
        https://simplywall.st/stocks/us/software/nyse-gtt/gtt-communications
        NOT IMPLEMENTED
        """
        url_sw = 'https://simplywall.st/stocks/us'
        return url_sw

    def scroll(self, px):
        self._Webscraper__driver.execute_script(f"window.scrollTo(0, {px})")
        logger.debug(f"Scrolled with {px} px")

    def screenshot(self, path):
        self._Webscraper__driver.save_screenshot(path)
        logger.info(f"Screenshot saved as {path} ")

    def test_run--- This code section failed: ---

 L. 167         0  SETUP_FINALLY        56  'to 56'

 L. 168         2  LOAD_GLOBAL              logger
                4  LOAD_METHOD              info
                6  LOAD_STR                 'Testrun on Selenium'
                8  CALL_METHOD_1         1  ''
               10  POP_TOP          

 L. 169        12  LOAD_FAST                'self'
               14  LOAD_METHOD              start
               16  CALL_METHOD_0         0  ''
               18  POP_TOP          

 L. 170        20  LOAD_FAST                'self'
               22  LOAD_ATTR                _Webscraper__driver
               24  LOAD_METHOD              get
               26  LOAD_STR                 'https://finance.yahoo.com/quote'
               28  CALL_METHOD_1         1  ''
               30  POP_TOP          

 L. 171        32  LOAD_FAST                'self'
               34  LOAD_METHOD              stop
               36  CALL_METHOD_0         0  ''
               38  POP_TOP          

 L. 172        40  LOAD_GLOBAL              logger
               42  LOAD_METHOD              info
               44  LOAD_STR                 'working'
               46  CALL_METHOD_1         1  ''
               48  POP_TOP          

 L. 173        50  POP_BLOCK        
               52  LOAD_CONST               True
               54  RETURN_VALUE     
             56_0  COME_FROM_FINALLY     0  '0'

 L. 174        56  DUP_TOP          
               58  LOAD_GLOBAL              Exception
               60  COMPARE_OP               exception-match
               62  POP_JUMP_IF_FALSE   110  'to 110'
               64  POP_TOP          
               66  STORE_FAST               'exe'
               68  POP_TOP          
               70  SETUP_FINALLY        98  'to 98'

 L. 175        72  LOAD_GLOBAL              logger
               74  LOAD_METHOD              warning
               76  LOAD_STR                 'Something gone wrong...'
               78  LOAD_FAST                'exe'
               80  FORMAT_VALUE          0  ''
               82  BUILD_STRING_2        2 
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          

 L. 176        88  POP_BLOCK        
               90  POP_EXCEPT       
               92  CALL_FINALLY         98  'to 98'
               94  LOAD_CONST               False
               96  RETURN_VALUE     
             98_0  COME_FROM            92  '92'
             98_1  COME_FROM_FINALLY    70  '70'
               98  LOAD_CONST               None
              100  STORE_FAST               'exe'
              102  DELETE_FAST              'exe'
              104  END_FINALLY      
              106  POP_EXCEPT       
              108  JUMP_FORWARD        112  'to 112'
            110_0  COME_FROM            62  '62'
              110  END_FINALLY      
            112_0  COME_FROM           108  '108'

Parse error at or near `RETURN_VALUE' instruction at offset 54


def ys_run(ticker, browser='Chrome'):
    yh = Webscraper(browser)
    yh.start()
    yh.accept_yf_cockies()
    result_df = yh.get_yahoo_statistics(ticker)
    yh.stop()
    return result_df


def tr_run(ticker, browser='Chrome'):
    tr = Webscraper(browser)
    tr.start()
    result_df = tr.tipranks_analysis(ticker)
    result_df.update(tr.tipranks_price(ticker))
    tr.stop()
    return result_df


if __name__ == '__main__':
    stock_list = [
     'GOOGL', 'GTT', 'VMW', 'AMD', 'NVDA', 'TSLA', 'IBM', 'DELL']
    pp(ys_run(stock_list[0]))