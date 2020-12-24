# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/auth.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 2299 bytes
"""Authorization management:
- Helpers to add and fetch principals.
"""
import logging
from pyramid import security
from xbus.monitor.models.monitor import DBSession
from xbus.monitor.models.monitor import User
log = logging.getLogger(__name__)
DATA_CLEARING_GROUP = 'xbus_data_clearer'
MANAGER_GROUP = 'xbus_manager'
UPLOADER_GROUP = 'xbus_uploader'
_USER_PREFIX = 'user:'
_DEFAULT_PRINCIPALS = set((security.Everyone, security.Authenticated))

def user_principal(user_id):
    return '%s%s' % (_USER_PREFIX, user_id)


def get_user_principals(login, request=None):
    """Gather security groups for the specified user.
    @return Pyramid principal list.
    """
    log.debug('Fetching principals for the user %s', login)
    principals = _DEFAULT_PRINCIPALS.copy()
    db_session = DBSession()
    user = db_session.query(User).filter(User.user_name == login).first()
    if not user:
        return principals
    principals.add(user_principal(user.user_id))
    if request and 'authentic_roles' in request.session:
        principals.update(request.session['authentic_roles'])
    else:
        principals.update(permission.permission_name for group in user.group_list for permission in group.permission_list)
    return list(principals)


def _get_logged_entities(request, security_prefix):
    """Find IDs of entities pointed to by principals starting with the
    specified prefix.
    """
    return [principal[len(security_prefix):] for principal in security.effective_principals(request) if principal.startswith(security_prefix)]


def get_logged_user_id(request):
    return _get_logged_entities(request, _USER_PREFIX)[0]