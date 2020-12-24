# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/amundsen_common/log/auth_caller_retrieval.py
# Compiled at: 2020-02-13 16:36:56
# Size of source mod 2**32: 377 bytes
import getpass
from flask import current_app as flask_app
from amundsen_common.log.caller_retrieval import BaseCallerRetriever

class AuthCallerRetrieval(BaseCallerRetriever):

    def get_caller(self) -> str:
        if flask_app.config.get('AUTH_USER_METHOD', None):
            return flask_app.config['AUTH_USER_METHOD'](flask_app).email
        return getpass.getuser()