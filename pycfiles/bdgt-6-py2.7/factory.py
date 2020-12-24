# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bdgt/commands/factory.py
# Compiled at: 2014-10-31 03:15:09
from bdgt.commands import accounts, budget, categories, config, importer, transactions
__all__ = [
 'CommandFactory']

class CommandFactory(object):

    @classmethod
    def create(cls, args):
        assert hasattr(args, 'command')
        if args.command == 'account':
            return AccountCommandFactory.create(args)
        if args.command == 'category':
            return CategoryCommandFactory.create(args)
        if args.command == 'config':
            return ConfigCommandFactory.create(args)
        if args.command == 'import':
            return ImportCommandFactory.create(args)
        if args.command == 'tx':
            return TxCommandFactory.create(args)
        if args.command == 'set':
            return budget.CmdSet(args.category_name, args.period, args.amount)
        if args.command == 'status':
            return budget.CmdStatus(args.month, args.year)
        assert False


class AccountCommandFactory(object):

    @classmethod
    def create(cls, args):
        assert hasattr(args, 'sub_command')
        if args.sub_command == 'add':
            return accounts.CmdAddAccount(args.name, args.number)
        if args.sub_command == 'delete':
            return accounts.CmdDeleteAccount(args.name)
        if args.sub_command == 'list':
            return accounts.CmdListAccounts()
        assert False


class CategoryCommandFactory(object):

    @classmethod
    def create(cls, args):
        assert hasattr(args, 'sub_command')
        if args.sub_command == 'add':
            return categories.CmdAdd(args.name, args.parent)
        if args.sub_command == 'delete':
            return categories.CmdDelete(args.name)
        if args.sub_command == 'rename':
            return categories.CmdRename(args.name, args.new_name)
        assert False


class ConfigCommandFactory(object):

    @classmethod
    def create(cls, args):
        return config.CmdList(args)


class ImportCommandFactory(object):

    @classmethod
    def create(cls, args):
        assert hasattr(args, 'sub_command')
        if args.sub_command == 'add':
            return importer.CmdAdd(args.transaction_ids)
        if args.sub_command == 'remove':
            return importer.CmdRemove(args.transaction_ids)
        if args.sub_command == 'reset':
            return importer.CmdReset()
        if args.sub_command == 'set':
            return importer.CmdSet(args.field, args.value, args.transaction_ids)
        if args.sub_command == 'commit':
            return importer.CmdCommit()
        if args.sub_command == 'file':
            return importer.CmdImport(args.type_, args.file_, args.commit)
        if args.sub_command == 'status':
            return importer.CmdStatus()
        assert False


class TxCommandFactory(object):

    @classmethod
    def create(cls, args):
        assert hasattr(args, 'sub_command')
        if args.sub_command == 'list':
            return transactions.CmdListTx(args.account_name)
        if args.sub_command == 'assign':
            return transactions.CmdAssignTx(args.category_name, args.transaction_ids)
        if args.sub_command == 'unassign':
            return transactions.CmdUnassignTx(args.transaction_ids)
        if args.sub_command == 'reconcile':
            return transactions.CmdReconcileTx(args.transaction_ids)
        assert False