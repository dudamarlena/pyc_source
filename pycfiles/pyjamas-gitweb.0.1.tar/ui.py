# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.5/site-packages/pyjamas/ui.py
# Compiled at: 2008-09-04 15:59:54
__doc__ = '\n    This module implements the Pyjamas user-interface widget set for\n    Pyjamas-Desktop.\n'
from pyjamas.__pyjamas__ import JS, doc
import DOM, pygwt
from DeferredCommand import DeferredCommand
import pyjslib
from History import History
import Window
from sets import Set

class Event():
    """
    This class contains flags and integer values used by the event system.
    
    It is not meant to be subclassed or instantiated.
    """
    BUTTON_LEFT = 1
    BUTTON_MIDDLE = 4
    BUTTON_RIGHT = 2
    ONBLUR = 4096
    ONCHANGE = 1024
    ONCLICK = 1
    ONDBLCLICK = 2
    ONERROR = 65536
    ONFOCUS = 2048
    ONKEYDOWN = 128
    ONKEYPRESS = 256
    ONKEYUP = 512
    ONLOAD = 32768
    ONLOSECAPTURE = 8192
    ONMOUSEDOWN = 4
    ONMOUSEMOVE = 64
    ONMOUSEOUT = 32
    ONMOUSEOVER = 16
    ONMOUSEUP = 8
    ONSCROLL = 16384
    FOCUSEVENTS = 6144
    KEYEVENTS = 896
    MOUSEEVENTS = 124


class FocusListener():

    def fireFocusEvent(self, listeners, sender, event):
        type = DOM.eventGetType(event)
        if type == 'focus':
            for listener in listeners:
                listener.onFocus(sender)

        elif type == 'blur':
            for listener in listeners:
                listener.onLostFocus(sender)


class KeyboardListener():
    KEY_ALT = 18
    KEY_BACKSPACE = 8
    KEY_CTRL = 17
    KEY_DELETE = 46
    KEY_DOWN = 40
    KEY_END = 35
    KEY_ENTER = 13
    KEY_ESCAPE = 27
    KEY_HOME = 36
    KEY_LEFT = 37
    KEY_PAGEDOWN = 34
    KEY_PAGEUP = 33
    KEY_RIGHT = 39
    KEY_SHIFT = 16
    KEY_TAB = 9
    KEY_UP = 38
    MODIFIER_ALT = 4
    MODIFIER_CTRL = 2
    MODIFIER_SHIFT = 1

    def getKeyboardModifiers(self, event):
        shift = 0
        ctrl = 0
        alt = 0
        if DOM.eventGetShiftKey(event):
            shift = KeyboardListener.MODIFIER_SHIFT
        if DOM.eventGetCtrlKey(event):
            ctrl = KeyboardListener.MODIFIER_CTRL
        if DOM.eventGetAltKey(event):
            alt = KeyboardListener.MODIFIER_ALT
        return shift | ctrl | alt

    def fireKeyboardEvent(self, listeners, sender, event):
        modifiers = KeyboardListener().getKeyboardModifiers(event)
        type = DOM.eventGetType(event)
        if type == 'keydown':
            for listener in listeners:
                listener.onKeyDown(sender, DOM.eventGetKeyCode(event), modifiers)

        elif type == 'keyup':
            for listener in listeners:
                listener.onKeyUp(sender, DOM.eventGetKeyCode(event), modifiers)

        elif type == 'keypress':
            for listener in listeners:
                listener.onKeyPress(sender, DOM.eventGetKeyCode(event), modifiers)


class MouseListener():

    def fireMouseEvent(self, listeners, sender, event):
        x = DOM.eventGetClientX(event) - DOM.getAbsoluteLeft(sender.getElement())
        y = DOM.eventGetClientY(event) - DOM.getAbsoluteTop(sender.getElement())
        type = DOM.eventGetType(event)
        if type == 'mousedown':
            for listener in listeners:
                listener.onMouseDown(sender, x, y)

        elif type == 'mouseup':
            for listener in listeners:
                listener.onMouseUp(sender, x, y)

        elif type == 'mousemove':
            for listener in listeners:
                listener.onMouseMove(sender, x, y)

        elif type == 'mouseover':
            from_element = DOM.eventGetFromElement(event)
            if not DOM.isOrHasChild(sender.getElement(), from_element):
                for listener in listeners:
                    listener.onMouseEnter(sender)

        elif type == 'mouseout':
            to_element = DOM.eventGetToElement(event)
            if not DOM.isOrHasChild(sender.getElement(), to_element):
                for listener in listeners:
                    listener.onMouseLeave(sender)


class UIObject():
    """ UIObject is the base class for user interface objects.
    """

    def getAbsoluteLeft(self):
        return DOM.getAbsoluteLeft(self.getElement())

    def getAbsoluteTop(self):
        return DOM.getAbsoluteTop(self.getElement())

    def getElement(self):
        """Get the DOM element associated with the UIObject, if any"""
        return self.element

    def getOffsetHeight(self):
        return DOM.getIntAttribute(self.element, 'offsetHeight')

    def getOffsetWidth(self):
        return DOM.getIntAttribute(self.element, 'offsetWidth')

    def getStyleName(self):
        return DOM.getAttribute(self.element, 'className')

    def getTitle(self):
        return DOM.getAttribute(self.element, 'title')

    def setElement(self, element):
        """Set the DOM element associated with the UIObject."""
        self.element = element

    def setHeight(self, height):
        """Set the height of the element associated with this UIObject.  The
           value should be given as a CSS value, such as 100px, 30%, or 50pi"""
        DOM.setStyleAttribute(self.element, 'height', height)

    def setPixelSize(self, width, height):
        """Set the width and height of the element associated with this UIObject
           in pixels.  Width and height should be numbers."""
        if width >= 0:
            self.setWidth(width + 'px')
        if height >= 0:
            self.setHeight(height + 'px')

    def setSize(self, width, height):
        """Set the width and height of the element associated with this UIObject.  The
           values should be given as a CSS value, such as 100px, 30%, or 50pi"""
        self.setWidth(width)
        self.setHeight(height)

    def addStyleName(self, style):
        """Append a style to the element associated with this UIObject.  This is
        a CSS class name.  It will be added after any already-assigned CSS class for
        the element."""
        self.setStyleName(self.element, style, True)

    def removeStyleName(self, style):
        """Remove a style from the element associated with this UIObject.  This is
        a CSS class name."""
        self.setStyleName(self.element, style, False)

    def setStyleName(self, element, style=None, add=True):
        """When called with a single argument, this replaces all the CSS classes
        associated with this UIObject's element with the given parameter.  Otherwise,
        this is assumed to be a worker function for addStyleName and removeStyleName."""
        if style == None:
            style = element
            DOM.setAttribute(self.element, 'className', style)
            return
        oldStyle = DOM.getAttribute(element, 'className')
        if oldStyle == None:
            oldStyle = ''
        idx = oldStyle.find(style)
        lastPos = len(oldStyle)
        while idx != -1:
            if idx == 0 or oldStyle[(idx - 1)] == ' ':
                last = idx + len(style)
                if last == lastPos or last < lastPos and oldStyle[last] == ' ':
                    break
            idx = oldStyle.find(style, idx + 1)

        if add:
            if idx == -1:
                DOM.setAttribute(element, 'className', oldStyle + ' ' + style)
        elif idx != -1:
            begin = oldStyle[:idx]
            end = oldStyle[idx + len(style):]
            DOM.setAttribute(element, 'className', begin + end)
        return

    def setTitle(self, title):
        DOM.setAttribute(self.element, 'title', title)

    def setzIndex(self, index):
        DOM.setIntStyleAttribute(self.element, 'zIndex', index)

    def setWidth(self, width):
        """Set the width of the element associated with this UIObject.  The
           value should be given as a CSS value, such as 100px, 30%, or 50pi"""
        DOM.setStyleAttribute(self.element, 'width', width)

    def sinkEvents(self, eventBitsToAdd):
        """Request that the given events be delivered to the event handler for this
        element.  The event bits passed are added (using inclusive OR) to the events
        already "sunk" for the element associated with the UIObject.  The event bits
        are a combination of values from class L{Event}."""
        if self.element:
            DOM.sinkEvents(self.getElement(), eventBitsToAdd | DOM.getEventsSunk(self.getElement()))

    def isVisible(self, element=None):
        """Determine whether this element is currently visible, by checking the CSS
        property 'display'"""
        if not element:
            element = self.element
        try:
            return element.props.style.display != 'none'
        except AttributeError:
            return True

    def setVisible(self, element, visible=None):
        """Set whether this element is visible or not.  If a single parameter is
        given, the self.element is used.  This modifies the CSS property 'display',
        which means that an invisible element not only is not drawn, but doesn't
        occupy any space on the page."""
        if visible == None:
            visible = element
            element = self.element
        if visible:
            DOM.setStyleAttribute(element, 'display', '')
        else:
            DOM.setStyleAttribute(element, 'display', 'none')
        return

    def unsinkEvents(self, eventBitsToRemove):
        """
            Reverse the operation of sinkEvents.  See L{UIObject.sinkEvents}.
        """
        DOM.sinkEvents(self.getElement(), ~eventBitsToRemove & DOM.getEventsSunk(self.getElement()))


class Widget(UIObject):
    """
        Base class for most of the UI classes.  This class provides basic services
        used by any Widget, including management of parents and adding/removing the
        event handler association with the DOM.
    """

    def __init__(self):
        self.attached = False
        self.parent = None
        self.layoutData = None
        return

    def getLayoutData(self):
        return self.layoutData

    def getParent(self):
        """Widgets are kept in a hierarchy, and widgets that have been added to a panel
        will have a parent widget that contains them.  This retrieves the containing
        widget for this widget."""
        return self.parent

    def isAttached(self):
        """Return whether or not this widget has been attached to the document."""
        return self.attached

    def onBrowserEvent(self, event):
        pass

    def onLoad(self, sender):
        pass

    def onAttach(self):
        """Called when this widget has an element, and that element is on the document's
        DOM tree, and we have a parent widget."""
        if self.attached:
            return
        self.attached = True
        DOM.setEventListener(self.getElement(), self)
        if self.onLoad.func_code.co_argcount == 2:
            self.onLoad(self)
        else:
            self.onLoad()

    def onDetach(self):
        """Called when this widget is being removed from the DOM tree of the document."""
        if not self.attached:
            return
        self.attached = False
        DOM.setEventListener(self.getElement(), None)
        return

    def setLayoutData(self, layoutData):
        self.layoutData = layoutData

    def setParent(self, parent):
        """Update the parent attribute.  If the parent is currently attached to the DOM this
        assumes we are being attached also and calls onAttach()."""
        self.parent = parent
        if parent == None:
            self.onDetach()
        elif parent.attached:
            self.onAttach()
        return

    def removeFromParent(self):
        """Remove ourself from our parent.  The parent widget will call setParent(None) on
        us automatically"""
        if hasattr(self.parent, 'remove'):
            self.parent.remove(self)

    def getID(self):
        """Get the id attribute of the associated DOM element."""
        return DOM.getAttribute(self.getElement(), 'id')

    def setID(self, id):
        """Set the id attribute of the associated DOM element."""
        DOM.setAttribute(self.getElement(), 'id', id)


class FocusWidget(Widget):
    """ FocusWidget is the base widget for objects which take user-input,
        such as Buttons, ListBoxes and Text input widgets.  It is only
        necessary to instantiate from this class if you intend to make
        your own custom input widget.
    """

    def __init__(self, element):
        Widget.__init__(self)
        self.clickListeners = []
        self.focusListeners = []
        self.keyboardListeners = []
        self.setElement(element)
        self.sinkEvents(Event.ONCLICK | Event.FOCUSEVENTS | Event.KEYEVENTS)

    def addClickListener(self, listener):
        self.clickListeners.append(listener)

    def addFocusListener(self, listener):
        self.focusListeners.append(listener)

    def addKeyboardListener(self, listener):
        self.keyboardListeners.append(listener)

    def getTabIndex(self):
        return Focus.getTabIndex(self, self.getElement())

    def isEnabled(self):
        return not DOM.getBooleanAttribute(self.getElement(), 'disabled')

    def onBrowserEvent(self, event):
        type = DOM.eventGetType(event)
        if type == 'click':
            for listener in self.clickListeners:
                if hasattr(listener, 'onClick'):
                    if listener.onClick.func_code.co_argcount == 2:
                        listener.onClick(self)
                    else:
                        listener.onClick(self, event)
                elif listener.func_code.co_argcount == 1:
                    listener(self)
                else:
                    listener(self, event)

        if type == 'blur' or type == 'focus':
            FocusListener().fireFocusEvent(self.focusListeners, self, event)
        if type == 'keydown' or type == 'keypress' or type == 'keyup':
            KeyboardListener().fireKeyboardEvent(self.keyboardListeners, self, event)

    def removeClickListener(self, listener):
        self.clickListeners.remove(listener)

    def removeFocusListener(self, listener):
        self.focusListeners.remove(listener)

    def removeKeyboardListener(self, listener):
        self.keyboardListeners.remove(listener)

    def setAccessKey(self, key):
        DOM.setAttribute(self.getElement(), 'accessKey', '' + key)

    def setEnabled(self, enabled):
        DOM.setBooleanAttribute(self.getElement(), 'disabled', not enabled)

    def setFocus(self, focused):
        if focused:
            Focus().focus(self.getElement())
        else:
            Focus().blur(self.getElement())

    def setTabIndex(self, index):
        Focus().setTabIndex(self.getElement(), index)


class ButtonBase(FocusWidget):
    """ ButtonBase is the base object for button-style objects, such as
        RadioButton, CheckBox and Button.  It is only necessary to
        instantiate from ButtonBase if you intend to create your own
        clickeable Widget
   """

    def __init__(self, element):
        FocusWidget.__init__(self, element)

    def getHTML(self):
        return DOM.getInnerHTML(self.getElement())

    def getText(self):
        return DOM.getInnerText(self.getElement())

    def setHTML(self, html):
        DOM.setInnerHTML(self.getElement(), html)

    def setText(self, text):
        DOM.setInnerText(self.getElement(), text)


class Button(ButtonBase):
    """ Button is a clickable button.
    """

    def __init__(self, html=None, listener=None):
        """
        Create a new button widget.
        
        @param html: Html content (e.g. the button label); see setHTML()
        @param listener: A new click listener; see addClickListener()
        
        """
        ButtonBase.__init__(self, DOM.createButton())
        self.adjustType(self.getElement())
        self.setStyleName('gwt-Button')
        if html:
            self.setHTML(html)
        if listener:
            self.addClickListener(listener)

    def adjustType(self, button):
        if button.props.type == 'submit':
            try:
                DOM.setAttribute(button, 'type', 'button')
            except:
                pass

    def click(self):
        """
        Simulate a button click.
        """
        self.getElement().click()


CheckBoxUnique = 0

