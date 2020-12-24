# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/button.py
# Compiled at: 2013-04-04 15:36:35
"""Defines a generic button component."""
from warnings import warn
from muntjac.ui.abstract_field import AbstractField
from muntjac.ui.component import Event as ComponentEvent
from muntjac.event.shortcut_listener import ShortcutListener
from muntjac.data.property import IProperty
from muntjac.terminal.gwt.client.mouse_event_details import MouseEventDetails
from muntjac.terminal.gwt.client.ui.v_button import VButton
from muntjac.event.field_events import BlurEvent, IBlurListener, IBlurNotifier, FocusEvent, IFocusListener, IFocusNotifier

class IClickListener(object):
    """Interface for listening for a L{ClickEvent} fired by a L{Component}.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def buttonClick(self, event):
        """Called when a L{Button} has been clicked. A reference to
        the button is given by L{ClickEvent.getButton}.

        @param event:
                   An event containing information about the click.
        """
        raise NotImplementedError


_BUTTON_CLICK_METHOD = getattr(IClickListener, 'buttonClick')

class Button(AbstractField, IBlurNotifier, IFocusNotifier):
    """A generic button component.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """
    CLIENT_WIDGET = None

    def __init__(self, *args):
        """Creates a new push button.

        @param args: tuple of the form
            - ()
            - (caption)
              1. the Button caption
            - (caption, listener)
              1. the Button caption
              2. the Button click listener
            - (caption, target, methodName)
              1. the Button caption
              2. the object having the method for listening button clicks
              3. the name of the method in target object, that receives
                 button click events
            - (state)
              1. the initial state of the switch-button
            - (state, dataSource)
              1. the initial state of the switch-button
              2. boolean property
        """
        super(Button, self).__init__()
        self._switchMode = False
        self._disableOnClick = False
        self.clickShortcut = None
        nargs = len(args)
        if nargs == 0:
            self.setValue(False)
        elif nargs == 1:
            caption, = args
            Button.__init__(self)
            self.setCaption(caption)
        elif nargs == 2:
            if isinstance(args[1], bool):
                caption, initialState = args
                self.setCaption(caption)
                self.setValue(bool(initialState))
                self.setSwitchMode(True)
            elif isinstance(args[1], IProperty):
                caption, dataSource = args
                self.setCaption(caption)
                self.setSwitchMode(True)
                self.setPropertyDataSource(dataSource)
            else:
                caption, listener = args
                Button.__init__(self, caption)
                if isinstance(listener, IClickListener):
                    self.addListener(listener, IClickListener)
                else:
                    self.addCallback(listener, ClickEvent)
        elif nargs == 3:
            caption, target, methodName = args
            Button.__init__(self, caption)
            self.registerListener(ClickEvent, target, methodName)
        else:
            raise ValueError, 'too many arguments'
        return

    def paintContent(self, target):
        """Paints the content of this component.

        @param target:
                   the PaintEvent.
        @raise IOException:
                    if the writing failed due to input/output error.
        @raise PaintException:
                    if the paint operation failed.
        """
        super(Button, self).paintContent(target)
        if self.isSwitchMode():
            target.addAttribute('type', 'switch')
        target.addVariable(self, 'state', self.booleanValue())
        if self.isDisableOnClick():
            target.addAttribute(VButton.ATTR_DISABLE_ON_CLICK, True)
        if self.clickShortcut is not None:
            target.addAttribute('keycode', self.clickShortcut.getKeyCode())
        return

    def changeVariables(self, source, variables):
        """Invoked when the value of a variable has changed. Button
        listeners are notified if the button is clicked.
        """
        super(Button, self).changeVariables(source, variables)
        if 'disabledOnClick' in variables:
            self.setEnabled(False)
        if not self.isReadOnly() and 'state' in variables:
            newValue = bool(variables.get('state'))
            oldValue = bool(self.getValue())
            if self.isSwitchMode():
                if newValue is not None and newValue != oldValue and not self.isReadOnly():
                    self.setValue(newValue)
                    if 'mousedetails' in variables:
                        self.fireClick(MouseEventDetails.deSerialize(variables.get('mousedetails')))
                    else:
                        self.fireClick()
            else:
                if newValue:
                    if 'mousedetails' in variables:
                        self.fireClick(MouseEventDetails.deSerialize(variables.get('mousedetails')))
                    else:
                        self.fireClick()
                if oldValue is None or oldValue:
                    self.setValue(False)
        if FocusEvent.EVENT_ID in variables:
            self.fireEvent(FocusEvent(self))
        if BlurEvent.EVENT_ID in variables:
            self.fireEvent(BlurEvent(self))
        return

    def isSwitchMode(self):
        """Checks if it is switchMode.

        @return: C{True} if it is in Switch Mode, otherwise C{False}.
        @deprecated: the L{CheckBox} component should be used instead
                     of Button in switch mode
        """
        warn('use CheckBox instead', DeprecationWarning)
        return self._switchMode

    def setSwitchMode(self, switchMode):
        """Sets the switchMode.

        @param switchMode:
                   The switchMode to set.
        @deprecated: the L{CheckBox} component should be used instead
                     of Button in switch mode
        """
        self._switchMode = switchMode
        if not switchMode:
            self.setImmediate(True)
            if self.booleanValue():
                self.setValue(False)

    def booleanValue(self):
        """Get the boolean value of the button state.

        @return: True iff the button is pressed down or checked.
        """
        value = self.getValue()
        if value is None:
            return False
        else:
            return bool(value)

    def setImmediate(self, immediate):
        """Sets immediate mode. Push buttons can not be set in
        non-immediate mode.

        @see: L{AbstractComponent.setImmediate}
        """
        super(Button, self).setImmediate(not self.isSwitchMode() or immediate)

    def getType(self):
        """The type of the button as a property.

        @see: L{IProperty.getType}
        """
        return bool

    STYLE_LINK = 'link'

    def addListener(self, listener, iface=None):
        """Adds the button click listener.

        @param listener:
                   the Listener to be added.
        """
        if isinstance(listener, IBlurListener) and (iface is None or issubclass(iface, IBlurListener)):
            self.registerListener(BlurEvent.EVENT_ID, BlurEvent, listener, IBlurListener.blurMethod)
        if isinstance(listener, IClickListener) and (iface is None or issubclass(iface, IClickListener)):
            self.registerListener(ClickEvent, listener, _BUTTON_CLICK_METHOD)
        if isinstance(listener, IFocusListener) and (iface is None or issubclass(iface, IFocusListener)):
            self.registerListener(FocusEvent.EVENT_ID, FocusEvent, listener, IFocusListener.focusMethod)
        super(Button, self).addListener(listener, iface)
        return

    def addCallback(self, callback, eventType=None, *args):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, BlurEvent):
            self.registerCallback(BlurEvent, callback, BlurEvent.EVENT_ID, *args)
        elif issubclass(eventType, ClickEvent):
            self.registerCallback(ClickEvent, callback, None, *args)
        elif issubclass(eventType, FocusEvent):
            self.registerCallback(FocusEvent, callback, FocusEvent.EVENT_ID, *args)
        else:
            super(Button, self).addCallback(callback, eventType, *args)
        return

    def removeListener(self, listener, iface=None):
        """Removes the button click listener.

        @param listener:
                   the Listener to be removed.
        """
        if isinstance(listener, IBlurListener) and (iface is None or issubclass(iface, IBlurListener)):
            self.withdrawListener(BlurEvent.EVENT_ID, BlurEvent, listener)
        if isinstance(listener, IClickListener) and (iface is None or issubclass(iface, IClickListener)):
            self.withdrawListener(ClickEvent, listener, _BUTTON_CLICK_METHOD)
        if isinstance(listener, IFocusListener) and (iface is None or issubclass(iface, IFocusListener)):
            self.withdrawListener(FocusEvent.EVENT_ID, FocusEvent, listener)
        super(Button, self).removeListener(listener, iface)
        return

    def removeCallback(self, callback, eventType=None):
        if eventType is None:
            eventType = callback._eventType
        if issubclass(eventType, BlurEvent):
            self.withdrawCallback(BlurEvent, callback, BlurEvent.EVENT_ID)
        elif issubclass(eventType, ClickEvent):
            self.withdrawCallback(ClickEvent, callback)
        elif issubclass(eventType, FocusEvent):
            self.withdrawCallback(FocusEvent, callback, FocusEvent.EVENT_ID)
        else:
            super(Button, self).removeCallback(callback, eventType)
        return

    def fireClick(self, details=None):
        """Fires a click event to all listeners.

        @param details:
                   MouseEventDetails from which keyboard modifiers and other
                   information about the mouse click can be obtained. If the
                   button was clicked by a keyboard event, some of the fields
                   may be empty/undefined.
        """
        if details is None:
            self.fireEvent(ClickEvent(self))
        else:
            self.fireEvent(ClickEvent(self, details))
        return

    def setInternalValue(self, newValue):
        if newValue is not None and not isinstance(newValue, bool):
            raise ValueError, self.__class__.__name__ + ' only accepts boolean values'
        super(Button, self).setInternalValue(newValue)
        return

    def setClickShortcut(self, keyCode, *modifiers):
        """Makes it possible to invoke a click on this button by pressing
        the given L{KeyCode} and (optional) L{ModifierKey}s.

        The shortcut is global (bound to the containing Window).

        @param keyCode:
                   the keycode for invoking the shortcut
        @param modifiers:
                   the (optional) modifiers for invoking the shortcut, null
                   for none
        """
        if self.clickShortcut is not None:
            self.removeShortcutListener(self.clickShortcut)
        self.clickShortcut = ClickShortcut(self, keyCode, *modifiers)
        self.addShortcutListener(self.clickShortcut)
        return

    def removeClickShortcut(self):
        """Removes the keyboard shortcut previously set with
        L{setClickShortcut}.
        """
        if self.clickShortcut is not None:
            self.removeShortcutListener(self.clickShortcut)
            self.clickShortcut = None
        return

    def isDisableOnClick(self):
        """Determines if a button is automatically disabled when clicked. See
        L{setDisableOnClick} for details.

        @return: true if the button is disabled when clicked, false otherwise
        """
        return self._disableOnClick

    def setDisableOnClick(self, disableOnClick):
        """Determines if a button is automatically disabled when clicked. If
        this is set to true the button will be automatically disabled when
        clicked, typically to prevent (accidental) extra clicks on a button.

        @param disableOnClick:
                  true to disable button when it is clicked, false otherwise
        """
        self.disableOnClick = disableOnClick
        self.requestRepaint()


class ClickShortcut(ShortcutListener):
    """A L{ShortcutListener} specifically made to define a keyboard
    shortcut that invokes a click on the given button.
    """

    def __init__(self, *args):
        """Creates a keyboard shortcut for clicking the given button using
        the shorthand notation defined in L{ShortcutAction} or using the
        given L{KeyCode} and L{ModifierKey}s.

        @param args: tuple of the form
            - (button, shorthandCaption)
              1. to be clicked when the shortcut is invoked
              2. the caption with shortcut keycode and modifiers indicated
            - (button, keyCode, modifiers)
              1. to be clicked when the shortcut is invoked
              2. KeyCode to react to
              3. optional modifiers for shortcut
            - (button, keyCode)
              1. to be clicked when the shortcut is invoked
              2. KeyCode to react to
        """
        args = args
        nargs = len(args)
        if nargs == 2:
            if isinstance(args[1], int):
                button, keyCode = args
                super(ClickShortcut, self).__init__(None, keyCode, tuple())
                self.button = button
            else:
                button, shorthandCaption = args
                super(ClickShortcut, self).__init__(shorthandCaption)
                self.button = button
        elif nargs >= 3:
            button, keyCode = args[:2]
            modifiers = args[2:]
            super(ClickShortcut, self).__init__(None, keyCode, modifiers)
            self.button = button
        else:
            raise ValueError, 'too few arguments'
        return

    def handleAction(self, sender, target):
        if self.button.isEnabled() and not self.button.isReadOnly():
            self.button.fireClick()


class ClickEvent(ComponentEvent):
    """Click event. This event is thrown, when the button is clicked.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, source, details=None):
        """New instance with mouse details

        @param source:
                   The source where the click took place
        @param details:
                   Details about the mouse click
        """
        super(ClickEvent, self).__init__(source)
        self._details = details

    def getButton(self):
        """Gets the Button where the event occurred.

        @return: the Source of the event.
        """
        return self.getSource()

    def getClientX(self):
        """Returns the mouse position (x coordinate) when the click took
        place. The position is relative to the browser client area.

        @return: The mouse cursor x position or -1 if unknown
        """
        if self._details is not None:
            return self._details.getClientX()
        else:
            return -1
            return

    def getClientY(self):
        """Returns the mouse position (y coordinate) when the click took
        place. The position is relative to the browser client area.

        @return: The mouse cursor y position or -1 if unknown
        """
        if self._details is not None:
            return self._details.getClientY()
        else:
            return -1
            return

    def getRelativeX(self):
        """Returns the relative mouse position (x coordinate) when the click
        took place. The position is relative to the clicked component.

        @return: The mouse cursor x position relative to the clicked layout
                 component or -1 if no x coordinate available
        """
        if self._details is not None:
            return self._details.getRelativeX()
        else:
            return -1
            return

    def getRelativeY(self):
        """Returns the relative mouse position (y coordinate) when the click
        took place. The position is relative to the clicked component.

        @return: The mouse cursor y position relative to the clicked layout
                 component or -1 if no y coordinate available
        """
        if self._details is not None:
            return self._details.getRelativeY()
        else:
            return -1
            return

    def isAltKey(self):
        """Checks if the Alt key was down when the mouse event took place.

        @return: true if Alt was down when the event occured, false
                 otherwise or if unknown
        """
        if self._details is not None:
            return self._details.isAltKey()
        else:
            return False
            return

    def isCtrlKey(self):
        """Checks if the Ctrl key was down when the mouse event took place.

        @return: true if Ctrl was pressed when the event occured, false
                 otherwise or if unknown
        """
        if self._details is not None:
            return self._details.isCtrlKey()
        else:
            return False
            return

    def isMetaKey(self):
        """Checks if the Meta key was down when the mouse event took place.

        @return: true if Meta was pressed when the event occurred, false
                 otherwise or if unknown
        """
        if self._details is not None:
            return self._details.isMetaKey()
        else:
            return False
            return

    def isShiftKey(self):
        """Checks if the Shift key was down when the mouse event took place.

        @return: true if Shift was pressed when the event occurred, false
                 otherwise or if unknown
        """
        if self._details is not None:
            return self._details.isShiftKey()
        else:
            return False
            return


def buttonClickCallback(func):
    func._eventType = ClickEvent
    return func