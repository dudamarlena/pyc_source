# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sake\login.py
# Compiled at: 2011-03-08 21:54:17
"""login module - Authentication"""
import errno, hashlib
from .app import app
from .const import ROLE_ANY, ROLE_USER, ROLE_ADMIN
from .errors import LoginError, ServiceNotFoundError
from .process import Process
from . import util
LOCAL_AUTH_FILENAME = 'local_authentication.txt'

def CreateMD5Password(username, password):
    """Creates a password hash used by local and web authentication"""
    return hashlib.md5('%s:%s:%s' % (username, 'miniframework', password)).hexdigest()


class LoginService(Process):
    serviceName = 'login'
    serviceIncludes = ['sessionManager']
    serviceAllowRPC = True
    _dummyID = 100000

    def StartProcess(self):
        self.localAuth = {}
        self.addToLocalAuth = True
        try:
            self._LoadLocalUsers()
        except Exception:
            self.log.exception('_LoadLocalUsers failed. File %s may be corrupt', LOCAL_AUTH_FILENAME)

        try:
            self.DB = app.GetService('DB')
        except ServiceNotFoundError:
            self.DB = None
        except Exception:
            self.DB = None

        return

    def _LoadLocalUsers(self):
        try:
            f = open(app.AbsPath(LOCAL_AUTH_FILENAME), 'r')
        except IOError as e:
            if e.errno != errno.ENOENT:
                self.log.exception('Unexpected error reading local user file: %s %s', e.errno, errno.ENOENT)
                raise
        else:
            import yaml
            entries = yaml.load(f)
            self.localAuth = dict([ (i[0], i) for i in entries ])

    def Login(self, username, password):
        passwordMD5 = CreateMD5Password(username, password)
        user = self.DB.zsystem.SQL("\n            select * from zuser.users\n            where userName = '%s' and passwordMD5 = '%s'\n            " % (username, passwordMD5))
        if not user:
            from binascii import crc32
            user = self.DB.zsystem.SQL("select %s as userID, '%s' as userName, 1 as role" % (crc32(username), username))
        user = user[0]
        self.log.info("User '%s' logging in", username)
        userid = user.userID
        for s in self.sessionManager.sessions:
            if s.userid == userid:
                s.Close()
                break

        session = util.GetSession()
        session.UpdateVariables(userid=user.userID, userName=user.userName, role=user.role, charid=userid)
        user = util.Bunch(dict(zip(user.__header__.Keys(), user)))
        import __builtin__
        __builtin__.user = user
        return user

    Login.access = ROLE_ANY

    def GetUserAuthenticationInfo(self, username):
        """Returns user info as a bunch of userID, userName, passwordMD5 and role.
        Retrieves info from DB if available, otherwise uses cached info from
        user.ini. If 'username' is not found in either DB or cache, then None is returned.
        Note: If DB info is used, then the local auth file is updated automatically.
        """
        if self.DB:
            rs = self.DB.zsystem.SQL("\n                select userID, userName, passwordMD5, role\n                from zuser.users\n                where userName = '%s'\n                " % (username,))
            info = rs[0]
            self.AddLocalAuthentication(info)
            return info
        if username in self.localAuth:
            data = self.localAuth[username]
            return util.Bunch(userName=data[0], userID=data[1], role=data[2], passwordMD5=data[3])
        self.log.error("Login: Can't authenticate user '%s'. There's no DB connection and no local authentication file or no entries in the file.", username)

    GetUserAuthenticationInfo.access = ROLE_ANY

    def Logout(self):
        s = util.GetSession()
        self.log.info("User '%s' logging off", s)
        s.Close()

    Logout.access = ROLE_ANY

    def AddLocalAuthentication(self, info):
        """Register 'username' in text file for local authentication. This is
        neccessary when there's no DB connection to do authentication.
        Note that authentication from DB is always used if available.
        """
        if not self.addToLocalAuth:
            return
        data = [info.userName, info.userID, info.role, info.passwordMD5]
        if info.userName in self.localAuth:
            if self.localAuth[info.userName] == data:
                return
        self.log.info("Login: Adding '%s' to local authentication file.", info.userName)
        try:
            f = open(app.AbsPath(LOCAL_AUTH_FILENAME), 'w')
        except IOError as e:
            if e.errno != 13:
                self.log.exception("AddLocalAuthentication: Couldn't open file %s", LOCAL_AUTH_FILENAME)
            self.addToLocalAuth = False
            return

        self.localAuth[info.userName] = data
        header = "# Local authentication\n#\n# This file contains users that can be authenticated locally, i.e. without DB\n# connection.\n# It gets populated automatically, but if this file is marked read-only, it will not.\n#\n# The format is yaml. Each entry is a list of user name, user ID, role and passwordMD5\n#\n# This entry here can be used for development purposes. The user name and password\n# is 'dev' with admin role: - ['dev', 999999, 64, 'a5f47b50469c83c15e245f22540a9bc4']\n#\n"
        f.write(header)
        for info in self.localAuth.itervalues():
            f.write("- ['%s', %s, %s, '%s']\n" % tuple(info))