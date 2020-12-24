# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/wsgi/debug/utils.py
# Compiled at: 2010-10-22 05:20:19
"""
    werkzeug.debug.utils
    ~~~~~~~~~~~~~~~~~~~~

    This module paches werkzeug's debug template to mako

    delived from one by Armin Ronacher.
"""
__author__ = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'
__licence__ = 'BSD'
from os.path import join, dirname
from mako.lookup import TemplateLookup
from mako import exceptions
tlookup = TemplateLookup(directories=[join(dirname(__file__), 'templates')], disable_unicode=False)

def get_template(filename):
    return tlookup.get_template(filename)


def render_template(template_filename, **context):
    t = get_template(template_filename)
    try:
        return t.render(**context)
    except:
        return exceptions.html_error_template().render()