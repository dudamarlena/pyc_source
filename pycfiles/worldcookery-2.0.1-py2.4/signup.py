# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.2-i386/egg/worldcookery/signup.py
# Compiled at: 2006-09-21 05:27:35
from zope.interface import Interface, implements
from zope.schema import List, Choice
from zope.i18nmessageid import MessageFactory
_ = MessageFactory('worldcookery')
from zope.app.authentication.principalfolder import PrincipalFolder
from zope.app.authentication.principalfolder import InternalPrincipal

class ISignup(Interface):
    __module__ = __name__
    signup_roles = List(title=_('Roles for new principals'), description=_('These roles will assigned to new principals.'), value_type=Choice(vocabulary='Role Ids'), unique=True)

    def signUp(login, password, title):
        """Add a principal for yourself.  Returns the new principal's ID
      """
        pass

    def changePasswordTitle(login, password, title):
        """Change the principal's password and/or title.
      """
        pass


class SignupPrincipalFolder(PrincipalFolder):
    """Principal folder that allows users to sign up.
    """
    __module__ = __name__
    implements(ISignup)
    signup_roles = []

    def signUp(self, login, password, title):
        self[login] = InternalPrincipal(login, password, title)
        return self.__parent__.prefix + self.prefix + login

    def changePasswordTitle(self, login, password, title):
        if login not in self:
            raise ValueError('Principal is not managed by this principal source.')
        principal = self[login]
        principal.password = password and password or principal.password
        principal.title = title and title or principal.title