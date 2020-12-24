# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/CreateAppendGet/CAG.py
# Compiled at: 2011-06-02 07:00:44
from persistent.list import PersistentList
import AccessControl
from Globals import InitializeClass
View = 'View'
Manage = 'Manage'

class CAG:
    CAG_prefix = 'cag_storage_'
    CAG_archive_limit = 500
    CAG_last_archive = 0
    security = AccessControl.ClassSecurityInfo()

    def __init__(self, id, title):
        setattr(self, self.CAG_prefix + str(self.CAG_last_archive), PersistentList())

    security.declareProtected(View, 'CAG_append')

    def CAG_append(self, item):
        active_archive = getattr(self, self.CAG_prefix + str(self.CAG_last_archive))
        active_archive.append(item)
        if len(active_archive) > self.CAG_archive_limit:
            last = self.CAG_last_archive = self.CAG_last_archive + 1
            archive_id = self.CAG_prefix + str(last)
            setattr(self, archive_id, PersistentList())

    security.declareProtected(View, 'CAG_get_numbered_item')

    def CAG_get_numbered_item(self, archive, index):
        return getattr(self, self.CAG_prefix + str(archive))[index]

    security.declareProtected(View, 'CAG_get_since')

    def CAG_get_since(self, since_function, numbered=False):
        entries = self.CAG_get(count=100000000, numbered=numbered)
        for index in range(len(entries)):
            if since_function(entries[index]):
                return entries[index:]
        else:
            return []

    security.declareProtected(View, 'CAG_get_numbered_since')

    def CAG_get_numbered_since(self, since_function):
        return self.CAG_get_since(since_function, numbered=True)

    security.declareProtected(View, 'CAG_get_numbered')

    def CAG_get_numbered(self, count=300, context_archive=None, context_index=None):
        return self.CAG_get(count=count, numbered=True, context_archive=context_archive, context_index=context_index)

    security.declareProtected(View, 'CAG_get')

    def CAG_get(self, count=300, numbered=False, context_archive=None, context_index=None):
        last_archive = self.CAG_last_archive
        items = []
        while len(items) < count:
            if last_archive is -1:
                break
            try:
                prior_items = list(getattr(self, self.CAG_prefix + str(last_archive)))
                if numbered:
                    prior_items_ = []
                    for index in range(len(prior_items)):
                        prior_items[index] = (
                         last_archive, index, prior_items[index])

                prior_items.extend(items)
                items = prior_items
                last_archive = last_archive - 1
            except AttributeError:
                break

        if context_archive is not None:
            context = self.CAG_archive_limit * context_archive
            context = context + context_index
            start = max(0, context - count / 2)
            stop = context + count / 2
            return items[start:stop]
        else:
            items = items[-count:]
            return items
            return


InitializeClass(CAG)