# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/example/venv_impex/lib/python3.5/site-packages/impaf/controller/tests/test_json.py
# Compiled at: 2015-06-17 12:23:17
# Size of source mod 2**32: 356 bytes
from pytest import fixture
from ..json import JsonController
from .test_controller import ControllerFixtures

class TestJsonController(ControllerFixtures):

    @fixture
    def controller(self, mroot_factory, mrequest):
        return JsonController(mroot_factory, mrequest)

    def test_normal_run(self, controller):
        assert controller() == {}