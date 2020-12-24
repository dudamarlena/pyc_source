# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/plone-production-nbf-1/zeocluster/src/Products.BlobNewsItem/PasteDeploy-1.5.0-py2.6.egg/paste/deploy/compat.py
# Compiled at: 2012-02-27 07:41:55
__doc__ = 'Python 2<->3 compatibility module'
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