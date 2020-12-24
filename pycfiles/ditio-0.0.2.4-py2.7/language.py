# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ditio/notebook/language.py
# Compiled at: 2018-01-30 20:16:16


class Python:
    COMMENT = '#'
    EXTENSION = '.py'


class Java:
    COMMENT = '//'
    EXTENSION = '.java'


class Clojure:
    COMMENT = ';;'
    EXTENSION = '.cjs'


class Groovy:
    COMMENT = '//'
    EXTENSION = '.groovy'


class Javascript:
    COMMENT = '//'
    EXTENSION = '.js'


__language__ = None

def set(l):
    global __language__
    __language__ = l


def get():
    return __language__