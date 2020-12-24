# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/divimon/lib/helpers.py
# Compiled at: 2008-07-28 05:37:25
"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from pylons import g
import webhelpers
from webhelpers import *

def javascript_include_tag(*args, **kw):
    tags = webhelpers.javascript_include_tag(*args, **kw)
    return tags.replace('src="/', 'src="%s/' % g.base_url).replace('href="/', 'href="%s/' % g.base_url)


def url_for(**kw):
    url = webhelpers.url_for(**kw)
    return '%s%s' % (g.base_url, url)


def cgi_for(**kw):
    args = []
    for (k, v) in kw.iteritems():
        if isinstance(v, list):
            for val in v:
                args.append('%s=%s' % (k, val))

        else:
            args.append('%s=%s' % (k, v))

    return ('&amp;').join(args)


def strip_prefix(number):
    for prefix in g.prefixes:
        number = prefix.sub('', number)

    return number