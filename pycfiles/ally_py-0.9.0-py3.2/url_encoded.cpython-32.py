# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ally/core/http/impl/url_encoded.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Apr 24, 2012

@package: ally core http
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Mihai Balaceanu

Provides the x-www-form-urlencoded decoding 
"""
from urllib.parse import unquote
from re import compile
PARSE_RGEXES = (
 compile('\\+'),
 compile('(?<=\\[)[^]]*(?=\\])'),
 compile('^([^[]+)'))

def parseStr(theString):
    """
    php parse_str function port to python
    @see: http://php.net/parse_str
    @author: Mihai Balaceanu
    """
    replace, keyFindNested, keyFind = PARSE_RGEXES
    paramPairArray, ret = theString.split('&'), {}
    for paramPair in paramPairArray:
        try:
            key, value = paramPair.split('=')
        except:
            key, value = paramPair, None

        value = unquote(replace.sub(' ', value)) if value is not None else value
        key = unquote(key).strip()
        keyEnd = key.find('\x00')
        if keyEnd != -1:
            key = key[:keyEnd]
        if not key:
            continue
        keys = keyFindNested.findall(key)
        keys[:0] = keyFind.findall(key)
        curRet = ret
        keysLen = len(keys)
        for k in range(keysLen):
            if keys[k].strip() == '':
                if not isinstance(curRet, list):
                    curRet[keys[(k - 1)]] = []
                    curRet = curRet[keys[(k - 1)]]
                if keysLen - 1 == k:
                    curRet.append(value)
            elif keys[k] not in curRet:
                if isinstance(curRet, list):
                    curRet.append({keys[k]: value if keysLen - 1 == k else {}})
                    curRet = curRet[(-1)]
                else:
                    if keysLen - 1 == k:
                        curRet[keys[k]] = value
                    else:
                        if keys[(k + 1)].strip() == '':
                            curRet[keys[k]] = []
                        else:
                            curRet[keys[k]] = {}
                    curRet = curRet[keys[k]]
            else:
                curRet = curRet[keys[k]]

    return ret