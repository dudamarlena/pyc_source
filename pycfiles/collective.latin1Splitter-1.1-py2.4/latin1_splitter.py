# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/latin1Splitter/latin1_splitter.py
# Compiled at: 2009-12-22 10:28:10
"""
Latin1 Splitter - Latin1 word splitter for ZCTextIndex
"""
from Products.ZCTextIndex.ISplitter import ISplitter
from Products.ZCTextIndex.PipelineFactory import element_factory
import re
from types import StringType

def getSupportedEncoding(encodings):
    return 'utf-8'


rxNormal = re.compile('[a-zA-Z0-9_]+|[\\uc0-\\uff]+', re.UNICODE)
rxGlob = re.compile('[a-zA-Z0-9_]+[*?]*|[\\uc0-\\uff]+[*?]*', re.UNICODE)

class Latin1Splitter:
    __module__ = __name__
    default_encoding = 'utf-8'
    accDict = {'À': 'A', 'Á': 'A', 'Â': 'A', 'Ã': 'A', 'Ä': 'A', 'Å': 'A', 'Æ': 'AE', 'à': 'a', 'Â': 'a', 'Ã': 'a', 'Ä': 'a', 'Å': 'a', 'Æ': 'a', 'Æ': 'a', 'Æ': 'ae', 'Ç': 'C', 'ç': 'c', 'È': 'E', 'É': 'E', 'Ê': 'E', 'Ë': 'E', 'è': 'e', 'é': 'e', 'ê': 'e', 'ë': 'e', 'Ì': 'I', 'Í': 'I', 'Î': 'I', 'Ï': 'I', 'ì': 'i', 'í': 'i', 'î': 'i', 'ï': 'i', 'Ù': 'U', 'Ú': 'U', 'Û': 'U', 'Ü': 'U', 'ù': 'u', 'ú': 'u', 'û': 'u', 'ü': 'u'}

    def process(self, lst, isGlob=0):
        result = []
        if isGlob:
            rx = rxGlob
        else:
            rx = rxNormal
        for s in lst:
            if type(s) is StringType:
                s = unicode(s, self.default_encoding, 'replace')
            deaccented = self.accent_replace(s)
            splitted = rx.findall(deaccented)
            for w in splitted:
                result.append(w)

        return result

    def processGlob(self, lst):
        return self.process(lst, 1)

    def accent_replace(self, text):
        rx = re.compile(('|').join(map(re.escape, self.accDict)))

        def one_xlat(match):
            return self.accDict[match.group(0)]

        return rx.sub(one_xlat, text)