# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/sqlmap/lib/request/comparison.py
# Compiled at: 2013-12-09 06:41:17
"""
Copyright (c) 2006-2013 sqlmap developers (http://sqlmap.org/)
See the file 'doc/COPYING' for copying permission
"""
import re
from lib.core.common import extractRegexResult
from lib.core.common import getFilteredPageContent
from lib.core.common import listToStrValue
from lib.core.common import removeDynamicContent
from lib.core.common import wasLastResponseDBMSError
from lib.core.common import wasLastResponseHTTPError
from lib.core.data import conf
from lib.core.data import kb
from lib.core.data import logger
from lib.core.exception import SqlmapNoneDataException
from lib.core.settings import DEFAULT_PAGE_ENCODING
from lib.core.settings import DIFF_TOLERANCE
from lib.core.settings import HTML_TITLE_REGEX
from lib.core.settings import MIN_RATIO
from lib.core.settings import MAX_RATIO
from lib.core.settings import REFLECTED_VALUE_MARKER
from lib.core.settings import LOWER_RATIO_BOUND
from lib.core.settings import UPPER_RATIO_BOUND
from lib.core.threads import getCurrentThreadData

def comparison(page, headers, code=None, getRatioValue=False, pageLength=None):
    _ = _adjust(_comparison(page, headers, code, getRatioValue, pageLength), getRatioValue)
    return _


def _adjust(condition, getRatioValue):
    if not any((conf.string, conf.notString, conf.regexp, conf.code)):
        retVal = not condition if kb.negativeLogic and condition is not None and not getRatioValue else condition
    else:
        retVal = condition if not getRatioValue else (MAX_RATIO if condition else MIN_RATIO)
    return retVal


def _comparison(page, headers, code, getRatioValue, pageLength):
    threadData = getCurrentThreadData()
    if kb.testMode:
        threadData.lastComparisonHeaders = listToStrValue(headers.headers) if headers else ''
        threadData.lastComparisonPage = page
    if page is None and pageLength is None:
        return
    else:
        seqMatcher = threadData.seqMatcher
        seqMatcher.set_seq1(kb.pageTemplate)
        if any((conf.string, conf.notString, conf.regexp)):
            rawResponse = '%s%s' % (listToStrValue(headers.headers) if headers else '', page)
            if conf.string:
                return conf.string in rawResponse
            if conf.notString:
                return conf.notString not in rawResponse
            if conf.regexp:
                return re.search(conf.regexp, rawResponse, re.I | re.M) is not None
        if conf.code:
            return conf.code == code
        if page:
            if kb.errorIsNone and (wasLastResponseDBMSError() or wasLastResponseHTTPError()):
                return
            if not kb.nullConnection:
                page = removeDynamicContent(page)
                seqMatcher.set_seq1(removeDynamicContent(kb.pageTemplate))
            if not pageLength:
                pageLength = len(page)
        if kb.nullConnection and pageLength:
            if not seqMatcher.a:
                errMsg = 'problem occurred while retrieving original page content '
                errMsg += 'which prevents sqlmap from continuation. Please rerun, '
                errMsg += 'and if the problem persists turn off any optimization switches'
                raise SqlmapNoneDataException(errMsg)
            ratio = 1.0 * pageLength / len(seqMatcher.a)
            if ratio > 1.0:
                ratio = 1.0 / ratio
        else:
            if isinstance(seqMatcher.a, str) and isinstance(page, unicode):
                page = page.encode(kb.pageEncoding or DEFAULT_PAGE_ENCODING, 'ignore')
            else:
                if isinstance(seqMatcher.a, unicode) and isinstance(page, str):
                    seqMatcher.a = seqMatcher.a.encode(kb.pageEncoding or DEFAULT_PAGE_ENCODING, 'ignore')
                seq1, seq2 = (None, None)
                if conf.titles:
                    seq1 = extractRegexResult(HTML_TITLE_REGEX, seqMatcher.a)
                    seq2 = extractRegexResult(HTML_TITLE_REGEX, page)
                else:
                    seq1 = getFilteredPageContent(seqMatcher.a, True) if conf.textOnly else seqMatcher.a
                    seq2 = getFilteredPageContent(page, True) if conf.textOnly else page
                if seq1 is None or seq2 is None:
                    return
                seq1 = seq1.replace(REFLECTED_VALUE_MARKER, '')
                seq2 = seq2.replace(REFLECTED_VALUE_MARKER, '')
                count = 0
                while count < min(len(seq1), len(seq2)):
                    if seq1[count] == seq2[count]:
                        count += 1
                    else:
                        break

                if count:
                    seq1 = seq1[count:]
                    seq2 = seq2[count:]
                seqMatcher.set_seq1(seq1)
                seqMatcher.set_seq2(seq2)
                ratio = round(seqMatcher.quick_ratio(), 3)
            if kb.matchRatio is None:
                if ratio >= LOWER_RATIO_BOUND and ratio <= UPPER_RATIO_BOUND:
                    kb.matchRatio = ratio
                    logger.debug('setting match ratio for current parameter to %.3f' % kb.matchRatio)
            if getRatioValue:
                return ratio
            if ratio > UPPER_RATIO_BOUND:
                return True
            if kb.matchRatio is None:
                return
        return ratio - kb.matchRatio > DIFF_TOLERANCE
        return