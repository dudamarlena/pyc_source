# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/password_field.py
# Compiled at: 2013-04-04 15:36:35
"""Defines a field that is used to enter secret text information like
passwords."""
from muntjac.ui.abstract_text_field import AbstractTextField
from muntjac.data.property import IProperty

class PasswordField(AbstractTextField):
    """A field that is used to enter secret text information like passwords.
    The entered text is not displayed on the screen.
    """
    CLIENT_WIDGET = None

    def __init__(self, *args):
        """Constructs a PasswordField with caption and/or value/data source.

        @param args: tuple of the form
            - ()
            - (caption)
              1. the caption for the field
            - (dataSource)
              1. the property data source for the field
            - (caption, dataSource)
              1. the caption for the field
              2. the property data source for the field
            - (caption, value)
              1. the caption for the field
              2. the value for the field
        """
        super(PasswordField, self).__init__()
        nargs = len(args)
        if nargs == 0:
            self.setValue('')
        elif nargs == 1:
            if isinstance(args[0], IProperty):
                dataSource, = args
                self.setPropertyDataSource(dataSource)
            else:
                caption, = args
                PasswordField.__init__(self)
                self.setCaption(caption)
        elif nargs == 2:
            if isinstance(args[1], IProperty):
                caption, dataSource = args
                PasswordField.__init__(self, dataSource)
                self.setCaption(caption)
            else:
                caption, value = args
                self.setValue(value)
                self.setCaption(caption)
        else:
            raise ValueError, 'too many arguments'