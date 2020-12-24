# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: b'C:\\Users\\muchu\\Desktop\\caseWorkspace\\003-\xa5d\xa6\xcc\xba\xb8scrapy\\CAMEO_git_code\\cameo_api\\apis.py'
# Compiled at: 2016-05-28 01:59:52
__doc__ = '\nCopyright (C) 2015, MuChu Hsu\nContributed by Muchu Hsu (muchu1983@gmail.com)\nThis file is part of BSD license\n\n<https://opensource.org/licenses/BSD-3-Clause>\n'
import logging
from cameo.externaldb import ExternalDbForCurrencyApi

def exchangeCurrency(strDate=None, fMoney=0.0, strFrom='TWD', strTo='TWD'):
    db = ExternalDbForCurrencyApi().mongodb
    fFromUSDRate = 0.0
    fToUSDRate = 0.0
    if strFrom == 'USD':
        fFromUSDRate = 1.0
    else:
        docFromExRate = db.ModelExRate.find_one({'strCurrencyName': 'USD' + strFrom})
        fFromUSDRate = docFromExRate['fUSDollar']
    if strTo == 'USD':
        fToUSDRate = 1.0
    else:
        docToExRate = db.ModelExRate.find_one({'strCurrencyName': 'USD' + strTo})
        fToUSDRate = docToExRate['fUSDollar']
    logging.info('exchange %f dollar from %s to %s' % (fMoney, strFrom, strTo))
    fResultMoney = fMoney * fToUSDRate / fFromUSDRate
    return fResultMoney