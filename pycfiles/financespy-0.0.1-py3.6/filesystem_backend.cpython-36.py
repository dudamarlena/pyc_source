# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/financespy/filesystem_backend.py
# Compiled at: 2019-06-26 14:52:36
# Size of source mod 2**32: 921 bytes
import os
from financespy.transaction import parse_transaction
_months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']

class FilesystemBackend:

    def __init__(self, folder):
        self.folder = folder

    def insert_record(self, date, record):
        with open(self.file(date), '+a') as (f):
            f.write(str(record) + '\n')
            f.close()

    def records(self, date):
        if not os.path.exists(self.file(date)):
            return
        with open(self.file(date)) as (f):
            for line in f:
                transaction = parse_transaction(line.strip())
                transaction.date = date
                yield transaction

    def file(self, date):
        return self.month_folder(date) + str(date.day) + '.csv'

    def month_folder(self, date):
        return self.folder + str(date.year) + '/' + _months[(date.month - 1)] + '/'