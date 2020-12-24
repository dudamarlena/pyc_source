# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webdb/adapter/abc.py
# Compiled at: 2018-02-13 11:58:53
# Size of source mod 2**32: 1835 bytes
from abc import ABCMeta, abstractmethod
from .exceptions import DatabaseError

class AbstractDBMS(metaclass=ABCMeta):
    __doc__ = '\n\tAbstract base class for all DBMS backends.\n\t'
    apilevel = None
    threadsafety = None

    def __init__(self):
        self.inject = None
        self.inject_as = None

    @abstractmethod
    def dispatch_DB(self, db_name):
        """
                Try to connect to this database. Return a new AbstractDB
                instance. This DB should not be opened yet 
                (``open`` will be called later).

                **Note**: A DBMS might manage several different DBs.
                """
        pass

    def handle_request(self, request):
        """
                Handle a request and return the result. The result might be 
                an exception or any kind of data that can be JSON serialized.
                """
        db = self.dispatch_DB(request['database'])
        if not db:
            raise DatabaseError()
        db.open()
        try:
            try:
                if self.inject_as:
                    result = db.handle_request((request['request']), inject=(self.inject()),
                      inject_as=(self.inject_as))
                else:
                    result = db.handle_request(request['request'])
            except BaseException as e:
                result = e

        finally:
            db.close()

        return result


class AbstractDB(metaclass=ABCMeta):
    __doc__ = '\n\tAbstract base class for Databases. \n\t'

    @abstractmethod
    def open(self, *args):
        """
                Bring this database in a state where it
                can execute queries.
                """
        pass

    @abstractmethod
    def close(self, *args):
        """
                Clean up the database after usage. Close sockets/files, ...
                """
        pass

    @abstractmethod
    def handle_request(self, request, inject=None, inject_as=None):
        """
                Handle a request. Inject ``inject`` if ``inject_as`` has a
                value that can be interpreted as True.
                Commit changes if necessary.

                Return the result (any JSON seriaziable) or raise an 
                exception.
                """
        pass