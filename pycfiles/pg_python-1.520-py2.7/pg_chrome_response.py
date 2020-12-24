# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-intel/egg/pg_python/pg_chrome_response.py
# Compiled at: 2019-03-05 03:55:08
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
            response = HtmlResponse(url=url, body=driver.page_source, encoding='utf-8')
            driver.close()
            return response
        except Exception as e:
            logging.error('Exception %s' % e)
            num_retries += 1

    logging.error('Could not fetch the url')
    if driver is not None:
        driver.close()
    return


if __name__ == '__main__':
    response = get_response('https://google.com')
    print response