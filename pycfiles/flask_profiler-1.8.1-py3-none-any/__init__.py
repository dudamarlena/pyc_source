# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/muatik/projects/flask-profiler/flask_profiler/storage/__init__.py
# Compiled at: 2015-10-24 18:16:00


def getCollection(conf):
    engine = conf.get('engine', '').lower()
    if engine == 'mongodb':
        from .mongo import Mongo
        return Mongo(conf)
    if engine == 'sqlite':
        from .sqlite import Sqlite
        return Sqlite(conf)
    raise ValueError(('flask-profiler requires a valid storage engine but it is missing or wrong. provided engine: {}').format(engine))