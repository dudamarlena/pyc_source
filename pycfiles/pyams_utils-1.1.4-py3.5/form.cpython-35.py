# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_utils/interfaces/form.py
# Compiled at: 2020-02-18 19:11:13
# Size of source mod 2**32: 1798 bytes
"""PyAMS_utils.interfaces.form module

This module contains a few special values which are used into forms.
"""
from zope.interface import Interface
__docformat__ = 'restructuredtext'

class NOT_CHANGED:
    __doc__ = 'Marker value for unchanged properties'

    def __repr__(self):
        return '<NOT_CHANGED>'


NOT_CHANGED = NOT_CHANGED()

class NO_VALUE:
    __doc__ = 'Marker value for properties without value'

    def __repr__(self):
        return '<NO_VALUE>'


NO_VALUE = NO_VALUE()

class TO_BE_DELETED:
    __doc__ = 'Marker value for properties to be deleted'

    def __repr__(self):
        return '<TO_BE_DELETED>'


TO_BE_DELETED = TO_BE_DELETED()

class IDataManager(Interface):
    __doc__ = 'Data manager interface'

    def get(self):
        """Get the value.

        If no value can be found, raise an error
        """
        pass

    def query(self, default=NO_VALUE):
        """Get the value.

        If no value can be found, return the default value.
        If access is forbidden, raise an error.
        """
        pass

    def set(self, value):
        """Set the value"""
        pass

    def can_access(self):
        """Can the value be accessed."""
        pass

    def can_write(self):
        """Can the data manager write a value."""
        pass