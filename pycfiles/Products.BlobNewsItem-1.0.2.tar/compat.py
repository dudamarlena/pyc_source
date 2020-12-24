# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteDeploy-1.5.0-py2.6.egg/paste/deploy/compat.py
# Compiled at: 2012-02-27 07:41:55
"""Python 2<->3 compatibility module"""
import sys

def print_(template, *args, **kwargs):
    template = str(template)
    if args:
        template = template % args
    elif kwargs:
        template = template % kwargs
    sys.stdout.writelines(template)


if sys.version_info < (3, 0):
    basestring = basestring
    from ConfigParser import ConfigParser
    from urllib import unquote
    iteritems = lambda d: d.iteritems()

    def reraise(t, e, tb):
        exec (
         'raise t, e, tb', dict(t=t, e=e, tb=tb))


else:
    basestring = str
    from configparser import ConfigParser
    from urllib.parse import unquote
    iteritems = lambda d: d.items()

    def reraise(t, e, tb):
        exec (
         'raise e from tb', dict(e=e, tb=tb))