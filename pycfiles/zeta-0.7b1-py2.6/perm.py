# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/auth/perm.py
# Compiled at: 2010-07-06 09:21:05
"""Permission definitions for the entire web application. This module is a copy
of the authkit.permissions module. This moddule and `users` module form the
applications authentication sub-system (derived from authkit).

Permission objects are used to define which users should have access to a
particular resource. They are checked using some of the authorization objects
either in the ``authkit.authorize`` module or ``authkit.pylons_adaptors``
module if you are using Pylons.

Permissions objects are very similar to WSGI applications and can perform a
check based on the request or the response. Not all of the authorization
objects have access to the response because the permission might be checked as
part of a code block before the response is generated. This leads to two
classes of permissions, request-based (which can be checked anywhere) and
response-based which can only be checked when the authorization object has
access to the response. 

All the built-in AuthKit permissions are request-based but you can use the
permissions objects defined in this module or create your own derived from
``authkit.permission.Permission``.

Permissions are described in detail in the AuthKit manual.
"""
import datetime, logging, types
from pylons import config
from pylons import tmpl_context as c
from authkit.users import *
from authkit.authorize import PermissionError, PermissionSetupError, NotAuthenticatedError, NotAuthorizedError, middleware
from authkit.permissions import AuthKitConfigError, no_authkit_users_in_environ, Permission, RequestPermission
from zeta.lib.error import ZetaPermError
from zeta.lib.pms import PMSystem
log = logging.getLogger('authkit.permissions')
permissions = {}

class AppPermission(object):
    """Create a new permission name for application."""

    def __init__(self, comp, perm_name, project=True):
        """Instantiate a permission object 'perm_name' belonging to 'comp'
        (component) which is optionally under a 'project' project's context"""
        self.perm_name = perm_name
        self.comp = comp
        self.project = project
        if perm_name in [ ap.perm_name for aplist in permissions.values() for ap in aplist
                        ]:
            raise ZetaPermError('App Permission %r already exists' % perm_name)
        permissions.setdefault(comp, []).append(self)

    def __repr__(self):
        return "<AppPermission('%s',%s)>" % (self.comp, self.perm_name)


(
 AppPermission('system', 'EMAIL_VIEW', project=False),)
(AppPermission('system', 'SITE_ADMIN', project=False),)
(AppPermission('system', 'STATICWIKI_CREATE', project=False),)
(
 AppPermission('license', 'LICENSE_VIEW', project=False),)
(AppPermission('license', 'LICENSE_CREATE', project=False),)
AppPermission('search', 'SEARCH_VIEW', project=False)
(
 AppPermission('project', 'PROJECT_VIEW'),)
(
 AppPermission('ticket', 'TICKET_VIEW'),)
(AppPermission('ticket', 'TICKET_CREATE'),)
(AppPermission('ticket', 'TICKET_STATUS_CREATE'),)
(AppPermission('ticket', 'TICKET_COMMENT_CREATE'),)
(
 AppPermission('review', 'REVIEW_VIEW'),)
(AppPermission('review', 'REVIEW_CREATE'),)
(
 AppPermission('vcs', 'VCS_VIEW'),)
(AppPermission('vcs', 'VCS_CREATE'),)
(
 AppPermission('wiki', 'WIKI_VIEW'),)
(AppPermission('wiki', 'WIKI_CREATE'),)
(AppPermission('wiki', 'WIKICOMMENT_CREATE'),)
(
 AppPermission('xmlrpc', 'XMLRPC_VIEW'),)

def _currentuser():
    try:
        authuser = getattr(c, 'authuser', None)
    except:
        authuser = None

    return authuser


def mapfor_usersite():
    """Generate the permission map for site users"""
    from zeta.lib.helpers import fromconfig
    from zeta.comp.project import ProjectComponent
    userscomp = fromconfig('userscomp')
    return userscomp.mapfor_usersite()


def mapfor_teamperms():
    """Generate the permission map for project teams"""
    from zeta.lib.helpers import fromconfig
    from zeta.comp.project import ProjectComponent
    compmgr = fromconfig('compmgr')
    projcomp = ProjectComponent(compmgr)
    return projcomp.mapfor_teamperms()


def mapfor_projadmins():
    """Generate the permission map for project teams"""
    from zeta.lib.helpers import fromconfig
    from zeta.comp.project import ProjectComponent
    compmgr = fromconfig('compmgr')
    projcomp = ProjectComponent(compmgr)
    return projcomp.mapfor_projadmins()


