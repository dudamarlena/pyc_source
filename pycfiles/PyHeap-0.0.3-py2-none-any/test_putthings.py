# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/tests/methods/test_putthings.py
# Compiled at: 2015-12-14 10:52:59
from healthvaultlib.tests.testbase import TestBase
from healthvaultlib.itemtypes.height import Height
from healthvaultlib.methods.putthings import PutThings
from healthvaultlib.methods.getthings import GetThings

class TestGetThings(TestBase):

    def test_putthings_create(self):
        h1 = self.get_height_object(1.2)
        h2 = self.get_height_object(1.4)
        method = PutThings([h1, h2])
        method.execute(self.connection)
        items = method.response.healthrecorditems
        for item in items:
            self.assertIsNotNone(item.key)

    def test_putthings_edit(self):
        h1 = self.get_height_object(1.2)
        method = PutThings([h1])
        method.execute(self.connection)
        items = method.response.healthrecorditems
        initial_key = items[0].key
        h1.value_m = 1.3
        method = PutThings([h1])
        method.execute(self.connection)
        items = method.response.healthrecorditems
        self.assertNotEqual(initial_key.version_stamp, items[0].key.version_stamp)

    def get_item_and_check_value(self, thing_key, value):
        height_filter = ThingFilter()
        height_format = ThingFormat()
        height_format.sections.append('core')
        height_format.sections.append('xml')
        height_filter.typeids.append('40750a6a-89b2-455c-bd8d-b420a4cb500b')
        group = ThingGroup([height_filter])
        group._format = height_format
        method = GetThings([group])
        method.execute(self.connection)

    def get_height_object(self, value_m):
        height = Height()
        height.value_m = value_m
        height.display_value = str(value_m * 100)
        height.display_units = 'cm'
        return height