# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/compactxml/resolve.py
# Compiled at: 2010-03-09 13:22:00
import urllib2

def resolve_filename(location):
    return open(location, 'r').read()


def resolve_url(location):
    return urllib2.urlopen(location).read()