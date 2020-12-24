# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/components/text_field_value_change.py
# Compiled at: 2013-04-04 15:36:37
import mox, unittest
from muntjac.test.server.components import abstract_test_field_value_change
from muntjac.ui.text_field import TextField
from muntjac.data.util.object_property import ObjectProperty
from muntjac.data.property import ValueChangeEvent, IValueChangeListener

class TestTextFieldValueChange(abstract_test_field_value_change.AbstractTestFieldValueChange):
    """Check that the value change listener for a text field is triggered
    exactly once when setting the value, at the correct time.
    """

    def setUp(self):
        super(TestTextFieldValueChange, self).setUp(TextField())

    def setValue(self, field):
        variables = dict()
        variables['text'] = 'newValue'
        field.changeVariables(field, variables)

    def testNoDataSource(self):
        """Case where the text field only uses its internal buffer, no
        external property data source.
        """
        self.getField().setPropertyDataSource(None)
        self.expectValueChangeFromSetValueNotCommit()
        return

    def testValueChangeEventPropagationWithReadThrough(self):
        """Test that field propagates value change events originating from
        property, but don't fire value change events twice if value has only
        changed once.

        TODO: make test field type agnostic (eg. combobox)
        """
        prop = ObjectProperty('')
        self.getField().setPropertyDataSource(prop)
        self.getField().setWriteThrough(True)
        self.getField().setReadThrough(True)
        self.getListener().valueChange(mox.IsA(ValueChangeEvent))
        mox.Replay(self.getListener())
        self.getField().addListener(self.getListener(), IValueChangeListener)
        prop.setValue('Foo')
        mox.Verify(self.getListener())
        value = self.getField().getValue()
        self.assertEquals('Foo', value)
        mox.Verify(self.getListener())

    def testValueChangePropagationWithReadThroughWithModifiedValue(self):
        """If read through is on and value has been modified, but not
        committed, the value should not propagate similar to
        L{#testValueChangeEventPropagationWithReadThrough()}

        TODO: make test field type agnostic (eg. combobox)
        """
        initialValue = 'initial'
        prop = ObjectProperty(initialValue)
        self.getField().setPropertyDataSource(prop)
        self.getField().setWriteThrough(False)
        self.getField().setReadThrough(True)
        mox.Replay(self.getListener())
        self.setValue(self.getField())
        self.assertTrue(self.getField().isModified())
        self.getField().addListener(self.getListener(), IValueChangeListener)
        prop.setValue('Foo')
        mox.Verify(self.getListener())
        value = self.getField().getValue()
        mox.Verify(self.getListener())
        isValueEqualToInitial = value == initialValue
        self.assertFalse(isValueEqualToInitial)
        isValueEqualToPropertyValue = value == prop.getValue()
        self.assertFalse(isValueEqualToPropertyValue)
        mox.Verify(self.getListener())

    def testValueChangePropagationWithReadThroughOff(self):
        """Value change events from property should not propagate if read
        through is false. Execpt when the property is being set.

        TODO: make test field type agnostic (eg. combobox)
        """
        initialValue = 'initial'
        prop = ObjectProperty(initialValue)
        self.getField().setWriteThrough(False)
        self.getField().setReadThrough(False)
        self.getListener().valueChange(mox.IsA(ValueChangeEvent))
        mox.Replay(self.getListener())
        self.getField().addListener(self.getListener(), IValueChangeListener)
        self.getField().setPropertyDataSource(prop)
        mox.Verify(self.getListener())
        prop.setValue('Foo')
        mox.Verify(self.getListener())
        value = self.getField().getValue()
        isValueEqualToInitial = value == initialValue
        self.assertTrue(isValueEqualToInitial)
        mox.Verify(self.getListener())


if __name__ == '__main__':
    unittest.main()