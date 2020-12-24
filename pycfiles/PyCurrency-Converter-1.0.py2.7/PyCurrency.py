# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/PyCurrency_Converter/PyCurrency.py
# Compiled at: 2016-11-23 09:29:20
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

try:
    from bs4 import BeautifulSoup
except ImportError:
    import BeautifulSoup

class PyCurrency:

    @staticmethod
    def convert(amount, _from, _to):
        url = ('https://www.google.com/finance/converter?a={}&from={}&to={}').format(amount, _from, _to)
        response = urllib2.urlopen(url)
        html = response.read()
        parsed = BeautifulSoup(html, 'lxml').body.find('span', attrs={'class': 'bld'}).text
        return parsed

    @staticmethod
    def codes():
        url = 'https://www.google.com/finance/converter'
        response = urllib2.urlopen(url)
        html = response.read()
        parser = BeautifulSoup(html, 'lxml').body.find_all('option')
        for code in parser:
            code = str(code).strip().split('<')[1]
            print code.strip().split('>')[(-1)]


def convert(amount, _from, _to):
    return PyCurrency.convert(amount, _from, _to)


def codes():
    return PyCurrency.codes()