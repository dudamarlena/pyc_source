# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kipe/workspace/raspautomation_v2/cli/venv/lib/python2.7/site-packages/raspautomation_cli/utils.py
# Compiled at: 2016-05-27 19:16:11
import click
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

class URIParamType(click.ParamType):
    name = 'uri'

    def convert(self, value, param, ctx):
        try:
            parsed = urlparse(value)
            return '%s://%s%s' % (
             parsed.scheme,
             parsed.netloc,
             parsed.path if parsed.path else '/')
        except:
            self.fail('%s is not a valid URL' % value)


URI = URIParamType()