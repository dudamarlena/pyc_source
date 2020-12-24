# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/abstract_text_field.py
# Compiled at: 2013-04-04 15:36:35
from warnings import warn
from muntjac.ui.abstract_field import AbstractField
from muntjac.terminal.gwt.client.ui.v_text_field import VTextField
from muntjac.event.field_events import BlurEvent, IBlurListener, IBlurNotifier, FocusEvent, IFocusListener, IFocusNotifier, TextChangeEvent, ITextChangeListener, ITextChangeNotifier, EVENT_METHOD

class AbstractTextField(AbstractField, IBlurNotifier, IFocusNotifier, ITextChangeNotifier):

    def __init__(self):
        super(AbstractTextField, self).__init__()
        self._format = None
        self._nullRepresentation = 'null'
        self._nullSettingAllowed = False
        self._maxLength = -1
        self._columns = 0
        self._inputPrompt = None
        self._lastKnownTextContent = None
        self._lastKnownCursorPosition = None
        self._textChangeEventPending = None
        self._textChangeEventMode = TextChangeEventMode.LAZY
        self._DEFAULT_TEXTCHANGE_TIMEOUT = 400
        self._textChangeEventTimeout = self._DEFAULT_TEXTCHANGE_TIMEOUT
        self._selectionPosition = -1
        self._selectionLength = None
        self._changingVariables = None
        return

    def paintContent(self, target):
        super(AbstractTextField, self).paintContent(target)
        if self.getMaxLength() >= 0:
            target.addAttribute('maxLength', self.getMaxLength())
        columns = self.getColumns()
        if columns != 0:
            target.addAttribute('cols', str(columns))
        if self.getInputPrompt() is not None:
            target.addAttribute('prompt', self.getInputPrompt())
        value = self.getFormattedValue()
        if value is None:
            value = self.getNullRepresentation()
        if value is None:
            raise ValueError('Null values are not allowed if the null-representation is null')
        target.addVariable(self, 'text', value)
        if self._selectionPosition != -1:
            target.addAttribute('selpos', self._selectionPosition)
            target.addAttribute('sellen', self._selectionLength)
            self._selectionPosition = -1
        if self.hasListeners(TextChangeEvent):
            target.addAttribute(VTextField.ATTR_TEXTCHANGE_EVENTMODE, str(self.getTextChangeEventMode()))
            target.addAttribute(VTextField.ATTR_TEXTCHANGE_TIMEOUT, self.getTextChangeTimeout())
            if self._lastKnownTextContent is not None:
                target.addAttribute(VTextField.ATTR_NO_VALUE_CHANGE_BETWEEN_PAINTS, True)
        return

    def getFormattedValue(self):
        """Gets the formatted string value. Sets the field value by using
        the assigned format.

        @return: the Formatted value.
        @see: L{setFormat}
        @deprecated:
        """
        warn('deprecated', DeprecationWarning)
        v = self.getValue()
        if v is None:
            return
        else:
            return str(v)

    def getValue(self):
        v = super(AbstractTextField, self).getValue()
        if self._format is None or v is None:
            return v
        try:
            warn('deprecated', DeprecationWarning)
            return self._format.format(v)
        except ValueError:
            return v

        return

    def changeVariables(self, source, variables):
        self._changingVariables = True
        try:
            super(AbstractTextField, self).changeVariables(source, variables)
            if VTextField.VAR_CURSOR in variables:
                obj = variables.get(VTextField.VAR_CURSOR)
                self._lastKnownCursorPosition = int(obj)
            if VTextField.VAR_CUR_TEXT in variables:
                self.handleInputEventTextChange(variables)
            if 'text' in variables and not self.isReadOnly():
                newValue = variables.get('text')
                if self.getMaxLength() != -1 and len(newValue) > self.getMaxLength():
                    newValue = newValue[:self.getMaxLength()]
                oldValue = self.getFormattedValue()
                if newValue is not None and (oldValue is None or self.isNullSettingAllowed()) and newValue == self.getNullRepresentation():
                    newValue = None
                if newValue != oldValue and (newValue is None or newValue != oldValue):
                    wasModified = self.isModified()
                    self.setValue(newValue, True)
                    if self._format is not None or wasModified != self.isModified():
                        self.requestRepaint()
            self.firePendingTextChangeEvent()
            if FocusEvent.EVENT_ID in variables:
                self.fireEvent(FocusEvent(self))
            if BlurEvent.EVENT_ID in variables:
                self.fireEvent(BlurEvent(self))
        finally:
            self._changingVariables = False

        return

    def getType(self):
        return str

    def getNullRepresentation(self):
        """Gets the null-string representation.

        The null-valued strings are represented on the user interface by
        replacing the null value with this string. If the null representation
        is set null (not 'null' string), painting null value throws exception.

        The default value is string 'null'.

        @return: the textual string representation for null strings.
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
        self.requestRepaint()

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
                   Should the null-string representation always be converted
                   to null-values.
        @see: L{TextField.getNullRepresentation}
        """
        self._nullSettingAllowed = nullSettingAllowed
        self.requestRepaint()

    def getFormat(self):
        """Gets the value formatter of TextField.

        @return: the format used to format the value.
        @deprecated: replaced by L{PropertyFormatter}
        """
        warn('replaced by PropertyFormatter', DeprecationWarning)
        return self._format

    def setFormat(self, fmt):
        """Gets the value formatter of TextField.

        @param fmt:
                   the Format used to format the value. Null disables the
                   formatting.
        @deprecated: replaced by L{PropertyFormatter}
        """
        warn('replaced by PropertyFormatter', DeprecationWarning)
        self._format = fmt
        self.requestRepaint()

    def isEmpty(self):
        return super(AbstractTextField, self).isEmpty() or len(str(self)) == 0

    def getMaxLength(self):
        """Returns the maximum number of characters in the field. Value -1 is
        considered unlimited. Terminal may however have some technical limits.

        @return: the maxLength
        """
        return self._maxLength

    def setMaxLength(self, maxLength):
        """Sets the maximum number of characters in the field. Value -1 is
        considered unlimited. Terminal may however have some technical limits.

        @param maxLength:
                   the maxLength to set
        """
        self._maxLength = maxLength
        self.requestRepaint()

    def getColumns(self):
        """Gets the number of columns in the editor. If the number of columns
        is set 0, the actual number of displayed columns is determined
        implicitly by the adapter.

        @return: the number of columns in the editor.
        """
        return self._columns

    def setColumns(self, columns):
        """Sets the number of columns in the editor. If the number of columns
        is set 0, the actual number of displayed columns is determined
        implicitly by the adapter.

        @param columns:
                   the number of columns to set.
        """
        if columns < 0:
            columns = 0
        self._columns = columns
        self.requestRepaint()

    def getInputPrompt(self):
        """Gets the current input prompt.

        @see: L{setInputPrompt}
        @return: the current input prompt, or null if not enabled
        """
        return self._inputPrompt

    def setInputPrompt(self, inputPrompt):
        """Sets the input prompt - a textual prompt that is displayed when
        the field would otherwise be empty, to prompt the user for input.
        """
        self._inputPrompt = inputPrompt
        self.requestRepaint()

    def firePendingTextChangeEvent(self):
        if self._textChangeEventPending:
            self._textChangeEventPending = False
            self.fireEvent(TextChangeEventImpl(self))

    def setInternalValue(self, newValue):
        if self._changingVariables and not self._textChangeEventPending:
            if newValue is None and self._lastKnownTextContent is not None and self._lastKnownTextContent != self.getNullRepresentation():
                self._lastKnownTextContent = self.getNullRepresentation()
                self._textChangeEventPending = True
            elif newValue is not None and str(newValue) != self._lastKnownTextContent:
                self._lastKnownTextContent = str(newValue)
                self._textChangeEventPending = True
            self.firePendingTextChangeEvent()
        self._lastKnownTextContent = None
        super(AbstractTextField, self).setInternalValue(newValue)
        return

    def setValue(self, newValue, repaintIsNotNeeded=None):
        if repaintIsNotNeeded is not None:
            super(AbstractTextField, self).setValue(newValue, repaintIsNotNeeded)
        else:
            super(AbstractTextField, self).setValue(newValue)
            if self._lastKnownTextContent is not None:
                self._lastKnownTextContent = None
                self.requestRepaint()
        return

    def handleInputEventTextChange(self, variables):
        obj = variables.get(VTextField.VAR_CUR_TEXT)
        self._lastKnownTextContent = obj
        self._textChangeEventPending = True

    def setTextChangeEventMode(self, inputEventMode):
        """Sets the mode how the TextField triggers L{TextChangeEvent}s.

        @param inputEventMode: the new mode

        @see: L{TextChangeEventMode}
        """
        self._textChangeEventMode = inputEventMode
        self.requestRepaint()

    def getTextChangeEventMode(self):
        """@return: the mode used to trigger L{TextChangeEvent}s."""
        return self._textChangeEventMode

    def addListener(self, listener, iface=None):
        if isinstance(listener, IBlurListener) and (iface is None or issubclass(iface, IBlurListener)):
            self.registerListener(BlurEvent.EVENT_ID, BlurEvent, listener, IBlurListener.blurMethod)
        if isinstance(listener, IFocusListener) and (iface is None or issubclass(iface, IFocusListener)):
            self.registerListener(FocusEvent.EVENT_ID, FocusEvent, listener, IFocusListener.focusMethod)
        if isinstance(listener, ITextChangeListener) and (iface is None or issubclass(iface, ITextChangeListener)):
            self.registerListener(ITextChangeListener.EVENT_ID, TextChangeEvent, listener, EVENT_METHOD)
        super(AbstractTextField, self).addListener(listener, iface)
        return

    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, BlurEvent):
            self.registerCallback(BlurEvent, callback, BlurEvent.EVENT_ID, *args)
        elif issubclass(eventType, FocusEvent):
            self.registerCallback(FocusEvent, callback, FocusEvent.EVENT_ID, *args)
        elif issubclass(eventType, TextChangeEvent):
            self.registerCallback(TextChangeEvent, callback, ITextChangeListener.EVENT_ID, *args)
        else:
            super(AbstractTextField, self).addCallback(callback, eventType, *args)
        return

    def removeListener(self, listener, iface=None):
        if isinstance(listener, IBlurListener) and (iface is None or issubclass(iface, IBlurListener)):
            self.withdrawListener(BlurEvent.EVENT_ID, BlurEvent, listener)
        if isinstance(listener, IFocusListener) and (iface is None or issubclass(iface, IFocusListener)):
            self.withdrawListener(FocusEvent.EVENT_ID, FocusEvent, listener)
        if isinstance(listener, ITextChangeListener) and (iface is None or issubclass(iface, ITextChangeListener)):
            self.withdrawListener(ITextChangeListener.EVENT_ID, TextChangeEvent, listener)
        super(AbstractTextField, self).addListener(listener, iface)
        return

    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, BlurEvent):
            self.withdrawCallback(BlurEvent, callback, BlurEvent.EVENT_ID)
        elif issubclass(eventType, FocusEvent):
            self.withdrawCallback(FocusEvent, callback, FocusEvent.EVENT_ID)
        elif issubclass(eventType, TextChangeEvent):
            self.withdrawCallback(TextChangeEvent, callback, ITextChangeListener.EVENT_ID)
        else:
            super(AbstractTextField, self).removeCallback(callback, eventType)
        return

    def setTextChangeTimeout(self, timeout):
        """The text change timeout modifies how often text change events
        are communicated to the application when
        L{getTextChangeEventMode} is L{TextChangeEventMode.LAZY}
        or L{TextChangeEventMode.TIMEOUT}.

        @see: L{getTextChangeEventMode}

        @param timeout: the timeout in milliseconds
        """
        self._textChangeEventTimeout = timeout
        self.requestRepaint()

    def getTextChangeTimeout(self):
        """Gets the timeout used to fire L{TextChangeEvent}s when the
        L{getTextChangeEventMode} is L{TextChangeEventMode.LAZY}
        or L{TextChangeEventMode.TIMEOUT}.

        @return: the timeout value in milliseconds
        """
        return self._textChangeEventTimeout

    def getCurrentTextContent(self):
        """Gets the current (or the last known) text content in the field.

        Note the text returned by this method is not necessary the same that
        is returned by the L{getValue} method. The value is updated
        when the terminal fires a value change event via e.g. blurring the
        field or by pressing enter. The value returned by this method is
        updated also on L{TextChangeEvent}s. Due to this high dependency
        to the terminal implementation this method is (at least at this
        point) not published.

        @return: the text which is currently displayed in the field.
        """
        if self._lastKnownTextContent is not None:
            return self._lastKnownTextContent
        else:
            text = self.getValue()
            if text is None:
                return self.getNullRepresentation()
            return str(text)
            return

    def selectAll(self):
        """Selects all text in the field.
        """
        text = '' if self.getValue() is None else str(self.getValue())
        self.setSelectionRange(0, len(text))
        return

    def setSelectionRange(self, pos, length):
        """Sets the range of text to be selected.

        As a side effect the field will become focused.

        @param pos:
                   the position of the first character to be selected
        @param length:
                   the number of characters to be selected
        """
        self._selectionPosition = pos
        self._selectionLength = length
        self.focus()
        self.requestRepaint()

    def setCursorPosition(self, pos):
        """Sets the cursor position in the field. As a side effect the
        field will become focused.

        @param pos:
                   the position for the cursor
        """
        self.setSelectionRange(pos, 0)
        self._lastKnownCursorPosition = pos

    def getCursorPosition(self):
        """Returns the last known cursor position of the field.

        Note that due to the client server nature or the GWT terminal, Muntjac
        cannot provide the exact value of the cursor position in most
        situations. The value is updated only when the client side terminal
        communicates to TextField, like on L{ValueChangeEvent}s and
        L{TextChangeEvent}s. This may change later if a deep push
        integration is built to Muntjac.

        @return: the cursor position
        """
        return self._lastKnownCursorPosition


class TextChangeEventMode(object):
    """Different modes how the TextField can trigger L{TextChangeEvent}s.
    """
    EAGER = 'EAGER'
    TIMEOUT = 'TIMEOUT'
    LAZY = 'LAZY'
    _values = [
     EAGER, TIMEOUT, LAZY]

    @classmethod
    def values(cls):
        return cls._values[:]


class TextChangeEventImpl(TextChangeEvent):

    def __init__(self, tf):
        super(TextChangeEventImpl, self).__init__(tf)
        self._curText = tf.getCurrentTextContent()
        self._cursorPosition = tf.getCursorPosition()

    def getComponent(self):
        return super(TextChangeEventImpl, self).getComponent()

    def getText(self):
        return self._curText

    def getCursorPosition(self):
        return self._cursorPosition