class CheckBox(ButtonBase):
    """ CheckBox is an input widget which can be checked or unchecked
    """

    def __init__(self, label=None, asHTML=False):
        """
        Create a new checkbox widget.
        
        @param label: Text content to be associated with the checkbox
                      (e.g. the checkbox label); see setHTML() and setText()
        @param asHTML: the label is HTML rather than plain text
        
        """
        self.initElement(DOM.createInputCheck())
        self.setStyleName('gwt-CheckBox')
        if label:
            if asHTML:
                self.setHTML(label)
            else:
                self.setText(label)

    def initElement(self, element):
        ButtonBase.__init__(self, DOM.createSpan())
        self.inputElem = element
        self.labelElem = DOM.createLabel()
        self.unsinkEvents(Event.FOCUSEVENTS | Event.ONCLICK)
        DOM.sinkEvents(self.inputElem, Event.FOCUSEVENTS | Event.ONCLICK | DOM.getEventsSunk(self.inputElem))
        DOM.appendChild(self.getElement(), self.inputElem)
        DOM.appendChild(self.getElement(), self.labelElem)
        uid = 'check%d' % self.getUniqueID()
        DOM.setAttribute(self.inputElem, 'id', uid)
        DOM.setAttribute(self.labelElem, 'htmlFor', uid)

    def getUniqueID(self):
        global CheckBoxUnique
        CheckBoxUnique += 1
        return CheckBoxUnique

    def getHTML(self):
        return DOM.getInnerHTML(self.labelElem)

    def getName(self):
        return DOM.getAttribute(self.inputElem, 'name')

    def getText(self):
        return DOM.getInnerText(self.labelElem)

    def setChecked(self, checked):
        DOM.setBooleanAttribute(self.inputElem, 'checked', checked)
        DOM.setBooleanAttribute(self.inputElem, 'defaultChecked', checked)

    def isChecked(self):
        if self.attached:
            propName = 'checked'
        else:
            propName = 'defaultChecked'
        return DOM.getBooleanAttribute(self.inputElem, propName)

    def isEnabled(self):
        return not DOM.getBooleanAttribute(self.inputElem, 'disabled')

    def setEnabled(self, enabled):
        DOM.setBooleanAttribute(self.inputElem, 'disabled', not enabled)

    def setFocus(self, focused):
        if focused:
            Focus().focus(self, self.inputElem)
        else:
            Focus().blur(self, self.inputElem)

    def setHTML(self, html):
        DOM.setInnerHTML(self.labelElem, html)

    def setName(self, name):
        DOM.setAttribute(self.inputElem, 'name', name)

    def setTabIndex(self, index):
        Focus.setTabIndex(self, self.inputElem, index)

    def setText(self, text):
        DOM.setInnerText(self.labelElem, text)

    def onDetach(self):
        self.setChecked(self.isChecked())
        ButtonBase.onDetach(self)


class RadioButton(CheckBox):
    """ RadioButton is a form of checkbox, which must be grouped with
        other RadioButtons.  Only one of the RadioButtons in the group
        can be checked at any one time.
    """

    def __init__(self, group, label=None, asHTML=False):
        """
        Create a new checkbox widget.
        
        @param group: A string naming the group that the RadioButton
                      is to be associated with.  All RadioButtons with
                      the same group string name will be in the same
                      mutually-exclusive group.
        @param label: Text content to be associated with the RadioButton
                      (e.g. the RadioButton label); see setHTML() and setText()
        @param asHTML: the label is HTML rather than plain text
        """
        self.initElement(DOM.createInputRadio(group))
        self.setStyleName('gwt-RadioButton')
        if label:
            if asHTML:
                self.setHTML(label)
            else:
                self.setText(label)


class Composite(Widget):

    def __init__(self):
        Widget.__init__(self)
        self.widget = None
        return

    def initWidget(self, widget):
        if self.widget != None:
            return
        widget.removeFromParent()
        self.setElement(widget.getElement())
        self.widget = widget
        widget.setParent(self)
        return

    def onAttach(self):
        Widget.onAttach(self)
        self.widget.onAttach()

    def onDetach(self):
        Widget.onDetach(self)
        self.widget.onDetach()

    def setWidget(self, widget):
        self.initWidget(widget)


class Panel(Widget):
    """ The basic 'Panel' widget class which can contain other widgets.
        Panel is a base class from which other Panel classes are derived:
        you will not need to instantiate a Panel class, but if you create
        your own Panel widgets, derive them from this class.
    """

    def __init__(self):
        Widget.__init__(self)
        self.children = []

    def add(self):
        console.error('This panel does not support no-arg add()')

    def clear(self):
        for child in list(self):
            self.remote(child)

    def disown(self, widget):
        if widget.getParent() != self:
            console.error('widget %o is not a child of this panel %o', widget, self)
        else:
            element = widget.getElement()
            widget.setParent(None)
            parentElement = DOM.getParent(element)
            if parentElement:
                DOM.removeChild(parentElement, element)
        return

    def adopt(self, widget, container):
        widget.removeFromParent()
        if container:
            DOM.appendChild(container, widget.getElement())
        widget.setParent(self)

    def remove(self, widget):
        pass

    def onAttach(self):
        Widget.onAttach(self)
        for child in self:
            child.onAttach()

    def onDetach(self):
        Widget.onDetach(self)
        for child in self:
            child.onDetach()

    def __iter__(self):
        return self.children.__iter__()


class CellFormatter():
    """ CellFormatter is a class for managing formatting of cells in
        various types of Panel classes, such as HTMLTable and Grid.
        These Panel classes typically use CellFormatter automatically
        on your behalf, although you can over-ride that to use your
        own CellFormatter class.
    """

    def __init__(self, outer):
        self.outer = outer

    def addStyleName(self, row, column, styleName):
        self.outer.prepareCell(row, column)
        self.outer.setStyleName(self.getElement(row, column), styleName, True)

    def getElement(self, row, column):
        self.outer.checkCellBounds(row, column)
        return DOM.getChild(self.outer.rowFormatter.getRow(self.outer.bodyElem, row), column)

    def getStyleName(self, row, column):
        return DOM.getAttribute(self.getElement(row, column), 'className')

    def isVisible(self, row, column):
        element = self.getElement(row, column)
        return self.outer.isVisible(element)

    def removeStyleName(self, row, column, styleName):
        self.checkCellBounds(row, column)
        self.outer.setStyleName(self.getElement(row, column), styleName, False)

    def setAlignment(self, row, column, hAlign, vAlign):
        self.setHorizontalAlignment(row, column, hAlign)
        self.setVerticalAlignment(row, column, vAlign)

    def setHeight(self, row, column, height):
        self.outer.prepareCell(row, column)
        element = self.getCellElement(self.outer.bodyElem, row, column)
        DOM.setStyleAttribute(element, 'height', height)

    def setHorizontalAlignment(self, row, column, align):
        self.outer.prepareCell(row, column)
        element = self.getCellElement(self.outer.bodyElem, row, column)
        DOM.setAttribute(element, 'align', align)

    def setStyleName(self, row, column, styleName):
        self.outer.prepareCell(row, column)
        self.setAttr(row, column, 'className', styleName)

    def setVerticalAlignment(self, row, column, align):
        self.outer.prepareCell(row, column)
        DOM.setStyleAttribute(self.getCellElement(self.outer.bodyElem, row, column), 'verticalAlign', align)

    def setVisible(self, row, column, visible):
        element = self.ensureElement(row, column)
        self.outer.setVisible(element, visible)

    def setWidth(self, row, column, width):
        self.outer.prepareCell(row, column)
        DOM.setStyleAttribute(self.getCellElement(self.outer.bodyElem, row, column), 'width', width)

    def setWordWrap(self, row, column, wrap):
        self.outer.prepareCell(row, column)
        if wrap:
            wrap_str = ''
        else:
            wrap_str = 'nowrap'
        DOM.setStyleAttribute(self.getElement(row, column), 'whiteSpace', wrap_str)

    def getCellElement(self, table, row, col):
        length = table.props.rows.props.length
        if row >= length:
            return
        cols = table.props.rows.item(row).props.cells
        length = cols.props.length
        if col >= length:
            return
        item = cols.item(col)
        return item

    def getRawElement(self, row, column):
        return self.getCellElement(self.outer.bodyElem, row, column)

    def ensureElement(self, row, column):
        self.outer.prepareCell(row, column)
        return DOM.getChild(self.outer.rowFormatter.ensureElement(row), column)

    def getAttr(self, row, column, attr):
        elem = self.getElement(row, column)
        return DOM.getAttribute(elem, attr)

    def setAttr(self, row, column, attrName, value):
        elem = self.getElement(row, column)
        DOM.setAttribute(elem, attrName, value)


class RowFormatter():
    """ RowFormatter is a class for managing formatting of rows in
        various types of Panel classes, such as HTMLTable and Grid.
        These Panel classes typically use RowFormatter automatically
        on your behalf, although you can over-ride that to use your
        own RowFormatter class.
    """

    def __init__(self, outer):
        self.outer = outer

    def addStyleName(self, row, styleName):
        self.outer.setStyleName(self.ensureElement(row), styleName, True)

    def getElement(self, row):
        self.outer.checkRowBounds(row)
        return self.getRow(self.outer.bodyElem, row)

    def getStyleName(self, row):
        return DOM.getAttribute(self.getElement(row), 'className')

    def isVisible(self, row):
        element = self.getElement(row)
        return self.outer.isVisible(element)

    def removeStyleName(self, row, styleName):
        self.outer.setStyleName(self.getElement(row), styleName, False)

    def setStyleName(self, row, styleName):
        elem = self.ensureElement(row)
        DOM.setAttribute(elem, 'className', styleName)

    def setVerticalAlign(self, row, align):
        DOM.setStyleAttribute(self.ensureElement(row), 'verticalAlign', align)

    def setVisible(self, row, visible):
        element = self.ensureElement(row)
        self.outer.setVisible(element, visible)

    def ensureElement(self, row):
        self.outer.prepareRow(row)
        return self.getRow(self.outer.bodyElem, row)

    def getRow(self, element, row):
        return element.props.rows.item(row)

    def setAttr(self, row, attrName, value):
        element = self.ensureElement(row)
        DOM.setAttribute(element, attrName, value)


class HTMLTable(Panel):
    """ HTMLTable is a panel with functionality of that of an HTML Table.
        HTMLTable is the Base for both the Grid and FlexTable classes, which
        provide additional functionality.  The key functions for adding
        widgets to HTMLTable are setHTML, setText and setWidget, which
        add HTML, Text or Widgets at the specified row and column,
        respectively.
    """

    def __init__(self):
        Panel.__init__(self)
        self.cellFormatter = CellFormatter(self)
        self.rowFormatter = RowFormatter(self)
        self.tableListeners = []
        self.widgetMap = {}
        self.tableElem = DOM.createTable()
        self.bodyElem = DOM.createTBody()
        DOM.appendChild(self.tableElem, self.bodyElem)
        self.setElement(self.tableElem)
        self.sinkEvents(Event.ONCLICK)

    def addTableListener(self, listener):
        self.tableListeners.append(listener)

    def clear(self):
        for row in range(self.getRowCount()):
            for col in range(self.getCellCount(row)):
                child = self.getWidget(row, col)
                if child != None:
                    self.removeWidget(child)

        return

    def clearCell(self, row, column):
        td = self.cellFormatter.getElement(row, column)
        return self.internalClearCell(td)

    def getCellCount(self, row):
        return 0

    def getCellFormatter(self):
        return self.cellFormatter

    def getCellPadding(self):
        return DOM.getIntAttribute(self.tableElem, 'cell-padding')

    def getCellSpacing(self):
        return DOM.getIntAttribute(self.tableElem, 'cell-spacing')

    def getHTML(self, row, column):
        element = self.cellFormatter.getElement(row, column)
        return DOM.getInnerHTML(element)

    def getRowCount(self):
        return 0

    def getRowFormatter(self):
        return self.rowFormatter

    def getText(self, row, column):
        self.checkCellBounds(row, column)
        element = self.cellFormatter.getElement(row, column)
        return DOM.getInnerText(element)

    def getWidget(self, row, column=None):
        if column == None:
            key = self.computeKeyForElement(row)
        else:
            self.checkCellBounds(row, column)
            key = self.computeKey(row, column)
        if key == None:
            return
        return self.widgetMap.get(key)

    def isCellPresent(self, row, column):
        if row >= self.getRowCount() or row < 0:
            return False
        if column < 0 or column >= self.getCellCount(row):
            return False
        return True

    def __iter__(self):
        return self.widgetMap.itervalues()

    def onBrowserEvent(self, event):
        if DOM.eventGetType(event) == 'click':
            td = self.getEventTargetCell(event)
            if not td:
                return
            tr = DOM.getParent(td)
            body = DOM.getParent(tr)
            row = DOM.getChildIndex(body, tr)
            column = DOM.getChildIndex(tr, td)
            for listener in self.tableListeners:
                if listener.onCellClicked:
                    listener.onCellClicked(self, row, column)
                else:
                    listener(self)

    def remove(self, widget):
        if widget.getParent() != self:
            return False
        self.removeWidget(widget)
        return True

    def removeTableListener(self, listener):
        self.tableListeners.remove(listener)

    def setBorderWidth(self, width):
        DOM.setAttribute(self.tableElem, 'border', width)

    def setCellPadding(self, padding):
        DOM.setIntAttribute(self.tableElem, 'cell-padding', padding)

    def setCellSpacing(self, spacing):
        DOM.setIntAttribute(self.tableElem, 'cell-spacing', spacing)

    def setHTML(self, row, column, html):
        self.prepareCell(row, column)
        td = self.cleanCell(row, column)
        if html != None:
            DOM.setInnerHTML(td, html)
        return

    def setText(self, row, column, text):
        self.prepareCell(row, column)
        td = self.cleanCell(row, column)
        if text != None:
            DOM.setInnerText(td, text)
        return

    def setWidget(self, row, column, widget):
        self.prepareCell(row, column)
        if widget == None:
            return
        widget.removeFromParent()
        td = self.cleanCell(row, column)
        widget_hash = hash(widget)
        element = widget.getElement()
        print 'TODO - setAttribute __hash'
        element.hash = widget_hash
        DOM.setElemAttribute(element, 'hash', str(widget_hash))
        self.widgetMap[widget_hash] = widget
        self.adopt(widget, td)
        return

    def cleanCell(self, row, column):
        td = self.cellFormatter.getRawElement(row, column)
        self.internalClearCell(td)
        return td

    def computeKey(self, row, column):
        element = self.cellFormatter.getRawElement(row, column)
        child = DOM.getFirstChild(element)
        if child == None:
            return
        return self.computeKeyForElement(child)

    def computeKeyForElement(self, widgetElement):
        try:
            return DOM.getElemAttribute(widgetElement, 'hash')
        except TypeError:
            return

        return widgetElement.hash

    def removeWidget(self, widget):
        self.disown(widget)
        wmap = self.computeKeyForElement(widget.getElement())
        if self.widgetMap.has_key(wmap):
            del self.widgetMap[wmap]
        return True

    def checkCellBounds(self, row, column):
        self.checkRowBounds(row)
        cellSize = self.getCellCount(row)

    def checkRowBounds(self, row):
        rowSize = self.getRowCount()

    def createCell(self):
        return DOM.createTD()

    def getBodyElement(self):
        return self.bodyElem

    def getDOMCellCount(self, element, row=None):
        if row == None:
            return self.getDOMCellCountImpl(self.bodyElem, element)
        return self.getDOMCellCountImpl(element, row)

    def getDOMCellCountImpl(self, element, row):
        return element.props.rows.item(row).props.cells.props.length

    def getDOMRowCount(self, element=None):
        if element == None:
            element = self.bodyElem
        return self.getDOMRowCountImpl(element)

    def getDOMRowCountImpl(self, element):
        return element.props.rows.props.length

    def getEventTargetCell(self, event):
        td = DOM.eventGetTarget(event)
        while td != None:
            if DOM.getAttribute(td, 'tagName').lower() == 'td':
                tr = DOM.getParent(td)
                body = DOM.getParent(tr)
                if DOM.compare(body, self.bodyElem):
                    return td
            if DOM.compare(td, self.bodyElem):
                return
            td = DOM.getParent(td)

        return

    def insertCell(self, row, column):
        tr = self.rowFormatter.getRow(self.bodyElem, row)
        td = self.createCell()
        DOM.insertChild(tr, td, column)

    def insertCells(self, row, column, count):
        tr = self.rowFormatter.getRow(self.bodyElem, row)
        for i in range(column, column + count):
            td = self.createCell()
            DOM.insertChild(tr, td, i)

    def insertRow(self, beforeRow):
        if beforeRow != self.getRowCount():
            self.checkRowBounds(beforeRow)
        tr = DOM.createTR()
        DOM.insertChild(self.bodyElem, tr, beforeRow)
        return beforeRow

    def internalClearCell(self, td):
        maybeChild = DOM.getFirstChild(td)
        widget = None
        if maybeChild != None:
            widget = self.getWidget(maybeChild)
        if widget != None:
            self.removeWidget(widget)
            return True
        DOM.setInnerHTML(td, '')
        return False

    def prepareCell(self, row, column):
        pass

    def prepareRow(self, row):
        pass

    def removeCell(self, row, column):
        self.checkCellBounds(row, column)
        td = self.cleanCell(row, column)
        tr = self.rowFormatter.getRow(self.bodyElem, row)
        DOM.removeChild(tr, td)

    def removeRow(self, row):
        for column in range(self.getCellCount(row)):
            self.cleanCell(row, column)

        DOM.removeChild(self.bodyElem, self.rowFormatter.getRow(self.bodyElem, row))

    def setCellFormatter(self, cellFormatter):
        self.cellFormatter = cellFormatter

    def setRowFormatter(self, rowFormatter):
        self.rowFormatter = rowFormatter


