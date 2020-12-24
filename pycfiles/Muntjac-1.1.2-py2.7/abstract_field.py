# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/abstract_field.py
# Compiled at: 2013-04-04 15:36:36
"""For implementing buffered property editors."""
from warnings import warn
from muntjac.event.shortcut_listener import ShortcutListener
from muntjac.event.action_manager import ActionManager
from muntjac.ui.abstract_component import AbstractComponent
from muntjac.ui.component import Event as ComponentEvent
from muntjac.event import action
from muntjac.ui import field
from muntjac.data import property as prop
from muntjac.data.validator import EmptyValueException
from muntjac.data.buffered import SourceException
from muntjac.data.validator import InvalidValueException
from muntjac.data.validatable import IValidatable
from muntjac.terminal.composite_error_message import CompositeErrorMessage
_VALUE_CHANGE_METHOD = getattr(prop.IValueChangeListener, 'valueChange')
_READ_ONLY_STATUS_CHANGE_METHOD = getattr(prop.IReadOnlyStatusChangeListener, 'readOnlyStatusChange')

class AbstractField(AbstractComponent, field.IField, action.IShortcutNotifier, prop.IReadOnlyStatusChangeNotifier, prop.IReadOnlyStatusChangeListener):
    """Abstract field component for implementing buffered property editors.
    The field may hold an internal value, or it may be connected to any data
    source that implements the L{IProperty}interface. C{AbstractField}
    implements that interface itself, too, so accessing the IProperty value
    represented by it is straightforward.

    AbstractField also provides the L{IBuffered} interface for buffering the
    data source value. By default the IField is in write through-mode and
    L{setWriteThrough}should be called to enable buffering.

    The class also supports L{validators<IValidator>} to
    make sure the value contained in the field is valid.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self):
        super(AbstractField, self).__init__()
        self._value = None
        self._dataSource = None
        self._validators = None
        self._writeThroughMode = True
        self._readThroughMode = True
        self._modified = False
        self._committingValueToDataSource = False
        self._currentBufferedSourceException = None
        self._invalidAllowed = True
        self._invalidCommitted = False
        self._tabIndex = 0
        self._required = False
        self._requiredError = ''
        self._validationVisible = True
        self._actionManager = None
        self._valueWasModifiedByDataSourceDuringCommit = False
        return

    def paintContent(self, target):
        if self.getTabIndex() != 0:
            target.addAttribute('tabindex', self.getTabIndex())
        if self.isModified():
            target.addAttribute('modified', True)
        if not self.isReadOnly() and self.isRequired():
            target.addAttribute('required', True)
        if self.shouldHideErrors():
            target.addAttribute('hideErrors', True)

    def shouldHideErrors(self):
        """Returns true if the error indicator be hidden when painting the
        component even when there are errors.

        This is a mostly internal method, but can be overridden in subclasses
        e.g. if the error indicator should also be shown for empty fields in
        some cases.

        @return: true to hide the error indicator, false to use the normal
                 logic to show it when there are errors
        """
        return self.isRequired() and self.isEmpty() and self.getComponentError() == None and self.getErrorMessage() != None

    def getType(self):
        raise NotImplementedError

    def isReadOnly(self):
        """The abstract field is read only also if the data source is in
        read only mode.
        """
        return super(AbstractField, self).isReadOnly() or self._dataSource is not None and self._dataSource.isReadOnly()

    def setReadOnly(self, readOnly):
        """Changes the readonly state and throw read-only status change
        events.

        @see: L{IComponent.setReadOnly}
        """
        super(AbstractField, self).setReadOnly(readOnly)
        self.fireReadOnlyStatusChange()

    def isInvalidCommitted(self):
        """Tests if the invalid data is committed to datasource.

        @see: L{BufferedValidatable.isInvalidCommitted}
        """
        return self._invalidCommitted

    def setInvalidCommitted(self, isCommitted):
        """Sets if the invalid data should be committed to datasource.

        @see: L{BufferedValidatable.setInvalidCommitted}
        """
        self._invalidCommitted = isCommitted

    def commit(self):
        if self._dataSource is not None and not self._dataSource.isReadOnly():
            if self.isInvalidCommitted() or self.isValid():
                newValue = self.getValue()
                self._valueWasModifiedByDataSourceDuringCommit = False
                self._committingValueToDataSource = True
                self._dataSource.setValue(newValue)
                self._committingValueToDataSource = False
            else:
                self.validate()
        repaintNeeded = False
        if self._modified:
            self._modified = False
            repaintNeeded = True
        if self._currentBufferedSourceException is not None:
            self._currentBufferedSourceException = None
            repaintNeeded = True
        if self._valueWasModifiedByDataSourceDuringCommit:
            self._valueWasModifiedByDataSourceDuringCommit = False
            self.fireValueChange(False)
        elif repaintNeeded:
            self.requestRepaint()
        return

    def discard(self):
        if self._dataSource is not None:
            newValue = None
            try:
                if self.getType() == str:
                    newValue = str(self._dataSource)
                else:
                    newValue = self._dataSource.getValue()
                if self._currentBufferedSourceException is not None:
                    self._currentBufferedSourceException = None
                    self.requestRepaint()
            except Exception as e:
                exception = SourceException(self, e)
                self._currentBufferedSourceException = exception
                self.requestRepaint()
                raise self._currentBufferedSourceException

            wasModified = self.isModified()
            self._modified = False
            if newValue is None and self._value is not None or newValue is not None and newValue != self._value:
                self.setInternalValue(newValue)
                self.fireValueChange(False)
            elif wasModified:
                self.requestRepaint()
        return

    def isModified(self):
        return self._modified

    def isWriteThrough(self):
        return self._writeThroughMode

    def setWriteThrough(self, writeThrough):
        if self._writeThroughMode == writeThrough:
            return
        self._writeThroughMode = writeThrough
        if self._writeThroughMode:
            self.commit()

    def isReadThrough(self):
        return self._readThroughMode

    def setReadThrough(self, readThrough):
        if self._readThroughMode == readThrough:
            return
        else:
            self._readThroughMode = readThrough
            if not self.isModified() and self._readThroughMode and self._dataSource is not None:
                if self.getType() == str:
                    self.setInternalValue(str(self._dataSource))
                else:
                    self.setInternalValue(self._dataSource.getValue())
                self.fireValueChange(False)
            return

    def __str__(self):
        """Returns the value of the IProperty in human readable textual
        format.
        """
        value = self.getValue()
        if value is None:
            return ''
        else:
            return str(self.getValue())

    def getValue(self):
        """Gets the current value of the field.

        This is the visible, modified and possible invalid value the user
        have entered to the field. In the read-through mode, the abstract
        buffer is also updated and validation is performed.

        Note that the object returned is compatible with getType(). For
        example, if the type is String, this returns Strings even when the
        underlying datasource is of some other type. In order to access the
        datasources native type, use getPropertyDatasource().getValue()
        instead.

        Note that when you extend AbstractField, you must reimplement this
        method if datasource.getValue() is not assignable to class returned
        by getType() AND getType() is not String. In case of Strings,
        getValue() calls datasource.toString() instead of
        datasource.getValue().

        @return: the current value of the field.
        """
        if self._dataSource is None or not self.isReadThrough() or self.isModified():
            return self._value
        else:
            if self.getType() == str:
                newValue = str(self._dataSource)
            else:
                newValue = self._dataSource.getValue()
            return newValue

    def setValue(self, newValue, repaintIsNotNeeded=False):
        """Sets the value of the field.

        @param newValue:
                   the new value of the field.
        @param repaintIsNotNeeded:
                   True iff caller is sure that repaint is not needed.
        @raise ReadOnlyException:
        @raise ConversionException:
        """
        if newValue is None and self._value is not None or newValue is not None and newValue != self._value:
            if self.isReadOnly():
                raise prop.ReadOnlyException()
            if repaintIsNotNeeded and (self.isRequired() or self.getValidators() is not None):
                repaintIsNotNeeded = False
            if not self.isInvalidAllowed():
                for v in self.getValidators():
                    v.validate(newValue)

            self.setInternalValue(newValue)
            self._modified = self._dataSource is not None
            self._valueWasModifiedByDataSourceDuringCommit = False
            if self.isWriteThrough() and self._dataSource is not None and (self.isInvalidCommitted() or self.isValid()):
                try:
                    try:
                        self._committingValueToDataSource = True
                        self._dataSource.setValue(newValue)
                        self._modified = False
                    except Exception as e:
                        exception = SourceException(self, e)
                        self._currentBufferedSourceException = exception
                        self.requestRepaint()
                        raise self._currentBufferedSourceException

                finally:
                    self._committingValueToDataSource = False

            if self._currentBufferedSourceException is not None:
                self._currentBufferedSourceException = None
                self.requestRepaint()
            if self._valueWasModifiedByDataSourceDuringCommit:
                self._valueWasModifiedByDataSourceDuringCommit = repaintIsNotNeeded = False
            self.fireValueChange(repaintIsNotNeeded)
        return

    def getPropertyDataSource(self):
        """Gets the current data source of the field, if any.

        @return: the current data source as a IProperty, or C{None}
                if none defined.
        """
        return self._dataSource

    def setPropertyDataSource(self, newDataSource):
        """Sets the specified IProperty as the data source for the field.
        All uncommitted changes are replaced with a value from the new data
        source.

        If the datasource has any validators, the same validators are added
        to the field. Because the default behavior of the field is to allow
        invalid values, but not to allow committing them, this only adds
        visual error messages to fields and do not allow committing them as
        long as the value is invalid. After the value is valid, the error
        message is not shown and the commit can be done normally.

        Note: before 6.5 we actually called discard() method in the beginning
        of the method. This was removed to simplify implementation, avoid
        excess calls to backing property and to avoid odd value change events
        that were previously fired (developer expects 0-1 value change events
        if this method is called). Some complex field implementations might
        now need to override this method to do housekeeping similar to
        discard().

        @param newDataSource:
                   the new data source property.
        """
        oldValue = self._value
        if self._dataSource is not None and issubclass(self._dataSource.__class__, prop.IValueChangeNotifier):
            self._dataSource.removeListener(self, prop.IValueChangeListener)
        if self._dataSource is not None and issubclass(self._dataSource.__class__, prop.IReadOnlyStatusChangeNotifier):
            self._dataSource.removeListener(self, prop.IReadOnlyStatusChangeListener)
        self._dataSource = newDataSource
        try:
            if self._dataSource is not None:
                if self.getType() == str:
                    self.setInternalValue(str(self._dataSource))
                else:
                    self.setInternalValue(self._dataSource.getValue())
            self._modified = False
        except Exception as e:
            exception = SourceException(self, e)
            self._currentBufferedSourceException = exception
            self._modified = True

        if isinstance(self._dataSource, prop.IValueChangeNotifier):
            self._dataSource.addListener(self, prop.IValueChangeListener)
        if isinstance(self._dataSource, prop.IReadOnlyStatusChangeNotifier):
            self._dataSource.addListener(self, prop.IReadOnlyStatusChangeListener)
        if isinstance(self._dataSource, IValidatable):
            validators = self._dataSource.getValidators()
            if validators is not None:
                for v in validators:
                    self.addValidator(v)

        if self._value != oldValue and self._value is not None and self._value != oldValue or self._value is None:
            self.fireValueChange(False)
        return

    def addValidator(self, validator):
        """Adds a new validator for the field's value. All validators added
        to a field are checked each time the its value changes.

        @param validator:
                   the new validator to be added.
        """
        if self._validators is None:
            self._validators = list()
        self._validators.append(validator)
        self.requestRepaint()
        return

    def getValidators(self):
        """Gets the validators of the field.

        @return: the Unmodifiable collection that holds all validators for
                the field.
        """
        if self._validators is None or len(self._validators) == 0:
            return
        return self._validators

    def removeValidator(self, validator):
        """Removes the validator from the field.

        @param validator:
                   the validator to remove.
        """
        if self._validators is not None:
            self._validators.remove(validator)
        self.requestRepaint()
        return

    def isValid(self):
        """Tests the current value against registered validators if the
        field is not empty. If the field is empty it is considered valid
        if it is not required and invalid otherwise. Validators are never
        checked for empty fields.

        @return: C{True} if all registered validators claim that
                the current value is valid or if the field is empty and
                not required, C{False} otherwise.
        """
        if self.isEmpty():
            if self.isRequired():
                return False
            else:
                return True

        if self._validators is None:
            return True
        else:
            value = self.getValue()
            for v in self._validators:
                if not v.isValid(value):
                    return False

            return True

    def validate(self):
        """Checks the validity of the IValidatable by validating the field
        with all attached validators except when the field is empty. An
        empty field is invalid if it is required and valid otherwise.

        The "required" validation is a built-in validation feature. If
        the field is required, but empty, validation will throw an
        EmptyValueException with the error message set with
        setRequiredError().

        @see: L{IValidatable.validate}
        """
        if self.isEmpty():
            if self.isRequired():
                raise EmptyValueException(self._requiredError)
            else:
                return
        if self._validators is None:
            return
        else:
            firstError = None
            errors = None
            value = self.getValue()
            for v in self._validators:
                try:
                    v.validate(value)
                except InvalidValueException as e:
                    if firstError is None:
                        firstError = e
                    else:
                        if errors is None:
                            errors = list()
                            errors.append(firstError)
                        errors.append(e)

            if firstError is None:
                return
            if errors is None:
                raise firstError
            exceptions = [
             None] * len(errors)
            index = 0
            for e in errors:
                exceptions[index] = e
                index += 1

            raise InvalidValueException(None, exceptions)
            return

    def isInvalidAllowed(self):
        """Fields allow invalid values by default. In most cases this is
        wanted, because the field otherwise visually forget the user input
        immediately.

        @return: true iff the invalid values are allowed.
        @see: L{IValidatable.isInvalidAllowed}
        """
        return self._invalidAllowed

    def setInvalidAllowed(self, invalidAllowed):
        """Fields allow invalid values by default. In most cases this is
        wanted, because the field otherwise visually forget the user input
        immediately.

        In common setting where the user wants to assure the correctness of
        the datasource, but allow temporarily invalid contents in the field,
        the user should add the validators to datasource, that should not
        allow invalid values. The validators are automatically copied to the
        field when the datasource is set.

        @see: L{IValidatable.setInvalidAllowed}
        """
        self._invalidAllowed = invalidAllowed

    def getErrorMessage(self):
        """Error messages shown by the fields are composites of the error
        message thrown by the superclasses (that is the component error
        message), validation errors and buffered source errors.

        @see: L{AbstractComponent.getErrorMessage}
        """
        validationError = None
        if self.isValidationVisible():
            try:
                self.validate()
            except InvalidValueException as e:
                if not e.isInvisible():
                    validationError = e

        superError = super(AbstractField, self).getErrorMessage()
        if superError is None and validationError is None and self._currentBufferedSourceException is None:
            return
        else:
            return CompositeErrorMessage([superError, validationError,
             self._currentBufferedSourceException])

    def addListener(self, listener, iface=None):
        if isinstance(listener, prop.IReadOnlyStatusChangeListener) and (iface is None or issubclass(iface, prop.IReadOnlyStatusChangeListener)):
            self.registerListener(prop.IReadOnlyStatusChangeEvent, listener, _READ_ONLY_STATUS_CHANGE_METHOD)
        if isinstance(listener, prop.IValueChangeListener) and (iface is None or issubclass(iface, prop.IValueChangeListener)):
            self.registerListener(field.ValueChangeEvent, listener, _VALUE_CHANGE_METHOD)
        super(AbstractField, self).addListener(listener, iface)
        return

    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, prop.IReadOnlyStatusChangeEvent):
            self.registerCallback(prop.IReadOnlyStatusChangeEvent, callback, None, *args)
        elif issubclass(eventType, prop.ValueChangeEvent):
            self.registerCallback(prop.ValueChangeEvent, callback, None, *args)
        else:
            super(AbstractField, self).addCallback(callback, eventType, *args)
        return

    def removeListener(self, listener, iface=None):
        if isinstance(listener, prop.IReadOnlyStatusChangeListener) and (iface is None or issubclass(iface, prop.IReadOnlyStatusChangeListener)):
            self.withdrawListener(prop.IReadOnlyStatusChangeEvent, listener, _READ_ONLY_STATUS_CHANGE_METHOD)
        if isinstance(listener, prop.IValueChangeListener) and (iface is None or issubclass(iface, prop.IValueChangeListener)):
            self.withdrawListener(field.ValueChangeEvent, listener, _VALUE_CHANGE_METHOD)
        super(AbstractField, self).removeListener(listener, iface)
        return

    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, prop.IReadOnlyStatusChangeEvent):
            self.withdrawCallback(prop.IReadOnlyStatusChangeEvent, callback)
        elif issubclass(eventType, prop.ValueChangeEvent):
            self.withdrawCallback(prop.ValueChangeEvent, callback)
        else:
            super(AbstractField, self).removeCallback(callback, eventType)
        return

    def fireValueChange(self, repaintIsNotNeeded):
        """Emits the value change event. The value contained in the
        field is validated before the event is created.
        """
        event = field.ValueChangeEvent(self)
        self.fireEvent(event)
        if not repaintIsNotNeeded:
            self.requestRepaint()

    def readOnlyStatusChange(self, event):
        """React to read only status changes of the property by
        requesting a repaint.

        @see: L{IReadOnlyStatusChangeListener}
        """
        self.requestRepaint()

    def fireReadOnlyStatusChange(self):
        """Emits the read-only status change event. The value contained
        in the field is validated before the event is created.
        """
        event = IReadOnlyStatusChangeEvent(self)
        self.fireEvent(event)

    def valueChange(self, event):
        """This method listens to data source value changes and passes
        the changes forwards.

        Changes are not forwarded to the listeners of the field during
        internal operations of the field to avoid duplicate notifications.

        @param event:
                   the value change event telling the data source
                   contents have changed.
        """
        if self.isReadThrough():
            if self._committingValueToDataSource:
                propertyNotifiesOfTheBufferedValue = event.getProperty().getValue() == self._value or self._value is not None and self._value == event.getProperty().getValue()
                if not propertyNotifiesOfTheBufferedValue:
                    self.readValueFromProperty(event)
                    self._valueWasModifiedByDataSourceDuringCommit = True
            elif not self.isModified():
                self.readValueFromProperty(event)
                self.fireValueChange(False)
        return

    def readValueFromProperty(self, event):
        self.setInternalValue(event.getProperty().getValue())

    def changeVariables(self, source, variables):
        super(AbstractField, self).changeVariables(source, variables)

    def focus(self):
        super(AbstractField, self).focus()

    @classmethod
    def constructField(cls, propertyType):
        """Creates abstract field by the type of the property.

        This returns most suitable field type for editing property of
        given type.

        @param propertyType:
                   the Type of the property, that needs to be edited.
        @deprecated: use e.g.
                L{DefaultFieldFactory.createFieldByPropertyType} instead
        """
        warn('use createFieldByPropertyType() instead', DeprecationWarning)
        from muntjac.ui.default_field_factory import DefaultFieldFactory
        return DefaultFieldFactory.createFieldByPropertyType(propertyType)

    def getTabIndex(self):
        return self._tabIndex

    def setTabIndex(self, tabIndex):
        self._tabIndex = tabIndex
        self.requestRepaint()

    def setInternalValue(self, newValue):
        """Sets the internal field value. This is purely used by AbstractField
        to change the internal IField value. It does not trigger valuechange
        events. It can be overridden by the inheriting classes to update all
        dependent variables.

        @param newValue:
                   the new value to be set.
        """
        self._value = newValue
        if self._validators is not None and len(self._validators) > 0:
            self.requestRepaint()
        return

    def attach(self):
        """Notifies the component that it is connected to an application.

        @see: L{IComponent.attach}
        """
        super(AbstractField, self).attach()
        if self._actionManager is not None:
            self._actionManager.setViewer(self.getWindow())
        return

    def detach(self):
        super(AbstractField, self).detach()
        if self._actionManager is not None:
            self._actionManager.setViewer(None)
        return

    def isRequired(self):
        """Is this field required. Required fields must filled by the user.

        If the field is required, it is visually indicated in the user
        interface. Furthermore, setting field to be required implicitly
        adds "non-empty" validator and thus isValid() == false or any
        isEmpty() fields. In those cases validation errors are not painted
        as it is obvious that the user must fill in the required fields.

        On the other hand, for the non-required fields isValid() == true
        if the field isEmpty() regardless of any attached validators.

        @return: C{True} if the field is required, otherwise C{False}.
        """
        return self._required

    def setRequired(self, required):
        """Sets the field required. Required fields must filled by the user.

        If the field is required, it is visually indicated in the user
        interface. Furthermore, setting field to be required implicitly adds
        "non-empty" validator and thus isValid() == false or any isEmpty()
        fields. In those cases validation errors are not painted as it is
        obvious that the user must fill in the required fields.

        On the other hand, for the non-required fields isValid() == true if
        the field isEmpty() regardless of any attached validators.

        @param required:
                   Is the field required.
        """
        self._required = required
        self.requestRepaint()

    def setRequiredError(self, requiredMessage):
        """Set the error that is show if this field is required, but empty.
        When setting requiredMessage to be "" or null, no error pop-up or
        exclamation mark is shown for a empty required field. This faults
        to "". Even in those cases isValid() returns false for empty
        required fields.

        @param requiredMessage:
                   Message to be shown when this field is required, but empty.
        """
        self._requiredError = requiredMessage
        self.requestRepaint()

    def getRequiredError(self):
        return self._requiredError

    def isEmpty(self):
        """Is the field empty?

        In general, "empty" state is same as null. As an exception,
        TextField also treats empty string as "empty".
        """
        return self.getValue() is None

    def isValidationVisible(self):
        """Is automatic, visible validation enabled?

        If automatic validation is enabled, any validators connected to
        this component are evaluated while painting the component and
        potential error messages are sent to client. If the automatic
        validation is turned off, isValid() and validate() methods still
        work, but one must show the validation in their own code.

        @return: True, if automatic validation is enabled.
        """
        return self._validationVisible

    def setValidationVisible(self, validateAutomatically):
        """Enable or disable automatic, visible validation.

        If automatic validation is enabled, any validators connected to
        this component are evaluated while painting the component and
        potential error messages are sent to client. If the automatic
        validation is turned off, isValid() and validate() methods still
        work, but one must show the validation in their own code.

        @param validateAutomatically:
                   True, if automatic validation is enabled.
        """
        if self._validationVisible != validateAutomatically:
            self.requestRepaint()
            self._validationVisible = validateAutomatically

    def setCurrentBufferedSourceException(self, currentBufferedSourceException):
        """Sets the current buffered source exception.
        """
        self._currentBufferedSourceException = currentBufferedSourceException
        self.requestRepaint()

    def getActionManager(self):
        """Gets the L{ActionManager} used to manage the
        L{ShortcutListener}s added to this L{IField}.

        @return: the ActionManager in use
        """
        if self._actionManager is None:
            self._actionManager = ActionManager()
            if self.getWindow() is not None:
                self._actionManager.setViewer(self.getWindow())
        return self._actionManager

    def addShortcutListener(self, shortcut):
        self.getActionManager().addAction(shortcut)

    def removeShortcutListener(self, shortcut):
        if self._actionManager is not None:
            self._actionManager.removeAction(shortcut)
        return


class FocusShortcut(ShortcutListener):
    """A ready-made L{ShortcutListener} that focuses the given
    L{Focusable} (usually a L{IField}) when the keyboard
    shortcut is invoked.
    """

    def __init__(self, *args):
        """Creates a keyboard shortcut for focusing the given
        L{IFocusable} using either the shorthand notation defined in
        L{ShortcutAction}, or the given key code.

        @param args: tuple of the form
            - (focusable, shorthandCaption)
              1. to b efocused when the shortcut is invoked
              2. caption with keycode and modifiers indicated
            - (focusable, keyCode, modifiers)
              1. to be focused when the shortcut is invoked
              2. keycode that invokes the shortcut
              3. modifiers required to invoke the shortcut
            - (focusable, keyCode)
              1. to focused when the shortcut is invoked
              2. keycode that invokes the shortcut
        """
        self.focusable = None
        nargs = len(args)
        if nargs == 2:
            if isinstance(args[1], int):
                focusable, keyCode = args
                FocusShortcut.__init__(self, focusable, keyCode, None)
            else:
                focusable, shorthandCaption = args
                super(FocusShortcut, self).__init__(shorthandCaption)
                self.focusable = focusable
        else:
            focusable, keyCode = args[:2]
            modifiers = args[2:]
            super(FocusShortcut, self).__init__(None, keyCode, modifiers)
            self.focusable = focusable
        return

    def handleAction(self, sender, target):
        self.focusable.focus()


class IReadOnlyStatusChangeEvent(ComponentEvent, prop.IProperty, prop.IReadOnlyStatusChangeEvent):
    """An C{Event} object specifying the IProperty whose
    read-only status has changed.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, source):
        """New instance of text change event.

        @param source:
                   the Source of the event.
        """
        super(IReadOnlyStatusChangeEvent, self).__init__(source)

    def getProperty(self):
        """IProperty where the event occurred.

        @return: the Source of the event.
        """
        return self.getSource()