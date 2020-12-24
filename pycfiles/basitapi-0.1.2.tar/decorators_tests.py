# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/omer/Projects/DjangoProjects/basitapi/basitapi/tests/decorators_tests.py
# Compiled at: 2013-04-25 14:26:42
from django.test import TestCase
from django.contrib.auth.models import User
from basitapi.decorators import load_model
from basitapi.tests import factories

class DecoratorsTest(TestCase):

    def test_load_model(self):
        user = factories.UserFactory()

        class TempObject:

            @load_model(model=User, id_name='user_id', access_name='user')
            def temp_method(self, request, user_id):
                print request
                return request.user.id

        class TempData:

            def __init__(self):
                pass

        temp_object = TempObject()
        self.assertEquals(user.id, temp_object.temp_method(TempData(), user_id=user.id))
        self.assertEquals(404, temp_object.temp_method(TempData(), user_id=123123123).status)