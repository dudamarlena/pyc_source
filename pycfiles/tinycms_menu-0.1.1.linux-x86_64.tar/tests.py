# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tinycms_menu/tests.py
# Compiled at: 2014-11-14 09:29:30
from django.test import TestCase
from django.test.client import Client
from models import *
from views import *
import datetime

class ModellTest(TestCase):

    def setUp(self):
        pass

    def test_model_normal(self):
        pass


class DummyRequest:

    def __init__(self, user=None, GET={}):
        self.user = user
        self.GET = GET
        self.POST = {}
        self.method = 'GET'


class ViewTest(TestCase):

    def setUp(self):
        Dispatcher.clear()

    def test_content(self):
        pass