class Grid(HTMLTable):
    """ The Grid Widget is a type of HTMLTable where all of the cells
        are pre-loaded at the very least with some blank content.
    """

    def __init__(self, rows=0, columns=0):
        HTMLTable.__init__(self)
        self.cellFormatter = CellFormatter(self)
        self.rowFormatter = RowFormatter(self)
        self.numColumns = 0
        self.numRows = 0
        if rows > 0 or columns > 0:
            self.resize(rows, columns)

    def resize(self, rows, columns):
        self.resizeColumns(columns)
        self.resizeRows(rows)

    def resizeColumns(self, columns):
        if self.numColumns == columns:
            return
        if self.numColumns > columns:
            for i in range(0, self.numRows):
                for j in range(self.numColumns - 1, columns - 1, -1):
                    self.removeCell(i, j)

        for i in range(self.numRows):
            for j in range(self.numColumns, columns):
                self.insertCell(i, j)

        self.numColumns = columns

    def resizeRows(self, rows):
        if self.numRows == rows:
            return
        if self.numRows < rows:
            self.addRows(self.getBodyElement(), rows - self.numRows, self.numColumns)
            self.numRows = rows
        while self.numRows > rows:
            self.numRows -= 1
            self.removeRow(self.numRows)

    def createCell(self):
        td = HTMLTable.createCell(self)
        DOM.setInnerHTML(td, '&nbsp;')
        return td

    def clearCell(self, row, column):
        td = self.cellFormatter.getElement(row, column)
        b = HTMLTable.internalClearCell(self, td)
        DOM.setInnerHTML(td, '&nbsp;')
        return b

    def prepareCell(self, row, column):
        pass

    def prepareRow(self, row):
        pass

    def getCellCount(self, row):
        return self.numColumns

    def getColumnCount(self):
        return self.numColumns

    def getRowCount(self):
        return self.numRows

    def addRows(self, table, numRows, columns):
        td = DOM.createElement('td')
        td.props.inner_html = '&nbsp;'
        row = DOM.createElement('tr')
        for cellNum in range(columns):
            cell = td.clone_node(True)
            row.append_child(cell)

        table.append_child(row)
        for rowNum in range(numRows):
            table.append_child(row.clone_node(True))


class FlexCellFormatter(CellFormatter):

    def __init__(self, outer):
        CellFormatter.__init__(self, outer)

    def getColSpan(self, row, column):
        return DOM.getIntAttribute(self.getElement(row, column), 'colSpan')

    def getRowSpan(self, row, column):
        return DOM.getIntAttribute(self.getElement(row, column), 'rowSpan')

    def setColSpan(self, row, column, colSpan):
        DOM.setIntAttribute(self.ensureElement(row, column), 'colSpan', colSpan)

    def setRowSpan(self, row, column, rowSpan):
        DOM.setIntAttribute(self.ensureElement(row, column), 'rowSpan', rowSpan)


class FlexTable(HTMLTable):
    """ FlexTable can create cells on demand. It can be jagged
        (that is, each row can contain a different number of cells)
        and individual cells can be set to span multiple rows or columns.
    """

    def __init__(self):
        HTMLTable.__init__(self)
        self.cellFormatter = FlexCellFormatter(self)
        self.rowFormatter = RowFormatter(self)

    def addCell(self, row):
        self.insertCell(row, self.getCellCount(row))

    def getCellCount(self, row):
        self.checkRowBounds(row)
        return self.getDOMCellCount(self.getBodyElement(), row)

    def getFlexCellFormatter(self):
        return self.getCellFormatter()

    def getRowCount(self):
        return self.getDOMRowCount()

    def removeCells(self, row, column, num):
        for i in range(num):
            self.removeCell(row, column)

    def prepareCell(self, row, column):
        self.prepareRow(row)
        cellCount = self.getCellCount(row)
        required = column + 1 - cellCount
        if required > 0:
            self.addCells(self.getBodyElement(), row, required)

    def prepareRow(self, row):
        rowCount = self.getRowCount()
        for i in range(rowCount, row + 1):
            self.insertRow(i)

    def addCells(self, table, row, num):
        rowElem = table.props.rows.item(row)
        for i in range(num):
            cell = doc().create_element('td')
            rowElem.append_child(cell)


class ComplexPanel(Panel):
    """
        Superclass for widgets with multiple children.
    """

    def __init__(self):
        Panel.__init__(self)
        self.children = []

    def add(self, widget, container):
        self.insert(widget, container, len(self.children))

    def getChildren(self):
        return self.children

    def insert(self, widget, container, beforeIndex):
        if widget.getParent() == self:
            return
        self.adopt(widget, container)
        self.children.insert(beforeIndex, widget)

    def remove(self, widget):
        if widget not in self.children:
            return False
        self.disown(widget)
        self.children.remove(widget)
        return True


class AbsolutePanel(ComplexPanel):
    """ An absolute panel positions all of its children absolutely,
        allowing them to overlap.

        Note that this panel will not automatically resize itself to
        allow enough room for its absolutely-positioned children.
        It must be explicitly sized in order to make room for them.

        Once a widget has been added to an absolute panel, the panel
        effectively "owns" the positioning of the widget. Any existing
        positioning attributes on the widget may be modified by the panel. 
    """

    def __init__(self):
        ComplexPanel.__init__(self)
        self.setElement(DOM.createDiv())
        DOM.setStyleAttribute(self.getElement(), 'position', 'relative')
        DOM.setStyleAttribute(self.getElement(), 'overflow', 'hidden')

    def add(self, widget, left=None, top=None):
        ComplexPanel.add(self, widget, self.getElement())
        if left != None:
            self.setWidgetPosition(widget, left, top)
        return

    def setWidgetPosition(self, widget, left, top):
        self.checkWidgetParent(widget)
        h = widget.getElement()
        if left == -1 and top == -1:
            DOM.setStyleAttribute(h, 'left', '')
            DOM.setStyleAttribute(h, 'top', '')
            DOM.setStyleAttribute(h, 'position', 'static')
        else:
            DOM.setStyleAttribute(h, 'position', 'absolute')
            DOM.setStyleAttribute(h, 'left', '%dpx' % left)
            DOM.setStyleAttribute(h, 'top', '%dpx' % top)

    def getWidgetLeft(self, widget):
        self.checkWidgetParent(widget)
        return DOM.getIntAttribute(widget.getElement(), 'offsetLeft')

    def getWidgetTop(self, widget):
        self.checkWidgetParent(widget)
        return DOM.getIntAttribute(widget.getElement(), 'offsetTop')

    def checkWidgetParent(self, widget):
        if widget.getParent() != self:
            console.error('Widget must be a child of this panel.')


class Label(Widget):
    """ A widget that contains arbitrary text, *not* interpreted as HTML.
    """

    def __init__(self, text=None, wordWrap=True):
        Widget.__init__(self)
        self.horzAlign = ''
        self.clickListeners = []
        self.mouseListeners = []
        self.setElement(DOM.createDiv())
        self.sinkEvents(Event.ONCLICK | Event.MOUSEEVENTS)
        self.setStyleName('gwt-Label')
        if text:
            self.setText(text)
        self.setWordWrap(wordWrap)

    def addClickListener(self, listener):
        self.clickListeners.append(listener)

    def addMouseListener(self, listener):
        self.mouseListeners.append(listener)

    def getHorizontalAlignment(self):
        return self.horzAlign

    def getText(self):
        return DOM.getInnerText(self.getElement())

    def getWordWrap(self):
        return not DOM.getStyleAttribute(self.getElement(), 'whiteSpace') == 'nowrap'

    def onBrowserEvent(self, event):
        type = DOM.eventGetType(event)
        if type == 'click':
            for listener in self.clickListeners:
                if hasattr(listener, 'onClick'):
                    if listener.onClick.func_code.co_argcount == 2:
                        listener.onClick(self)
                    else:
                        listener.onClick(self, event)
                elif listener.func_code.co_argcount == 1:
                    listener(self)
                else:
                    listener(self, event)

        if type == 'mousedown' or type == 'mouseup' or type == 'mousemove' or type == 'mouseover' or type == 'mouseout':
            MouseListener().fireMouseEvent(self.mouseListeners, self, event)

    def removeClickListener(self, listener):
        self.clickListeners.remove(listener)

    def removeMouseListener(self, listener):
        self.mouseListeners.remove(listener)

    def setHorizontalAlignment(self, align):
        self.horzAlign = align
        DOM.setStyleAttribute(self.getElement(), 'textAlign', align)

    def setText(self, text):
        DOM.setInnerText(self.getElement(), text)

    def setWordWrap(self, wrap):
        if wrap:
            style = 'normal'
        else:
            style = 'nowrap'
        DOM.setStyleAttribute(self.getElement(), 'whiteSpace', style)


class HTML(Label):
    """ A widget that can contain arbitrary HTML.

        If you only need a simple label (text, but not HTML), then the
        Label widget is more appropriate, as it disallows the use of HTML,
        which can lead to potential security issues if not used properly. 
    """

    def __init__(self, html=None, wordWrap=True):
        Label.__init__(self)
        self.setElement(DOM.createDiv())
        self.sinkEvents(Event.ONCLICK | Event.MOUSEEVENTS)
        self.setStyleName('gwt-HTML')
        if html:
            self.setHTML(html)
        self.setWordWrap(wordWrap)

    def getHTML(self):
        return DOM.getInnerHTML(self.getElement())

    def setHTML(self, html):
        DOM.setInnerHTML(self.getElement(), html)


class HasHorizontalAlignment():
    ALIGN_LEFT = 'left'
    ALIGN_CENTER = 'center'
    ALIGN_RIGHT = 'right'


class HasVerticalAlignment():
    ALIGN_TOP = 'top'
    ALIGN_MIDDLE = 'middle'
    ALIGN_BOTTOM = 'bottom'


class HasAlignment():
    ALIGN_BOTTOM = 'bottom'
    ALIGN_MIDDLE = 'middle'
    ALIGN_TOP = 'top'
    ALIGN_CENTER = 'center'
    ALIGN_LEFT = 'left'
    ALIGN_RIGHT = 'right'


class CellPanel(ComplexPanel):
    """ A panel whose child widgets are contained within the cells of a table.

        Each cell's size may be set independently.
        Each child widget can take up a subset of its cell
        and can be aligned within it.
    """

    def __init__(self):
        ComplexPanel.__init__(self)
        self.table = DOM.createTable()
        self.body = DOM.createTBody()
        DOM.appendChild(self.table, self.body)
        self.setElement(self.table)

    def getTable(self):
        return self.table

    def getBody(self):
        return self.body

    def getSpacing(self):
        return self.spacing

    def getWidgetTd(self, widget):
        if widget.getParent() != self:
            return
        return DOM.getParent(widget.getElement())

    def setBorderWidth(self, width):
        DOM.setAttribute(self.table, 'border', '' + width)

    def setCellHeight(self, widget, height):
        td = DOM.getParent(widget.getElement())
        DOM.setAttribute(td, 'height', height)

    def setCellHorizontalAlignment(self, widget, align):
        td = self.getWidgetTd(widget)
        if td != None:
            DOM.setAttribute(td, 'align', align)
        return

    def setCellVerticalAlignment(self, widget, align):
        td = self.getWidgetTd(widget)
        print 'vertical align', td, align
        if td != None:
            DOM.setStyleAttribute(td, 'verticalAlign', align)
        return

    def setCellWidth(self, widget, width):
        td = DOM.getParent(widget.getElement())
        DOM.setAttribute(td, 'width', width)

    def setSpacing(self, spacing):
        self.spacing = spacing
        DOM.setIntAttribute(self.table, 'cellSpacing', spacing)


class HorizontalPanel(CellPanel):
    """ A panel that lays all of its widgets out in a single horizontal column.
    """

    def __init__(self):
        CellPanel.__init__(self)
        self.horzAlign = HasHorizontalAlignment.ALIGN_LEFT
        self.vertAlign = HasVerticalAlignment.ALIGN_TOP
        self.tableRow = DOM.createTR()
        DOM.appendChild(self.getBody(), self.tableRow)
        DOM.setAttribute(self.getTable(), 'cellSpacing', '0')
        DOM.setAttribute(self.getTable(), 'cellPadding', '0')

    def add(self, widget):
        self.insert(widget, self.getWidgetCount())

    def getHorizontalAlignment(self):
        return self.horzAlign

    def getVerticalAlignment(self):
        return self.vertAlign

    def getWidget(self, index):
        return self.children[index]

    def getWidgetCount(self):
        return len(self.children)

    def getWidgetIndex(self, child):
        return self.children.index(child)

    def insert(self, widget, beforeIndex):
        widget.removeFromParent()
        td = DOM.createTD()
        DOM.insertChild(self.tableRow, td, beforeIndex)
        CellPanel.insert(self, widget, td, beforeIndex)
        self.setCellHorizontalAlignment(widget, self.horzAlign)
        self.setCellVerticalAlignment(widget, self.vertAlign)

    def remove(self, widget):
        if widget.getParent() != self:
            return False
        td = DOM.getParent(widget.getElement())
        DOM.removeChild(self.tableRow, td)
        CellPanel.remove(widget)
        return True

    def setHorizontalAlignment(self, align):
        self.horzAlign = align

    def setVerticalAlignment(self, align):
        self.vertAlign = align


class VerticalPanel(CellPanel):
    """ A panel that lays all of its widgets out in a single vertical column.
    """

    def __init__(self):
        CellPanel.__init__(self)
        self.horzAlign = HasHorizontalAlignment.ALIGN_LEFT
        self.vertAlign = HasVerticalAlignment.ALIGN_TOP
        DOM.setAttribute(self.getTable(), 'cellSpacing', '0')
        DOM.setAttribute(self.getTable(), 'cellPadding', '0')

    def add(self, widget):
        self.insert(widget, self.getWidgetCount())

    def getHorizontalAlignment(self):
        return self.horzAlign

    def getVerticalAlignment(self):
        return self.vertAlign

    def getWidget(self, index):
        return self.children[index]

    def getWidgetCount(self):
        return len(self.children)

    def getWidgetIndex(self, child):
        return self.children.index(child)

    def setWidget(self, index, widget):
        """Replace the widget at the given index with a new one"""
        existing = self.getWidget(index)
        if existing:
            self.remove(existing)
        self.insert(widget, index)

    def insert(self, widget, beforeIndex):
        widget.removeFromParent()
        tr = DOM.createTR()
        td = DOM.createTD()
        DOM.insertChild(self.getBody(), tr, beforeIndex)
        DOM.appendChild(tr, td)
        CellPanel.insert(self, widget, td, beforeIndex)
        self.setCellHorizontalAlignment(widget, self.horzAlign)
        self.setCellVerticalAlignment(widget, self.vertAlign)

    def remove(self, widget):
        if pyjslib.isNumber(widget):
            widget = self.getWidget(widget)
        if widget.getParent() != self:
            return False
        td = DOM.getParent(widget.getElement())
        tr = DOM.getParent(td)
        DOM.removeChild(self.getBody(), tr)
        CellPanel.remove(self, widget)
        return True

    def setHorizontalAlignment(self, align):
        self.horzAlign = align

    def setVerticalAlignment(self, align):
        self.vertAlign = align


