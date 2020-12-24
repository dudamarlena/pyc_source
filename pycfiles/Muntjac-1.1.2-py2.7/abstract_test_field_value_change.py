# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/test/server/components/abstract_test_field_value_change.py
# Compiled at: 2013-04-04 15:36:37
import mox
from unittest import TestCase
from muntjac.data.property import IValueChangeListener, ValueChangeEvent
from muntjac.data.util.object_property import ObjectProperty

class AbstractTestFieldValueChange(TestCase):
    """Base class for tests for checking that value change listeners for
    fields are not called exactly once when they should be, and not at
    other times.

    Does not check all cases (e.g. properties that do not implement
    L{ValueChangeNotifier}).

    Subclasses should implement L{#setValue()} and call super C{setValue}.
    Also, subclasses should typically override L{setValue} to set the field
    value via C{changeVariables()}.
    """

    def setUp(self, field):
        TestCase.setUp(self)
        self._field = field
        self.mox = mox.Mox()
        self._listener = self.mox.CreateMock(IValueChangeListener)

    def getListener(self):
        return self._listener

    def testRemoveListener(self):
        """Test that listeners are not called when they have been
        unregistered."""
        self.getField().setPropertyDataSource(ObjectProperty(''))
        self.getField().setWriteThrough(True)
        self.getField().setReadThrough(True)
        self._listener.valueChange(mox.IsA(ValueChangeEvent))
        mox.Replay(self._listener)
        self.getField().addListener(self._listener, IValueChangeListener)
        self.setValue(self.getField())
        mox.Verify(self._listener)
        self.getField().removeListener(self._listener, IValueChangeListener)
        self.setValue(self.getField())
        mox.Verify(self._listener)

    def testWriteThroughReadThrough(self):
        """Common unbuffered case: both writeThrough (auto-commit) and
        readThrough are on. Calling commit() should not cause notifications.

        Using the readThrough mode allows changes made to the property value
        to be seen in some cases also when there is no notification of value
        change from the property.

        Field value change notifications closely mirror value changes of the
        data source behind the field.
        """
        self.getField().setPropertyDataSource(ObjectProperty(''))
        self.getField().setWriteThrough(True)
        self.getField().setReadThrough(True)
        self.expectValueChangeFromSetValueNotCommit()

    def testNoWriteThroughNoReadThrough(self):
        """Fully buffered use where the data source is neither read nor
        modified during editing, and is updated at commit().

        Field value change notifications reflect the buffered value in the
        field, not the original data source value changes.
        """
        self.getField().setPropertyDataSource(ObjectProperty(''))
        self.getField().setWriteThrough(False)
        self.getField().setReadThrough(False)
        self.expectValueChangeFromSetValueNotCommit()

    def testWriteThroughNoReadThrough(self):
        """Less common partly buffered case: writeThrough (auto-commit) is
        on and readThrough is off. Calling commit() should not cause
        notifications.

        Without readThrough activated, changes to the data source that do
        not cause notifications are not reflected by the field value.

        Field value change notifications correspond to changes made to the
        data source value through the text field or the (notifying) property.
        """
        self.getField().setPropertyDataSource(ObjectProperty(''))
        self.getField().setWriteThrough(True)
        self.getField().setReadThrough(False)
        self.expectValueChangeFromSetValueNotCommit()

    def testNoWriteThroughReadThrough(self):
        """Partly buffered use where the data source is read but not nor
        modified during editing, and is updated at commit().

        When used like this, a field is updated from the data source if
        necessary when its value is requested and the property value has
        changed but the field has not been modified in its buffer.

        Field value change notifications reflect the buffered value in the
        field, not the original data source value changes.
        """
        self.getField().setPropertyDataSource(ObjectProperty(''))
        self.getField().setWriteThrough(False)
        self.getField().setReadThrough(True)
        self.expectValueChangeFromSetValueNotCommit()

    def expectValueChangeFromSetValueNotCommit(self):
        self._listener.valueChange(mox.IsA(ValueChangeEvent))
        mox.Replay(self._listener)
        self.getField().addListener(self._listener, IValueChangeListener)
        self.setValue(self.getField())
        mox.Verify(self._listener)
        self.getField().commit()
        mox.Verify(self._listener)

    def getField(self):
        return self._field

    def setValue(self, field):
        """Override in subclasses to set value with changeVariables()."""
        field.setValue('newValue')