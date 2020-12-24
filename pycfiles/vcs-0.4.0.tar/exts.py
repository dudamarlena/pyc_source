# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lukasz/develop/workspace/vcs/docs/exts.py
# Compiled at: 2013-02-18 15:07:34


def setup(app):
    app.add_crossref_type(directivename='command', rolename='command', indextemplate='pair: %s; command')
    app.add_crossref_type(directivename='setting', rolename='setting', indextemplate='pair: %s; setting')