class LayoutData():

    def __init__(self, direction):
        self.direction = direction
        self.hAlign = 'left'
        self.height = ''
        self.td = None
        self.vAlign = 'top'
        self.width = ''
        return


class DockPanel(CellPanel):
    """ A panel that lays its child widgets out "docked" at its outer edges,
        and allows its last widget to take up the remaining space in its center.
    """
    CENTER = 'center'
    EAST = 'east'
    NORTH = 'north'
    SOUTH = 'south'
    WEST = 'west'

    def __init__(self):
        CellPanel.__init__(self)
        self.horzAlign = HasHorizontalAlignment.ALIGN_LEFT
        self.vertAlign = HasVerticalAlignment.ALIGN_TOP
        self.center = None
        self.dock_children = []
        DOM.setIntAttribute(self.getTable(), 'cellSpacing', 0)
        DOM.setIntAttribute(self.getTable(), 'cellPadding', 0)
        return

    def add(self, widget, direction):
        if direction == self.CENTER:
            if self.center != None:
                print 'Only one CENTER widget may be added'
            self.center = widget
        layout = LayoutData(direction)
        widget.setLayoutData(layout)
        self.setCellHorizontalAlignment(widget, self.horzAlign)
        self.setCellVerticalAlignment(widget, self.vertAlign)
        self.dock_children.append(widget)
        self.realizeTable(widget)
        return

    def getHorizontalAlignment(self):
        return self.horzAlign

    def getVerticalAlignment(self):
        return self.vertAlign

    def getWidgetDirection(self, widget):
        if widget.getParent() != self:
            return
        return widget.getLayoutData().direction

    def remove(self, widget):
        if widget == self.center:
            self.center = None
        ret = CellPanel.remove(self, widget)
        if ret:
            self.dock_children.remove(widget)
            self.realizeTable(None)
        return ret

    def setCellHeight(self, widget, height):
        data = widget.getLayoutData()
        data.height = height
        if data.td:
            DOM.setStyleAttribute(data.td, 'height', data.height)

    def setCellHorizontalAlignment(self, widget, align):
        data = widget.getLayoutData()
        data.hAlign = align
        if data.td:
            DOM.setAttribute(data.td, 'align', data.hAlign)

    def setCellVerticalAlignment(self, widget, align):
        data = widget.getLayoutData()
        data.vAlign = align
        if data.td:
            DOM.setStyleAttribute(data.td, 'verticalAlign', data.vAlign)

    def setCellWidth(self, widget, width):
        data = widget.getLayoutData()
        data.width = width
        if data.td:
            DOM.setStyleAttribute(data.td, 'width', data.width)

    def setHorizontalAlignment(self, align):
        self.horzAlign = align

    def setVerticalAlignment(self, align):
        self.vertAlign = align

    def realizeTable(self, beingAdded):
        bodyElement = self.getBody()
        while DOM.getChildCount(bodyElement) > 0:
            DOM.removeChild(bodyElement, DOM.getChild(bodyElement, 0))

        rowCount = 1
        colCount = 1
        for child in self.dock_children:
            dir = child.getLayoutData().direction
            if dir == self.NORTH or dir == self.SOUTH:
                rowCount += 1
            elif dir == self.EAST or dir == self.WEST:
                colCount += 1

        rows = []
        for i in range(rowCount):
            rows.append(DockPanelTmpRow())
            rows[i].tr = DOM.createTR()
            DOM.appendChild(bodyElement, rows[i].tr)

        westCol = 0
        eastCol = colCount - 1
        northRow = 0
        southRow = rowCount - 1
        centerTd = None
        for child in self.dock_children:
            layout = child.getLayoutData()
            td = DOM.createTD()
            layout.td = td
            DOM.setAttribute(layout.td, 'align', layout.hAlign)
            DOM.setStyleAttribute(layout.td, 'verticalAlign', layout.vAlign)
            DOM.setAttribute(layout.td, 'width', layout.width)
            DOM.setAttribute(layout.td, 'height', layout.height)
            if layout.direction == self.NORTH:
                DOM.insertChild(rows[northRow].tr, td, rows[northRow].center)
                self.appendAndMaybeAdopt(td, child.getElement(), beingAdded)
                DOM.setIntAttribute(td, 'colSpan', eastCol - westCol + 1)
                northRow += 1
            elif layout.direction == self.SOUTH:
                DOM.insertChild(rows[southRow].tr, td, rows[southRow].center)
                self.appendAndMaybeAdopt(td, child.getElement(), beingAdded)
                DOM.setIntAttribute(td, 'colSpan', eastCol - westCol + 1)
                southRow -= 1
            elif layout.direction == self.WEST:
                row = rows[northRow]
                DOM.insertChild(row.tr, td, row.center)
                row.center += 1
                self.appendAndMaybeAdopt(td, child.getElement(), beingAdded)
                DOM.setIntAttribute(td, 'rowSpan', southRow - northRow + 1)
                westCol += 1
            elif layout.direction == self.EAST:
                row = rows[northRow]
                DOM.insertChild(row.tr, td, row.center)
                self.appendAndMaybeAdopt(td, child.getElement(), beingAdded)
                DOM.setIntAttribute(td, 'rowSpan', southRow - northRow + 1)
                eastCol -= 1
            elif layout.direction == self.CENTER:
                centerTd = td

        if self.center != None:
            row = rows[northRow]
            DOM.insertChild(row.tr, centerTd, row.center)
            self.appendAndMaybeAdopt(centerTd, self.center.getElement(), beingAdded)
        return

    def appendAndMaybeAdopt(self, parent, child, beingAdded):
        if beingAdded != None:
            if DOM.compare(child, beingAdded.getElement()):
                CellPanel.add(self, beingAdded, parent)
                return
        DOM.appendChild(parent, child)
        return


class DockPanelTmpRow():
    center = 0
    tr = None


rootPanels = {}

class RootPanelCls(AbsolutePanel):
    """ The panel to which all other widgets must ultimately be added.
        RootPanels are never created directly. Rather, they are accessed
        via the RootPanel() function.

        Most applications will add widgets to the default root panel
        in their EntryPoint.onModuleLoad() methods. 
    """

    def __init__(self, element=None):
        AbsolutePanel.__init__(self)
        if element == None:
            element = self.getBodyElement()
        self.setElement(element)
        self.onAttach()
        return

    def getBodyElement(self):
        els = doc().get_elements_by_tag_name('body')
        return els.item(0)

    @classmethod
    def get(cls, id=None):
        """
        
        """
        global rootPanels
        if rootPanels.has_key(id):
            return rootPanels[id]
        element = None
        if id:
            element = DOM.getElementById(id)
            if not element:
                return
        if len(rootPanels) < 1:
            cls.hookWindowClosing()
        panel = RootPanel(element)
        rootPanels[id] = panel
        return panel

    @classmethod
    def hookWindowClosing(cls):
        Window.addWindowCloseListener(cls)

    @classmethod
    def onWindowClosed(cls):
        for panel in rootPanels.itervalues():
            panel.onDetach()

    @classmethod
    def onWindowClosing(cls):
        return


def RootPanel(element=None):
    """ The function which is used to obtain a Root Panel, to which
        all widgets must ultimately be added.

        @param element: element can be None, in which case the default
                        root panel is returned.
                        element can be a string, in which case the
                        widget in the underlying DOM model with the
                        'id' given by element is returned.
                        element can also be a node in the underlying DOM model.
                        A good way to think of this is in terms of an
                        HTML document.  if element is None, the HTML
                        "body" is returned.  if element is a string,
                        getElementById('element') is returned.
    """
    if pyjslib.isString(element):
        return RootPanelCls().get(element)
    return RootPanelCls(element)


class Hyperlink(Widget):
    """ A widget that serves as an "internal" hyperlink. That is, it is a
        link to another state of the running application. When clicked,
        it will create a new history frame using
        History.newItem(targetHistoryToken), but without reloading the page.

        Being a true hyperlink, it is also possible for the user to
        "right-click, open link in new window", which will cause the
        application to be loaded in a new window at the state specified
        by the hyperlink. 
    """

    def __init__(self, text='', asHTML=False, targetHistoryToken=''):
        Widget.__init__(self)
        self.clickListeners = []
        self.targetHistoryToken = ''
        self.setElement(DOM.createDiv())
        self.anchorElem = DOM.createAnchor()
        DOM.appendChild(self.getElement(), self.anchorElem)
        self.sinkEvents(Event.ONCLICK)
        self.setStyleName('gwt-Hyperlink')
        if asHTML:
            self.setHTML(text)
        else:
            self.setText(text)
        if targetHistoryToken:
            self.setTargetHistoryToken(targetHistoryToken)

    def addClickListener(self, listener):
        self.clickListeners.append(listener)

    def getHTML(self):
        return DOM.getInnerHTML(self.anchorElem)

    def getTargetHistoryToken(self):
        return self.targetHistoryToken

    def getText(self):
        return DOM.getInnerText(self.anchorElem)

    def onBrowserEvent(self, event):
        if DOM.eventGetType(event) == 'click':
            for listener in self.clickListeners:
                if hasattr(listener, 'onClick'):
                    if listener.onClick.func_code.co_argcount == 2:
                        listener.onClick(self)
                    else:
                        listener.onClick(self, event)
                elif listener.func_code.co_argcount == 1:
                    listener(self)
                else:
                    listener(self, event)

            History().newItem(self.targetHistoryToken)
            DOM.eventPreventDefault(event)

    def removeClickListener(self, listener):
        self.clickListeners.remove(listener)

    def setHTML(self, html):
        DOM.setInnerHTML(self.anchorElem, html)

    def setTargetHistoryToken(self, targetHistoryToken):
        self.targetHistoryToken = targetHistoryToken
        DOM.setAttribute(self.anchorElem, 'href', '#' + targetHistoryToken)

    def setText(self, text):
        DOM.setInnerText(self.anchorElem, text)


prefetchImages = {}

class Image(Widget):
    """ A widget that displays the image at a given URL.
    """

    def __init__(self, url=''):
        Widget.__init__(self)
        self.clickListeners = []
        self.loadListeners = []
        self.mouseListeners = []
        self.setElement(DOM.createImg())
        self.sinkEvents(Event.ONCLICK | Event.MOUSEEVENTS | Event.ONLOAD | Event.ONERROR)
        self.setStyleName('gwt-Image')
        if url:
            self.setUrl(url)

    def addClickListener(self, listener):
        self.clickListeners.append(listener)

    def addLoadListener(self, listener):
        self.loadListeners.append(listener)

    def addMouseListener(self, listener):
        self.mouseListeners.append(listener)

    def getUrl(self):
        return DOM.getAttribute(self.getElement(), 'src')

    def onBrowserEvent(self, event):
        type = DOM.eventGetType(event)
        if type == 'click':
            for listener in self.clickListeners:
                if hasattr(listener, 'onClick'):
                    if listener.onClick.func_code.co_argcount == 2:
                        listener.onClick(self)
                    else:
                        listener.onClick(self, event)
                elif listener.func_code.co_argcount == 1:
                    listener(self)
                else:
                    listener(self, event)

        elif type == 'mousedown' or type == 'mouseup' or type == 'mousemove' or type == 'mouseover' or type == 'mouseout':
            MouseListener().fireMouseEvent(self.mouseListeners, self, event)
        elif type == 'load':
            for listener in self.loadListeners:
                listener.onLoad(self)

        elif type == 'error':
            for listener in self.loadListeners:
                listener.onError(self)

    def prefetch(self, url):
        global prefetchImages
        img = DOM.createImg()
        DOM.setAttribute(img, 'src', url)
        prefetchImages[url] = img

    def setUrl(self, url):
        DOM.setAttribute(self.getElement(), 'src', url)


class FlowPanel(ComplexPanel):
    """ A panel that formats its child widgets using default HTML layout
        behavior.  Child widgets layout will therefore "flow" as the
        FlowPanel panel is resized.  Usually this will be from left to
        right, followed by filling the next available vertical space,
        downwards, if a child widget cannot fit on the same horizontal
        space.
    """

    def __init__(self):
        ComplexPanel.__init__(self)
        self.setElement(DOM.createDiv())

    def add(self, w):
        ComplexPanel.add(self, w, self.getElement())

    def getWidget(self, index):
        return self.children[index]

    def getWidgetCount(self):
        return len(self.children)

    def getWidgetIndex(self, child):
        return self.children.index(child)

    def remove(self, index):
        if pyjslib.isNumber(index):
            index = self.getWidget(index)
        return ComplexPanel.remove(self, index)


HTMLPanel_sUid = 0

def HTMLPanel_createUniqueId():
    global HTMLPanel_sUid
    HTMLPanel_sUid += 1
    return 'HTMLPanel_%d' % HTMLPanel_sUid


class HTMLPanel(ComplexPanel):
    """ A panel that contains HTML, and which can attach child widgets
        to identified elements within that HTML.
    """

    def __init__(self, html):
        ComplexPanel.__init__(self)
        self.setElement(DOM.createDiv())
        DOM.setInnerHTML(self.getElement(), html)

    def add(self, widget, id):
        element = self.getElementById(self.getElement(), id)
        if element == None:
            return
        ComplexPanel.add(self, widget, element)
        return

    def createUniqueId(self):
        return HTMLPanel_createUniqueId()

    def getElementById(self, element, id):
        element_id = DOM.getAttribute(element, 'id')
        if element_id != None and element_id == id:
            return element
        child = DOM.getFirstChild(element)
        while child != None:
            ret = self.getElementById(child, id)
            if ret != None:
                return ret
            child = DOM.getNextSibling(child)

        return


class DeckPanel(ComplexPanel):
    """ A panel that displays all of its child widgets in a 'deck',
        where only one can be visible at a time. It is used by TabPanel.

        Once a widget has been added to a DeckPanel, its visibility, width,
        and height attributes will be manipulated. When the widget is
        removed from the DeckPanel, it will be visible, and its width and
        height attributes will be cleared. 
    """

    def __init__(self):
        ComplexPanel.__init__(self)
        self.visibleWidget = None
        self.setElement(DOM.createDiv())
        self.beforeIndex = 0
        return

    def add(self, widget):
        self.insert(widget, self.getWidgetCount())

    def getVisibleWidget(self):
        return self.getWidgetIndex(self.visibleWidget)

    def getWidget(self, index):
        return self.children[index]

    def getWidgetCount(self):
        return len(self.children)

    def getWidgetIndex(self, child):
        return self.children.index(child)

    def insert(self, widget, beforeIndex):
        if self.beforeIndex < 0 or self.beforeIndex > self.getWidgetCount():
            return
        ComplexPanel.insert(self, widget, self.getElement(), beforeIndex)
        child = widget.getElement()
        DOM.setStyleAttribute(child, 'width', '100%')
        DOM.setStyleAttribute(child, 'height', '100%')
        widget.setVisible(False)

    def remove(self, widget):
        if pyjslib.isNumber(widget):
            widget = self.getWidget(widget)
        if not ComplexPanel.remove(self, widget):
            return False
        if self.visibleWidget == widget:
            self.visibleWidget = None
        return True

    def showWidget(self, index):
        self.checkIndex(index)
        if self.visibleWidget != None:
            self.visibleWidget.setVisible(False)
        self.visibleWidget = self.getWidget(index)
        self.visibleWidget.setVisible(True)
        return

    def checkIndex(self, index):
        if index < 0 or index >= self.getWidgetCount():
            pass


