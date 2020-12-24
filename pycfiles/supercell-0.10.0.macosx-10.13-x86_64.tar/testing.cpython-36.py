# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jannis/Documents/code/rtr-supercell/supercell/env3/lib/python3.6/site-packages/supercell/testing.py
# Compiled at: 2019-01-08 09:09:15
# Size of source mod 2**32: 1312 bytes
from __future__ import absolute_import, division, print_function, with_statement
import sys
from tornado.ioloop import IOLoop
from tornado.testing import AsyncHTTPTestCase as TornadoAsyncHTTPTestCase
import pytest

class AsyncHTTPTestCase(TornadoAsyncHTTPTestCase):
    ARGV = []
    SERVICE = None

    @pytest.fixture(autouse=True)
    def set_commandline(self, monkeypatch):
        monkeypatch.setattr(sys, 'argv', ['pytest'] + self.ARGV)

    def get_new_ioloop(self):
        return IOLoop.current()

    def get_app(self):
        service = self.SERVICE()
        service.initialize_logging()
        return service.get_app()