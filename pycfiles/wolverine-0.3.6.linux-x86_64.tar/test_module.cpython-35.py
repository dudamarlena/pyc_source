# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lance/.virtualenvs/wolverine/lib/python3.5/site-packages/tests/test_module.py
# Compiled at: 2016-01-06 17:07:29
# Size of source mod 2**32: 364 bytes
from wolverine.module import MicroModule
from wolverine.test import TestMicroApp

def test_micro_module(event_loop):
    app = TestMicroApp(loop=event_loop)
    module = MicroModule()
    module.name = 'mod'
    module.register_app(app)
    assert module.app == app
    module.run()
    event_loop.run_until_complete(module.stop())
    assert module.name == 'mod'