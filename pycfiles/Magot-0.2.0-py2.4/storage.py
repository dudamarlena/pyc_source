# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/magot/storage.py
# Compiled at: 2006-05-08 16:28:05
import cPickle
from peak.api import *
from peak.storage.files import EditableFile
from magot.model import *
from magot.commands import DB_FILEPATH

class AccountDM(storage.EntityDM):
    __module__ = __name__
    defaultClass = Account
    filename = binding.Obtain(DB_FILEPATH)
    file = binding.Make(lambda self: EditableFile(filename=self.filename))

    def root(self):
        text = self.file.text
        root = cPickle.loads(text)
        return root

    root = binding.Make(root)

    def _load(self, oid, ob):
        return self.get(oid)

    def _new(self, ob):
        self._save(ob)
        return ob.name

    def _save(self, ob):
        pass

    def flush(self, ob=None):
        super(AccountDM, self).flush(ob)
        self.file.text = cPickle.dumps(self.root)

    def get(self, oid, default=None):
        if oid in self.cache:
            return self.cache[oid]
        else:
            account = self._findAccount(oid, self.root)
            if account is None:
                raise exceptions.NameNotFound('Account ' + oid + ' not found')
            self.register(account)
            self.cache[oid] = account
            return account
        return default

    def _findAccount(self, oid, parent):
        for account in parent.subAccounts:
            if oid == account.name:
                return account

        for account in parent.subAccounts:
            acc = self._findAccount(oid, account)
            if acc is not None:
                return acc

        return

    def abortTransaction(self, ob):
        self._delBinding('root')
        super(AccountDM, self).abortTransaction(ob)