class SimplePanel(Panel):
    """ A panel which contains a single widget.  Useful if you have an
        area where you'd like to be able to replace the widget with another,
        or if you need to wrap something in a DIV.
    """

    def __init__(self, element=None):
        Panel.__init__(self)
        if element == None:
            element = DOM.createDiv()
        self.setElement(element)
        return

    def add(self, widget):
        if self.getWidget() != None:
            console.error('SimplePanel can only contain one child widget')
            return
        self.setWidget(widget)
        return

    def getWidget(self):
        if len(self.children):
            return self.children[0]
        return

    def remove(self, widget):
        if self.getWidget() == widget:
            self.disown(widget)
            del self.children[0]
            return True
        return False

    def getContainerElement(self):
        return self.getElement()

    def setWidget(self, widget):
        if self.getWidget() != None:
            self.disown(self.getWidget())
            del self.children[0]
        if widget != None:
            self.adopt(widget, self.getContainerElement())
            self.children.append(widget)
        return


class ScrollPanel(SimplePanel):
    """ A simple panel that wraps its contents in a scrollable area.
    """

    def __init__(self, child=None):
        SimplePanel.__init__(self)
        self.scrollListeners = []
        self.setAlwaysShowScrollBars(False)
        self.sinkEvents(Event.ONSCROLL)
        if child != None:
            self.setWidget(child)
        return

    def addScrollListener(self, listener):
        self.scrollListeners.append(listener)

    def ensureVisible(self, item):
        scroll = self.getElement()
        element = item.getElement()
        self.ensureVisibleImpl(scroll, element)

    def getScrollPosition(self):
        return DOM.getIntAttribute(self.getElement(), 'scroll-top')

    def getHorizontalScrollPosition(self):
        return DOM.getIntAttribute(self.getElement(), 'scroll-left')

    def onBrowserEvent(self, event):
        type = DOM.eventGetType(event)
        if type == 'scroll':
            for listener in self.scrollListeners:
                listener.onScroll(self, self.getHorizontalScrollPosition(), self.getScrollPosition())

    def removeScrollListener(self, listener):
        self.scrollListeners.remove(listener)

    def setAlwaysShowScrollBars(self, alwaysShow):
        if alwaysShow:
            style = 'scroll'
        else:
            style = 'auto'
        DOM.setStyleAttribute(self.getElement(), 'overflow', style)

    def setScrollPosition(self, position):
        DOM.setIntAttribute(self.getElement(), 'scroll-top', position)

    def setHorizontalScrollPosition(self, position):
        DOM.setIntAttribute(self.getElement(), 'scroll-left', position)

    def ensureVisibleImpl(self, scroll, e):
        if not e:
            return
        item = e
        realOffset = 0
        while item and item != scroll:
            realOffset += item.props.offset_top
            item = item.props.offset_parent

        scroll.props.scroll_top = realOffset - scroll.props.offset_height / 2
        return
        JS('\n        if (!e) return;\n\n        var item = e;\n        var realOffset = 0;\n        while (item && (item != scroll)) {\n            realOffset += item.offsetTop;\n            item = item.offsetParent;\n            }\n\n        scroll.scrollTop = realOffset - scroll.offsetHeight / 2;\n        ')


class PopupPanel(SimplePanel):
    """ A panel that can "pop up" over other widgets. 

        The width and height of the PopupPanel cannot be explicitly set;
        they are determined by the PopupPanel's widget.
        Calls to setWidth(String) and setHeight(String) will call these
        methods on the PopupPanel's child widget. 
    """

    def __init__(self, autoHide=False):
        self.popupListeners = []
        self.showing = False
        self.autoHide = False
        SimplePanel.__init__(self, self.createElement())
        DOM.setStyleAttribute(self.getElement(), 'position', 'absolute')
        if autoHide:
            self.autoHide = autoHide

    def addPopupListener(self, listener):
        self.popupListeners.append(listener)

    def getPopupLeft(self):
        return DOM.getIntAttribute(self.getElement(), 'offsetLeft')

    def getPopupTop(self):
        return DOM.getIntAttribute(self.getElement(), 'offsetTop')

    def createElement(self):
        return DOM.createDiv()

    def hide(self, autoClosed=False):
        if not self.showing:
            return
        self.showing = False
        DOM.removeEventPreview(self)
        RootPanel().get().remove(self)
        self.onHideImpl(self.getElement())
        for listener in self.popupListeners:
            if listener.onPopupClosed:
                listener.onPopupClosed(self, autoClosed)
            else:
                listener(self, autoClosed)

    def onEventPreview(self, event):
        target = DOM.eventGetTarget(event)
        event_targets_popup = target and DOM.isOrHasChild(self.getElement(), target)
        type = DOM.eventGetType(event)
        if type == 'keydown':
            return self.onKeyDownPreview(DOM.eventGetKeyCode(event), KeyboardListener().getKeyboardModifiers(event)) and event_targets_popup
        elif type == 'keyup':
            return self.onKeyUpPreview(DOM.eventGetKeyCode(event), KeyboardListener().getKeyboardModifiers(event)) and event_targets_popup
        elif type == 'keypress':
            return self.onKeyPressPreview(DOM.eventGetKeyCode(event), KeyboardListener().getKeyboardModifiers(event)) and event_targets_popup
        elif type == 'mousedown' or type == 'mouseup' or type == 'mousemove' or type == 'click' or type == 'dblclick':
            if DOM.getCaptureElement() == None:
                if not event_targets_popup and self.autoHide and type == 'mousedown':
                    self.hide(True)
                    return True
        return event_targets_popup

    def onKeyDownPreview(self, key, modifiers):
        return True

    def onKeyPressPreview(self, key, modifiers):
        return True

    def onKeyUpPreview(self, key, modifiers):
        return True

    def onHideImpl(self, popup):
        pass

    def onShowImpl(self, popup):
        pass

    def removePopupListener(self, listener):
        self.popupListeners.remove(listener)

    def setPopupPosition(self, left, top):
        if left < 0:
            left = 0
        if top < 0:
            top = 0
        element = self.getElement()
        DOM.setStyleAttribute(element, 'left', '%dpx' % left)
        DOM.setStyleAttribute(element, 'top', '%dpx' % top)

    def show(self):
        if self.showing:
            return
        self.showing = True
        DOM.addEventPreview(self)
        RootPanel().get().add(self)
        self.onShowImpl(self.getElement())


class MenuItem(UIObject):
    """ A widget that can be placed in a MenuBar. Menu items can either
        fire a Command when they are clicked, or open a cascading sub-menu.
    """

    def __init__(self, text, asHTML, subMenu=None):
        """ also callable as:
            MenuItem(text, cmd)
            MenuItem(text, asHTML, cmd)
            MenuItem(text, subMenu)
            MenuItem(text, asHTML)
        """
        cmd = None
        if subMenu == None:
            if hasattr(asHTML, 'execute'):
                cmd = asHTML
                asHTML = False
            elif hasattr(asHTML, 'onShow'):
                subMenu = asHTML
                asHTML = False
        elif hasattr(subMenu, 'execute'):
            cmd = subMenu
            subMenu = None
        self.command = None
        self.parentMenu = None
        self.subMenu = None
        self.setElement(DOM.createTD())
        self.sinkEvents(Event.ONCLICK | Event.ONMOUSEOVER | Event.ONMOUSEOUT)
        self.setSelectionStyle(False)
        if asHTML:
            self.setHTML(text)
        else:
            self.setText(text)
        self.setStyleName('gwt-MenuItem')
        if cmd:
            self.setCommand(cmd)
        if subMenu:
            self.setSubMenu(subMenu)
        return

    def getCommand(self):
        return self.command

    def getHTML(self):
        return DOM.getInnerHTML(self.getElement())

    def getParentMenu(self):
        return self.parentMenu

    def getSubMenu(self):
        return self.subMenu

    def getText(self):
        return DOM.getInnerText(self.getElement())

    def setCommand(self, cmd):
        self.command = cmd

    def setHTML(self, html):
        DOM.setInnerHTML(self.getElement(), html)

    def setSubMenu(self, subMenu):
        self.subMenu = subMenu

    def setText(self, text):
        DOM.setInnerText(self.getElement(), text)

    def setParentMenu(self, parentMenu):
        self.parentMenu = parentMenu

    def setSelectionStyle(self, selected):
        if selected:
            self.addStyleName('gwt-MenuItem-selected')
        else:
            self.removeStyleName('gwt-MenuItem-selected')


class MenuBar(Widget):
    """ A standard menu bar widget. A menu bar can contain any number of
        menu items, each of which can either fire a Command or open a
        cascaded menu bar.
    """

    def __init__(self, vertical=False):
        Widget.__init__(self)
        self.body = None
        self.items = []
        self.parentMenu = None
        self.popup = None
        self.selectedItem = None
        self.shownChildMenu = None
        self.vertical = False
        self.autoOpen = False
        Widget.__init__(self)
        table = DOM.createTable()
        self.body = DOM.createTBody()
        DOM.appendChild(table, self.body)
        if not vertical:
            tr = DOM.createTR()
            DOM.appendChild(self.body, tr)
        self.vertical = vertical
        outer = DOM.createDiv()
        DOM.appendChild(outer, table)
        self.setElement(outer)
        self.setStyleName('gwt-MenuBar')
        return

    def addItem(self, item, asHTML=None, popup=None):
        if not hasattr(item, 'setSubMenu'):
            item = MenuItem(item, asHTML, popup)
        if self.vertical:
            tr = DOM.createTR()
            DOM.appendChild(self.body, tr)
        else:
            tr = DOM.getChild(self.body, 0)
        DOM.appendChild(tr, item.getElement())
        item.setParentMenu(self)
        item.setSelectionStyle(False)
        self.items.append(item)
        return item

    def clearItems(self):
        container = self.getItemContainerElement()
        while DOM.getChildCount(container) > 0:
            DOM.removeChild(container, DOM.getChild(container, 0))

        self.items = []

    def getAutoOpen(self):
        return self.autoOpen

    def onBrowserEvent(self, event):
        Widget.onBrowserEvent(self, event)
        item = self.findItem(DOM.eventGetTarget(event))
        if item == None:
            return
        type = DOM.eventGetType(event)
        if type == 'click':
            self.doItemAction(item, True)
        elif type == 'mouseover':
            self.itemOver(item)
        elif type == 'mouseout':
            self.itemOver(None)
        return

    def onPopupClosed(self, sender, autoClosed):
        if autoClosed:
            self.closeAllParents()
        self.onHide()
        self.shownChildMenu = None
        self.popup = None
        return

    def removeItem(self, item):
        idx = self.items.index(item)
        if idx == -1:
            return
        container = self.getItemContainerElement()
        DOM.removeChild(container, DOM.getChild(container, idx))
        del self.items[idx]

    def setAutoOpen(self, autoOpen):
        self.autoOpen = autoOpen

    def closeAllParents(self):
        curMenu = self
        while curMenu != None:
            curMenu.close()
            if curMenu.parentMenu == None and curMenu.selectedItem != None:
                curMenu.selectedItem.setSelectionStyle(False)
                curMenu.selectedItem = None
            curMenu = curMenu.parentMenu

        return

    def doItemAction(self, item, fireCommand):
        if self.shownChildMenu != None and item.getSubMenu() == self.shownChildMenu:
            return
        if self.shownChildMenu != None:
            self.shownChildMenu.onHide()
            self.popup.hide()
        if item.getSubMenu() == None:
            if fireCommand:
                self.closeAllParents()
                cmd = item.getCommand()
                if cmd != None:
                    DeferredCommand().add(cmd)
            return
        self.selectItem(item)
        self.popup = MenuBarPopupPanel(item)
        self.popup.addPopupListener(self)
        print list(self.getElement().props)
        print 'margin left', DOM.getAttribute(item.getElement(), 'offset-width')
        if self.vertical:
            self.popup.setPopupPosition(item.getAbsoluteLeft() + item.getOffsetWidth(), item.getAbsoluteTop())
        else:
            self.popup.setPopupPosition(item.getAbsoluteLeft(), item.getAbsoluteTop() + item.getOffsetHeight())
        self.shownChildMenu = item.getSubMenu()
        sub_menu = item.getSubMenu()
        sub_menu.parentMenu = self
        self.popup.show()
        return

    def onDetach(self):
        if self.popup != None:
            self.popup.hide()
        Widget.onDetach(self)
        return

    def itemOver(self, item):
        if item == None:
            if self.selectedItem != None and self.shownChildMenu == self.selectedItem.getSubMenu():
                return
        self.selectItem(item)
        if item != None:
            if self.shownChildMenu != None or self.parentMenu != None or self.autoOpen:
                self.doItemAction(item, False)
        return

    def close(self):
        if self.parentMenu != None:
            self.parentMenu.popup.hide()
        return

    def findItem(self, hItem):
        for item in self.items:
            if DOM.isOrHasChild(item.getElement(), hItem):
                return item

        return

    def getItemContainerElement(self):
        if self.vertical:
            return self.body
        else:
            return DOM.getChild(self.body, 0)

    def onHide(self):
        if self.shownChildMenu != None:
            self.shownChildMenu.onHide()
            self.popup.hide()
        return

    def onShow(self):
        if len(self.items) > 0:
            self.selectItem(self.items[0])

    def selectItem(self, item):
        if item == self.selectedItem:
            return
        if self.selectedItem != None:
            self.selectedItem.setSelectionStyle(False)
        if item != None:
            item.setSelectionStyle(True)
        self.selectedItem = item
        return


class MenuBarPopupPanel(PopupPanel):

    def __init__(self, item):
        self.item = item
        PopupPanel.__init__(self, True)
        self.setWidget(item.getSubMenu())
        item.getSubMenu().onShow()

    def onEventPreview(self, event):
        type = DOM.eventGetType(event)
        if type == 'click':
            target = DOM.eventGetTarget(event)
            parentMenuElement = self.item.getParentMenu().getElement()
            if DOM.isOrHasChild(parentMenuElement, target):
                return False
        return PopupPanel.onEventPreview(self, event)


