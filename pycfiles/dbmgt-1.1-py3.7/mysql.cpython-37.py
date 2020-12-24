# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dbmgt/mysql.py
# Compiled at: 2019-07-19 08:38:20
# Size of source mod 2**32: 17293 bytes
"""
@author: sunway
@version v1
"""
import os
basedir = os.path.dirname(os.path.abspath(__file__))
logdir = os.path.join(basedir, 'logs')
if not os.path.exists(logdir):
    os.mkdir(logdir)
import MySQLdb, random, string, logging
logging.basicConfig(level=(logging.DEBUG), format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
  datefmt='%a, %d %b %Y %H:%M:%S',
  filename=('%s/dbmgt.log' % logdir),
  filemode='a')

class DBtool(object):

    def __init__(self, **kwargs):
        self._DBtool__dbhost = kwargs['dbhost']
        self._DBtool__dbport = kwargs['dbport']
        self._DBtool__dbuser = kwargs['dbuser']
        self._DBtool__dbpwd = kwargs['dbpwd']
        self._DBtool__dbname = kwargs['dbname']
        self._DBtool__charset = kwargs['charset']
        self.conn = None

    def getConn(self):
        try:
            self.conn = MySQLdb.connect(host=(self._DBtool__dbhost), port=(self._DBtool__dbport), user=(self._DBtool__dbuser), password=(self._DBtool__dbpwd), db=(self._DBtool__dbname),
              charset=(self._DBtool__charset))
            if self.conn:
                return self.conn
            return '连接数据库失败'
        except Exception as e:
            try:
                raise e
                print(e.args)
            finally:
                e = None
                del e

    def getColumns(self, sql):
        cursor = self.getConn().cursor()
        try:
            try:
                cursor.execute(sql)
                cols = [col[0] for col in cursor.description]
                return cols
            except Exception as e:
                try:
                    raise Exception(e)
                finally:
                    e = None
                    del e

        finally:
            cursor.close()
            self.conn.close()

    def sqlDml(self, sql):
        cursor = self.getConn().cursor()
        try:
            try:
                cursor.execute(sql)
                self.conn.commit()
                if cursor.rowcount > 0:
                    return 0
                return 2
            except Exception as e:
                try:
                    self.conn.rollback()
                    raise Exception('error')
                finally:
                    e = None
                    del e

        finally:
            cursor.close()
            self.conn.close()

    def sqlDmlp(self, sql, *args):
        cursor = self.getConn().cursor()
        try:
            try:
                cursor.execute(sql, args)
                self.conn.commit()
                if cursor.rowcount > 0:
                    return 0
                return 2
            except Exception as e:
                try:
                    self.conn.rollback()
                    raise Exception('error')
                finally:
                    e = None
                    del e

        finally:
            cursor.close()
            self.conn.close()

    def sqlDql(self, sql):
        cursor = self.getConn().cursor()
        try:
            try:
                cursor.execute(sql)
                return cursor.fetchall()
            except Exception as e:
                try:
                    logging.exception(e)
                finally:
                    e = None
                    del e

        finally:
            cursor.close()
            self.conn.close()

    def sqlDqlp(self, sql, *args):
        cursor = self.getConn().cursor()
        try:
            try:
                cursor.execute(sql, args)
                return cursor.fetchall()
            except Exception as e:
                try:
                    print(e)
                finally:
                    e = None
                    del e

        finally:
            cursor.close()
            self.conn.close()

    def sqlDdl(self, sql):
        cursor = self.getConn().cursor()
        try:
            res = cursor.execute(sql)
            return res
        except Exception as e:
            try:
                logging.exception(str(e))
                raise e
            finally:
                e = None
                del e

    def flushPrivs(self):
        cursor = self.getConn().cursor()
        sql = 'flush privileges'
        try:
            res = cursor.execute(sql)
            return res
        except Exception as e:
            try:
                logging.exception(str(e))
                raise e
            finally:
                e = None
                del e

    def grant_user_privs(self, user, host, db, table=None, privs=[]):
        speprivs = set(set(privs) & set(['super', 'file', 'process', 'replication slave', 'all']))
        routines = set(set(privs) & set(['create routine', 'alter routine']))
        print('speprivs:', speprivs, 'routines', routines)
        if speprivs:
            if routines:
                mix_privs = list(set(set(speprivs) | set(routines)))
                if len(mix_privs) > 1:
                    for p in mix_privs:
                        try:
                            if p == 'all':
                                sql = "grant {p} on {db}.* to {user}@'{host}'".format(p=p, db=db, user=user, host=host)
                                res = self.sqlDdl(sql)
                            else:
                                sql = "grant {p} on *.* to {user}@'{host}'".format(p=p, user=user, host=host)
                                res = self.sqlDdl(sql)
                        except Exception as e:
                            try:
                                logging.exception(str(e))
                                break
                                return 1
                            finally:
                                e = None
                                del e

                    if res == 0:
                        return 0
                    return 1
                else:
                    if list(mix_privs)[0] == 'all':
                        sql = "grant {p} on {db}.* to {user}@'{host}'".format(p=(list(speprivs)[0]), db=db, user=user, host=host)
                    else:
                        sql = "grant {p} on *.* to {user}@'{host}'".format(p=(list(speprivs)[0]), db=db, user=user, host=host)
                    print(sql)
                    res = self.sqlDdl(sql)
                    if res == 0:
                        return 0
                    return 1
            if list(speprivs):
                if len(speprivs) > 1:
                    for p in speprivs:
                        try:
                            if p == 'all':
                                sql = "grant {p} on {db}.* to {user}@'{host}'".format(p=p, db=db, user=user, host=host)
                                res = self.sqlDdl(sql)
                            else:
                                sql = "grant {p} on *.* to {user}@'{host}'".format(p=p, user=user, host=host)
                                res = self.sqlDdl(sql)
                        except Exception as e:
                            try:
                                logging.exception(str(e))
                                break
                                return 1
                            finally:
                                e = None
                                del e

                    if res == 0:
                        return 0
                    return 1
        else:
            if list(speprivs)[0] == 'all':
                sql = "grant {p} on {db}.* to {user}@'{host}'".format(p=(list(speprivs)[0]), db=db, user=user, host=host)
            else:
                sql = "grant {p} on *.* to {user}@'{host}'".format(p=(list(speprivs)[0]), db=db, user=user, host=host)
            print(sql)
            res = self.sqlDdl(sql)
        if res == 0:
            return 0
            return 1
        else:
            if list(routines):
                if len(routines) > 1:
                    for p in routines:
                        sql = "grant {p} on {db}.* to {user}@'{host}'".format(p=p, db=db, user=user, host=host)
                        print(sql)
                        try:
                            res = self.sqlDdl(sql)
                        except Exception as e:
                            try:
                                logging.exception(str(e))
                                break
                                return 1
                            finally:
                                e = None
                                del e

                    if res == 0:
                        return 0
                    return 1
                else:
                    sql = "grant {p} on {db}.* to {user}@'{host}'".format(p=(list(routines)[0]), db=db, user=user, host=host)
                    print(sql)
                    res = self.sqlDdl(sql)
                    if res == 0:
                        return 0
                    return 1
            if table:
                if len(privs) > 1:
                    for p in privs:
                        sql = "grant {p} on {db}.{table} to {user}@'{host}'".format(p=p, db=db, table=table, user=user, host=host)
                        print(sql)
                        res = self.sqlDdl(sql)
                        if res != 0:
                            break
                            return 1

                    return 0
                sql = "grant {p} on {db}.{table} to {user}@'{host}'".format(p=privs, db=db, table=table, user=user, host=host)
                print(sql)
                res = self.sqlDdl(sql)
                if res == 0:
                    return 0
                return 1
            else:
                if len(privs) > 1:
                    for p in privs:
                        sql = "grant {p} on {db}.* to {user}@'{host}'".format(p=p, db=db, user=user, host=host)
                        res = self.sqlDdl(sql)
                        if res != 0:
                            break
                            return 1

                    return 0
                sql = "grant {p} on {db}.* to {user}@'{host}'".format(p=privs, db=db, user=user, host=host)
                res = self.sqlDdl(sql)
                if res == 0:
                    return 0
                return 1

    def colseConn(self):
        self.conn.close()

    def getUser(self, db=None):
        if db:
            sql = "select DISTINCT concat(user,'@',host) from mysql.db where db='{db}'".format(db=db)
        else:
            sql = "select DISTINCT concat(user,'@',host) from mysql.user"
        return [db[0] for db in self.sqlDql(sql) if not str(db[0]).startswith(('root',
                                                                               'dbx',
                                                                               'mysql'))]

    def createUser(self, username, pwd):
        user = str(username).split('@')[0]
        host = str(username).split('@')[1]
        sql = "create user {user}@'{host}' identified by '{pwd}'".format(user=user, host=host, pwd=pwd)
        res = self.sqlDdl(sql)
        return res

    def dropUser(self, username):
        user = str(username).split('@')[0]
        host = str(username).split('@')[1]
        if host:
            sql = 'drop user {user}@{host}'.format(user=user, host=host)
            res = self.sqlDdl(sql)
        else:
            sql = 'drop user {user}'.format(user=user)
            res = self.sqlDdl(sql)
        return res

    def lockUser(self, user, host):
        sql = "alter user '{username}'@{host} account lock".format(username=user, host=host)
        print(sql)
        res = self.sqlDdl(sql)
        return res

    def unLockUser(self, user, host):
        sql = "alter user '{username}'@{host} account unlock".format(username=user, host=host)
        res = self.sqlDdl(sql)
        return res

    def getPrivileges(self, username):
        sql = 'show grants for {username}'.format(username=username)
        try:
            res = self.sqlDql(sql)
        except Exception as e:
            try:
                logging.exception(str(e))
                raise str(e)
            finally:
                e = None
                del e

        else:
            if res:
                return [p[0] for p in res]
            return res[0]

    def revokePrivs(self, user, host, db, table=None, privs=[]):
        speprivs = set(set(privs) & set(['super', 'file', 'process', 'replication slave', 'all']))
        routines = set(set(privs) & set(['create routine', 'alter routine']))
        if speprivs:
            if routines:
                mix_privs = list(set(set(speprivs) | set(routines)))
                if len(mix_privs) > 1:
                    for p in mix_privs:
                        try:
                            if p == 'all':
                                sql = "revoke {p} on {db}.* from {user}@'{host}'".format(p=p, db=db, user=user, host=host)
                                res = self.sqlDdl(sql)
                            else:
                                sql = "revoke {p} on *.* from {user}@'{host}'".format(p=p, user=user, host=host)
                                res = self.sqlDdl(sql)
                        except Exception as e:
                            try:
                                logging.exception(str(e))
                                break
                                return 1
                            finally:
                                e = None
                                del e

                    if res == 0:
                        return 0
                    return 1
                else:
                    if list(mix_privs)[0] == 'all':
                        sql = "revoke {p} on {db}.* from {user}@'{host}'".format(p=(list(speprivs)[0]), db=db, user=user, host=host)
                    else:
                        sql = "revoke {p} on *.* from {user}@'{host}'".format(p=(list(speprivs)[0]), db=db, user=user, host=host)
                    print(sql)
                    res = self.sqlDdl(sql)
                    if res == 0:
                        return 0
                    return 1
        if list(speprivs):
            if len(speprivs) > 1:
                for p in speprivs:
                    try:
                        if p == 'all':
                            sql = "revoke {p} on {db}.* from {user}@'{host}'".format(p=p, db=db, user=user, host=host)
                            res = self.sqlDdl(sql)
                        else:
                            sql = "revoke {p} on *.* from {user}@'{host}'".format(p=p, user=user, host=host)
                            res = self.sqlDdl(sql)
                    except Exception as e:
                        try:
                            logging.exception(str(e))
                            break
                            return 1
                        finally:
                            e = None
                            del e

                if res == 0:
                    return 0
                return 1
            else:
                if list(speprivs)[0] == 'all':
                    sql = "revoke {p} on {db}.* from {user}@'{host}'".format(p=(list(speprivs)[0]), db=db, user=user, host=host)
                else:
                    sql = "revoke {p} on *.* from {user}@'{host}'".format(p=(list(speprivs)[0]), db=db, user=user, host=host)
                res = self.sqlDdl(sql)
                if res == 0:
                    return 0
                return 1
        else:
            if list(routines):
                if len(routines) > 1:
                    for p in routines:
                        sql = "revoke {p} on {db}.* from {user}@'{host}'".format(p=p, db=db, user=user, host=host)
                        print(sql)
                        try:
                            res = self.sqlDdl(sql)
                            print(res)
                        except Exception as e:
                            try:
                                logging.exception(str(e))
                                break
                                return 1
                            finally:
                                e = None
                                del e

                        else:
                            if res == 0:
                                return 0

                else:
                    sql = "revoke {p} on {db}.* from {user}@'{host}'".format(p=(list(routines)[0]), db=db, user=user, host=host)
                    res = self.sqlDdl(sql)
                    if res == 0:
                        return 0
                    return 1
            if table:
                if len(privs) > 1:
                    for p in privs:
                        if p in list(set(set(speprivs) | set(routines))):
                            sql = "revoke {p} on *.* from {user}@'{host}'".format(p=p, user=user, host=host)
                        else:
                            sql = "revoke {p} on {db}.{table} from {user}@'{host}'".format(p=p, db=db, table=table, user=user,
                              host=host)
                        res = self.sqlDdl(sql)
                        if res != 0:
                            break
                            return 1

                    return 0
                sql = "revoke {p} on {db}.{table} from {user}@'{host}'".format(p=privs, db=db, table=table, user=user,
                  host=host)
                res = self.sqlDdl(sql)
                if res == 0:
                    return 0
                return 1
            else:
                if len(privs) > 1:
                    for p in privs:
                        if p in list(set(set(speprivs) | set(routines))):
                            sql = "revoke {p} on *.* from {user}@'{host}'".format(p=p, user=user, host=host)
                        else:
                            sql = "revoke {p} on {db}.* from {user}@'{host}'".format(p=p, db=db, user=user, host=host)
                        res = self.sqlDdl(sql)
                        if res != 0:
                            break
                            return 1

                    return 0
                sql = "revoke {p} on {db}.* from {user}@'{host}'".format(p=privs, db=db, user=user, host=host)
                res = self.sqlDdl(sql)
                if res == 0:
                    return 0
                return 1

    def generatePwd(self):
        pwd = random.sample(string.ascii_letters + string.digits, 10)
        return ''.join(pwd)


if __name__ == '__main__':
    logging.info('test...')