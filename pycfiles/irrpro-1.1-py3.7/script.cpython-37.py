# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/irrpro/script.py
# Compiled at: 2019-01-10 18:13:22
# Size of source mod 2**32: 871 bytes
import numpy as np
from lxml import html
import requests, math
from time import sleep

def parser(ads_cnt=30):
    url = 'https://irr.ru/real-estate/rent/'
    url_cur = url
    url_all = np.array([])
    title_all = np.array([])
    i = 1
    while i <= math.ceil(ads_cnt / 30):
        url_cur = url + 'page' + str(i)
        page = requests.get(url_cur)
        tree = html.fromstring(page.content)
        url_list = tree.xpath('//div[@class="listing__itemTitleWrapper"]/a/@href')
        url_all = np.append(url_all, url_list)
        i = i + 1

    for j in range(0, ads_cnt):
        url_cur = url_all[j]
        page = requests.get(url_cur)
        tree = html.fromstring(page.content)
        title = tree.xpath('//div[@class="productPage__wrapperTitle js-wrapperTitle"]/h1/text()')
        title = str(title).replace('\\t', '').replace('\\n', '').replace('  ', '')
        title_all = np.append(title_all, title)
        sleep(0.1)

    print(title_all)