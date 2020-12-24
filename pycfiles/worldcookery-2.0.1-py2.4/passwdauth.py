# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/passwdauth.py
# Compiled at: 2006-09-21 06:43:54
from persistent import Persistent
from zope.interface import Interface, implements
from zope.schema import TextLine
from zope.location.interfaces import ILocation
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('worldcookery')
from zope.app.authentication.interfaces import IAuthenticatorPlugin
from zope.app.authentication.principalfolder import PrincipalInfo

class IPasswd(Interface):
    __module__ = __name__
    prefix = TextLine(title=_('Prefix'), description=_('Prefix to be added to all principal IDs'), missing_value='', default='', readonly=True)
    filename = TextLine(title=_('File name'), description=_('Absolute path to the data file'), required=True)


class PasswdAuthenticator(Persistent):
    __module__ = __name__
    implements(IPasswd, IAuthenticatorPlugin, ILocation)
    __parent__ = __name__ = None

    def __init__(self, prefix='', filename=None):
        self.prefix = prefix
        self.filename = filename

    def _filedata(self):
        if self.filename is None:
            raise StopIteration
        for line in file(self.filename):
            yield line.strip().split(':', 3)

        return

    def authenticateCredentials(self, credentials):
        if not (credentials and 'login' in credentials and 'password' in credentials):
            return
        login, password = credentials['login'], credentials['password']
        for (username, passwd, title) in self._filedata():
            if (
             login, password) == (username, passwd):
                return PrincipalInfo(self.prefix + login, login, title, title)

    def principalInfo(self, id):
        if id.startswith(self.prefix):
            login = id[len(self.prefix):]
            for (username, passwd, title) in self._filedata():
                if login == username:
                    return PrincipalInfo(id, login, title, title)