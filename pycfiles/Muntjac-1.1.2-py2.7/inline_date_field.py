# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/inline_date_field.py
# Compiled at: 2013-04-04 15:36:35
"""Defines a date entry component, which displays the actual date selector
inline."""
from datetime import datetime
from muntjac.ui.date_field import DateField
from muntjac.data.property import IProperty

class InlineDateField(DateField):
    """A date entry component, which displays the actual date selector inline.

    @see: L{DateField}
    @see: L{PopupDateField}
    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """
    CLIENT_WIDGET = None

    def __init__(self, *args):
        nargs = len(args)
        if nargs == 0:
            super(InlineDateField, self).__init__()
        elif nargs == 1:
            if isinstance(args[0], IProperty):
                dataSource, = args
                super(InlineDateField, self).__init__(dataSource)
            else:
                caption, = args
                super(InlineDateField, self).__init__(caption)
        elif nargs == 2:
            if isinstance(args[1], datetime):
                caption, value = args
                super(InlineDateField, self).__init__(caption, value)
            else:
                caption, dataSource = args
                super(InlineDateField, self).__init__(caption, dataSource)
        else:
            raise ValueError, 'too many arguments'