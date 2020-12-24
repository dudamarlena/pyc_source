# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/standalone/conf.py
# Compiled at: 2010-03-07 07:27:28
"""
This is a collection of utilities to setup the environment
for a standalone django script. This uses option parsers and
fake django settings.
"""

def settings(**kw):
    """
    This function returns the settings that are created for
    a simple sqlite3 database with a given file name. The
    settings are preconfigured so you can actually do normal
    chores with them.

    It uses sqlite3 as default for the database engine because
    that is based on a driver that will be preinstalled in
    modern python installations.

    You can pass in anything you want the settings to carry
    as named parameters - values from the parameter list will
    override potential library defaults.
    """
    from django.conf import settings
    if 'DATABASE_ENGINE' not in kw:
        kw['DATABASE_ENGINE'] = 'sqlite3'
    if 'INSTALLED_APPS' in kw:
        kw['INSTALLED_APPS'] = kw['INSTALLED_APPS'] + ('standalone', )
    else:
        kw['INSTALLED_APPS'] = ('standalone', )
    settings.configure(**kw)
    return settings