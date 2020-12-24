# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fixture/django_testcase.py
# Compiled at: 2017-10-02 03:31:12
# Size of source mod 2**32: 630 bytes
from django.test.testcases import TestCase
from fixture import DjangoFixture

class FixtureTestCase(TestCase):
    __doc__ = "\n    Overrides django's fixture setup and teardown code to use DataSets.\n\n    See :ref:`Using Fixture With Django <using-fixture-with-django>` for a\n    complete example.\n\n    "

    @classmethod
    def setUpTestData(cls):
        super(FixtureTestCase, cls).setUpTestData()
        fixture = DjangoFixture()
        cls.data = (fixture.data)(*cls.datasets)
        cls.data.setup()

    @classmethod
    def tearDownClass(cls):
        cls.data.teardown()
        super(FixtureTestCase, cls).tearDownClass()