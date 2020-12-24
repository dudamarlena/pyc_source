# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/components/combo_box_value_change.py
# Compiled at: 2013-04-04 15:36:37
from muntjac.test.server.components import abstract_test_field_value_change
from muntjac.ui.combo_box import ComboBox

class TestComboBoxValueChange(abstract_test_field_value_change.AbstractTestFieldValueChange):
    """Check that the value change listener for a combo box is triggered
    exactly once when setting the value, at the correct time.
    """

    def setUp(self):
        combo = ComboBox()
        combo.addItem('myvalue')
        super(TestComboBoxValueChange, self).setUp(combo)

    def setValue(self, field):
        variables = dict()
        variables['selected'] = ['myvalue']
        field.changeVariables(field, variables)