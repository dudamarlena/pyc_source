# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lance/.virtualenvs/wolverine/lib/python3.5/site-packages/tests/test_app.py
# Compiled at: 2016-01-06 17:38:29
# Size of source mod 2**32: 355 bytes
from wolverine.test import TestMicroApp

def test_app_init(event_loop):
    app = TestMicroApp(event_loop)
    assert app.config != None
    app.run()
    assert app.router != None
    print(app.modules.keys())
    assert 'registry' in app.modules.keys()
    assert 'router' in app.modules.keys()
    event_loop.run_until_complete(app.stop('SIGINT'))