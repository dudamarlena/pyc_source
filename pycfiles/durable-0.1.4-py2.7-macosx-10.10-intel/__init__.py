# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/durable/__init__.py
# Compiled at: 2014-11-03 02:10:02


def run(ruleset_definitions=None, databases=['/tmp/redis.sock'], start=None):
    import engine, interface
    main_host = engine.Host(ruleset_definitions, databases)
    if start:
        start(main_host)
    main_app = interface.Application(main_host)
    main_app.run()