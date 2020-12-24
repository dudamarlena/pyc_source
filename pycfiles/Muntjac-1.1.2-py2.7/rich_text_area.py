# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/rich_text_area.py
# Compiled at: 2013-04-04 15:36:35
"""Defines a simple C{RichTextArea} to edit HTML format text."""
from warnings import warn
from muntjac.ui.abstract_field import AbstractField
from muntjac.data.property import IProperty

class RichTextArea(AbstractField):
    """A simple RichTextArea to edit HTML format text.

    Note, that using L{TextField.setMaxLength} method in
    L{RichTextArea} may produce unexpected results as formatting
    is counted into length of field.
    """
    CLIENT_WIDGET = None

    def __init__(self, *args):
        """Constructs an empty C{RichTextArea} with optional caption, value
        and/or data source.

        @param args: tuple of the form
            - ()
            - (caption)
              1. the caption for the editor.
            - (dataSource)
              1. the data source for the editor value
            - (caption, dataSource)
              1. the caption for the editor.
              2. the data source for the editor value
            - (caption, value)
              1. the caption for the editor.
              2. the initial text content of the editor.
        """
        super(RichTextArea, self).__init__()
        self._format = None
        self._nullRepresentation = 'null'
        self._nullSettingAllowed = False
        self._selectAll = False
        nargs = len(args)
        if nargs == 0:
            self.setValue('')
        elif nargs == 1:
            if isinstance(args[0], IProperty):
                dataSource, = args
                self.setPropertyDataSource(dataSource)
            else:
                caption, = args
                RichTextArea.__init__(self)
                self.setCaption(caption)
        elif nargs == 2:
            if isinstance(args[1], IProperty):
                caption, dataSource = args
                RichTextArea.__init__(self, dataSource)
                self.setCaption(caption)
            else:
                caption, value = args
                self.setValue(value)
                self.setCaption(caption)
        else:
            raise ValueError, 'too many arguments'
        return

    def paintContent(self, target):
        if self._selectAll:
            target.addAttribute('selectAll', True)
            self._selectAll = False
        value = self.getFormattedValue()
        if value is None:
            value = self.getNullRepresentation()
        if value is None:
            raise ValueError, 'Null values are not allowed if the null-representation is null'
        target.addVariable(self, 'text', value)
        super(RichTextArea, self).paintContent(target)
        return

    def setReadOnly(self, readOnly):
        super(RichTextArea, self).setReadOnly(readOnly)
        if readOnly:
            self.addStyleName('v-richtextarea-readonly')
        else:
            self.removeStyleName('v-richtextarea-readonly')

    def selectAll(self):
        """Selects all text in the rich text area. As a side effect,
        focuses the rich text area.
        """
        self._selectAll = True
        self.focus()
        self.requestRepaint()

    def getFormattedValue(self):
        """Gets the formatted string value. Sets the field value by using
        the assigned Format.

        @return: the Formatted value.
        @see: L{setFormat}
        @deprecated:
        """
        v = self.getValue()
        if v is None:
            return
        else:
            return str(v)

    def getValue(self):
        v = super(RichTextArea, self).getValue()
        if self._format is None or v is None:
            return v
        try:
            warn('deprecated', DeprecationWarning)
            return self._format.format(v)
        except ValueError:
            return v

        return

    def changeVariables(self, source, variables):
        super(RichTextArea, self).changeVariables(source, variables)
        if 'text' in variables and not self.isReadOnly():
            newValue = variables.get('text')
            oldValue = self.getFormattedValue()
            if newValue is not None and (oldValue is None or self.isNullSettingAllowed()) and newValue == self.getNullRepresentation():
                newValue = None
            if newValue != oldValue and (newValue is None or newValue != oldValue):
                wasModified = self.isModified()
                self.setValue(newValue, True)
                if self._format is not None or wasModified != self.isModified():
                    self.requestRepaint()
        return

    def getType(self):
        return str

    def getNullRepresentation(self):
        """Gets the null-string representation.

        The null-valued strings are represented on the user interface by
        replacing the null value with this string. If the null representation
        is set null (not 'null' string), painting null value throws exception.

        The default value is string 'null'.

        @return: the string textual representation for null strings.
        @see: L{TextField.isNullSettingAllowed}
        """
        return self._nullRepresentation

    def isNullSettingAllowed(self):
        """Is setting nulls with null-string representation allowed.

        If this property is true, writing null-representation string to text
        field always sets the field value to real null. If this property is
        false, null setting is not made, but the null values are maintained.
        Maintenance of null-values is made by only converting the textfield
        contents to real null, if the text field matches the null-string
        representation and the current value of the field is null.

        By default this setting is false

        @return: Should the null-string represenation be always
                 converted to null-values.
        @see: L{TextField.getNullRepresentation}
        """
        return self._nullSettingAllowed

    def setNullRepresentation(self, nullRepresentation):
        """Sets the null-string representation.

        The null-valued strings are represented on the user interface by
        replacing the null value with this string. If the null representation
        is set null (not 'null' string), painting null value throws exception.

        The default value is string 'null'

        @param nullRepresentation:
                   Textual representation for null strings.
        @see: L{TextField.setNullSettingAllowed}
        """
        self._nullRepresentation = nullRepresentation

    def setNullSettingAllowed(self, nullSettingAllowed):
        """Sets the null conversion mode.

        If this property is true, writing null-representation string to text
        field always sets the field value to real null. If this property is
        false, null setting is not made, but the null values are maintained.
        Maintenance of null-values is made by only converting the textfield
        contents to real null, if the text field matches the null-string
        representation and the current value of the field is null.

        By default this setting is false.

        @param nullSettingAllowed:
                   Should the null-string representation be always converted
                   to null-values.
        @see: L{TextField.getNullRepresentation}
        """
        self._nullSettingAllowed = nullSettingAllowed

    def getFormat(self):
        """Gets the value formatter of TextField.

        @return: the format used to format the value.
        @deprecated: replaced by L{PropertyFormatter}
        """
        warn('replaced by PropertyFormatter', DeprecationWarning)
        return self._format

    def setFormat(self, frmt):
        """Gets the value formatter of TextField.

        @param frmt:
                   the format used to format the value. Null disables the
                   formatting.
        @deprecated: replaced by L{PropertyFormatter}
        """
        warn('replaced by PropertyFormatter', DeprecationWarning)
        self._format = frmt
        self.requestRepaint()

    def isEmpty(self):
        return super(RichTextArea, self).isEmpty() or len(str(self)) == 0