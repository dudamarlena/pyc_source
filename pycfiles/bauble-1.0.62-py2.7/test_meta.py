# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bauble/test/test_meta.py
# Compiled at: 2016-10-03 09:39:22
import bauble.meta as meta
from bauble.test import BaubleTestCase

class MetaTests(BaubleTestCase):

    def __init__(self, *args):
        super(MetaTests, self).__init__(*args)

    def test_get_default(self):
        """
        Test bauble.meta.get_default()
        """
        name = 'name'
        obj = meta.get_default(name)
        self.assert_(obj is None)
        value = 'value'
        meta.get_default(name, default=value)
        obj = self.session.query(meta.BaubleMeta).filter_by(name=name).one()
        self.assert_(obj.value == value)
        value2 = 'value2'
        obj = meta.get_default(name, default=value2)
        self.assert_(obj.value == value)
        obj = meta.get_default('name2', default=value, session=self.session)
        self.assert_(obj in self.session.new)
        return