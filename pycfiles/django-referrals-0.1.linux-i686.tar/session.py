# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/craterdome/work/magikally/lib/python2.7/site-packages/referrals/session.py
# Compiled at: 2011-12-28 15:16:05


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

    def __len__(self):
        return len(self._session)

    def __getitem__(self, key):
        return self._get_or_set(key, None)

    def __setitem__(self, key, value):
        return self._get_or_set(key, value)

    def __delitem__(self, key):
        del self._session[key]

    def __contains__(self, key):
        key = '%s%s' % (self._prepend_key_with, key)
        return key in self._session


class ReferralSessionManager(SessionManagerBase):

    def __init__(self, request):
        super(ReferralSessionManager, self).__init__(request, 'referrals-')