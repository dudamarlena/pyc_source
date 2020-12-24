# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/GRSplitter/GRSplitter.py
# Compiled at: 2008-07-02 04:44:30
"""
GRSplitter - Greek word splitter for ZCTextIndex

(C) G. Gozadinoso
http://qiweb.net
ggozad _at_ qiweb.net
License: see LICENSE.txt

"""
from Products.ZCTextIndex.ISplitter import ISplitter
from Products.ZCTextIndex.PipelineFactory import element_factory
import re
from types import StringType

def getSupportedEncoding(encodings):
    return 'utf-8'


rxNormal = re.compile('[a-zA-Z0-9_]+|[Ͱ-Ͽ]+', re.UNICODE)
rxGlob = re.compile('[a-zA-Z0-9_]+[*?]*|[Ͱ-Ͽ]+[*?]*', re.UNICODE)

class GRSplitter:
    __module__ = __name__
    default_encoding = 'utf-8'
    accDict = {'ά': 'α', 'Ά': 'Α', 'έ': 'ε', 'Έ': 'Ε', 'ή': 'η', 'Ή': 'Η', 'ί': 'ι', 'ϊ': 'ι', 'ΐ': 'ι', 'Ί': 'Ι', 'Ϊ': 'Ι', 'ό': 'ο', 'Ό': 'Ο', 'ύ': 'υ', 'ϋ': 'υ', 'ΰ': 'υ', 'Ύ': 'Υ', 'Ϋ': 'Υ', 'ώ': 'ω', 'Ώ': 'Ω'}

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