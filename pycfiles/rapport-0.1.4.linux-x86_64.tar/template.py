# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/rapport/template.py
# Compiled at: 2013-07-30 09:03:11
from __future__ import print_function
import os, sys, jinja2

def _get_template_dirs(type='plugin'):
    """Return a list of directories where templates may be located.
    """
    template_dirs = [
     os.path.expanduser(os.path.join('~', '.rapport', 'templates', type)),
     os.path.join('rapport', 'templates', type)]
    return template_dirs


_JINJA2_ENV = {}

def init():
    for type in ['plugin', 'email', 'web']:
        loader = jinja2.FileSystemLoader(_get_template_dirs(type))
        env = jinja2.Environment(loader=loader, extensions=[
         'jinja2.ext.i18n', 'jinja2.ext.loopcontrols'], line_statement_prefix='%%', line_comment_prefix='##', trim_blocks=True)
        env.install_null_translations(newstyle=False)
        _JINJA2_ENV[type] = env


def get_template(name, format='text', type='plugin'):
    if not _JINJA2_ENV:
        init()
    template_name = ('{0}.{1}.jinja2').format(name, format)
    try:
        return _JINJA2_ENV[type].get_template(template_name)
    except jinja2.TemplateNotFound:
        print(('Missing template {0}/{1}!').format(type, template_name), file=sys.stderr)