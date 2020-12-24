# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/Products/BigramSplitter/BigramSplitter.py
# Compiled at: 2010-01-29 02:38:04
"""
BigramSplitter.py

Created by Mikio Hokari, CMScom and Manabu Terada, CMScom on 2009-09-30.
"""
import unicodedata
from Products.ZCTextIndex.ISplitter import ISplitter
from Products.ZCTextIndex.PipelineFactory import element_factory
from Products.CMFPlone.utils import classImplements
from Products.BigramSplitter.config import rx_U, rxGlob_U, rx_L, rxGlob_L, rx_all, pattern, pattern_g

def bigram(u, limit=1):
    u""" Split into bi-gram.
    limit arg describes ending process.
    If limit = 0 then
        日本人-> [日本,本人, 人]
        金 -> [金]
    If limit = 1 then
        日本人-> [日本,本人]
        金 -> []
    """
    return [ u[i:i + 2] for i in xrange(len(u) - limit) ]


def process_str_post(s, enc):
    """Receive str, remove ? and *, then return str.
    If decode gets successful, process str as unicode.
    If decode gets failed, process str as ASCII.
    """
    try:
        if not isinstance(s, unicode):
            uni = s.decode(enc, 'strict')
        else:
            uni = s
    except UnicodeDecodeError, e:
        return s.replace('?', '').replace('*', '')

    try:
        return uni.replace('?', '').replace('*', '').encode(enc, 'strict')
    except UnicodeEncodeError, e:
        return s.replace('?', '').replace('*', '')


def process_str(s, enc):
    """Receive str and encoding, then return the list 
    of str as bi-grammed result.
    Decode str into unicode and pass it to process_unicode.
    When decode failed, return the result splitted per word.
    Splitting depends on locale specified by rx_L.
    """
    try:
        if not isinstance(s, unicode):
            uni = s.decode(enc, 'strict')
        else:
            uni = s
    except UnicodeDecodeError, e:
        return rx_L.findall(s)

    bigrams = process_unicode(uni)
    return [ x.encode(enc, 'strict') for x in bigrams ]


def process_str_glob(s, enc):
    """Receive str and encoding, then return the list
    of str considering glob processing.
    Decode str into unicode and pass it to process_unicode_glob.
    When decode failed, return the result splitted per word.
    Splitting depends on locale specified by rxGlob_L.
    """
    try:
        if not isinstance(s, unicode):
            uni = s.decode(enc, 'strict')
        else:
            uni = s
    except UnicodeDecodeError, e:
        return rxGlob_L.findall(s)

    bigrams = process_unicode_glob(uni)
    return [ x.encode(enc, 'strict') for x in bigrams ]


def process_unicode(uni):
    """Receive unicode string, then return a list of unicode
    as bi-grammed result.
    """
    normalized = unicodedata.normalize('NFKC', uni)
    for word in rx_U.findall(normalized):
        swords = [ g.group() for g in pattern.finditer(word) ]
        for sword in swords:
            if not rx_all.match(sword[0]):
                yield sword
            else:
                for x in bigram(sword, 0):
                    yield x


def process_unicode_glob(uni):
    """Receive unicode string, then return a list of unicode
    as bi-grammed result.  Considering globbing.
    """
    normalized = unicodedata.normalize('NFKC', uni)
    for word in rxGlob_U.findall(normalized):
        swords = [ g.group() for g in pattern_g.finditer(word) if g.group() not in '*?' ]
        for (i, sword) in enumerate(swords):
            if not rx_all.match(sword[0]):
                yield sword
            else:
                if i == len(swords) - 1:
                    limit = 1
                else:
                    limit = 0
                if len(sword) == 1:
                    bigramed = [
                     sword + '*']
                else:
                    bigramed = bigram(sword, limit)
                for x in bigramed:
                    yield x


class BigramSplitter(object):
    __module__ = __name__
    meta_type = 'BigramSplitter'
    __implements__ = ISplitter

    def process(self, lst):
        """ Will be called when indexing.
        Receive list of str, make it bi-grammed, then return
        the list of str.
        """
        enc = 'utf-8'
        result = [ x for s in lst for x in process_str(s, enc) ]
        return result

    def processGlob(self, lst):
        """ Will be called once when searching.
        Receive list of str, make it bi-grammed considering
        globbing, then return the list of str.
        """
        enc = 'utf-8'
        result = [ x for s in lst for x in process_str_glob(s, enc) ]
        return result

    def process_post_glob(self, lst):
        """ Will be called twice when searching.
        Receive list of str, Remove ? and *, then return
        the list of str.
        """
        enc = 'utf-8'
        result = [ process_str_post(s, enc) for s in lst ]
        return result


classImplements(BigramSplitter, BigramSplitter.__implements__)
try:
    element_factory.registerFactory('Word Splitter', 'Bigram Splitter', BigramSplitter)
except ValueError:
    pass

class BigramCaseNormalizer(object):
    __module__ = __name__

    def process(self, lst):
        enc = 'utf-8'
        result = []
        for s in lst:
            try:
                if not isinstance(s, unicode):
                    s = unicode(s, enc)
            except (UnicodeDecodeError, TypeError):
                result.append(s.lower())
            else:
                result.append(s.lower().encode(enc))

        return result


try:
    element_factory.registerFactory('Case Normalizer', 'Bigram Case Normalizer', BigramCaseNormalizer)
except ValueError:
    pass