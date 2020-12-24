# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: b'C:\\Users\\muchu\\Desktop\\caseWorkspace\\003-\xa5d\xa6\xcc\xba\xb8scrapy\\CAMEO_git_code\\cameo_api\\apis.py'
# Compiled at: 2016-05-28 01:59:52
"""
Copyright (C) 2015, MuChu Hsu
Contributed by Muchu Hsu (muchu1983@gmail.com)
This file is part of BSD license

<https://opensource.org/licenses/BSD-3-Clause>
"""
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