class ListBox(FocusWidget):
    """ A widget that presents a list of choices to the user, either as a
        list box or as a drop-down list.
    """

    def __init__(self):
        self.changeListeners = []
        self.INSERT_AT_END = -1
        FocusWidget.__init__(self, DOM.createSelect())
        self.sinkEvents(Event.ONCHANGE)
        self.setStyleName('gwt-ListBox')

    def addChangeListener(self, listener):
        self.changeListeners.append(listener)

    def addItem(self, item, value=None):
        self.insertItem(item, value, self.INSERT_AT_END)

    def clear(self):
        h = self.getElement()
        while DOM.getChildCount(h) > 0:
            DOM.removeChild(h, DOM.getChild(h, 0))

    def getItemCount(self):
        return DOM.getChildCount(self.getElement())

    def getItemText(self, index):
        child = DOM.getChild(self.getElement(), index)
        return DOM.getInnerText(child)

    def getName(self):
        return DOM.getAttribute(self.getElement(), 'name')

    def getSelectedIndex(self):
        return DOM.getIntAttribute(self.getElement(), 'selectedIndex')

    def getValue(self, index):
        self.checkIndex(index)
        option = DOM.getChild(self.getElement(), index)
        return DOM.getAttribute(option, 'value')

    def getVisibleItemCount(self):
        return DOM.getIntAttribute(self.getElement(), 'size')

    def insertItem(self, item, value, index=None):
        if index == None:
            index = value
            value = None
        DOM.insertListItem(self.getElement(), item, value, index)
        return

    def isItemSelected(self, index):
        self.checkIndex(index)
        option = DOM.getChild(self.getElement(), index)
        return DOM.getBooleanAttribute(option, 'selected')

    def isMultipleSelect(self):
        return DOM.getBooleanAttribute(self.getElement(), 'multiple')

    def onBrowserEvent(self, event):
        if DOM.eventGetType(event) == 'change':
            for listener in self.changeListeners:
                if hasattr(listener, 'onChange'):
                    listener.onChange(self)
                else:
                    listener(self)

        else:
            FocusWidget.onBrowserEvent(self, event)

    def removeChangeListener(self, listener):
        self.changeListeners.remove(listener)

    def removeItem(self, idx):
        child = DOM.getChild(self.getElement(), idx)
        DOM.removeChild(self.getElement(), child)

    def setItemSelected(self, index, selected):
        self.checkIndex(index)
        option = DOM.getChild(self.getElement(), index)
        DOM.setBooleanAttribute(option, 'selected', selected)

    def setMultipleSelect(self, multiple):
        DOM.setBooleanAttribute(self.getElement(), 'multiple', multiple)

    def setName(self, name):
        DOM.setAttribute(self.getElement(), 'name', name)

    def setSelectedIndex(self, index):
        DOM.setIntAttribute(self.getElement(), 'selectedIndex', index)

    def selectValue(self, value):
        for n in range(self.getItemCount()):
            if self.getValue(n) == value:
                self.setSelectedIndex(n)
                return n

        return

    def setItemText(self, index, text):
        self.checkIndex(index)
        if text == None:
            console.error('Cannot set an option to have null text')
            return
        DOM.setOptionText(self.getElement(), text, index)
        return

    def setValue(self, index, value):
        self.checkIndex(index)
        option = DOM.getChild(self.getElement(), index)
        DOM.setAttribute(option, 'value', value)

    def setVisibleItemCount(self, visibleItems):
        DOM.setIntAttribute(self.getElement(), 'size', visibleItems)

    def checkIndex(self, index):
        elem = self.getElement()
        if index < 0 or index >= DOM.getChildCount(elem):
            pass


class DialogBox(PopupPanel):
    """ A form of popup that has a caption area at the top and can
        be dragged by the user.
    """

    def __init__(self, autoHide=None):
        PopupPanel.__init__(self, autoHide)
        self.caption = HTML()
        self.child = None
        self.dragging = False
        self.dragStartX = 0
        self.dragStartY = 0
        self.panel = FlexTable()
        self.panel.setWidget(0, 0, self.caption)
        self.panel.setHeight('100%')
        self.panel.setBorderWidth(0)
        self.panel.setCellPadding(0)
        self.panel.setCellSpacing(0)
        self.panel.getCellFormatter().setHeight(1, 0, '100%')
        self.panel.getCellFormatter().setWidth(1, 0, '100%')
        self.panel.getCellFormatter().setAlignment(1, 0, HasHorizontalAlignment.ALIGN_CENTER, HasVerticalAlignment.ALIGN_MIDDLE)
        PopupPanel.setWidget(self, self.panel)
        self.setStyleName('gwt-DialogBox')
        self.caption.setStyleName('Caption')
        self.caption.addMouseListener(self)
        return

    def getHTML(self):
        return self.caption.getHTML()

    def getText(self):
        return self.caption.getText()

    def onMouseDown(self, sender, x, y):
        self.dragging = True
        DOM.setCapture(self.caption.getElement())
        self.dragStartX = x
        self.dragStartY = y

    def onMouseEnter(self, sender):
        pass

    def onMouseLeave(self, sender):
        pass

    def onMouseMove(self, sender, x, y):
        if self.dragging:
            absX = x + self.getAbsoluteLeft()
            absY = y + self.getAbsoluteTop()
            self.setPopupPosition(absX - self.dragStartX, absY - self.dragStartY)

    def onMouseUp(self, sender, x, y):
        self.dragging = False
        DOM.releaseCapture(self.caption.getElement())

    def remove(self, widget):
        if self.child != widget:
            return False
        self.panel.remove(widget)
        return True

    def setHTML(self, html):
        self.caption.setHTML(html)

    def setText(self, text):
        self.caption.setText(text)

    def setWidget(self, widget):
        if self.child != None:
            self.panel.remove(self.child)
        if widget != None:
            self.panel.setWidget(1, 0, widget)
        self.child = widget
        return


class Frame(Widget):
    """ A widget that wraps an IFRAME element, which can contain an
        arbitrary web site.

        Note that if you are using History, any browser history items
        generated by the Frame will interleave with your application's history.
    """

    def __init__(self, url=''):
        Widget.__init__(self)
        self.setElement(DOM.createIFrame())
        if url:
            self.setUrl(url)

    def getUrl(self):
        return DOM.getAttribute(self.getElement(), 'src')

    def setUrl(self, url):
        return DOM.setAttribute(self.getElement(), 'src', url)


class TabBar(Composite):
    """ A horizontal bar of folder-style tabs, most commonly used as
        part of a TabPanel.
    """

    def __init__(self):
        Composite.__init__(self)
        self.panel = HorizontalPanel()
        self.selectedTab = None
        self.tabListeners = []
        self.initWidget(self.panel)
        self.sinkEvents(Event.ONCLICK)
        self.setStyleName('gwt-TabBar')
        self.panel.setVerticalAlignment(HasAlignment.ALIGN_BOTTOM)
        first = HTML('&nbsp;', True)
        rest = HTML('&nbsp;', True)
        first.setStyleName('gwt-TabBarFirst')
        rest.setStyleName('gwt-TabBarRest')
        first.setHeight('100%')
        rest.setHeight('100%')
        self.panel.add(first)
        self.panel.add(rest)
        first.setHeight('100%')
        self.panel.setCellHeight(first, '100%')
        self.panel.setCellWidth(rest, '100%')
        return

    def addTab(self, text, asHTML=False):
        self.insertTab(text, asHTML, self.getTabCount())

    def addTabListener(self, listener):
        self.tabListeners.append(listener)

    def getSelectedTab(self):
        if self.selectedTab == None:
            return -1
        return self.panel.getWidgetIndex(self.selectedTab) - 1

    def getTabCount(self):
        return self.panel.getWidgetCount() - 2

    def getTabHTML(self, index):
        if index >= self.getTabCount():
            return
        widget = self.panel.getWidget(index + 1)
        if widget.getHTML:
            return widget.getHTML()
        else:
            return widget.getText()
        return

    def insertTab(self, text, asHTML, beforeIndex=None):
        if beforeIndex == None:
            beforeIndex = asHTML
            asHTML = False
        if beforeIndex < 0 or beforeIndex > self.getTabCount():
            pass
        if asHTML:
            item = HTML(text)
        else:
            item = Label(text)
        item.setWordWrap(False)
        item.addClickListener(self)
        item.setStyleName('gwt-TabBarItem')
        self.panel.insert(item, beforeIndex + 1)
        return

    def onClick(self, sender):
        for i in range(1, self.panel.getWidgetCount() - 1):
            if self.panel.getWidget(i) == sender:
                self.selectTab(i - 1)
                return

    def removeTab(self, index):
        self.checkTabIndex(index)
        toRemove = self.panel.getWidget(index + 1)
        if toRemove == self.selectedTab:
            self.selectedTab = None
        self.panel.remove(toRemove)
        return

    def removeTabListener(self, listener):
        self.tabListeners.remove(listener)

    def selectTab(self, index):
        self.checkTabIndex(index)
        for listener in self.tabListeners:
            if not listener.onBeforeTabSelected(self, index):
                return False

        self.setSelectionStyle(self.selectedTab, False)
        if index == -1:
            self.selectedTab = None
            return True
        self.selectedTab = self.panel.getWidget(index + 1)
        self.setSelectionStyle(self.selectedTab, True)
        for listener in self.tabListeners:
            listener.onTabSelected(self, index)

        return True

    def checkTabIndex(self, index):
        if index < -1 or index >= self.getTabCount():
            pass

    def setSelectionStyle(self, item, selected):
        if item != None:
            if selected:
                item.addStyleName('gwt-TabBarItem-selected')
            else:
                item.removeStyleName('gwt-TabBarItem-selected')
        return


class TabPanel(Composite):
    """ A panel that represents a tabbed set of pages, each of which contains
        another widget. Its child widgets are shown as the user selects the
        various tabs associated with them. The tab text identifying each
        page can contain arbitrary HTML.

        Note that this widget is not a panel per se, but rather a Composite
        that aggregates a TabBar and a DeckPanel. It does, however,
        implement HasWidgets.
    """

    def __init__(self):
        Composite.__init__(self)
        self.tab_children = []
        self.deck = DeckPanel()
        self.tabBar = TabBar()
        self.tabListeners = []
        panel = VerticalPanel()
        panel.add(self.tabBar)
        panel.add(self.deck)
        panel.setCellHeight(self.deck, '100%')
        self.tabBar.setWidth('100%')
        self.tabBar.addTabListener(self)
        self.initWidget(panel)
        self.setStyleName('gwt-TabPanel')
        self.deck.setStyleName('gwt-TabPanelBottom')

    def add(self, widget, tabText=None, asHTML=False):
        if tabText == None:
            console.error('A tabText parameter must be specified with add().')
        self.insert(widget, tabText, asHTML, self.getWidgetCount())
        return

    def addTabListener(self, listener):
        self.tabListeners.append(listener)

    def clear(self):
        while self.getWidgetCount() > 0:
            self.remove(self.getWidget(0))

    def getDeckPanel(self):
        return self.deck

    def getTabBar(self):
        return self.tabBar

    def getWidget(self, index):
        return self.tab_children[index]

    def getWidgetCount(self):
        return len(self.tab_children)

    def getWidgetIndex(self, child):
        return self.tab_children.index(child)

    def insert(self, widget, tabText, asHTML, beforeIndex=None):
        if beforeIndex == None:
            beforeIndex = asHTML
            asHTML = False
        self.tab_children.insert(beforeIndex, widget)
        self.tabBar.insertTab(tabText, asHTML, beforeIndex)
        self.deck.insert(widget, beforeIndex)
        return

    def __iter__(self):
        return self.tab_children.__iter__()

    def onBeforeTabSelected(self, sender, tabIndex):
        for listener in self.tabListeners:
            if not listener.onBeforeTabSelected(sender, tabIndex):
                return False

        return True

    def onTabSelected(self, sender, tabIndex):
        self.deck.showWidget(tabIndex)
        for listener in self.tabListeners:
            listener.onTabSelected(sender, tabIndex)

    def remove(self, widget):
        if pyjslib.isNumber(widget):
            widget = self.getWidget(widget)
        index = self.getWidgetIndex(widget)
        if index == -1:
            return False
        self.tab_children.remove(widget)
        self.tabBar.removeTab(index)
        self.deck.remove(widget)
        return True

    def removeTabListener(self, listener):
        self.tabListeners.remove(listener)

    def selectTab(self, index):
        self.tabBar.selectTab(index)


class StackPanel(ComplexPanel):
    """ A panel that stacks its children vertically, displaying only one at
        a time, with a header for each child which the user can click to
        display.
    """

    def __init__(self):
        ComplexPanel.__init__(self)
        self.body = None
        self.visibleStack = -1
        table = DOM.createTable()
        self.setElement(table)
        self.body = DOM.createTBody()
        DOM.appendChild(table, self.body)
        DOM.setIntAttribute(table, 'cellSpacing', 0)
        DOM.setIntAttribute(table, 'cellPadding', 0)
        DOM.sinkEvents(table, Event.ONCLICK)
        self.setStyleName('gwt-StackPanel')
        return

    def add(self, widget, stackText='', asHTML=False):
        widget.removeFromParent()
        index = self.getWidgetCount()
        tr = DOM.createTR()
        td = DOM.createTD()
        DOM.appendChild(self.body, tr)
        DOM.appendChild(tr, td)
        self.setStyleName(td, 'gwt-StackPanelItem', True)
        DOM.setIntElemAttribute(td, '__index', index)
        td.__index = index
        DOM.setAttribute(td, 'height', '1px')
        tr = DOM.createTR()
        td = DOM.createTD()
        DOM.appendChild(self.body, tr)
        DOM.appendChild(tr, td)
        DOM.setAttribute(td, 'height', '100%')
        DOM.setAttribute(td, 'vAlign', 'top')
        ComplexPanel.add(self, widget, td)
        self.setStackVisible(index, False)
        if self.visibleStack == -1:
            self.showStack(0)
        if stackText != '':
            self.setStackText(self.getWidgetCount() - 1, stackText, asHTML)

    def getWidget(self, index):
        return self.children[index]

    def getWidgetCount(self):
        return len(self.children)

    def getWidgetIndex(self, child):
        return self.children.index(child)

    def onBrowserEvent(self, event):
        if DOM.eventGetType(event) == 'click':
            index = self.getDividerIndex(DOM.eventGetTarget(event))
            if index != -1:
                self.showStack(index)

    def remove(self, child, index=None):
        if index == None:
            if pyjslib.isNumber(child):
                index = child
                child = self.getWidget(child)
            else:
                index = self.getWidgetIndex(child)
        if child.getParent() != self:
            return False
        if self.visibleStack == index:
            self.visibleStack = -1
        elif self.visibleStack > index:
            self.visibleStack -= 1
        rowIndex = 2 * index
        tr = DOM.getChild(self.body, rowIndex)
        DOM.removeChild(self.body, tr)
        tr = DOM.getChild(self.body, rowIndex)
        DOM.removeChild(self.body, tr)
        ComplexPanel.remove(self, child)
        rows = self.getWidgetCount() * 2
        for i in range(rowIndex, rows, 2):
            childTR = DOM.getChild(self.body, i)
            td = DOM.getFirstChild(childTR)
            curIndex = DOM.getIntElemAttribute(td, '__index')
            DOM.setIntElemAttribute(td, '__index', index)
            index += 1

        return True

    def setStackText(self, index, text, asHTML=False):
        if index >= self.getWidgetCount():
            return
        td = DOM.getChild(DOM.getChild(self.body, index * 2), 0)
        if asHTML:
            DOM.setInnerHTML(td, text)
        else:
            DOM.setInnerText(td, text)

    def showStack(self, index):
        if index >= self.getWidgetCount() or index == self.visibleStack:
            return
        if self.visibleStack >= 0:
            self.setStackVisible(self.visibleStack, False)
        self.visibleStack = index
        self.setStackVisible(self.visibleStack, True)

    def getDividerIndex(self, elem):
        while elem != None and not DOM.compare(elem, self.getElement()):
            expando = DOM.getIntElemAttribute(elem, '__index')
            if expando != None:
                return int(expando)
            elem = DOM.getParent(elem)

        return -1

    def setStackVisible(self, index, visible):
        tr = DOM.getChild(self.body, index * 2)
        if tr == None:
            return
        td = DOM.getFirstChild(tr)
        self.setStyleName(td, 'gwt-StackPanelItem-selected', visible)
        tr = DOM.getChild(self.body, index * 2 + 1)
        self.setVisible(tr, visible)
        self.getWidget(index).setVisible(visible)
        return

    def getSelectedIndex(self):
        return self.visibleStack


