# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pf3/pdf/fo.py
# Compiled at: 2014-08-15 05:01:34
# Size of source mod 2**32: 1330 bytes
import logging, traceback
COMMASPACE = ', '

class fo:
    obj = {}
    pages = []
    defaultFont = {'family': 'Times Roman', 
     'size': '12pt'}

    def __init__(self):
        self.logger = logging.getLogger('pf3')
        self.addPage(1)

    def addPage(self, page_number, page):
        if len(self.pages) < page_number:
            p = len(self.pages)
            while p < page_number - 1:
                self.pages[p] = {}
                p += 1

        self.pages[page_number] = page

    def addPageElement(self, page_number, element):
        page = self.getPage(page_number)
        self.pages['page_number']['elements'].append(element)

    def getPage(self, page_number):
        return self.pages[(page_number - 1)]

    def toXml(self):
        result = '<fo:root xmlns:fo="http://www.w3.org/1999/XSL/Format" font-family="' + self.defaultFont['family'] + ' font-size=' + self.defaultFont['family'] + '">'
        result += '<fo:layout-master-set>'
        result += '<fo:page-sequence>'
        result += '</fo:page-sequence>'
        result += '</fo:layout-master-set>'
        result += '</fo:root>'
        return result