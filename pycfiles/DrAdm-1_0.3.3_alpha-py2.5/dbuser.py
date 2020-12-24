# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DrAdm1/mod/dbuser.py
# Compiled at: 2009-08-17 02:35:16
"""
DrAdm1 utilities pack - www.dradm.org
(c) Axel <dev@axel.pp.ru>
Under GPL v3
"""
from utils import *

class DbUserError(Exception):

    def __init__(self, obj, msg=''):
        Exception.__init__(self)
        self.type = obj.section
        self.name = obj.name
        self.project = obj.project
        self.server_host = obj.server_host
        self.client_host = obj.client_host
        self.msg = msg
        if not self.msg:
            self.msg = "Operation error in 'dbuser' module."

    def __str__(self):
        return self.msg


class DbUser:
    """ Work with database users.
    Tested with mysql only yet!
    """

    def __init__(self, config, name='', project='', host='localhost', dbtype='MYSQL'):
        self.section = dbtype.upper()
        self.name = name
        self.project = project
        self.client_host = host
        try:
            import MySQLdb as DB
        except ImportError:
            DatabaseError(self, 'MySQL support not installed. You need install python-mysql module to the system.')

        self.DB = DB
        if not name:
            if not project:
                raise DbUserError(self, 'You need set either one of username or project')
            self.passwd = pwgen()
            self.realname = name or self.project
        else:
            self.realname = self.name
        self.server_host = config.get(self.section, 'host')
        sysuser = config.get(self.section, 'user')
        syspasswd = config.get(self.section, 'passwd')
        try:
            db = self.DB.connect(host=self.server_host, user=sysuser, passwd=syspasswd)
            self.cursor = db.cursor()
        except:
            raise DbUserError(self, "Can't connect to MySQL server at %s" % self.server_host)

    def getname(self):
        return self.realname

    def getpasswd(self):
        return self.passwd

    def getserverhost(self):
        """ Returns DBMS server host/ip.
        """
        return self.server_host

    def getclienthost(self):
        """ Returns client host/ip.
        """
        return self.client_host

    def exists(self):
        """ Is user exists?
        """
        try:
            return self.cursor.execute('SELECT user FROM mysql.user WHERE user = %s AND host = %s', (self.realname, self.client_host))
        except:
            raise DbUserError(self, "Can't check existence of the %s database." % self.realname)

    def list_get(self):
        pass

    def list_print(self):
        pass

    @addactions
    def add(self, passwd=''):
        if passwd:
            self.passwd = passwd
        try:
            self.cursor.execute('CREATE USER %s@%s', (self.realname, self.client_host))
        except self.DB.OperationalError:
            raise DbUserError(self, "Can't create database user %s" % self.realname)

        try:
            self.cursor.execute('SET PASSWORD FOR %s@%s = PASSWORD(%s)', (self.realname, self.client_host, self.passwd))
        except self.DB.OperationalError:
            self.cursor.execute('DROP USER %s@%s', (self.realname, self.client_host))
            raise DbUserError(self, "Can't set password for database user %s. User was deleted." % self.realname)

        return self.passwd

    @addactions
    def drop(self):
        self.cursor.execute('DROP USER %s@%s', (self.realname, self.client_host))
        try:
            self.cursor.execute('DROP USER %s@%s', (self.realname, self.client_host))
        except self.DB.OperationalError:
            raise DbUserError(self, "Can't delete %s user %s." % (self.section, self.realname))

    @addactions
    def modify(self):
        self.cursor.execute('SET PASSWORD FOR %s@%s = PASSWORD(%s)', (self.realname, self.client_host, self.passwd))
        return self.passwd

    @addactions
    def grant(self, dbname):
        try:
            self.cursor.execute('GRANT ALL ON %s.* TO %s@%s' % (dbname, self.realname, self.client_host))
        except self.DB.OperationalError:
            raise DbUserError(self, "Can't grant access to user %s on database %s." % (self.realname, dbname))

    @addactions
    def revoke(self, dbname):
        try:
            self.cursor.execute('REVOKE ALL ON %s FROM %s@%s' % (dbname + '.*', self.realname, self.client_host))
        except self.DB.OperationalError:
            raise DbUserError(self, "Can't revoke access from user %s on database %s." % (self.realname, dbname))


if __name__ == '__main__':
    if not rootcheck():
        error('You need run this utility as root!')
    cfg = Config()
    test = DbUser(cfg, 'test1314')
    print test.add()
    test.drop()