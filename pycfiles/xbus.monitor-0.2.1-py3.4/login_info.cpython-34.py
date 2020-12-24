# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xbus/monitor/views/login_info.py
# Compiled at: 2016-06-27 04:20:00
# Size of source mod 2**32: 1186 bytes
import hashlib
from pyramid.security import NO_PERMISSION_REQUIRED
from pyramid.view import view_config
from xbus.monitor.models.monitor import DBSession
from xbus.monitor.models.monitor import User

@view_config(route_name='login_info', request_method='GET', permission=NO_PERMISSION_REQUIRED, renderer='json', http_cache=0)
def login_info(request):
    """Get information about the connected user.
    """
    login = request.authenticated_userid
    if not login:
        return {'login': login}
    db_session = DBSession()
    user = db_session.query(User).filter(User.user_name == login).first()
    if not user:
        return {'login': login}
    email = user.email_address
    avatar_url = 'http://www.gravatar.com/avatar/%s' % hashlib.md5(email.encode('utf-8')).hexdigest()
    return {'avatar_url': avatar_url, 
     'display_name': user.display_name, 
     'email': email, 
     'login': login}