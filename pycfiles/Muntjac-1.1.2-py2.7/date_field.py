# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/date_field.py
# Compiled at: 2013-04-04 15:36:35
"""Defines a date editor component."""
from datetime import datetime
from babel.dates import parse_date
from muntjac.ui.abstract_field import AbstractField
from muntjac.data.property import IProperty, ConversionException
from muntjac.ui.form import Form
from muntjac.data.validator import InvalidValueException
from muntjac.terminal.gwt.client.ui.v_date_field import VDateField
from muntjac.event.field_events import BlurEvent, IBlurListener, IBlurNotifier, FocusEvent, IFocusListener, IFocusNotifier
from muntjac.util import totalseconds

class DateField(AbstractField, IBlurNotifier, IFocusNotifier):
    """A date editor component that can be bound to any L{IProperty}
    that is compatible with C{datetime}.

    Since C{DateField} extends C{AbstractField} it implements the L{IBuffered}
    interface.

    A C{DateField} is in write-through mode by default, so
    L{AbstractField.setWriteThrough} must be called to enable buffering.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """
    CLIENT_WIDGET = None
    RESOLUTION_MSEC = 0
    RESOLUTION_SEC = 1
    RESOLUTION_MIN = 2
    RESOLUTION_HOUR = 3
    RESOLUTION_DAY = 4
    RESOLUTION_MONTH = 5
    RESOLUTION_YEAR = 6
    _largestModifiable = RESOLUTION_YEAR

    def __init__(self, *args):
        """Constructs an new C{DateField}.

        @param args: tuple of the form
            - ()
            - (caption)
              1. the caption of the datefield.
            - (caption, dataSource)
              1. the caption string for the editor.
              2. the IProperty to be edited with this editor.
            - (dataSource)
              1. the IProperty to be edited with this editor.
            - (caption, value)
              1. the caption string for the editor.
              2. the date value.
        """
        super(DateField, self).__init__()
        self._calendar = None
        self._dateFormat = None
        self._lenient = False
        self._dateString = None
        self._uiHasValidDateString = True
        self._showISOWeekNumbers = False
        self._currentParseErrorMessage = None
        self._defaultParseErrorMessage = 'Date format not recognized'
        self._timeZone = None
        self._resolution = self.RESOLUTION_MSEC
        nargs = len(args)
        if nargs == 0:
            pass
        elif nargs == 1:
            if isinstance(args[0], IProperty):
                dataSource, = args
                if not issubclass(dataSource.getType(), datetime):
                    raise ValueError, "Can't use " + dataSource.getType().__name__ + ' typed property as datasource'
                self.setPropertyDataSource(dataSource)
            else:
                caption, = args
                self.setCaption(caption)
        elif nargs == 2:
            if isinstance(args[1], datetime):
                caption, value = args
                self.setValue(value)
                self.setCaption(caption)
            else:
                caption, dataSource = args
                DateField.__init__(self, dataSource)
                self.setCaption(caption)
        else:
            raise ValueError, 'too many arguments'
        return

    def __getstate__(self):
        result = self.__dict__.copy()
        del result['_calendar']
        return result

    def __setstate__(self, d):
        self.__dict__ = d
        self._calendar = None
        return

    def paintContent(self, target):
        super(DateField, self).paintContent(target)
        l = self.getLocale()
        if l is not None:
            target.addAttribute('locale', str(l))
        if self.getDateFormat() is not None:
            target.addAttribute('format', self._dateFormat)
        if not self.isLenient():
            target.addAttribute('strict', True)
        target.addAttribute(VDateField.WEEK_NUMBERS, self.isShowISOWeekNumbers())
        target.addAttribute('parsable', self._uiHasValidDateString)
        calendar = self.getCalendar()
        currentDate = self.getValue()
        r = self._resolution
        while r <= self._largestModifiable:
            t = -1
            if r == self.RESOLUTION_MSEC:
                if currentDate is not None:
                    t = calendar.microsecond / 1000.0
                target.addVariable(self, 'msec', t)
            elif r == self.RESOLUTION_SEC:
                if currentDate is not None:
                    t = calendar.second
                target.addVariable(self, 'sec', t)
            elif r == self.RESOLUTION_MIN:
                if currentDate is not None:
                    t = calendar.minute
                target.addVariable(self, 'min', t)
            elif r == self.RESOLUTION_HOUR:
                if currentDate is not None:
                    t = calendar.hour
                target.addVariable(self, 'hour', t)
            elif r == self.RESOLUTION_DAY:
                if currentDate is not None:
                    t = calendar.day
                target.addVariable(self, 'day', t)
            elif r == self.RESOLUTION_MONTH:
                if currentDate is not None:
                    t = calendar.month
                target.addVariable(self, 'month', t)
            elif r == self.RESOLUTION_YEAR:
                if currentDate is not None:
                    t = calendar.year
                target.addVariable(self, 'year', t)
            r += 1

        return

    def shouldHideErrors(self):
        shouldHideErrors = super(DateField, self).shouldHideErrors()
        return shouldHideErrors and self._uiHasValidDateString

    def changeVariables(self, source, variables):
        super(DateField, self).changeVariables(source, variables)
        if not self.isReadOnly() and ('year' in variables or 'month' in variables or 'day' in variables or 'hour' in variables or 'min' in variables or 'sec' in variables or 'msec' in variables or 'dateString' in variables):
            oldDate = self.getValue()
            newDate = None
            newDateString = variables.get('dateString')
            self._dateString = newDateString
            year = -1 if variables.get('year') is None else int(variables.get('year')) if 'year' in variables else -1
            month = -1 if variables.get('month') is None else int(variables.get('month')) if 'month' in variables else -1
            day = -1 if variables.get('day') is None else int(variables.get('day')) if 'day' in variables else -1
            hour = -1 if variables.get('hour') is None else int(variables.get('hour')) if 'hour' in variables else -1
            minn = -1 if variables.get('min') is None else int(variables.get('min')) if 'min' in variables else -1
            sec = -1 if variables.get('sec') is None else int(variables.get('sec')) if 'sec' in variables else -1
            msec = -1 if variables.get('msec') is None else int(variables.get('msec')) if 'msec' in variables else -1
            if year < 0 and month < 0 and day < 0 and hour < 0 and min < 0 and sec < 0 and msec < 0:
                newDate = None
            else:
                cal = self.getCalendar()
                year = cal.year if year < 0 else year
                month = cal.month if month < 0 else month
                day = cal.day if day < 0 else day
                hour = cal.hour if hour < 0 else hour
                minn = cal.minute if minn < 0 else minn
                sec = cal.second if sec < 0 else sec
                msec = cal.microsecond * 1000.0 if msec < 0 else msec
                cal = datetime(year, month, day, hour, minn, sec, int(msec / 1000.0))
                newDate = cal
            if newDate is None and self._dateString is not None and '' != self._dateString:
                try:
                    parsedDate = self.handleUnparsableDateString(self._dateString)
                    self.setValue(parsedDate, True)
                    self.requestRepaint()
                except ConversionException as e:
                    if oldDate is not None:
                        self.setValue(None)
                        self._dateString = newDateString
                    self._currentParseErrorMessage = e.getLocalizedMessage()
                    self._uiHasValidDateString = False
                    self.notifyFormOfValidityChange()
                    self.requestRepaint()

            elif newDate != oldDate and (newDate is None or newDate != oldDate):
                self.setValue(newDate, True)
            elif not self._uiHasValidDateString:
                self.setValue(None)
        if FocusEvent.EVENT_ID in variables:
            self.fireEvent(FocusEvent(self))
        if BlurEvent.EVENT_ID in variables:
            self.fireEvent(BlurEvent(self))
        return

    def handleUnparsableDateString(self, dateString):
        """This method is called to handle a non-empty date string from
        the client if the client could not parse it as a C{datetime}.

        By default, a C{ConversionException} is thrown, and the
        current value is not modified.

        This can be overridden to handle conversions, to return null
        (equivalent to empty input), to throw an exception or to fire
        an event.

        @raise ConversionException:
                    to keep the old value and indicate an error
        """
        self._currentParseErrorMessage = None
        raise ConversionException(self.getParseErrorMessage())
        return

    def getType(self):
        return datetime

    def setValue(self, newValue, repaintIsNotNeeded=False):
        if newValue is None and not self._uiHasValidDateString:
            self.setInternalValue(None)
            self.notifyFormOfValidityChange()
            self.requestRepaint()
            return
        else:
            if newValue is None or isinstance(newValue, datetime):
                super(DateField, self).setValue(newValue, repaintIsNotNeeded)
            else:
                try:
                    app = self.getApplication()
                    if app is not None:
                        l = app.getLocale()
                    currentTimeZone = self.getTimeZone()
                    if currentTimeZone is not None:
                        currentTimeZone
                    val = parse_date(str(newValue), locale=l)
                    super(DateField, self).setValue(val, repaintIsNotNeeded)
                except ValueError:
                    self._uiHasValidDateString = False
                    raise ConversionException(self.getParseErrorMessage())

            return

    def notifyFormOfValidityChange(self):
        """Detects if this field is used in a Form (logically) and if so,
        notifies it (by repainting it) that the validity of this field might
        have changed.
        """
        parenOfDateField = self.getParent()
        formFound = False
        while parenOfDateField is not None or formFound:
            if isinstance(parenOfDateField, Form):
                f = parenOfDateField
                visibleItemProperties = f.getItemPropertyIds()
                for fieldId in visibleItemProperties:
                    field = fieldId
                    if field == self:
                        f.requestRepaint()
                        formFound = True
                        break

            if formFound:
                break
            parenOfDateField = parenOfDateField.getParent()

        return

    def setPropertyDataSource(self, newDataSource):
        """Sets the DateField datasource. Datasource type must assignable
        to Date.

        @see: L{Viewer.setPropertyDataSource}
        """
        if newDataSource is None or issubclass(newDataSource.getType(), datetime):
            super(DateField, self).setPropertyDataSource(newDataSource)
        else:
            raise ValueError, 'DateField only supports datetime properties'
        return

    def setInternalValue(self, newValue):
        if newValue is not None:
            self._dateString = str(newValue)
        else:
            self._dateString = None
        if not self._uiHasValidDateString:
            self.setComponentError(None)
            self._uiHasValidDateString = True
            self._currentParseErrorMessage = None
        super(DateField, self).setInternalValue(newValue)
        return

    def getResolution(self):
        """Gets the resolution.
        """
        return self._resolution

    def setResolution(self, resolution):
        """Sets the resolution of the C{DateField}.

        @param resolution:
                   the resolution to set.
        """
        self._resolution = resolution
        self.requestRepaint()

    def getCalendar(self):
        """Returns new instance calendar used in Date conversions.

        Returns new clone of the calendar object initialized using the the
        current date (if available)

        If this is no calendar is assigned the C{calendar} is used.

        @return: the calendar
        @see: L{setCalendar}
        """
        if self._calendar is None:
            self._calendar = datetime.now()
        timestamp = totalseconds(self._calendar - datetime(1970, 1, 1))
        newCal = datetime.fromtimestamp(timestamp)
        currentDate = self.getValue()
        if currentDate is not None:
            newCal = currentDate
        currentTimeZone = self.getTimeZone()
        if currentTimeZone is not None:
            currentTimeZone
        return newCal

    def setDateFormat(self, dateFormat):
        """Sets formatting used by some component implementations.

        By default it is encouraged to used default formatting defined
        by Locale.

        @param dateFormat: the dateFormat to set
        @see: L{AbstractComponent.setLocale}
        """
        self._dateFormat = dateFormat
        self.requestRepaint()

    def getDateFormat(self):
        """Returns a format string used to format date value on client side
        or null if default formatting from L{IComponent.getLocale} is
        used.

        @return: the dateFormat
        """
        return self._dateFormat

    def setLenient(self, lenient):
        """Specifies whether or not date/time interpretation in component is
        to be lenient.

        @see: L{isLenient}
        @param lenient:
                   true if the lenient mode is to be turned on; false if it
                   is to be turned off.
        """
        self._lenient = lenient
        self.requestRepaint()

    def isLenient(self):
        """Returns whether date/time interpretation is to be lenient.

        @see: L{setLenient}
        @return: true if the interpretation mode of this calendar is lenient;
                false otherwise.
        """
        return self._lenient

    def addListener(self, listener, iface=None):
        if isinstance(listener, IBlurListener) and (iface is None or issubclass(iface, IBlurListener)):
            self.registerListener(BlurEvent.EVENT_ID, BlurEvent, listener, IBlurListener.blurMethod)
        if isinstance(listener, IFocusListener) and (iface is None or issubclass(iface, IFocusListener)):
            self.registerListener(FocusEvent.EVENT_ID, FocusEvent, listener, IFocusListener.focusMethod)
        super(DateField, self).addListener(listener, iface)
        return

    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, BlurEvent):
            self.registerCallback(BlurEvent, callback, BlurEvent.EVENT_ID, *args)
        elif issubclass(eventType, FocusEvent):
            self.registerCallback(FocusEvent, callback, FocusEvent.EVENT_ID, *args)
        else:
            super(DateField, self).addCallback(callback, eventType, *args)
        return

    def removeListener(self, listener, iface=None):
        if isinstance(listener, IBlurListener) and (iface is None or issubclass(iface, IBlurListener)):
            self.withdrawListener(BlurEvent.EVENT_ID, BlurEvent, listener)
        if isinstance(listener, IFocusListener) and (iface is None or issubclass(iface, IFocusListener)):
            self.withdrawListener(FocusEvent.EVENT_ID, FocusEvent, listener)
        super(DateField, self).removeListener(listener, iface)
        return

    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, BlurEvent):
            self.withdrawCallback(BlurEvent, callback, BlurEvent.EVENT_ID)
        elif issubclass(eventType, FocusEvent):
            self.withdrawCallback(FocusEvent, callback, FocusEvent.EVENT_ID)
        else:
            super(DateField, self).removeCallback(callback, eventType)
        return

    def isShowISOWeekNumbers(self):
        """Checks whether ISO 8601 week numbers are shown in the date
        selector.

        @return: true if week numbers are shown, false otherwise.
        """
        return self._showISOWeekNumbers

    def setShowISOWeekNumbers(self, showWeekNumbers):
        """Sets the visibility of ISO 8601 week numbers in the date selector.
        ISO 8601 defines that a week always starts with a Monday so the week
        numbers are only shown if this is the case.

        @param showWeekNumbers:
                   true if week numbers should be shown, false otherwise.
        """
        self._showISOWeekNumbers = showWeekNumbers
        self.requestRepaint()

    def isValid(self):
        """Tests the current value against registered validators if the field
        is not empty. Note that DateField is considered empty (value == null)
        and invalid if it contains text typed in by the user that couldn't be
        parsed into a Date value.

        @see: L{AbstractField.isValid}
        """
        return self._uiHasValidDateString and super(DateField, self).isValid()

    def validate(self):
        if not self._uiHasValidDateString:
            raise UnparsableDateString(self._currentParseErrorMessage)
        super(DateField, self).validate()

    def getParseErrorMessage(self):
        """Return the error message that is shown if the user inputted value
        can't be parsed into a datetime object. If
        L{handleUnparsableDateString} is overridden and it
        throws a custom exception, the message returned by
        L{Exception.message} will be used instead of the
        value returned by this method.

        @see: L{setParseErrorMessage}

        @return: the error message that the DateField uses when it can't parse
                 the textual input from user to a Date object
        """
        return self._defaultParseErrorMessage

    def setParseErrorMessage(self, parsingErrorMessage):
        """Sets the default error message used if the DateField cannot parse
        the text input by user to a datetime field. Note that if the
        L{handleUnparsableDateString} method is overridden, the localized
        message from its exception is used.

        @see: L{getParseErrorMessage}
        @see: L{handleUnparsableDateString}
        """
        self._defaultParseErrorMessage = parsingErrorMessage

    def setTimeZone(self, timeZone):
        """Sets the time zone used by this date field. The time zone is used
        to convert the absolute time in a Date object to a logical time
        displayed in the selector and to convert the select time back to a
        datetime object.

        If no time zone has been set, the current default time zone returned
        by C{TimeZone.getDefault()} is used.

        @see L{getTimeZone()}
        @param timeZone:
                 the time zone to use for time calculations.
        """
        self._timeZone = timeZone
        self.requestRepaint()

    def getTimeZone(self):
        """Gets the time zone used by this field. The time zone is used to
        convert the absolute time in a Date object to a logical time displayed
        in the selector and to convert the select time back to a datetime
        object.

        If {@code null} is returned, the current default time zone returned by
        C{TimeZone.getDefault()} is used.

        @return: the current time zone
        """
        return self._timeZone


class UnparsableDateString(InvalidValueException):

    def __init__(self, message):
        super(UnparsableDateString, self).__init__(message)