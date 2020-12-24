# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.11.1-i386/egg/ximenez/shared/zope.py
# Compiled at: 2008-01-15 14:24:11
"""Define various classes and functions related to Zope.

$Id: zope.py 44 2008-01-15 19:20:19Z damien.baty $
"""
import re, socket, urllib2
from xmlrpclib import Fault
from xmlrpclib import ServerProxy
from xmlrpclib import ProtocolError
from ximenez.shared import ConnectionException
ROLES_REGEXP = re.compile('<OPTION VALUE="(?:(.*))"(?:(.*))>')
DOMAINS_REGEXP = re.compile('<INPUT TYPE="TEXT" NAME="domains:tokens" SIZE="30"(?:\n|\r\n|\r)  VALUE="(.*?)"')

class UnauthorizedException(Exception):
    """User has not been authorized to do that."""
    __module__ = __name__


class UserAlreadyExistException(Exception):
    """User already exists."""
    __module__ = __name__


class UserDoNoExistException(Exception):
    """User does not exist."""
    __module__ = __name__


class ZopeInstance(object):
    """Represent an instance of a Zope server."""
    __module__ = __name__

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def __repr__(self):
        return (':').join((self.host, str(self.port)))

    def usesPAS(self, manager, manager_pwd):
        """Tells whether the server uses PAS (Pluggable Authentication
        Service) or a standard user folder.

        We do that by trying an XML-RPC request on a method which the
        standard user folder does not implement, whereas PAS does.
        """
        try:
            self.performCall(manager, manager_pwd, 'acl_users', 'searchPrincipals')
        except Fault, exc:
            if 'NotFound' in exc.faultString:
                return False
            not_found_zope_2_5 = 'Cannot locate object at: http://%s:%s/acl_users/searchPrincipals' % (self.host, self.port)
            if not_found_zope_2_5 in exc.faultString:
                return False
            raise

        return True

    def performCall(self, manager, manager_pwd, path, method, args=()):
        """Perform XML-RPC on the current Zope instance.

        This method might raise various exceptions, notably
        ``ProtocolError`` and ``Fault`` (both from ``xmlrpclib``), and
        also ``UnauthorizedException`` (which is actually a
        ``ProtocolError`` exception with a specific message, which we
        are able to detect).
        """
        url = 'http://%s:%s@%s:%s/%s' % (manager, manager_pwd, self.host, self.port, path)
        server = ServerProxy(url, allow_none=True)
        try:
            result = getattr(server, method)(*args)
        except socket.error, exc:
            raise ConnectionException
        except ProtocolError, exc:
            if exc.errmsg == 'Unauthorized':
                raise UnauthorizedException()
            exc.url = exc.url.replace(manager_pwd, '########')
            raise

        return result

    def addUser(self, userid, pwd, manager, manager_pwd):
        """Add ``userid`` with a ``Manager`` role.

        This method may raise the following exceptions:

        - ``UnauthorizedException``;

        - ``UserAlreadyExistException``.
        """
        pas = self.usesPAS(manager, manager_pwd)
        if pas:
            path = 'acl_users/users'
            method = 'manage_addUser'
            args = (userid, userid, pwd, pwd, None)
        else:
            path = 'acl_users'
            method = 'userFolderAddUser'
            args = (userid, pwd, ['Manager'], [])
        if not pas:
            try:
                self.downloadUserEditForm(userid, manager, manager_pwd)
                raise UserAlreadyExistException
            except UserDoNoExistException:
                pass

        try:
            self.performCall(manager, manager_pwd, path, method, args)
        except Fault, exc:
            error = exc.faultString
            if error.find("'Duplicate user ID: %s'" % userid):
                raise UserAlreadyExistException()
            raise

        if pas:
            path = 'acl_users/roles'
            method = 'assignRoleToPrincipal'
            args = ('Manager', userid)
            self.performCall(manager, manager_pwd, path, method, args)
        return

    def modifyUserPassword(self, userid, password, manager, manager_pwd):
        """Set password of ``userid`` as ``password``.

        This method may raise the following exceptions:

        - ``UnauthorizedException``;

        - ``UserDoNoExistException``.
        """
        if self.usesPAS(manager, manager_pwd):
            path = 'acl_users/users'
            method = 'manage_updateUserPassword'
            args = (userid, password, password, None)
        else:
            path = 'acl_users'
            method = 'userFolderEditUser'
            edit_form = self.downloadUserEditForm(userid, manager, manager_pwd)
            roles = self.getUserRoles('', '', '', edit_form)
            domains = self.getUserDomains('', '', '', edit_form)
            args = (userid, password, roles, domains)
        try:
            self.performCall(manager, manager_pwd, path, method, args)
        except Fault, exc:
            error = exc.faultString
            if error.find("'Invalid user ID: %s'" % userid):
                raise UserDoNoExistException()
            raise

        return

    def removeUser(self, userid, manager, manager_pwd):
        """Remove ``userid``.

        This method may raise the following exceptions:

        - ``UnauthorizedException``;

        - ``UserDoNoExistException``.
        """
        if self.usesPAS(manager, manager_pwd):
            path = 'acl_users/users'
            method = 'manage_removeUsers'
            args = ((userid,), None)
        else:
            path = 'acl_users'
            method = 'userFolderDelUsers'
            args = ((userid,),)
        try:
            self.performCall(manager, manager_pwd, path, method, args)
        except Fault, exc:
            error = exc.faultString
            if error.endswith("exceptions.KeyError - '%s'" % userid):
                raise UserDoNoExistException()
            if error.find("'Invalid user ID: %s'" % userid):
                raise UserDoNoExistException()
            raise

        return

    def downloadUserEditForm(self, userid, manager, manager_pwd):
        """Return HTML code of the edit form of the user.

        **Warning:** this only works for standard user folder, not
        PAS.
        """
        auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password('Zope', 'http://%s:%s' % (self.host, self.port), manager, manager_pwd)
        opener = urllib2.build_opener(auth_handler)
        url = 'http://%s:%s/acl_users/manage_users' % (self.host, self.port)
        try:
            page = opener.open(url, data='name=%s&submit=Edit' % userid)
        except urllib2.HTTPError, exc:
            if exc.msg == 'Unauthorized':
                raise UnauthorizedException()
            if exc.msg == 'Internal Server Error' and exc.hdrs.get('bobo-exception-type') == 'AttributeError':
                raise UserDoNoExistException()
            raise
        except urllib2.URLError, exc:
            raise ConnectionException

        html = page.read()
        page.close()
        return html

    def getUserRoles(self, userid, manager, manager_pwd, html=None):
        """Return roles of ``userid``.

        **Warning:** this only works for standard user folder, not
        PAS.
        """
        if html is None:
            html = self.downloadUserEditForm(userid, manager, manager_pwd)
        found = ROLES_REGEXP.findall(html)
        roles = [ r for (r, selected) in found if selected ]
        return roles

    def getUserDomains(self, userid, manager, manager_pwd, html=None):
        """Return domains of ``userid``.

        If ``html`` is not None, then we use it instead of trying to
        download the edit form.

        **Warning:** this only works for standard user folder, not
        PAS.
        """
        if html is None:
            html = self.downloadUserEditForm(userid, manager, manager_pwd)
        found = DOMAINS_REGEXP.search(html)
        domains = found.groups()[0]
        domains = domains.split(' ')
        domains = [ d for d in domains if d ]
        return domains