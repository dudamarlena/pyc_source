# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\migration\base_classes.py
# Compiled at: 2006-11-01 19:21:05
migrations = dict()

class MigrationMeta(type):
    __module__ = __name__

    def __init__(cls, name, *args, **kw):
        if name not in ['Migration', 'SOMigration', 'SAMigration'] and name.startswith('Migration'):
            version = int(name[-3:])
            migrations[version] = cls
        super(MigrationMeta, cls).__init__(*args, **kw)


class Migration(object):
    __module__ = __name__
    __metaclass__ = MigrationMeta

    def add_column(self, *args, **kw):
        assert 0, 'This has to be overriden'

    def del_column(self, *args, **kw):
        assert 0, 'This has to be overriden'

    def create_table(self, *args, **kw):
        assert 0, 'This has to be overriden'

    def drop_table(self, *args, **kw):
        assert 0, 'This has to be overriden'

    def up(self):
        assert 0, 'This has to be overriden'

    def down(self):
        assert 0, 'This has to be overriden'

    def query(self, query):
        assert 0, 'This has to be overriden'


class PackageVersion(object):
    __module__ = __name__

    def get_version(self):
        assert 0, 'This has to be overriden'

    def set_version(self, version):
        assert 0, 'This has to be overriden'