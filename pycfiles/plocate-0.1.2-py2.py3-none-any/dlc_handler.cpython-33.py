# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ploader/dlc_handler.py
# Compiled at: 2014-01-06 19:25:51
# Size of source mod 2**32: 885 bytes
import urllib.request, urllib.parse
from bs4 import BeautifulSoup
import json

def dlc_to_links(url):
    data = urllib.parse.urlencode({'pro_links': url,  'modo_links': 'text',  'modo_recursivo': 'on',  'link_cache': 'on'})
    data = data.encode('utf-8')
    request = urllib.request.Request('http://linkdecrypter.com/')
    request.add_header('Content-Type', 'application/x-www-form-urlencoded;charset=utf-8')
    request.add_header('cookie', 'PHPSESSID=7p88jo0pkaek7vf6qei550ops4')
    f = urllib.request.urlopen(request, data)
    request2 = urllib.request.Request('http://linkdecrypter.com/')
    request2.add_header('cookie', 'PHPSESSID=7p88jo0pkaek7vf6qei550ops4')
    f2 = urllib.request.urlopen(request2)
    soup = BeautifulSoup(f2.read().decode('utf-8'))
    textarea = soup.find('textarea', {'class': 'caja_des'})
    if textarea != None:
        return textarea.getText().split('\n')
    else:
        return
        return