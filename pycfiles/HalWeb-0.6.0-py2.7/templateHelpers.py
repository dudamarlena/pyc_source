# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/lib/templateHelpers.py
# Compiled at: 2011-12-25 05:31:43
from config import djangoVars

def convertToTemplate(text, input={}):
    result = text
    for k, v in djangoVars.iteritems():
        result = result.replace(v, '{-{' + k + '}-}')

    for k, v in input.iteritems():
        result = result.replace(v, '{-{' + k + '}-}')

    result = result.replace('{-{', '{{')
    result = result.replace('}-}', '}}')
    return result


def convertToReal(text, input={}):
    result = text
    for k, v in djangoVars.iteritems():
        result = result.replace(k, v)

    for k, v in input.iteritems():
        result = result.replace(k, v)

    return result