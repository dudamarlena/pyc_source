# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/Products/BigramSplitter/config.py
# Compiled at: 2010-01-29 02:38:04
import re
STOP_WORD = []
rangetable = dict(hangul='가-\ud7af', cj='\u3040-ヿ一-\u9fff㐀-\u4dbf豈-\ufaff', thai='\u0e00-\u0e7f')
ps = rangetable.values()
allp = ('').join(ps)
glob_true = '[^%s]([^%s]|[\\*\\?])*|' % (allp, allp) + ('|').join([ '[%s]+' % (x,) for x in ps ])
glob_false = '[^%s]+|' % allp + ('|').join(('[%s]+' % x for x in ps))
rx_all = re.compile('[%s]' % allp, re.UNICODE)
rx_U = re.compile('\\w+', re.UNICODE)
rxGlob_U = re.compile('\\w+[\\w*?]*', re.UNICODE)
rx_L = re.compile('\\w+', re.LOCALE)
rxGlob_L = re.compile('\\w+[\\w*?]*', re.LOCALE)
pattern = re.compile(glob_false, re.UNICODE)
pattern_g = re.compile(glob_true, re.UNICODE)