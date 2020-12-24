# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/data/util/object_property.py
# Compiled at: 2013-04-04 15:36:37
"""A simple data object containing one typed value."""
from muntjac.data.util.abstract_property import AbstractProperty
from muntjac.data.property import ReadOnlyException, ConversionException

class ObjectProperty(AbstractProperty):
    """A simple data object containing one typed value. This class is a
    straightforward implementation of the the L{IProperty} interface.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, value, typ=None, readOnly=None):
        """Creates a new instance of ObjectProperty with the given value,
        type and read-only mode status.

        Any value of type Object is accepted, see L{ObjectProperty}.

        @param value:
                   the Initial value of the property.
        @param typ:
                   the type of the value. C{value} must be assignable
                   to this type.
        @param readOnly:
                   Sets the read-only mode.
        """
        super(ObjectProperty, self).__init__()
        self._value = None
        self._type = None
        if typ is None and readOnly is None:
            ObjectProperty.__init__(self, value, value.__class__)
        elif readOnly is None:
            self._type = typ
            self.setValue(value)
        else:
            ObjectProperty.__init__(self, value, typ)
            self.setReadOnly(readOnly)
        return

    def getType(self):
        """Returns the type of the ObjectProperty. The methods C{getValue}
        and C{setValue} must be compatible with this type: one must be
        able to safely cast the value returned from C{getValue} to the
        given type and pass any variable assignable to this type as an
        argument to C{setValue}.

        @return: type of the Property
        """
        return self._type

    def getValue(self):
        """Gets the value stored in the Property.

        @return: the value stored in the Property
        """
        return self._value

    def setValue(self, newValue):
        """Sets the value of the property. This method supports setting from
        C{str} if either C{str} is directly assignable to property type, or
        the type class contains a string constructor.

        @param newValue:
                   the New value of the property.
        @raise ReadOnlyException:
                   if the object is in read-only mode
        @raise ConversionException:
                   if the newValue can't be converted into the Property's
                   native type directly or through C{str}
        """
        if self.isReadOnly():
            raise ReadOnlyException()
        if newValue is None or issubclass(newValue.__class__, self._type):
            self._value = newValue
        else:
            try:
                constr = self.getType()
                self._value = constr(str(newValue))
            except Exception as e:
                raise ConversionException(e)

        self.fireValueChange()
        return