# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/secobj/provider/unix.py
# Compiled at: 2012-08-27 08:56:03
import grp, os, pwd, weakref
from secobj.exceptions import UnknownPrincipalError
from secobj.localization import _
from secobj.memoizer import memoize
from secobj.principal import USER_NAME, GROUP_NAME
from secobj.principal import Group, GroupList, Subject, User
from secobj.provider import SecurityProvider
from secobj.utils import error
_cached_subjects = weakref.WeakValueDictionary()

class UnixSecurityProvider(SecurityProvider):

    def __init__(self):
        self._currentuser = User.make(pwd.getpwuid(os.getuid()).pw_name)
        super(UnixSecurityProvider, self).__init__()

    def getcurrentuser(self):
        return self._currentuser

    def _setcurrentuser(self, user):
        assert isinstance(user, User)
        self._currentuser = user

    @memoize(cache=_cached_subjects, method=True)
    def _getsubject(self, name):
        if USER_NAME.match(name) is not None:
            try:
                return User.make(pwd.getpwnam(name).pw_name)
            except KeyError:
                pass

        elif GROUP_NAME.match(name) is not None:
            try:
                return Group.make(grp.getgrnam(name[1:]).gr_name)
            except KeyError:
                pass

        return super(UnixSecurityProvider, self)._getsubject(name)

    def is_subject_in_group(self, subject, group):

        def test(group):
            try:
                for name in grp.getgrnam(group.plainname).gr_mem:
                    if name == subject.name:
                        return True

            except KeyError:
                pass

            return False

        if test(group):
            return True
        if isinstance(group, GroupList):
            for member in group:
                if test(member):
                    return True

        return False