def mapfor_siteadmin():
    """Generate the permission map for site administrator"""
    from zeta.lib.helpers import fromconfig
    userscomp = fromconfig('userscomp')
    return {'admin': ['PMS_SITE_ADMIN', 'PMS_PROJECT_ADMIN'] + userscomp.perm_names}


def mapfor_anonymous():
    """Generate the permission map for anonymous user"""
    from zeta.lib.helpers import fromconfig
    userscomp = fromconfig('userscomp')
    return {'anonymous': ['LICENSE_VIEW', 'PROJECT_VIEW', 'TICKET_VIEW',
                   'REVIEW_VIEW', 'WIKI_VIEW', 'SEARCH_VIEW']}


def ctxtfor_projadmin():
    """Generate the context for project admin"""
    return c.project and [
     (
      c.project.projectname, c.authusername)] or []


def ctxtfor_projteams():
    """Generate the context for the project team"""
    from zeta.lib.helpers import fromconfig
    from zeta.comp.project import ProjectComponent
    compmgr = fromconfig('compmgr')
    projcomp = ProjectComponent(compmgr)
    if c.project:
        teams = projcomp.userinteams(c.project, c.authusername) + (c.authusername != 'anonymous' and [
         projcomp.team_nomember] or [])
        return [ (c.project.projectname, t) for t in teams ]
    else:
        return []


pms_usersite = None
pms_projteams = None
pms_projadmin = None
pms_siteadmin = None
pms_anonymous = None
pms_root = None

def init_pms(ctxt=None):
    """Initialize the permission system
        siteadmin
            |
            |-- projadmin
                    |
                    |-- projteams
                    |-- usersite
                           |
                           |-- anonymous*

    `ctxt` is used only for testing
    """
    global pms_projadmin
    global pms_projteams
    global pms_root
    global pms_siteadmin
    global pms_usersite
    if not pms_siteadmin:
        if ctxt:
            strictauth = ctxt.get('strictauth')
        else:
            strictauth = c.sysentries['strictauth']
        usersite_children = []
        if strictauth in ('False', 'false'):
            pms_anonymous = PMSystem('anonymous', lambda : [
             c.authusername], mapfor_anonymous, [])
            usersite_children = [
             pms_anonymous]
        pms_usersite = PMSystem('usersite', lambda : [
         c.authusername], mapfor_usersite, usersite_children)
        pms_projteams = PMSystem('projteams', ctxtfor_projteams, mapfor_teamperms, [])
        pms_projadmin = PMSystem('projadmin', ctxtfor_projadmin, mapfor_projadmins, [
         pms_projteams, pms_usersite])
        pms_siteadmin = PMSystem('siteadmin', lambda : [
         c.authusername], mapfor_siteadmin(), [
         pms_projadmin])
    pms_root = pms_siteadmin


class UserIn(RequestPermission):
    """Simple permission object. Does not use Permission Mapping
    System(PMS).
    Checks whether REMOTE_USER is one of the users specified.
    """

    def __init__(self, users):
        """Takes the following arguments:
        `users`
            A list of usernames, to whom permission is granted.

        If there is no `REMOTE_USER` `NotAuthenticatedError` is raised. If
        the `REMOTE_USER` is not in `users` a `NotAuthorizedError` is raised.

        `username` in `users` are expected to be in lower case."""
        self.users = users

    def check(self, app, environ, start_response):
        authusername = environ.get('REMOTE_USER', 'anonymous')
        if authusername not in self.users:
            raise NotAuthorizedError('You are not allowed to access this resource.')
        return app(environ, start_response)


class Exists(RequestPermission):
    """Simple permission object. Does not use Permission Mapping
    System(PMS).
    Checks whether specified key is present in the ``environ``."""

    def __init__(self, key, error=NotAuthorizedError('Not Authorized')):
        """Takes the following arguments:
            `key`
                The required key
            `error`
                The error to be raised if the key is missing.
                XXX This argument may be deprecated soon.
        """
        self.key = key
        self.error = error

    def check(self, app, environ, start_response):
        if self.key not in environ:
            raise self.error
        return app(environ, start_response)


class PermAnd(RequestPermission):
    """Checks all the permission objects listed as keyword arguments in turn.
    Permissions are checked from left to right. The error raised by the ``And``
    permission is the error raised by the first permission check to fail.
    """

    def __init__(self, *permissions):
        if len(permissions) < 2:
            raise PermissionSetupError('Expected at least 2 permissions objects')
        permissions = list(permissions)
        permissions.reverse()
        self.permissions = permissions

    def check(self, app, environ, start_response):
        for permission in self.permissions:
            app = middleware(app, permission)

        return app(environ, start_response)


