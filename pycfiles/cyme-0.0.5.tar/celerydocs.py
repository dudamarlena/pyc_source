# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/devel/cyme/docs/_ext/celerydocs.py
# Compiled at: 2011-11-29 10:38:59


def setup(app):
    app.add_crossref_type(directivename='setting', rolename='setting', indextemplate='pair: %s; setting')
    app.add_crossref_type(directivename='sig', rolename='sig', indextemplate='pair: %s; sig')
    app.add_crossref_type(directivename='state', rolename='state', indextemplate='pair: %s; state')
    app.add_crossref_type(directivename='control', rolename='control', indextemplate='pair: %s; control')
    app.add_crossref_type(directivename='signal', rolename='signal', indextemplate='pair: %s; signal')