# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/spectras/projects/hvad/django-hvad/docs/_ext/djangodocs.py
# Compiled at: 2015-12-22 11:30:12
# Size of source mod 2**32: 808 bytes


def setup(app):
    app.add_crossref_type(directivename='label', rolename='djterm', indextemplate='pair: %s; label')
    app.add_crossref_type(directivename='setting', rolename='setting', indextemplate='pair: %s; setting')
    app.add_crossref_type(directivename='templatetag', rolename='ttag', indextemplate='pair: %s; template tag')
    app.add_crossref_type(directivename='templatefilter', rolename='tfilter', indextemplate='pair: %s; template filter')
    app.add_crossref_type(directivename='fieldlookup', rolename='lookup', indextemplate='pair: %s; field lookup type')