# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\spiderlib\test05.py
# Compiled at: 2020-03-27 22:59:07
# Size of source mod 2**32: 885 bytes
import requests
from lxml import html
from spiderlib import DrupalPipeline
resp = requests.get('http://www.ala.org/news/press-releases')
if resp.status_code == 200:
    links = html.etree.HTML(resp.text).xpath("//span[@class='field-content']//@href")
    links = ['http://www.ala.org' + x for x in links]
    for link in links:
        resp = requests.get(link)
        if resp.status_code == 200:
            root = html.etree.HTML(resp.text)
            title = root.xpath("//h1[@class='page-header']//text()")
            title = ''.join(title)
            content = root.xpath("//div[@class='field-items']//text()")
            content = '<p>'.join(content)
            content = '来源地址 ' + link + '<p>' + content