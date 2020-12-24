# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/craterdome/work/django_common/lib/python2.7/site-packages/django_common/session.py
# Compiled at: 2012-03-11 19:20:35


class SessionManagerBase(object):
    """
    Base class that a "SessionManager" concrete class should extend. It should have a list called _SESSION_KEYS that
    lists all the keys that class uses/depends on.
    
    Ideally each app has a session.py that has this class and is used in the apps views etc.
    """

    def __init__(self, request, prepend_key_with=''):
        self._session = request.session
        self._prepend_key_with = prepend_key_with

    def _get_or_set(self, key, value):
        key = '%s%s' % (self._prepend_key_with, key)
        if value is not None:
            self._session[key] = value
            return value
        else:
            return self._session.get(key)

    def reset_keys(self):
        for key in self._SESSION_KEYS:
            key = '%s%s' % (self._prepend_key_with, key)
            if self._session.has_key(key):
                del self._session[key]