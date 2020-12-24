# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/magot/commands.py
# Compiled at: 2006-11-05 14:27:02
from peak.api import *
from magot.model import *
from magot.refdata import *
DB_FILENAME = PropertyName('magot.db.filename')
DB_FILEPATH = PropertyName('magot.db.filepath')

class Magot(commands.Bootstrap):
    __module__ = __name__
    acceptURLs = False
    usage = '\nUsage: magot <command> [<arguments>]\n\nAvailable commands:\n\n    gui      -- launchs user interface\n    newdb    -- creates a new database\n    accounts -- displays all accounts with their balances\n    account <accountName> -- displays one account\n    check    -- checks the accounting equation\n    addTx <desc debitAccount creditAccount amount [date num]> -- adds a new Transaction\n'
    db_filename = binding.Obtain(DB_FILENAME)

    def db_filepath(self):
        import os, user
        result = user.home + '/.magot'
        if not os.path.exists(result):
            os.mkdir(result)
        return result + '/' + self.db_filename

    db_filepath = binding.Make(db_filepath, offerAs=[DB_FILEPATH])
    Accounts = binding.Make('magot.storage.AccountDM', offerAs=[storage.DMFor(Account)])


class newDatabaseCmd(commands.AbstractCommand):
    __module__ = __name__
    usage = '\nUsage: newdb\n\ncreate a new database.\n'
    Accounts = binding.Obtain(storage.DMFor(Account))
    db_filepath = binding.Obtain(DB_FILEPATH)

    def _run(self):
        if len(self.argv) < 1:
            raise commands.InvocationError('Missing command')
        if len(self.argv) == 1:
            from magot.tests import test_storage
            test_storage.makeDB(self.db_filepath)
        else:
            from magot.tests import test_real_estate
            test_real_estate.makeDB(self.db_filepath)


class displayAccountsCmd(commands.AbstractCommand):
    __module__ = __name__
    usage = '\nUsage: accounts\n\nDisplays all accounts.\n'
    Accounts = binding.Obtain(storage.DMFor(Account))

    def _run(self):
        if len(self.argv) < 1:
            raise commands.InvocationError('Missing command')
        storage.begin(self)
        for acc1 in self.Accounts.root.subAccounts:
            print >> self.stdout, repr(acc1)
            for acc2 in acc1.subAccounts:
                print >> self.stdout, '\t' + repr(acc2)

        storage.abort(self)


class checkEquationCmd(commands.AbstractCommand):
    __module__ = __name__
    usage = '\nUsage: check\n\nChecks the accounting equation : Assets + Expenses = Equity + Liabilities + Income\n'
    Accounts = binding.Obtain(storage.DMFor(Account))

    def _run(self):
        if len(self.argv) < 1:
            raise commands.InvocationError('Missing command')
        storage.begin(self)
        debit = credit = Money.Zero
        for account in self.Accounts.root.subAccounts:
            if account.isDebit:
                debit += account.balance
            else:
                credit += account.balance

        assert debit == credit, 'The accounting equation is not correct'
        print 'The accounting equation is correct'
        storage.abort(self)


class displayAccountCmd(commands.AbstractCommand):
    __module__ = __name__
    usage = '\nUsage: account accountName\n\nDisplays one account.\n'
    Accounts = binding.Obtain(storage.DMFor(Account))

    def _run(self):
        if len(self.argv) < 2:
            raise commands.InvocationError('Missing account name')
        storage.begin(self)
        account = self.Accounts.get(self.argv[1])
        print >> self.stdout, str(account)
        if isinstance(account, Account):
            for entry in account.entries:
                print >> self.stdout, str(entry)

        storage.abort(self)


class addTransactionCmd(commands.AbstractCommand):
    __module__ = __name__
    usage = '\nUsage: addTx desc debitAccount creditAccount amount [date num]\n\nAdd a new Transaction.\n'
    Accounts = binding.Obtain(storage.DMFor(Account))

    def _run(self):
        if len(self.argv) < 5:
            raise commands.InvocationError('Missing arguments')
        parts = (' ').join(self.argv[1:]).split(' ')
        if len(parts) != 4:
            raise commands.InvocationError('Bad argument format')
        (desc, debit, credit, amount) = [ part.strip() for part in parts ]
        storage.begin(self)
        debitAcc = self.Accounts.get(debit)
        creditAcc = self.Accounts.get(credit)
        tx = Transaction(Date.today(), desc, debitAcc, creditAcc, amount)
        storage.commit(self)


def runMain():
    root = config.makeRoot(iniFiles=(('peak', 'peak.ini'), ('magot', 'magot.ini')))
    Magot(root).run()


if __name__ == '__main__':
    runMain()