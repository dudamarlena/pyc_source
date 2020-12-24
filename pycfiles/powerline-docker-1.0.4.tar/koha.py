# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/powerline/plugins/koha.py
# Compiled at: 2008-04-11 17:59:53
from powerline import database
from powerline.database import user_checker, settings_model
from datetime import date
import MySQLdb, dbwrap
from decimal import Decimal

class koha_checker(user_checker):

    def __init__(self, connection):
        try:
            self.connection = dbwrap.wrapper(MySQLdb.connect(user=database.koha_user, host=getattr(database, 'koha_host', 'localhost'), passwd=database.koha_password, db=getattr(database, 'koha_db', 'Koha'), use_unicode=True, charset='utf8'), placeholder='%s')
        except AttributeError, e:
            raise AttributeError('koha.py not configured; %s' % e)

        settings_model(connection).register('koha.threshold', 0.0, 'decimal')
        self.threshold = settings_model(connection)['koha.threshold']

    def verify(self, username):
        if not self.exists(username):
            raise KeyError(username)
        fines = self.connection.accountlines.rows('borrowernumber = (SELECT borrowernumber FROM borrowers WHERE cardnumber = %s)', username).select_value('SUM(amountoutstanding)')
        if fines > self.threshold:
            return (False, 'You have $%.2f in fines that need to be paid' % fines)
        else:
            return (
             True, '')

    def exists(self, username):
        return self.connection.borrowers.rows(cardnumber=username).exist()