class TextBoxBase(FocusWidget):
    ALIGN_CENTER = 'center'
    ALIGN_JUSTIFY = 'justify'
    ALIGN_LEFT = 'left'
    ALIGN_RIGHT = 'right'

    def __init__(self, element):
        self.changeListeners = []
        self.clickListeners = []
        self.currentEvent = None
        self.keyboardListeners = []
        FocusWidget.__init__(self, element)
        self.sinkEvents(Event.ONCHANGE)
        return

    def addChangeListener(self, listener):
        self.changeListeners.append(listener)

    def addClickListener(self, listener):
        self.clickListeners.append(listener)

    def addKeyboardListener(self, listener):
        self.keyboardListeners.append(listener)

    def cancelKey(self):
        if self.currentEvent != None:
            DOM.eventPreventDefault(self.currentEvent)
        return

    def getCursorPos(self):
        element = self.getElement()
        try:
            return element.props.selection_start
        except:
            return 0

    def getName(self):
        return DOM.getAttribute(self.getElement(), 'name')

    def getSelectedText(self):
        start = self.getCursorPos()
        length = self.getSelectionLength()
        text = self.getText()
        return text[start:start + length]

    def getSelectionLength(self):
        element = self.getElement()
        try:
            return element.props.selection_end - element.props.selection_start
        except:
            return 0

    def getText(self):
        return DOM.getAttribute(self.getElement(), 'value')

    def onBrowserEvent(self, event):
        FocusWidget.onBrowserEvent(self, event)
        type = DOM.eventGetType(event)
        if type == 'change':
            for listener in self.changeListeners:
                if listener.onChange:
                    listener.onChange(self)
                else:
                    listener(self)

    def removeChangeListener(self, listener):
        self.changeListeners.remove(listener)

    def removeClickListener(self, listener):
        self.clickListeners.remove(listener)

    def removeKeyboardListener(self, listener):
        self.keyboardListeners.remove(listener)

    def selectAll(self):
        length = len(self.getText())
        if length > 0:
            self.setSelectionRange(0, length)

    def setCursorPos(self, pos):
        self.setSelectionRange(pos, 0)

    def setKey(self, key):
        if self.currentEvent != None:
            DOM.eventSetKeyCode(self.currentEvent, key)
        return

    def setName(self, name):
        DOM.setAttribute(self.getElement(), 'name', name)

    def setSelectionRange(self, pos, length):
        if length < 0:
            console.error('Length must be a positive integer. Length: ' + length)
        if pos < 0 or length + pos > len(self.getText()):
            console.error('From Index: ' + pos + '  To Index: ' + (pos + length) + '  Text Length: ' + len(self.getText()))
        element = self.getElement()
        element.set_selection_range(pos, pos + length)

    def setText(self, text):
        DOM.setAttribute(self.getElement(), 'value', text)

    def setTextAlignment(self, align):
        DOM.setStyleAttribute(self.getElement(), 'textAlign', align)


class TextBox(TextBoxBase):
    """ TextBox is a standard single-line text box.
    """

    def __init__(self):
        TextBoxBase.__init__(self, DOM.createInputText())
        self.setStyleName('gwt-TextBox')

    def getMaxLength(self):
        return DOM.getIntAttribute(self.getElement(), 'maxLength')

    def getVisibleLength(self):
        return DOM.getIntAttribute(self.getElement(), 'size')

    def setMaxLength(self, length):
        DOM.setIntAttribute(self.getElement(), 'maxLength', length)

    def setVisibleLength(self, length):
        DOM.setIntAttribute(self.getElement(), 'size', length)


class PasswordTextBox(TextBoxBase):
    """ PasswordTextBox is a text box that visually masks its input to
        prevent eavesdropping.
    """

    def __init__(self):
        TextBoxBase.__init__(self, DOM.createInputPassword())
        self.setStyleName('gwt-PasswordTextBox')


class TextArea(TextBoxBase):
    """ HTML textarea widget, allowing multi-line text entry.
        Use setText/getText to get and access the current text.
    """

    def __init__(self):
        TextBoxBase.__init__(self, DOM.createTextArea())
        self.setStyleName('gwt-TextArea')

    def getCharacterWidth(self):
        return DOM.getIntAttribute(self.getElement(), 'cols')

    def getCursorPos(self):
        return TextBoxBase.getCursorPos(self)

    def getVisibleLines(self):
        return DOM.getIntAttribute(self.getElement(), 'rows')

    def setCharacterWidth(self, width):
        DOM.setIntAttribute(self.getElement(), 'cols', width)

    def setVisibleLines(self, lines):
        DOM.setIntAttribute(self.getElement(), 'rows', lines)


class TreeContentPanel(SimplePanel):

    def __init__(self, element):
        SimplePanel.__init__(self, element)
        self.tree_item = None
        return

    def getTreeItem(self):
        return self.tree_item

    def setTreeItem(self, tree_item):
        self.tree_item = tree_item

    def setParent(self, widget):
        console.error("Cannot directly setParent on a WidgetTreeItem's ContentPanel")

    def treeSetParent(self, widget):
        SimplePanel.setParent(self, widget)


class TreeItem(UIObject):
    """ An item that can be contained within a Tree.
    """

    def __init__(self, html=None):
        self.children = []
        self.contentPanel = None
        self.itemTable = None
        self.contentElem = None
        self.imgElem = None
        self.childSpanElem = None
        self.open = False
        self.parent = None
        self.selected = False
        self.tree = None
        self.userObject = None
        self.setElement(DOM.createDiv())
        self.itemTable = DOM.createTable()
        self.contentElem = DOM.createSpan()
        self.childSpanElem = DOM.createSpan()
        self.imgElem = DOM.createImg()
        tbody = DOM.createTBody()
        tr = DOM.createTR()
        tdImg = DOM.createTD()
        tdContent = DOM.createTD()
        DOM.appendChild(self.itemTable, tbody)
        DOM.appendChild(tbody, tr)
        DOM.appendChild(tr, tdImg)
        DOM.appendChild(tr, tdContent)
        DOM.setStyleAttribute(tdImg, 'verticalAlign', 'middle')
        DOM.setStyleAttribute(tdContent, 'verticalAlign', 'middle')
        DOM.appendChild(self.getElement(), self.itemTable)
        DOM.appendChild(self.getElement(), self.childSpanElem)
        DOM.appendChild(tdImg, self.imgElem)
        DOM.appendChild(tdContent, self.contentElem)
        DOM.setStyleAttribute(self.contentElem, 'display', 'inline')
        DOM.setStyleAttribute(self.getElement(), 'whiteSpace', 'nowrap')
        DOM.setStyleAttribute(self.childSpanElem, 'whiteSpace', 'nowrap')
        self.setStyleName(self.contentElem, 'gwt-TreeItem', True)
        if html != None:
            if pyjslib.isString(html):
                self.setHTML(html)
            else:
                self.setWidget(html)
        return

    def addItem(self, item):
        if not hasattr(item, 'getTree'):
            item = TreeItem(item)
        if item.getParentItem() != None or item.getTree() != None:
            item.remove()
        item.setTree(self.tree)
        item.setParentItem(self)
        self.children.append(item)
        DOM.setStyleAttribute(item.getElement(), 'marginLeft', '16px')
        DOM.appendChild(self.childSpanElem, item.getElement())
        if len(self.children) == 1:
            self.updateState()
        return item

    def getChild(self, index):
        if index < 0 or index >= len(self.children):
            return
        return self.children[index]

    def getChildCount(self):
        return len(self.children)

    def getChildIndex(self, child):
        return self.children.index(child)

    def getHTML(self):
        return DOM.getInnerHTML(self.contentElem)

    def getText(self):
        return DOM.getInnerText(self.contentElem)

    def getParentItem(self):
        return self.parent

    def getState(self):
        return self.open

    def getTree(self):
        return self.tree

    def getUserObject(self):
        return self.userObject

    def getWidget(self):
        if self.contentPanel == None:
            return
        return self.contentPanel.getWidget()

    def isSelected(self):
        return self.selected

    def remove(self):
        if self.parent != None:
            self.parent.removeItem(self)
        elif self.tree != None:
            self.tree.removeItem(self)
        return

    def removeItem(self, item):
        if item not in self.children:
            return
        item.setTree(None)
        item.setParentItem(None)
        self.children.remove(item)
        DOM.removeChild(self.childSpanElem, item.getElement())
        if len(self.children) == 0:
            self.updateState()
        return

    def removeItems(self):
        while self.getChildCount() > 0:
            self.removeItem(self.getChild(0))

    def setHTML(self, html):
        self.clearContentPanel()
        DOM.setInnerHTML(self.contentElem, html)

    def setText(self, text):
        self.clearContentPanel()
        DOM.setInnerText(self.contentElem, text)

    def setSelected(self, selected):
        if self.selected == selected:
            return
        self.selected = selected
        self.setStyleName(self.contentElem, 'gwt-TreeItem-selected', selected)

    def setState(self, open, fireEvents=True):
        if open and len(self.children) == 0:
            return
        self.open = open
        self.updateState()
        if fireEvents:
            self.tree.fireStateChanged(self)

    def setUserObject(self, userObj):
        self.userObject = userObj

    def setWidget(self, widget):
        self.ensureContentPanel()
        self.contentPanel.setWidget(widget)

    def clearContentPanel(self):
        if self.contentPanel != None:
            child = self.contentPanel.getWidget()
            if child != None:
                self.contentPanel.remove(child)
            if self.tree != None:
                self.tree.disown(self.contentPanel)
                self.contentPanel = None
        return

    def ensureContentPanel(self):
        if self.contentPanel == None:
            DOM.setInnerHTML(self.contentElem, '')
            self.contentPanel = TreeContentPanel(self.contentElem)
            self.contentPanel.setTreeItem(self)
            if self.getTree() != None:
                self.tree.adopt(self.contentPanel)
        return

    def addTreeItems(self, accum):
        for item in self.children:
            accum.append(item)
            item.addTreeItems(accum)

    def getChildren(self):
        return self.children

    def getContentElem(self):
        return self.contentElem

    def getContentHeight(self):
        return DOM.getIntAttribute(self.itemTable, 'offsetHeight')

    def getImageElement(self):
        return self.imgElem

    def getTreeTop(self):
        item = self
        ret = 0
        while item != None:
            ret += DOM.getIntAttribute(item.getElement(), 'offsetTop')
            item = item.getParentItem()

        return ret

    def getFocusableWidget(self):
        widget = self.getWidget()
        if hasattr(widget, 'setFocus'):
            return widget
        return

    def imgSrc(self, img):
        if self.tree == None:
            return img
        src = self.tree.getImageBase() + img
        return src

    def setParentItem(self, parent):
        self.parent = parent

    def setTree(self, tree):
        if self.tree == tree:
            return
        if self.tree != None:
            if self.tree.getSelectedItem() == self:
                self.tree.setSelectedItem(None)
            if self.contentPanel != None:
                self.tree.disown(self.contentPanel)
        self.tree = tree
        for child in self.children:
            child.setTree(tree)

        self.updateState()
        if tree != None and self.contentPanel != None:
            tree.adopt(self.contentPanel)
        return

    def updateState(self):
        if len(self.children) == 0:
            self.setVisible(self.childSpanElem, False)
            DOM.setAttribute(self.imgElem, 'src', self.imgSrc('tree_white.gif'))
            return
        if self.open:
            self.setVisible(self.childSpanElem, True)
            DOM.setAttribute(self.imgElem, 'src', self.imgSrc('tree_open.gif'))
        else:
            self.setVisible(self.childSpanElem, False)
            DOM.setAttribute(self.imgElem, 'src', self.imgSrc('tree_closed.gif'))

    def updateStateRecursive(self):
        self.updateState()
        for i in range(len(self.children)):
            child = self.children[i]
            child.updateStateRecursive()


class RootTreeItem(TreeItem):

    def addItem(self, item):
        if item.getParentItem() != None or item.getTree() != None:
            item.remove()
        item.setTree(self.getTree())
        item.setParentItem(None)
        self.children.append(item)
        DOM.setIntStyleAttribute(item.getElement(), 'marginLeft', 0)
        return

    def removeItem(self, item):
        if item not in self.children:
            return
        item.setTree(None)
        item.setParentItem(None)
        self.children.remove(item)
        return


