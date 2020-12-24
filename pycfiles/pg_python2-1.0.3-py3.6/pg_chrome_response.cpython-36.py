# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pg_python2/pg_chrome_response.py
# Compiled at: 2018-06-20 09:55:01
# Size of source mod 2**32: 810 bytes
from selenium.webdriver import Chrome
from scrapy.http.response.html import HtmlResponse
import logging
MAX_NUM_RETRY = 3

def get_response(url):
    num_retries = 0
    driver = None
    while num_retries < MAX_NUM_RETRY:
        try:
            driver = Chrome()
            driver.get(url)
            response = HtmlResponse(url=url, body=(driver.page_source), encoding='utf-8')
            driver.close()
            return response
        except Exception as e:
            logging.error('Exception %s' % e)
            num_retries += 1

    logging.error('Could not fetch the url')
    if driver is not None:
        driver.close()


if __name__ == '__main__':
    response = get_response('https://google.com')
    print(response)