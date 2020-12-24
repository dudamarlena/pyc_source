# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hgwebcommit/repository/base.py
# Compiled at: 2011-10-28 19:16:45


class BaseRepository(object):

    def __init__(self, **kwargs):
        pass

    def get_name(self):
        raise NotImplementedError

    @property
    def name(self):
        return self.get_name()

    def get_path(self):
        raise NotImplementedError

    @property
    def path(self):
        return self.get_path()

    def parent_date(self):
        raise NotImplementedError

    def parent_revision(self):
        raise NotImplementedError

    def parent_number(self):
        raise NotImplementedError

    def branch(self):
        raise NotImplementedError

    def status_modified(self):
        raise NotImplementedError

    def status_added(self):
        raise NotImplementedError

    def status_removed(self):
        raise NotImplementedError

    def status_deleted(self):
        raise NotImplementedError

    def status_unknown(self):
        raise NotImplementedError

    def add(self, files):
        raise NotImplementedError

    def commit(self, files, commit_message):
        raise NotImplementedError

    def revert(self, files, no_backup=True):
        raise NotImplementedError

    def remove(self, files):
        raise NotImplementedError