class RemoteUser(RequestPermission):
    """Checks someone is signed in by checking for the presence of the
    REMOTE_USER.
    
    """

    def __init__(self, anonymous=False, accept_empty=False):
        """If 'accept_empty' is 'False' (the default) then an empty
        'REMOTE_USER' will not be accepted and the value of 'REMOTE_USER' must
        evaluate to 'True' in Python."""
        self.accept_empty = accept_empty
        self.anonymous = anonymous

    def check(self, app, environ, start_response):
        if self.anonymous:
            if 'REMOTE_USER' in environ:
                raise NotAuthorizedError('Not an anonymous user')
        elif 'REMOTE_USER' not in environ:
            raise NotAuthenticatedError('Not Authenticated')
        elif self.accept_empty == False and not environ['REMOTE_USER']:
            raise NotAuthorizedError('Not Authorized')
        return app(environ, start_response)


class HasPermgroup(RequestPermission):
    """Designed to work with the user management API described in the AuthKit 
    manual.

    This permission checks that the signed in user belongs to one of the
    permission groups specified in ``permgroups``."""

    def __init__(self, permgroups, all=True, strict=None, error=None):
        if isinstance(permgroups, str):
            permgroups = [
             permgroups]
        self.permgroups = permgroups
        self.all = all
        self.error = error
        self.strict = strict

    def check(self, app, environ, start_response):
        """
        Should return True if the user belong to all or any of the permission
        group or False if the user doesn't exist or permission check fails.

        In this implementation group names are lower case.
        """
        from zeta.lib.helpers import fromconfig
        from zeta.comp.system import SystemComponent
        compmgr = fromconfig('compmgr')
        syscomp = SystemComponent(compmgr)
        if not environ.get('authkit.users'):
            raise no_authkit_users_in_environ
        authusername = environ.get('REMOTE_USER', 'anonymous')
        userscomp = environ['authkit.users']
        if not _currentuser() and not userscomp.user_exists(authusername):
            raise NotAuthorizedError('No such user')
        strict = self.strict or syscomp.get_sysentry('strictauth')
        if authusername == 'anonymous' and strict in ('True', 'true'):
            raise NotAuthenticatedError('Please login or Register yourself')
        if not userscomp.user_has_permgroups(authusername, self.permgroups, self.all):
            if self.error:
                raise self.error
            else:
                raise NotAuthorizedError("User doesn't belong to permgroups %s" % self.permgroups)
        return app(environ, start_response)


class ValidUser(UserIn):
    """Checks that the signed in user is one of the registered users.
    If `strict` is False,
        then `anonymous` user will be considered a valid user.
    If `strict` is True,
        then `anonymous` user will not be considered a valid user.
    """

    def __init__(self, strict=None):
        self.strict = strict

    def check(self, app, environ, start_response):
        from zeta.lib.helpers import fromconfig
        from zeta.comp.system import SystemComponent
        userscomp = environ.get('authkit.users')
        compmgr = fromconfig('compmgr')
        syscomp = SystemComponent(compmgr)
        if not userscomp:
            raise no_authkit_users_in_environ
        authusername = environ.get('REMOTE_USER', 'anonymous')
        strict = self.strict or syscomp.get_sysentry('strictauth')
        if authusername == 'anonymous' and strict in ('True', 'true'):
            raise NotAuthenticatedError('Please login or Register yourself')
        if not _currentuser() and not userscomp.user_exists(authusername):
            raise NotAuthorizedError('You are allowed to access this resource.')
        return app(environ, start_response)


class SiteAdmin(RequestPermission):
    """Check whether the logged in user is the site administrator."""

    def __init__(self, strict=None):
        self.strict = strict

    def check(self, app, environ, start_response):
        from zeta.lib.helpers import fromconfig
        from zeta.comp.system import SystemComponent
        compmgr = fromconfig('compmgr')
        syscomp = SystemComponent(compmgr)
        if not environ.get('authkit.users'):
            raise no_authkit_users_in_environ
        authusername = environ.get('REMOTE_USER', 'anonymous')
        strict = self.strict or syscomp.get_sysentry('strictauth')
        if authusername == 'anonymous' and strict in ('True', 'true'):
            raise NotAuthenticatedError('Please login or Register yourself')
        status = pms_root.check([
         'PMS_SITE_ADMIN'], context=lambda : [
         authusername])
        if status == False:
            raise NotAuthorizedError('You are not site administrator')
        return app(environ, start_response)


