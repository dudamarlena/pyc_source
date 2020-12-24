# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/BTEdb.py
# Compiled at: 2016-06-11 23:27:28
import sys, json, copy, dill, base64, os, itertools
if __name__ == '__main__':
    print 'Python schemaless JSON/YAML database interface'
    print 'Do not execute directly'
    sys.exit(1)

class DatabaseNotCreatedException(BaseException):
    pass


class DatabaseWriteIOErrorException(BaseException):
    pass


class TableDoesNotExistException(BaseException):
    pass


class SavepointDoesNotExistException(BaseException):
    pass


class TriggerDoesNotExistException(BaseException):
    pass


class DuplicateTriggerNameExistsException(BaseException):
    pass


class NoTransactionInProgressException(BaseException):
    pass


class TransactionNotRevertableException(BaseException):
    pass


class Database:

    def __init__(self, filename=False, pretty=False):
        self.master = False
        self.fileObj = None
        self.init = False
        self.pretty = False
        self.saves = False
        self.triggers = False
        self.TransactionInProgress = False
        if filename:
            self.OpenDatabase(filename, pretty)
        return

    def __str__(self):
        return str(self.master)

    def __repr__(self):
        return '<BTEdb Database object. Initialized: ' + str(self.init) + ', file: ' + str(fileObj) + '>'

    def OpenDatabase(self, filename, pretty=False):
        if self.init == True:
            self.Destroy()
        self.__init__()
        self.pretty = pretty
        try:
            if type(filename) == str:
                try:
                    self.fileObj = open(filename, 'r+', os.O_NONBLOCK, encoding='utf8')
                except TypeError:
                    self.fileObj = open(filename, 'r+', os.O_NONBLOCK)

            else:
                self.master = json.loads(filename.read())
                self.fileObj = filename
            self.fileObj.seek(0, 0)
            self.master, self.saves, self.triggers = json.loads(self.fileObj.read())
            self._write(True)
        except (IOError, ValueError):
            try:
                self.fileObj = open(filename, 'w', os.O_NONBLOCK)
                self.master = {}
                self.saves = {}
                self.triggers = []
            except:
                raise DatabaseWriteIOErrorException()

        except:
            raise DatabaseWriteIOErrorException()
            self.master = {}
            self.saves = {}
            self.triggers = []

        self.init = True

    def Destroy(self):
        self._write(True)
        self.init = False
        self.fileObj.close()
        self.__init__()

    def _matches(self, z, args, kwargs):
        for x, y in kwargs.items():
            try:
                if z[x] != y:
                    return False
            except KeyError:
                return False

        for a in args:
            if type(a) != type(lambda : True):
                raise TypeError
            if not a(z):
                return False

        return True

    def Create(self, table):
        if not self.init:
            raise DatabaseNotCreatedException()
        if self.TableExists(table):
            self.Truncate(table)
        else:
            self.master[table] = []
        self._write()

    def CreateTable(self, name):
        self.Create(name)

    def Drop(self, table):
        if not self.init:
            raise DatabaseNotCreatedException()
        if not self.TableExists(table):
            raise TableDoesNotExistException()
        del self.master[table]
        self._write()

    def TableExists(self, table):
        if not self.init:
            raise DatabaseNotCreatedException()
        if table in self.master:
            return True
        else:
            return False

    def Select(self, table, *args, **kwargs):
        if not self.init:
            raise DatabaseNotCreatedException()
        if not self.TableExists(table):
            raise TableDoesNotExistException()
        results = []
        for z in self.master[table]:
            if self._matches(z, args, kwargs):
                results.append(z)

        return results

    def Update(self, table, olddata, *args, **kwargs):
        if not self.init:
            raise DatabaseNotCreatedException()
        if not self.TableExists(table):
            raise TableDoesNotExistException()
        for x in olddata:
            self._runTrigger('BEFORE UPDATE', table, x)
            idx = self.master[table].index(x)
            for y, z in kwargs.items():
                self.master[table][idx][y] = z

            for arg in args:
                self.master[table][idx][arg[0]] = arg[1]

            self._runTrigger('AFTER UPDATE', table, self.master[table][idx])

        self._write()

    def Delete(self, table, *args, **kwargs):
        if not self.init:
            raise DatabaseNotCreatedException()
        results = []
        for z in copy.deepcopy(self.master[table]):
            if self._matches(z, args, kwargs):
                self._runTrigger('BEFORE DELETE', table, z)
                del self.master[table][self.master[table].index(z)]
                self._runTrigger('AFTER DELETE', table, z)
                results.append(z)

        self._write()
        return results

    def Dump(self, table=False):
        if not self.init:
            raise DatabaseNotCreatedException()
        if table:
            if self.TableExists(table):
                return self.master[table]
            raise TableDoesNotExistException()
        return self.master

    def Insert(self, table, *args, **kwargs):
        if not self.init:
            raise DatabaseNotCreatedException()
        if not self.TableExists(table):
            raise TableDoesNotExistException()
        for arg in args:
            kwargs[arg[0]] = arg[1]

        self._runTrigger('BEFORE INSERT', table, kwargs)
        self.master[table].append(kwargs)
        self._runTrigger('AFTER INSERT', table, kwargs)
        self._write()

    def Truncate(self, table):
        if not self.init:
            raise DatabaseNotCreatedException()
        if self.TableExists(table):
            self.master[table] = []
        else:
            raise TableDoesNotExistException()
        self._write()

    def ListTables(self):
        if not self.init:
            raise DatabaseNotCreatedException()
        return [ x for x, y in self.master.items() ]

    def Vacuum(self):
        self._write(True)

    def BeginTransaction(self, makeSave=True):
        self.TransactionInProgress = True
        if makeSave:
            self.Save('transaction')
        elif self.SaveExists('transaction'):
            self.RemoveSave('transaction')

    def CommitTransaction(self):
        if not self.TransactionInProgress:
            raise NoTransactionInProgressException()
        self.TransactionInProgress = False
        if self.SaveExists('transaction'):
            self.RemoveSave('transaction')
        self._write()

    def RevertTransaction(self):
        if not self.TransactionInProgress:
            raise NoTransactionInProgressException()
        if self.SaveExists('transaction'):
            self.Revert('transaction')
            self.RemoveSave('transaction')
        else:
            raise TransactionNotRevertableException()
        self.TransactionInProgress = False
        self._write()

    def _write(self, override=False):
        if not self.init and not override:
            raise DatabaseNotCreatedException()
        if self.TransactionInProgress and not override:
            return
        try:
            self.fileObj.seek(0, 0)
            if self.pretty:
                self.fileObj.write(json.dumps([self.master, self.saves, self.triggers], indent=self.pretty))
            else:
                self.fileObj.write(json.dumps([self.master, self.saves, self.triggers]))
            self.fileObj.truncate()
            if self.fileObj.flush():
                os.fsync(self.fileObj.fileno())
        except IOError:
            raise DatabaseWriteIOErrorException()

    def SaveExists(self, name):
        if not self.init:
            raise DatabaseNotCreatedException()
        return name in self.saves

    def Save(self, name, table=False):
        if not self.init:
            raise DatabaseNotCreatedException()
        self.saves[name] = {}
        if table:
            self.saves[name][table] = copy.deepcopy(self.master[table])
        else:
            self.saves[name] = copy.deepcopy(self.master)
        self._write()

    def RemoveSave(self, name):
        if not self.init:
            raise DatabaseNotCreatedException()
        if not self.SaveExists(name):
            raise SavepointDoesNotExistException()
        del self.saves[name]

    def Revert(self, name, table=False):
        if not self.init:
            raise DatabaseNotCreatedException()
        if self.SaveExists(name):
            if table:
                self.master[table] = copy.deepcopy(self.saves[name][table])
            else:
                for table, unused in self.saves[name].items():
                    self.master[table] = copy.deepcopy(self.saves[name][table])

        else:
            raise SavepointDoesNotExistException()
        self._write()

    def GetSave(self, name=False, table=False):
        if not self.init:
            raise DatabaseNotCreatedException()
        if name:
            if table:
                return self.saves[name][table]
            return self.saves[name]
        else:
            return self.saves

    def ListSaves(self):
        if not self.init:
            raise DatabaseNotCreatedException()
        return [ x for x, y in self.saves.items() ]

    def PutSave(self, data, name=False):
        if not self.init:
            raise DatabaseNotCreatedException()
        if type(data) != dict:
            raise TypeError
        if name:
            self.saves[name] = data
        else:
            self.saves = data
        self._write()

    def _runTrigger(self, triggertype, table, datapoint):
        for x in self.triggers:
            if table == x[0] and triggertype == x[1]:
                dill.loads(base64.b64decode(x[2]))(self, datapoint, table, triggertype)

    def AddTrigger(self, name, triggertype, table, action):
        if triggertype not in ('BEFORE INSERT', 'AFTER INSERT', 'BEFORE DELETE', 'AFTER DELETE',
                               'BEFORE UPDATE', 'AFTER UPDATE'):
            raise NotImplementedError
        if not self.init:
            raise DatabaseNotCreatedException()
        if self.TriggerExists(name):
            raise DuplicateTriggerNameExistsException()
        if not self.TableExists(table):
            raise TableDoesNotExistException()
        self.triggers.append([table, triggertype, base64.b64encode(dill.dumps(action)).decode('utf-8', 'replace'), name])
        self._write()

    def RemoveTrigger(self, name):
        if not self.init:
            raise DatabaseNotCreatedException()
        if not self.TriggerExists(name):
            raise TriggerDoesNotExistException()
        for x in self.triggers:
            if x[3] == name:
                del self.triggers[self.triggers.index(x)]
                break

        self._write()

    def ListTriggers(self):
        if not self.init:
            raise DatabaseNotCreatedException()
        results = []
        for x in self.triggers:
            results.append([x[3], x[1], x[0]])

        return results

    def TriggerExists(self, name):
        if not self.init:
            raise DatabaseNotCreatedException()
        for x in self.triggers:
            if x[3] == name:
                return True

        return False