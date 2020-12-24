# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/scandb/models.py
# Compiled at: 2019-09-17 10:08:37
# Size of source mod 2**32: 1950 bytes
from peewee import Proxy, SqliteDatabase
from peewee import Model, TextField, IntegerField, ForeignKeyField
database_proxy = Proxy()

class BaseModel(Model):

    class Meta:
        database = database_proxy


class Scan(BaseModel):
    file_hash = TextField(unique=True, null=False)
    name = TextField(null=False)
    type = TextField(null=False)
    start = TextField(null=True)
    end = TextField(null=True)
    elapsed = TextField(null=True)
    hosts_total = IntegerField(null=True)
    hosts_up = IntegerField(null=True)
    hosts_down = IntegerField(null=True)


class Host(BaseModel):
    address = TextField(null=False)
    hostname = TextField(null=True)
    os = TextField(null=True)
    os_gen = TextField(null=True)
    status = TextField(null=True)
    scan = ForeignKeyField(Scan, related_name='belongs_to')


class Port(BaseModel):
    host = ForeignKeyField(Host, related_name='from_host')
    address = TextField(null=False)
    port = IntegerField(null=False)
    protocol = TextField(null=False)
    service = TextField(null=True)
    banner = TextField(null=True)
    status = TextField(null=False)


class Vuln(BaseModel):
    host = ForeignKeyField(Host, related_name='vuln_on_host')
    description = TextField(null=False)
    synopsis = TextField(null=True)
    port = IntegerField(null=False)
    protocol = TextField(null=False)
    service = TextField(null=False)
    solution = TextField(null=True)
    severity = TextField(null=True)
    xref = TextField(null=True)
    info = TextField(null=True)
    plugin = TextField(null=True)
    risk = TextField(null=True)


def init_db(db):
    database = SqliteDatabase(db)
    database_proxy.initialize(database)
    database.connect()
    database.create_tables(models=[Scan, Host, Port, Vuln], safe=True)
    return database