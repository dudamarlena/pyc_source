# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/compactxml/resolve.py
# Compiled at: 2010-03-09 13:22:00
import urllib2

def resolve_filename(location):
    return open(location, 'r').read()


def resolve_url(location):
    return urllib2.urlopen(location).read()