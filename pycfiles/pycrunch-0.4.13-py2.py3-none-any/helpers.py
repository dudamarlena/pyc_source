# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pycrud/lib/helpers.py
# Compiled at: 2008-06-20 03:40:59
__doc__ = "Helper functions\n\nConsists of functions to typically be used within templates, but also\navailable to Controllers. This module is available to both as 'h'.\n"
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