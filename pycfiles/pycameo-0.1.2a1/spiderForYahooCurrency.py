# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: b'C:\\Users\\muchu\\Desktop\\caseWorkspace\\003-\xa5d\xa6\xcc\xba\xb8scrapy\\CAMEO_git_code\\cameo_api\\spiderForYahooCurrency.py'
# Compiled at: 2016-05-24 20:07:08
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
from selenium import webdriver
import os, logging, time, datetime, re, random, pkg_resources
from cameo.externaldb import ExternalDbForCurrencyApi

class SpiderForYahooCurrency:

    def __init__(self):
        self.driver = None
        self.db = ExternalDbForCurrencyApi().mongodb
        return

    def getDriver(self):
        phantomjsDriverExeFilePath = pkg_resources.resource_filename('cameo_res', 'phantomjs.exe')
        driver = webdriver.PhantomJS(phantomjsDriverExeFilePath)
        return driver

    def initDriver(self):
        if self.driver is None:
            self.driver = self.getDriver()
        return

    def quitDriver(self):
        self.driver.quit()
        self.driver = None
        return

    def runSpider(self):
        self.initDriver()
        self.updateExRateData()
        self.quitDriver()

    def updateExRateData(self):
        self.driver.get('https://tw.money.yahoo.com/currency')
        elesAreaTabLi = self.driver.find_elements_by_css_selector('ul.sub-tabs.D-ib li')
        intCurrentAreaTab = 0
        while len(elesAreaTabLi) == 3:
            time.sleep(random.randint(20, 30))
            elesAreaTabLi[intCurrentAreaTab].click()
            time.sleep(random.randint(20, 30))
            elesExRateTr = self.driver.find_elements_by_css_selector('tbody tr.Bd-b')
            for eleExRateTr in elesExRateTr:
                strExRateHref = eleExRateTr.find_element_by_css_selector('td.Ta-start a').get_attribute('href')
                strCurrencyName = re.match('https://tw.money.yahoo.com/currency/(USD...)=X', strExRateHref).group(1)
                strUSDollar = eleExRateTr.find_element_by_css_selector('td.Ta-end:nth-of-type(3)').text
                logging.info('start update ex-rate data...')
                strTimeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.db.ModelExRate.update_one({'strCurrencyName': strCurrencyName}, {'$set': {'strDate': strTimeNow, 'strCurrencyName': strCurrencyName, 
                            'fUSDollar': float(strUSDollar)}}, upsert=True)
                logging.info('ex-rate data updated. [%s]' % strTimeNow)

            elesAreaTabLi = self.driver.find_elements_by_css_selector('ul.sub-tabs.D-ib li')
            intCurrentAreaTab = (intCurrentAreaTab + 1) % 3