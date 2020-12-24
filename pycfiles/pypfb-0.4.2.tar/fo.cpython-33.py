# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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