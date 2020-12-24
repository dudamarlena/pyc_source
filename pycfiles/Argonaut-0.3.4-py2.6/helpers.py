# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/lib/helpers.py
# Compiled at: 2011-02-19 07:56:00
"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to templates as 'h'.
"""
from pylons import url
from argonaut.model import *
from argonaut.model import forms
from argonaut.lib.base import render
import argonaut.lib.timehelpers as timehelpers, argonaut.lib.authentication as authentication, argonaut.lib.mailer as mailer
from webhelpers.html import literal
from webhelpers.html.tools import auto_link
from webhelpers.html.tags import *
from webhelpers.text import urlify
from webhelpers.util import *
from webhelpers.html.builder import escape
import argonaut.lib.version as version

def format_environ(environ):
    result = []
    keys = environ.keys()
    keys.sort()
    for key in keys:
        result.append('%s: %r' % (key, environ[key]))

    return ('\n').join(result)


def resolve_page_url(page_id):
    page_url = page.get_url(page_id)
    if page_url:
        return page_url
    else:
        return page_type.get_url(page.get_page_type_id(page_id), page.get_url_param(page_id))