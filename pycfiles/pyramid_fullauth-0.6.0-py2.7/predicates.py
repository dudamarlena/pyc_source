# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyramid_fullauth/routing/predicates.py
# Compiled at: 2017-02-24 16:57:38
"""Routing predicate definitions."""
from sqlalchemy.orm.exc import NoResultFound
from pyramid.config.predicates import CheckCSRFTokenPredicate
from pyramid.httpexceptions import HTTPUnauthorized
import pyramid_basemodel
from pyramid_fullauth.models import User

def reset_hash(info, request):
    """
    Check whether reset hash is correct.

    :param dict info: pyramid info dict with path fragments and info
    :param pyramid.request.Request request: request object

    :returns: whether reset hash exists or not
    :rtype: bool

    """
    reset_hash = info['match'].get('hash', None)
    if reset_hash:
        try:
            info['match']['user'] = pyramid_basemodel.Session.query(User).filter(User.reset_key == reset_hash).one()
            return True
        except NoResultFound:
            pass

    return False


def change_email_hash(info, request):
    """
    Check whether change email hash is correct.

    :param dict info: pyramid info dict with path fragments and info
    :param pyramid.request.Request request: request object

    :returns: whether change email hash exists or not
    :rtype: bool

    """
    change_email_hash = info['match'].get('hash', None)
    if change_email_hash:
        try:
            info['match']['user'] = pyramid_basemodel.Session.query(User).filter(User.email_change_key == change_email_hash).one()
            return True
        except NoResultFound:
            pass

    return False


class CSRFCheckPredicate(CheckCSRFTokenPredicate):
    """
    Run csrf check dependant on configuration.

    .. note::

        Raises HTTPUnauthorized exception if check fails.

    :raises: pyramid.httpexceptions.HTTPUnauthorized

    :returns: True if check succeeds or turned off.
    :rtype: bool

    """

    def __call__(self, context, request):
        """
        Run predicate check.

        :param context:
        :param pyramid.request.Request request:

        """
        if request.registry['config'].fullauth.check_csrf:
            result = CheckCSRFTokenPredicate.__call__(self, context, request)
            if not result:
                raise HTTPUnauthorized
        return True