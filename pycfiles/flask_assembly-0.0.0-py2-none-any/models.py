# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Mardix/Dropbox/Projects/Python/Flasik/devlab/new/t1/application/models.py
# Compiled at: 2019-08-24 20:44:56
"""
Flasik: models.py

Contains applications models and other databases connections.

Do not `import`. This module is loaded implicitely by Flasik

To setup: `flasik-admin sync-models`

-----
# ActiveAlchemy, 

Accessor: models.[ClassName]
ie: models.MyModel

class MyModel(db.Model):
    ...

-----

# Redis
Redis can also be connected in here

> db.connect_redis(name='rdb', url=get_config("REDIS_URL"))

Accessor: db.redis.[name]
ie: db.redis.rdb.set("key", "value")
"""
from flasik import db, get_config

class Test(db.Model):
    name = db.Column(db.String(255), index=True)