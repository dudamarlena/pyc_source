# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/gorgou/request.py
# Compiled at: 2018-02-04 02:31:15
# Size of source mod 2**32: 1001 bytes
import os, requests
from lxml import etree

def downloadImage(imgUrl, fold, local_filename):
    r = requests.get(imgUrl, stream=True)
    if not os.path.exists(fold):
        os.mkdir(fold)
    path = os.path.join(fold, local_filename)
    with open(path, 'wb') as (f):
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
                f.flush()

        f.close()
    return local_filename


def get_pageitems_by_xpath(url, xpath, fileenc=None, htmldec=None):
    r = requests.get(url)
    if fileenc:
        r.encoding = fileenc
    if r.status_code == 200:
        html = r.text
        return get_htmlitems_by_xpath(html, xpath, htmldec)


def get_htmlitems_by_xpath(html, xpath, htmldec=None):
    if htmldec:
        html = html.decode(htmldec)
    page = etree.HTML(html)
    rows = page.xpath(xpath)
    return rows