class Tree(Widget):
    """ A standard hierarchical tree widget. The tree contains a hierarchy
        of TreeItems that the user can open, close, and select.
    """

    def __init__(self):
        Widget.__init__(self)
        self.root = None
        self.childWidgets = Set()
        self.curSelection = None
        self.focusable = None
        self.focusListeners = []
        self.mouseListeners = []
        self.imageBase = pygwt.getModuleBaseURL()
        self.keyboardListeners = []
        self.listeners = []
        self.lastEventType = ''
        self.setElement(DOM.createDiv())
        DOM.setStyleAttribute(self.getElement(), 'position', 'relative')
        self.focusable = Focus().createFocusable()
        DOM.setStyleAttribute(self.focusable, 'fontSize', '0')
        DOM.setStyleAttribute(self.focusable, 'position', 'absolute')
        DOM.setIntStyleAttribute(self.focusable, 'zIndex', -1)
        DOM.appendChild(self.getElement(), self.focusable)
        self.sinkEvents(Event.MOUSEEVENTS | Event.ONCLICK | Event.KEYEVENTS)
        DOM.sinkEvents(self.focusable, Event.FOCUSEVENTS | Event.KEYEVENTS | DOM.getEventsSunk(self.focusable))
        self.root = RootTreeItem()
        self.root.setTree(self)
        self.setStyleName('gwt-Tree')
        return

    def add(self, widget):
        self.addItem(widget)

    def addFocusListener(self, listener):
        self.focusListeners.append(listener)

    def addItem(self, item):
        if pyjslib.isString(item):
            item = TreeItem(item)
        ret = self.root.addItem(item)
        DOM.appendChild(self.getElement(), item.getElement())
        return ret

    def addKeyboardListener(self, listener):
        self.keyboardListeners.append(listener)

    def addMouseListener(self, listener):
        self.mouseListeners.append(listener)

    def addTreeListener(self, listener):
        self.listeners.append(listener)

    def clear(self):
        size = self.root.getChildCount()
        for i in range(size, 0, -1):
            self.root.getChild(i - 1).remove()

    def ensureSelectedItemVisible(self):
        if self.curSelection == None:
            return
        parent = self.curSelection.getParentItem()
        while parent != None:
            parent.setState(True)
            parent = parent.getParentItem()

        return

    def getImageBase(self):
        return self.imageBase

    def getItem(self, index):
        return self.root.getChild(index)

    def getItemCount(self):
        return self.root.getChildCount()

    def getSelectedItem(self):
        return self.curSelection

    def getTabIndex(self):
        return Focus.getTabIndex(self, self.focusable)

    def __iter__(self):
        return self.childWidgets.__iter__()

    def onBrowserEvent(self, event):
        type = DOM.eventGetType(event)
        if type == 'click':
            e = DOM.eventGetTarget(event)
            if not self.shouldTreeDelegateFocusToElement(e):
                self.setFocus(True)
        elif type == 'mousedown':
            MouseListener().fireMouseEvent(self.mouseListeners, self, event)
            self.elementClicked(self.root, DOM.eventGetTarget(event))
        elif type == 'mouseup' or type == 'mousemove' or type == 'mouseover' or type == 'mouseout':
            MouseListener().fireMouseEvent(self.mouseListeners, self, event)
        elif type == 'blur' or type == 'focus':
            FocusListener().fireFocusEvent(self.focusListeners, self, event)
        elif type == 'keydown':
            if self.curSelection == None:
                if self.root.getChildCount() > 0:
                    self.onSelection(self.root.getChild(0), True)
                Widget.onBrowserEvent(self, event)
                return
            if self.lastEventType == 'keydown':
                return
            keycode = DOM.eventGetKeyCode(event)
            if keycode == KeyboardListener.KEY_UP:
                self.moveSelectionUp(self.curSelection)
                DOM.eventPreventDefault(event)
            elif keycode == KeyboardListener.KEY_DOWN:
                self.moveSelectionDown(self.curSelection, True)
                DOM.eventPreventDefault(event)
            elif keycode == KeyboardListener.KEY_LEFT:
                if self.curSelection.getState():
                    self.curSelection.setState(False)
                DOM.eventPreventDefault(event)
            elif keycode == KeyboardListener.KEY_RIGHT:
                if not self.curSelection.getState():
                    self.curSelection.setState(True)
                DOM.eventPreventDefault(event)
        elif type == 'keyup':
            if DOM.eventGetKeyCode(event) == KeyboardListener.KEY_TAB:
                chain = []
                self.collectElementChain(chain, self.getElement(), DOM.eventGetTarget(event))
                item = self.findItemByChain(chain, 0, self.root)
                if item != self.getSelectedItem():
                    self.setSelectedItem(item, True)
        elif type == 'keypress':
            KeyboardListener.fireKeyboardEvent(self, self.keyboardListeners, self, event)
        Widget.onBrowserEvent(self, event)
        self.lastEventType = type
        return

    def remove(self, widget):
        console.error('Widgets should never be directly removed from a tree')

    def removeFocusListener(self, listener):
        self.focusListeners.remove(listener)

    def removeItem(self, item):
        self.root.removeItem(item)
        DOM.removeChild(self.getElement(), item.getElement())

    def removeItems(self):
        while self.getItemCount() > 0:
            self.removeItem(self.getItem(0))

    def removeKeyboardListener(self, listener):
        self.keyboardListeners.remove(listener)

    def removeTreeListener(self, listener):
        self.listeners.remove(listener)

    def setAccessKey(self, key):
        Focus.setAccessKey(self, self.focusable, key)

    def setFocus(self, focus):
        if focus:
            Focus().focus(self.focusable)
        else:
            Focus().blur(self.focusable)

    def setImageBase(self, baseUrl):
        self.imageBase = baseUrl
        self.root.updateStateRecursive()

    def setSelectedItem(self, item, fireEvents=True):
        if item == None:
            if self.curSelection == None:
                return
            self.curSelection.setSelected(False)
            self.curSelection = None
            return
        self.onSelection(item, fireEvents)
        return

    def setTabIndex(self, index):
        Focus.setTabIndex(self, self.focusable, index)

    def treeItemIterator(self):
        accum = []
        self.root.addTreeItems(accum)
        return accum.__iter__()

    def collectElementChain(self, chain, hRoot, hElem):
        if hElem == None or DOM.compare(hElem, hRoot):
            return
        self.collectElementChain(chain, hRoot, DOM.getParent(hElem))
        chain.append(hElem)
        return

    def elementClicked(self, root, hElem):
        chain = []
        self.collectElementChain(chain, self.getElement(), hElem)
        item = self.findItemByChain(chain, 0, root)
        if item != None:
            if DOM.compare(item.getImageElement(), hElem):
                item.setState(not item.getState(), True)
                return True
            elif DOM.isOrHasChild(item.getElement(), hElem):
                self.onSelection(item, True)
                return True
        return False

    def findDeepestOpenChild(self, item):
        if not item.getState():
            return item
        return self.findDeepestOpenChild(item.getChild(item.getChildCount() - 1))

    def findItemByChain(self, chain, idx, root):
        if idx == len(chain):
            return root
        hCurElem = chain[idx]
        for i in range(root.getChildCount()):
            child = root.getChild(i)
            if DOM.compare(child.getElement(), hCurElem):
                retItem = self.findItemByChain(chain, idx + 1, root.getChild(i))
                if retItem == None:
                    return child
                return retItem

        return self.findItemByChain(chain, idx + 1, root)

    def moveFocus(self, selection):
        focusableWidget = selection.getFocusableWidget()
        if focusableWidget != None:
            focusableWidget.setFocus(True)
            DOM.scrollIntoView(focusableWidget.getElement())
        else:
            selectedElem = selection.getContentElem()
            containerLeft = self.getAbsoluteLeft()
            containerTop = self.getAbsoluteTop()
            left = DOM.getAbsoluteLeft(selectedElem) - containerLeft
            top = DOM.getAbsoluteTop(selectedElem) - containerTop
            width = DOM.getIntAttribute(selectedElem, 'offsetWidth')
            height = DOM.getIntAttribute(selectedElem, 'offsetHeight')
            DOM.setIntStyleAttribute(self.focusable, 'left', left)
            DOM.setIntStyleAttribute(self.focusable, 'top', top)
            DOM.setIntStyleAttribute(self.focusable, 'width', width)
            DOM.setIntStyleAttribute(self.focusable, 'height', height)
            DOM.scrollIntoView(self.focusable)
            Focus().focus(self.focusable)
        return

    def moveSelectionDown(self, sel, dig):
        if sel == self.root:
            return
        parent = sel.getParentItem()
        if parent == None:
            parent = self.root
        idx = parent.getChildIndex(sel)
        if not dig or not sel.getState():
            if idx < parent.getChildCount() - 1:
                self.onSelection(parent.getChild(idx + 1), True)
            else:
                self.moveSelectionDown(parent, False)
        elif sel.getChildCount() > 0:
            self.onSelection(sel.getChild(0), True)
        return

    def moveSelectionUp(self, sel, climb):
        parent = sel.getParentItem()
        if parent == None:
            parent = self.root
        idx = parent.getChildIndex(sel)
        if idx > 0:
            sibling = parent.getChild(idx - 1)
            self.onSelection(self.findDeepestOpenChild(sibling), True)
        else:
            self.onSelection(parent, True)
        return

    def onSelection(self, item, fireEvents):
        if item == self.root:
            return
        if self.curSelection != None:
            self.curSelection.setSelected(False)
        self.curSelection = item
        if self.curSelection != None:
            self.moveFocus(self.curSelection)
            self.curSelection.setSelected(True)
            if fireEvents and len(self.listeners):
                for listener in self.listeners:
                    listener.onTreeItemSelected(item)

        return

    def onAttach(self):
        Widget.onAttach(self)
        for child in self:
            child.onAttach()

    def onDetach(self):
        Widget.onDetach(self)
        for child in self:
            child.onDetach()

    def onLoad(self, sender):
        self.root.updateStateRecursive()

    def adopt(self, content):
        self.childWidgets.add(content)
        content.treeSetParent(self)

    def disown(self, item):
        self.childWidgets.remove(item)
        item.treeSetParent(None)
        return

    def fireStateChanged(self, item):
        for listener in self.listeners:
            listener.onTreeItemStateChanged(item)

    def getChildWidgets(self):
        return self.childWidgets

    def shouldTreeDelegateFocusToElement(self, elem):
        return elem.props.node_name == 'select' or elem.props.node_name == 'input' or elem.props.node_name == 'checkbox'


class FocusPanel(SimplePanel):
    """ A simple panel that makes its contents focusable,
        and adds the ability to catch mouse and keyboard events.
    """

    def __init__(self, child=None):
        self.clickListeners = []
        self.focusListeners = []
        self.keyboardListeners = []
        self.mouseListeners = []
        SimplePanel.__init__(self, Focus().createFocusable(self))
        self.sinkEvents(Event.FOCUSEVENTS | Event.KEYEVENTS | Event.ONCLICK | Event.MOUSEEVENTS)
        if child:
            self.setWidget(child)

    def addClickListener(self, listener):
        self.clickListeners.append(listener)

    def addFocusListener(self, listener):
        self.focusListeners.append(listener)

    def addKeyboardListener(self, listener):
        self.keyboardListeners.append(listener)

    def addMouseListener(self, listener):
        self.mouseListeners.append(listener)

    def getTabIndex(self):
        return Focus.getTabIndex(self, self.getElement())

    def onBrowserEvent(self, event):
        type = DOM.eventGetType(event)
        if type == 'click':
            for listener in self.clickListeners:
                if listener.onClick.func_code.co_argcount == 2:
                    listener.onClick(self)
                else:
                    listener.onClick(self, event)

        elif type == 'mousedown' or type == 'mouseup' or type == 'mousemove' or type == 'mouseover' or type == 'mouseout':
            MouseListener().fireMouseEvent(self.mouseListeners, self, event)
        else:
            if type == 'blur' or type == 'focus':
                FocusListener().fireFocusEvent(self.focusListeners, self, event)
            if type == 'keydown' or type == 'keypress' or type == 'keyup':
                KeyboardListener().fireKeyboardEvent(self.keyboardListeners, self, event)

    def removeClickListener(self, listener):
        self.clickListeners.remove(listener)

    def removeFocusListener(self, listener):
        self.focusListeners.remove(listener)

    def removeKeyboardListener(self, listener):
        self.keyboardListeners.remove(listener)

    def removeMouseListener(self, listener):
        self.mouseListeners.remove(listener)

    def setAccessKey(self, key):
        Focus.setAccessKey(self, self.getElement(), key)

    def setFocus(self, focused):
        if focused:
            Focus().focus(self, self.getElement())
        else:
            Focus().blur(self, self.getElement())

    def setTabIndex(self, index):
        Focus.setTabIndex(self, self.getElement(), index)


class Focus():

    def blur(self, elem):
        elem.blur()

    def createFocusable(self):
        e = DOM.createDiv()
        e.props.tab_index = 0
        return e

    def focus(self, elem):
        elem.focus()

    def getTabIndex(self, elem):
        return elem.props.tab_index

    def setAccessKey(self, elem, key):
        elem.props.access_key = key

    def setTabIndex(self, elem, index):
        elem.props.tab_index = index


class FileUpload(Widget):
    """ A widget that wraps the HTML <input type='file'> element.
        This widget must be used with FormPanel if it is to be submitted
        to a server.
    """

    def __init__(self):
        Widget.__init__(self)
        self.setElement(DOM.createElement('input'))
        DOM.setAttribute(self.getElement(), 'type', 'file')
        self.setStyleName('gwt-FileUpload')

    def getFilename(self):
        return DOM.getAttribute(self.getElement(), 'value')

    def getName(self):
        return DOM.getAttribute(self.getElement(), 'name')

    def setName(self, name):
        DOM.setAttribute(self.getElement(), 'name', name)


class Hidden(Widget):
    """ Represents a hidden field in a form.
    """

    def __init__(self, name=None, value=None):
        Widget.__init__(self)
        element = DOM.createElement('input')
        self.setElement(element)
        DOM.setAttribute(element, 'type', 'hidden')
        if name != None:
            self.setName(name)
        if value != None:
            self.setValue(value)
        return

    def getDefaultValue(self):
        return DOM.getAttribute(self.getElement(), 'defaultValue')

    def getName(self):
        return DOM.getAttribute(self.getElement(), 'name')

    def getValue(self):
        return DOM.getAttribute(self.getElement(), 'value')

    def setDefaultValue(self, defaultValue):
        DOM.setAttribute(self.getElement(), 'defaultValue', defaultValue)

    def setName(self, name):
        if name == None:
            console.error('Name cannot be null')
        elif len(name) == 0:
            console.error('Name cannot be an empty string.')
        DOM.setAttribute(self.getElement(), 'name', name)
        return

    def setValue(self, value):
        DOM.setAttribute(self.getElement(), 'value', value)


class NamedFrame(Frame):
    """ A Frame that has a 'name' associated with it.
        This allows the frame to be the target of a FormPanel
    """

    def __init__(self, name):
        Frame.__init__(self)
        div = DOM.createDiv()
        DOM.setInnerHTML(div, "<iframe name='" + name + "'>")
        iframe = DOM.getFirstChild(div)
        self.setElement(iframe)

    def getName(self):
        return DOM.getAttribute(self.getElement(), 'name')


class EventObject():

    def __init__(self, source):
        self.source = source

    def getSource(self):
        return self.source


class FormSubmitEvent(EventObject):

    def __init__(self, source):
        EventObject.__init__(self, source)
        self.cancel = False

    def isCancelled(self):
        return self.cancel

    def setCancelled(self):
        self.cancel = self.cancel


class FormSubmitCompleteEvent(EventObject):

    def __init__(self, source, results):
        EventObject.__init__(self, source)
        self.results = results

    def getResults(self):
        return self.results


FormPanel_formId = 0

class FormPanel(SimplePanel):
    """
        A panel that wraps its contents in an HTML <FORM> element.

        This panel can be used to achieve interoperability with servers
        that accept traditional HTML form encoding. The following widgets
        will be submitted to the server if they are contained within this panel:

        * L{TextBox}
        * L{PasswordTextBox}
        * L{RadioButton}
        * L{CheckBox}
        * L{TextArea}
        * L{ListBox}
        * L{FileUpload}
        * L{Hidden}

        In particular, FileUpload is only useful when used within a
        L{FormPanel}, because the browser will only upload files using
        form submission.
    """
    ENCODING_MULTIPART = 'multipart/form-data'
    ENCODING_URLENCODED = 'application/x-www-form-urlencoded'
    METHOD_GET = 'get'
    METHOD_POST = 'post'

    def __init__(self, target=None):
        global FormPanel_formId
        if hasattr(target, 'getName'):
            target = target.getName()
        SimplePanel.__init__(self, DOM.createForm())
        self.formHandlers = []
        self.iframe = None
        FormPanel_formId += 1
        formName = 'FormPanel_' + str(FormPanel_formId)
        DOM.setAttribute(self.getElement(), 'target', formName)
        DOM.setInnerHTML(self.getElement(), "<iframe name='" + formName + "'>")
        self.iframe = DOM.getFirstChild(self.getElement())
        DOM.setIntStyleAttribute(self.iframe, 'width', 0)
        DOM.setIntStyleAttribute(self.iframe, 'height', 0)
        DOM.setIntStyleAttribute(self.iframe, 'border', 0)
        self.sinkEvents(Event.ONLOAD)
        if target != None:
            self.setTarget(target)
        return

    def addFormHandler(self, handler):
        self.formHandlers.append(handler)

    def getAction(self):
        return DOM.getAttribute(self.getElement(), 'action')

    def getEncoding(self):
        return self.getElement().props.enctype

    def getMethod(self):
        return DOM.getAttribute(self.getElement(), 'method')

    def getTarget(self):
        return DOM.getAttribute(self.getElement(), 'target')

    def getTextContents(self, iframe):
        try:
            if not iframe.props.content_document:
                return
            return iframe.props.content_document.props.body.props.inner_html
        except:
            return

        return

    def _onload(self, form, event, b):
        iframe = event.props.target
        if not iframe._formAction:
            return
        self._listener.onFrameLoad()

    def _onsubmit(self, form, event, b):
        iframe = event.props.target
        if iframe:
            iframe._formAction = form.props.action
        return self.onFormSubmit()

    def hookEvents(self, iframe, form, listener):
        self._listener = listener
        if iframe:
            iframe.connect('browser-event', self._onload)
            iframe.add_event_listener('load', True)
        form.connect('browser-event', self._onsubmit)
        form.add_event_listener('onsubmit', True)

    def onFormSubmit(self):
        event = FormSubmitEvent(self)
        for handler in self.formHandlers:
            handler.onSubmit(event)

        return not event.isCancelled()

    def onFrameLoad(self):
        event = FormSubmitCompleteEvent(self, self.getTextContents(self.iframe))
        for handler in self.formHandlers:
            handler.onSubmitComplete(event)

    def removeFormHandler(self, handler):
        self.formHandlers.remove(handler)

    def setAction(self, url):
        DOM.setAttribute(self.getElement(), 'action', url)

    def setEncoding(self, encodingType):
        form = self.getElement()
        form.props.enctype = encodingType
        form.props.encoding = encodingType

    def setMethod(self, method):
        DOM.setAttribute(self.getElement(), 'method', method)

    def submit(self):
        event = FormSubmitEvent(self)
        for handler in self.formHandlers:
            handler.onSubmit(event)

        if event.isCancelled():
            return
        self.submitImpl(self.getElement(), self.iframe)

    def submitImpl(self, form, iframe):
        if iframe:
            iframe._formAction = form.props.action
        form.submit()

    def onAttach(self):
        SimplePanel.onAttach(self)
        self.hookEvents(self.iframe, self.getElement(), self)

    def onDetach(self):
        SimplePanel.onDetach(self)
        self.unhookEvents(self.iframe, self.getElement())

    def setTarget(self, target):
        DOM.setAttribute(self.getElement(), 'target', target)

    def unhookEvents(self, iframe, form):
        print 'TODO'
        JS('\n        if (iframe)\n            iframe.onload = null;\n        form.onsubmit = null;\n        ')