# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/beautifulpredicates/tests/predicates.py
# Compiled at: 2013-01-12 10:46:36
from django.test import TestCase, RequestFactory
from beautifulpredicates.predicates import RequestParamPredicate

class RequestParamPredicateTest(TestCase):
    rf = RequestFactory()

    def test_with_key(self):
        predicate = RequestParamPredicate('ritsu')
        self.assertEqual(predicate.k, 'ritsu')
        self.assertEqual(predicate.v, None)
        request = self.rf.get('/?ritsu', REQUEST_METHOD='GET')
        self.assertEqual(predicate(request), True)
        request = self.rf.get('/?mio', REQUEST_METHOD='GET')
        self.assertEqual(predicate(request), False)
        return

    def test_with_key_and_value(self):
        predicate = RequestParamPredicate('ritsu=drum')
        self.assertEqual(predicate.k, 'ritsu')
        self.assertEqual(predicate.v, 'drum')
        request = self.rf.get('/?ritsu=drum', REQUEST_METHOD='GET')
        self.assertEqual(predicate(request), True)
        request = self.rf.get('/?ritsu=bass', REQUEST_METHOD='GET')
        self.assertEqual(predicate(request), False)
        request = self.rf.get('/?ritsu', REQUEST_METHOD='GET')
        self.assertEqual(predicate(request), False)
        request = self.rf.get('/?mio=drum', REQUEST_METHOD='GET')
        self.assertEqual(predicate(request), False)