# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/lib/auth.py
# Compiled at: 2016-09-19 13:27:02
"""Modules containing functionality used by numerous other modules.

.. module:: lib
   :synopsis: functionality used by numerous other modules.

"""
import simplejson as json
from decorator import decorator
from pylons import session, response
from utils import unauthorized_msg
import logging
log = logging.getLogger(__name__)

def authenticate(target):
    """Authentication decorator.
    
    If user is not logged in and tries to call a controller action with this
    decorator, then the response header status will be ``401 Unauthorized`` and
    the response body will be ``{error: "401 Unauthorized"}``.
    """

    def wrapper(target, *args, **kwargs):
        if getattr(session.get('user'), 'username', None):
            return target(*args, **kwargs)
        else:
            response.status_int = 401
            return {'error': 'Authentication is required to access this resource.'}

    return decorator(wrapper)(target)


def authenticate_with_JSON(target):
    """Authentication decorator that returns JSON error messages.
    
    Identical to the authenticate decorator except that the response body is
    json.dumped beforehand.  This is decorator is only needed in those few
    actions whose successful output is not JSON, e.g., the actions that serve
    file data, cf. the ``serve`` and ``serve_file`` actions of the
    ``FilesController`` and ``CorporaController``.
    
    """

    def wrapper(target, *args, **kwargs):
        if getattr(session.get('user'), 'username', None):
            return target(*args, **kwargs)
        else:
            response.status_int = 401
            return json.dumps({'error': 'Authentication is required to access this resource.'})

    return decorator(wrapper)(target)


def authorize(roles, users=None, user_id_is_args1=False):
    """Authorization decorator.  If user tries to request a controller action
    but has insufficient authorization, this decorator will respond with a
    header status of '403 Forbidden' and a JSON object explanation.

    The user is unauthorized if *any* of the following are true:

    - the user does not have one of the roles in roles
    - the user is not one of the users in users
    - the user does not have the same id as the id of the entity the action
      takes as argument

    Example 1: (user must be an administrator or a contributor): 
    >@authorize(['administrator', 'contributor'])
    >def action_name(self):
    >   ...

    Example 2: (user must be either an administrator or the contributor with Id 2): 
    >@authorize(['administrator', 'contributor'], [2])
    >def action_name(self):
    >   ...

    Example 3: (user must have the same ID as the entity she is trying to affect): 
    >@authorize(['administrator', 'contributor', 'viewer'], user_id_is_args1=True)
    >def action_name(self, id):
    >   ...

    """

    def wrapper(target, *args, **kwargs):
        role = getattr(session.get('user'), 'role', None)
        if role in roles:
            id = getattr(session.get('user'), 'id', None)
            if users:
                if role != 'administrator' and id not in users:
                    response.status_int = 403
                    return unauthorized_msg
            if user_id_is_args1:
                if role != 'administrator' and int(id) != int(args[1]):
                    response.status_int = 403
                    return unauthorized_msg
            return target(*args, **kwargs)
        else:
            response.status_int = 403
            return unauthorized_msg
            return

    return decorator(wrapper)