class ProjectAdmin(RequestPermission):
    """Check whether the logged in user is the administrator for the
    project"""

    def __init__(self, project=None, strict=None):
        self.strict = strict
        self.project = project

    def check(self, app, environ, start_response):
        from zeta.lib.helpers import fromconfig
        from zeta.comp.system import SystemComponent
        compmgr = fromconfig('compmgr')
        syscomp = SystemComponent(compmgr)
        if not environ.get('authkit.users'):
            raise no_authkit_users_in_environ
        authusername = environ.get('REMOTE_USER', 'anonymous')
        strict = self.strict or syscomp.get_sysentry('strictauth')
        if authusername == 'anonymous' and strict in ('True', 'true'):
            raise NotAuthenticatedError('Please login or Register yourself')
        if self.project:
            p = self.project
            context = [(p.projectname, authusername)]
        else:
            context = None
        status = pms_root.check(['PMS_PROJECT_ADMIN'], context=context)
        if status == False:
            raise NotAuthorizedError('You are not the project administrator')
        return app(environ, start_response)


class HasPermname(RequestPermission):
    """Designed to work with the user management API described in the AuthKit 
    manual.

    This permission checks that the signed in user has any of the permission
    names specified in 'permnames'. If 'all' is 'True', the user must 
    have all the permission names for the permission check to pass."""

    def __init__(self, permnames, all=False, project=None, strict=None, error=None):
        if isinstance(permnames, (str, unicode)):
            permnames = [
             permnames]
        self.all = all
        self.permnames = permnames
        self.project = project
        self.error = error
        self.strict = strict

    def check(self, app, environ, start_response):
        """Should return True if the user has all or any permissions or
        False if the user doesn't exist or the permission check fails.

        In this implementation permission names are uppercase."""
        from zeta.lib.helpers import fromconfig
        from zeta.comp.project import ProjectComponent
        from zeta.comp.system import SystemComponent
        compmgr = fromconfig('compmgr')
        syscomp = SystemComponent(compmgr)
        if not environ.get('authkit.users'):
            raise no_authkit_users_in_environ
        users = environ['authkit.users']
        projcomp = ProjectComponent(compmgr)
        authusername = environ.get('REMOTE_USER', 'anonymous')
        if not _currentuser() and not users.user_exists(authusername):
            raise NotAuthorizedError('No such user %s' % authusername)
        strict = self.strict or syscomp.get_sysentry('strictauth')
        if authusername == 'anonymous' and strict in ('True', 'true'):
            raise NotAuthenticatedError('Please login or Register yourself')
        if self.project:
            p = self.project
            teams = projcomp.userinteams(p, authusername) + [
             projcomp.team_nomember]
            context = [ (p.projectname, t) for t in teams ] + [authusername]
        else:
            context = None
        status = pms_root.check(self.permnames, allliterals=self.all, context=context)
        if status == False:
            raise NotAuthorizedError("User doesn't have the permissions %s" % self.permnames)
        return app(environ, start_response)


class FromIP(RequestPermission):
    """Checks that the remote host specified in the environment ``key`` is one 
    of the hosts specified in ``hosts``.
    """

    def __init__(self, hosts, key='REMOTE_ADDR'):
        self.hosts = hosts
        if not isinstance(self.hosts, (list, tuple)):
            self.hosts = [
             hosts]
        self.key = key

    def check(self, app, environ, start_response):
        if self.key not in environ:
            raise Exception('No such key %r in environ so cannot check the host' % self.key)
        if environ.get(self.key) not in self.hosts:
            raise NotAuthorizedError('Host %r not allowed' % environ.get(self.key))
        return app(environ, start_response)


class BetweenTimes(RequestPermission):
    """Only grants access if the request is made on or after ``start`` and 
    before ``end``. Times should be specified as datetime.time objects.
    """

    def __init__(self, start, end, error=NotAuthorizedError('Not authorized at this time of day')):
        self.start = start
        self.end = end
        self.error = error

    def check(self, app, environ, start_response):
        today = datetime.datetime.now()
        now = datetime.time(today.hour, today.minute, today.second, today.microsecond)
        if self.end > self.start:
            if now >= self.start and now < self.end:
                return app(environ, start_response)
            raise self.error
        else:
            if now < datetime.time(23, 59, 59, 999999) and now >= self.start:
                return app(environ, start_response)
            if now >= datetime.time(0) and now < self.end:
                return app(environ, start_response)
            raise self.error