# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jmcarp/miniconda/envs/guardian/lib/python2.7/site-packages/examples/flask_sqla/permissions.py
# Compiled at: 2015-04-05 12:09:17
from __future__ import absolute_import
import httplib, functools, flask
from flask.ext.login import current_user
from guardrail.core import decorators
from guardrail.ext.sqlalchemy import SqlalchemyLoader
from guardrail.ext.sqlalchemy import SqlalchemyPermissionManager
import models
manager = SqlalchemyPermissionManager(models.db.session)

def user_loader(*args, **kwargs):
    return current_user._get_current_object()


error_messages = {decorators.AGENT_NOT_FOUND: httplib.NOT_FOUND, 
   decorators.TARGET_NOT_FOUND: httplib.NOT_FOUND, 
   decorators.FORBIDDEN: httplib.FORBIDDEN}

def error_handler(message):
    flask.abort(error_messages.get(message, httplib.INTERNAL_SERVER_ERROR))


has_permission = functools.partial(decorators.has_permission, manager=manager, agent_loader=user_loader, error_handler=error_handler)
has_post_permission = functools.partial(has_permission, target_loader=SqlalchemyLoader(models.Post, models.db.session))