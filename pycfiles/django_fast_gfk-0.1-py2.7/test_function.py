# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fast_gfk/tests/test_function.py
# Compiled at: 2017-07-19 04:35:55
from threading import local
from django import db
from django.test import TestCase, override_settings
from fast_gfk import fetch
from fast_gfk.tests.models import Foo, Bar

class FunctionTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        super(FunctionTestCase, cls).setUpTestData()
        cls.foo1 = Foo.objects.create(title='Foo 1')
        cls.foo2 = Foo.objects.create(title='Foo 2')
        cls.bar1 = Bar.objects.create(title='Bar 1', target=cls.foo1)
        cls.bar2 = Bar.objects.create(title='Bar 2', target=cls.foo2)

    def test_fetch(self):
        bars = list(Bar.objects.all())
        dc = bars[0].target.title
        db.connections.close_all()
        old_connections = db.connections._connections
        db.connections._connections = local()
        try:
            dc = bars[1].target.title
            self.fail('The database was not destroyed correctly')
        except db.OperationalError:
            pass

        db.connections._connections = old_connections
        bars = list(fetch(Bar.objects.all(), 'target'))
        dc = bars[0].target.title
        db.connections.close_all()
        old_connections = db.connections._connections
        db.connections._connections = local()
        try:
            dc = bars[1].target.title
        except db.OperationalError:
            self.fail('The database should not be accessed')

        db.connections._connections = old_connections