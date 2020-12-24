# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/wsgi/debug/utils.py
# Compiled at: 2010-10-22 05:20:19
__doc__ = "\n    werkzeug.debug.utils\n    ~~~~~~~~~~~~~~~~~~~~\n\n    This module paches werkzeug's debug template to mako\n\n    delived from one by Armin Ronacher.\n"
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