# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/mg_globals.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 2115 bytes
"""
In some places, we need to access the database, public_store, queue_store
"""
import gettext, pkg_resources, threading, six
database = None
public_store = None
queue_store = None
workbench_manager = None
thread_scope = threading.local()
thread_scope.translations = gettext.translation('mediagoblin', pkg_resources.resource_filename('mediagoblin', 'i18n'), ['en'], fallback=True)
app_config = None
global_config = None
app = None

def setup_globals(**kwargs):
    """
    Sets up a bunch of globals in this module.

    Takes the globals to setup as keyword arguments.  If globals are
    specified that aren't set as variables above, then throw an error.
    """
    from mediagoblin import mg_globals
    for key, value in six.iteritems(kwargs):
        assert hasattr(mg_globals, key), 'Global %s not known' % key
        setattr(mg_globals, key, value)