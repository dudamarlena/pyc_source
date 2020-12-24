# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/v2/theme/Extensions/migration.py
# Compiled at: 2010-11-24 05:03:53


def migrate(self, xmlFilePath, typeToCreate, folder):
    from v2.theme.migrator import XMLMigrator
    migrator = XMLMigrator(self, xmlFilePath, typeToCreate, folder)
    print '=== Starting Migration. ==='
    migrator.startMigration()
    return '=== Migration sucessfull. Created %d items on folder %s (%d errors and %d skipped) ===' % (migrator.created, migrator.folderPath, migrator.errors, migrator.skipped)