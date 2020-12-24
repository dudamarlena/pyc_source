# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: scrp/error_page.py
# Compiled at: 2018-02-17 10:40:37
from bs4 import BeautifulSoup

def isErrorPageFromSoup(soup):
    print 'starting isErrorPageFromSoup with', len(soup.text)
    text = soup.text.lower().strip()
    for phrase in ('غير موجود', '404'):
        print 'phrase is', [phrase]
        if phrase in text:
            return True

    return False


def isErrorPageFromHtmlText(html):
    return isErrorPageFromSoup(BeautifulSoup(html, 'html5lib'))


def isErrorPageFromTextContent(textContent):
    textContent = textContent.lower().strip()
    for phrase in ['غير موجود', '404']:
        if phrase in textContent:
            return True

    return False