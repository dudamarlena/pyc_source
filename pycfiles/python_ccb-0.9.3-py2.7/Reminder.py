# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ccb/Reminder.py
# Compiled at: 2012-11-09 16:40:24
"""
Copyright 2012 Oscar Curero

This code is free software; you can redistribute it and/or modify it
under the terms of the GPL 3 license (see the file
COPYING.txt included with the distribution).
"""
from Utils import *
from Exceptions import *
from Base import *
from Transaction import *
from Account import *

def getReminderList(auth, cache, upcoming_days=False):
    reminderList = []
    if upcoming_days == False:
        data = {}
    else:
        data = {'upcoming_days': upcoming_days}
    response = sendCommand('GET', 'reminders', data, auth)
    for item in response:
        reminder = Reminder(auth, cache, item)
        reminder.onCommit = ''
        reminderList.append(reminder)

    return tuple(reminderList)


def getReminderFromId(auth, cache, id):
    reminder = searchCacheById(cache, 'reminders', id)
    if reminder != False:
        deleteCache(cache, reminder, id)
        reminder = Reminder(auth, cache, sendCommand('GET', 'reminder', {'id': id}, auth))
        setattr(reminder, 'onCommit', 'modify')
        return reminder
    for reminder in getReminderList(auth, cache, False):
        if hasattr(reminder, 'id') and getattr(reminder, 'id') == id:
            reminder = Reminder(auth, cache, sendCommand('GET', 'reminder', {'id': id}, auth))
            setattr(reminder, 'onCommit', 'modify')
            return reminder

    raise ReminderNotFoundError('reminder_id %s not found' % (id,))


def getReminderObjectFromName(auth, cache, name):
    reminder = searchCacheByName(cache, 'reminders', name)
    if name is None:
        return
    else:
        if reminder != False:
            return reminder
        for reminder in getReminderList(auth, cache):
            if hasattr(reminder, 'name') and getattr(reminder, 'name').upper() == name.upper():
                return reminder

        raise ReminderNotFoundError('%s' % (name,))
        return


class Reminder(Base):
    SPECIALATTRS = [
     'EMAIL', 'OCCUR_ONCE', 'OCCUR_REPEATING', 'OCCUR_FLOATING', 'REPEAT_EVERY', 'FLOAT_EVERY', 'TRANSACTION', 'TRANS_TRANSACTION_TYPE']
    EMAIL = OCCUR_ONCE = OCCUR_REPEATING = OCCUR_FLOATING = TRANSACTION = {True: 'true', False: 'false'}
    REPEAT_EVERY = {'day': 1, 'week': 2, 'month': 3, 'year': 4}
    FLOAT_EVERY = {'sunday': 0, 'monday': 1, 'tuesday': 2, 'wednesday': 3, 'thursday': 4, 'friday': 5, 'saturday': 6, 'day': -1}
    TRANS_TRANSACTION_TYPE = {'withdraw': 0, 'deposit': 1, 'transfer': 3}

    def __init__(self, auth, cache, data):
        Base.__init__(self, auth, cache, data)
        self.name = self.title
        self.reminder_id = self.id
        if self.trans_amount != 0:
            self.transaction = True
            data_transact = {}
            data_transact['account_id'] = self.trans_account_id
            data_transact['category_id'] = self.trans_category_id
            data_transact['trans_transfertoaccount'] = self.trans_transfertoaccount
            data_transact['amount'] = self.trans_amount
            data_transact['description'] = self.trans_description
            data_transact['transaction_type'] = self.trans_transaction_type
            data_transact['check_sum'] = self.trans_check_num
            data_transact['memo'] = self.trans_memo
            data_transact['payee'] = self.trans_payee
            self.transact = Transaction(auth, None, data_transact)
            self.transact.onCommit = ''
        else:
            self.transaction = False
        self.attributes.append('transaction')
        self.attributes = self.attributes + ['occur_floating', 'occur_repeating',
         'occur_once', 'email', 'emailDays', 'start_year', 'start_month', 'start_day',
         'end_year', 'end_month', 'end_day']
        self.email = self.notify
        del self.notify
        self.attributes.remove('notify')
        self.emailDays = self.notify_time
        del self.notify_time
        self.attributes.remove('notify_time')
        if self.trans_transaction_type == 'transfer':
            self.attributes = self.attributes + ['trans_accountFrom', 'trans_accountTo']
            self.trans_accountFrom = self.trans_account_id
            self.trans_accountTo = self.trans_transfertoaccount
            del self.trans_transfertoaccount
            self.attributes.remove('trans_transfertoaccount')
        if self.floats:
            self.occur_floating = True
        else:
            self.occur_floating = False
        if self.repeat:
            self.occur_repeating = True
        else:
            self.occur_repeating = False
        if not self.floats and not self.repeat:
            self.occur_once = True
        else:
            self.occur_once = False
        self.start_year = self.start_date.split(' ')[0].split('-')[0]
        self.start_month = self.start_date.split(' ')[0].split('-')[1]
        self.start_day = self.start_date.split(' ')[0].split('-')[2]
        self.end_year = self.end_date.split(' ')[0].split('-')[0]
        self.end_month = self.end_date.split(' ')[0].split('-')[1]
        self.end_day = self.end_date.split(' ')[0].split('-')[2]
        del self.floats
        self.attributes.remove('floats')
        del self.repeat
        self.attributes.remove('repeat')
        del self.start_date
        self.attributes.remove('start_date')
        del self.end_date
        self.attributes.remove('end_date')
        self.attributes.append('reminder_id')
        return

    def deleteAssociatedTransaction(self):
        if self.transaction == True:
            self.transact = None
            self.transaction = False
        return

    def createAssociatedTransaction(self, data):
        self.transact = Transaction(self.auth, None, None)
        self.transaction = True
        return

    def cloneReminder(self):
        return cloneObject(self)

    def getAccountFrom(self):
        account = searchCacheById(self.cache, 'accounts', self.trans_account_id)
        if account != False:
            return account
        else:
            return getAccountObjectFromId(self.auth, self.cache, self.trans_account_id)

    def getAccountTo(self):
        account = searchCacheById(self.cache, 'accounts', self.trans_accountTo)
        if account != False:
            return account
        else:
            return getAccountObjectFromId(self.auth, self.cache, self.trans_accountTo)