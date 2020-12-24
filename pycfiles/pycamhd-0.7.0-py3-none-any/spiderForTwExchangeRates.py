# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: b'C:\\Users\\muchu\\Desktop\\caseWorkspace\\003-\xa5d\xa6\xcc\xba\xb8scrapy\\CAMEO_git_code\\cameo_api\\spiderForTwExchangeRates.py'
# Compiled at: 2016-05-28 01:59:00
__doc__ = '\nCopyright (C) 2015, MuChu Hsu\nContributed by Muchu Hsu (muchu1983@gmail.com)\nThis file is part of BSD license\n\n<https://opensource.org/licenses/BSD-3-Clause>\n'
from selenium import webdriver
import os, logging, time, datetime, re, random, pkg_resources
from cameo.externaldb import ExternalDbForCurrencyApi

class SpiderForTwExchangeRates:

    def __init__(self):
        self.driver = None
        self.db = ExternalDbForCurrencyApi().mongodb
        return

    def getDriver(self):
        chromeDriverExeFilePath = pkg_resources.resource_filename('cameo_res', 'chromedriver.exe')
        driver = webdriver.Chrome(chromeDriverExeFilePath)
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
        self.driver.get('http://tw.exchange-rates.org/')
        elesAreaLink = self.driver.find_elements_by_css_selector('div#currencies-region div a.link')
        intCurrentAreaLink = 0
        while len(elesAreaLink) == 5:
            time.sleep(random.randint(20, 30))
            strAreaLink = elesAreaLink[intCurrentAreaLink].get_attribute('href')
            self.driver.get(strAreaLink)
            logging.info('search ex-rate on %s' % strAreaLink)
            time.sleep(random.randint(20, 30))
            elesExRateTr = self.driver.find_elements_by_css_selector('table.table-exchangeX.large-only tbody tr')
            for eleExRateTr in elesExRateTr:
                strExRateHref = eleExRateTr.find_element_by_css_selector('td.text-nowrapX a:nth-of-type(1)').get_attribute('href')
                strCurrencyName = re.match('http://tw.exchange-rates.org/currentRates/./(...)', strExRateHref).group(1)
                strXXXToUSD = eleExRateTr.find_element_by_css_selector('td:nth-of-type(5)').text
                fUSDToXXX = 1.0 / float(strXXXToUSD.strip())
                logging.info('find ex-rate: 1 USD to %s is %f' % (strCurrencyName, fUSDToXXX))
                logging.info('start update ex-rate data...')
                strTimeNow = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.db.ModelExRate.update_one({'strCurrencyName': 'USD' + strCurrencyName}, {'$set': {'strDate': strTimeNow, 'strCurrencyName': 'USD' + strCurrencyName, 
                            'fUSDollar': fUSDToXXX}}, upsert=True)
                logging.info('ex-rate data updated. [%s]' % strTimeNow)

            elesAreaLink = self.driver.find_elements_by_css_selector('div#currencies-region div a.link')
            intCurrentAreaLink = (intCurrentAreaLink + 1) % 5