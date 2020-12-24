# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/scpketer/Dev/rknfind/.env/lib/python3.7/site-packages/rknfind/db/model.py
# Compiled at: 2019-09-21 07:31:52
# Size of source mod 2**32: 873 bytes
import peewee
database = peewee.SqliteDatabase(None)

class BlockEntry(peewee.Model):
    decree = peewee.CharField()
    date = peewee.DateField()
    issuer = peewee.CharField()

    class Meta:
        database = database
        db_table = 'block_entries'


class BlockURL(peewee.Model):
    url = peewee.CharField()
    entry = peewee.ForeignKeyField(BlockEntry)

    class Meta:
        database = database
        db_table = 'block_urls'


class BlockDomain(peewee.Model):
    domain = peewee.CharField()
    entry = peewee.ForeignKeyField(BlockEntry)

    class Meta:
        database = database
        db_table = 'block_domains'


class BlockAddress(peewee.Model):
    address = peewee.CharField()
    entry = peewee.ForeignKeyField(BlockEntry)

    class Meta:
        database = database
        db_table = 'block_addresses'