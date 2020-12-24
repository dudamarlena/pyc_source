# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/mahound/projects/ourse/ourse/driver/ZEODriver.py
# Compiled at: 2008-04-04 14:26:47
import re
from ZEO import ClientStorage
from ZODB.DB import DB
from persistent.list import PersistentList
import transaction
from basic import OURSEDriverException, OURSEDriver

class ZEODriver(OURSEDriver):

    class PathRunner:

        def get(self, node, path, bindings):
            if path == []:
                return node
            else:
                field = path[0]
                m = re.match('{(.+)}', field)
                if m:
                    print getattr(node, m.group(1))
                    return self.get(getattr(node, m.group(1)), path[1:], bindings)
                m = re.match('@@(.+)@@', field)
                if m:
                    field = bindings[m.group(1)]
                return self.get(node[field], path[1:], bindings)

        def __init__(self, driverInstance, zpath):
            self._driverInstance = driverInstance
            self._path = path = zpath.encode('latin-1').split('/')

        def execute(self, bindings):
            result = self.get(self._driverInstance.getRoot(), self._path, bindings)
            return result

    class Instance:
        pass

    def __init__(self, protocol, address, username, password):
        if protocol != 'zeo':
            raise OURSEDriverException("Protocol '%s' unknown..." % protocol)
        m = re.match('((?P<username>.*)(:(?P<password>.*))?@)?(?P<host>.*):(?P<port>.*)', address)
        if not m:
            raise OURSEDriverException("Address '%s' unknown." % address)
        data = m.groupdict()
        self.__instance = None
        self.__connection = None
        self.__root = None
        (self._username, self._password, self._host, self._port) = (
         data['username'], data['password'], data['host'], data['port'])
        return

    def getInstance(self):
        if not self.__instance:
            self.__instance = ZEODriver.Instance()
            self.__instance.storage = ClientStorage.ClientStorage((self._host, int(self._port)), username=self._username, password=self._password)
            self.__instance.db = DB(self.getInstance().storage)
        return self.__instance

    def getRoot(self):
        if self.__connection == None:
            raise OURSEDriverException('Connection was not started!')
        return self.__root

    def startRequest(self):
        self.__connection = self.getInstance().db.open()
        self.__root = self.__connection.root()

    def endRequest(self):
        self.__connection.close()
        self.__root = None
        self.__connection = None
        return

    def isList(self, obj):
        if type(obj) in [list, PersistentList]:
            return True
        else:
            return False