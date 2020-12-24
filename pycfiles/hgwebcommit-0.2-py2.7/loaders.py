# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hgwebcommit/actions/loaders.py
# Compiled at: 2011-10-28 19:16:45
from werkzeug import import_string
from hgwebcommit import app

class ActionLoader(object):

    def load_actions(self):
        action_modules = app.config.get('HGWEBCOMMIT_ACTIONS') or []
        for mod_name in action_modules:
            mod = import_string(mod_name)