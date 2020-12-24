# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\spiderlib\test03.py
# Compiled at: 2020-03-25 09:13:48
# Size of source mod 2**32: 676 bytes
import requests
from lxml import etree
from spiderlib import *
resp = requests.get('https://www.cnblogs.com')
root = etree.HTML(resp.text)
titles = root.xpath("//a[@class='titlelnk']//text()")
links = root.xpath("//a[@class='titlelnk']//@href")
redis = RedisRedup()
values = []
values.append(['title', 'link'])
for item in zip(titles, links):
    if not redis.loaded(item[1]):
        values.append(item)

mysql = MySQLPipeline(database='bee', table='data')
mysql.save(values)