# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/sharpertool/proj/pypi/django-comments-tree/docs/extensions.py
# Compiled at: 2019-04-11 11:47:11
# Size of source mod 2**32: 621 bytes


def setup(app):
    app.add_crossref_type(directivename='setting',
      rolename='setting',
      indextemplate='pair: %s; setting')
    app.add_crossref_type(directivename='templatetag',
      rolename='ttag',
      indextemplate='pair: %s; template tag')
    app.add_crossref_type(directivename='templatefilter',
      rolename='tfilter',
      indextemplate='pair: %s; template filter')
    app.add_crossref_type(directivename='class',
      rolename='pclass',
      indextemplate='pair: %s; class')