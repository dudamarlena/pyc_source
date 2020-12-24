# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/pymage/ui.py
# Compiled at: 2007-08-15 13:53:28
__doc__ = '\nGame user interface based on widget objects\n\nThere are three types of coordinate systems when dealing with widgets:\n\nScreen coordinates\n    Absolute coordinates\n\nLocal coordinates\n    Coordinates relative to the origin of the containing widget.  If the\n    widget has no parent, then this is the same as screen coordinates.\n\nBounds coordinates\n    Coordinates relative to the origin of the widget.  If the origin of the\n    widget is (0, 0), then this is the same as local coordinates.\n\n:Variables:\n    left_align : int\n        Left alignment constant for `TextWidget`\n    center_align : int\n        Center alignment constant for `TextWidget`\n    right_align : int\n        Right alignment constant for `TextWidget`\n'
import weakref, pygame
from pygame.locals import *
from pymage import sprites
__author__ = 'Ross Light'
__date__ = 'July 20, 2006'
__all__ = ['left_align',
 'center_align',
 'right_align',
 'Widget',
 'Container',
 'TextWidget',
 'ImageWidget',
 'CursorWidget',
 'ButtonState',
 'StretchState',
 'Button',
 'PushButton']
__docformat__ = 'reStructuredText'
left_align = 0
center_align = 1
right_align = 2

class Widget(object):
    """
    Base class for all UI components.
    
    :IVariables:
        rect : ``pygame.Rect``
            The widget's rectangle in local coordinates.
        parent : `Widget`
            The parent widget.
    """

    def __init__(self, parent=None, rect=Rect(0, 0, 0, 0), cache=False):
        """
        Initialize the widget.
        
        :Parameters:
            parent : `Widget`
                Parent widget
            rect : ``pygame.Rect``
                Initial button size and position
            cache : bool
                Whether to cache the button
        """
        self.__oldRect = None
        self.rect = rect
        self.__children = set()
        self.parent = parent
        self.__updates = [Rect(0, 0, self.rect.width, self.rect.height)]
        if cache:
            self.createCache()
        else:
            self.destroyCache()
        self.__active = False
        return

    def createCache(self):
        """(Re)Creates a cache for the widget."""
        self.__cache = pygame.Surface(self.rect.size).convert_alpha()
        self.refresh()

    def destroyCache(self):
        """Destroys the widget's cache."""
        self.__cache = None
        self.refresh()
        return

    def hasCache(self):
        """Returns whether the widget has a cache."""
        return bool(self.__cache is not None)

    def __len__(self):
        return len(self.__children)

    def __iter__(self):
        return iter(self.__children)

    def children(self):
        """
        Returns a list of all children.
        
        :ReturnType: list
        """
        return list(self.__children)

    def childTree(self, include_self=False, topdown=True):
        """
        Returns an iterator descending the entire child tree.
        
        :Keywords:
            include_self : bool
                Specifies whether the widget is included in the iterator.
            topdown : bool
                Specifies whether to go from widget to bottom or from bottom to
                widget.
        :ReturnType: iterator
        """
        if include_self and topdown:
            yield self
        for child in self.__children:
            tree = child.childTree(include_self=True, topdown=topdown)
            for subchild in tree:
                yield subchild

        if include_self and not topdown:
            yield self

    def addChild(self, child):
        """
        Adds a child widget.
        
        :Parameters:
            child : `Widget`
                New child to add
        """
        self.__children.add(child)
        child.parent = self

    def addChildren(self, children):
        """
        Adds children widgets.
        
        :Parameters:
            child : list of `Widget` objects
                New children to add
        """
        self.__children.update(frozenset(children))
        for child in children:
            child.parent = self

    def removeChild(self, child):
        """
        Removes a child widget.
        
        :Parameters:
            child : `Widget`
                Child to remove
        """
        self.__children.remove(child)
        del child.parent

    def removeAllChildren(self):
        """Removes all child widgets."""
        children = list(self.__children)
        self.__children.clear()
        for child in children:
            del child.parent

    def _getParent(self):
        """Retrieves the widget's parent."""
        if self.__parent is None:
            return
        else:
            parent = self.__parent()
            if parent is None:
                self.__parent = None
            return parent
        return

    def _setParent(self, new_parent):
        """Changes the widget's parent, and removes it from the old one."""
        self._delParent()
        if new_parent is None:
            self.__parent = new_parent
        else:
            if self not in new_parent.children():
                new_parent.addChild(self)
            self.__parent = weakref.ref(new_parent)
        return

    def _delParent(self):
        """Remove the widget from its parent."""
        try:
            if self.__parent is not None:
                parent = self.__parent()
                if parent is not None and self in parent:
                    parent.removeChild(self)
        except AttributeError:
            pass

        self.__parent = None
        return

    @property
    def root(self):
        """The root of the hierarchy."""
        widget = self
        while True:
            parent = widget.parent
            if parent is None:
                break
            widget = parent

        return widget

    parent = property(_getParent, _setParent, _delParent)

    def handle(self, event):
        """
        Handles a single event.
        
        Override to perform custom event-handling.  Default implementation
        returns ``False``.
        
        :Parameters:
            event : ``pygame.event.Event``
                The event to handle.
        :Returns: ``True`` if the event was handled successfully, ``False``
                  otherwise.
        :ReturnType: bool
        """
        return False

    def processEvent(self, event):
        """
        Process an event.
        
        The event will start at a certain widget and traverse up the child
        hierarchy until the event is handled or the root is reached.  The
        starting widget is dependent on what the event type is:
        
        * If the event is a mouse event, the widget that the mouse is/was over.
        * Otherwise, the active widget.
        
        .. Note:: Do not override this method to perform event handling;
                  instead, override the `handle` method.
        
        :Parameters:
            event : ``pygame.event.Event``
                The event to process.
        :Returns: Whether the event was processed successfully.
        :ReturnType: bool
        """
        if event.type in (MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION):
            tree = self.root.childTree(include_self=True, topdown=False)
            for child in tree:
                if child.screenRect().collidepoint(*event.pos):
                    widget = child
                    break
            else:
                widget = None
        else:
            widget = self.root.activeWidget()
        while widget is not None:
            if widget.handle(event):
                return True
            widget = widget.parent
        else:
            return False

        return

    def canFocus(self):
        """
        Returns whether the widget can be focused.
        
        Default returns ``False``.
        
        :ReturnType: bool
        """
        return False

    def focus(self, force_blur=False, force_focus=False):
        """
        Makes the widget the active one.
        
        .. Tip:: You may extend this implementation to perform custom handling,
                 but always call this implementation to actually focus the
                 widget.
        
        :Keywords:
            force_blur : bool
                Whether to force the currently active widget to blur.
            force_focus : bool
                Whether to force the widget to focus.
        :Returns: Whether the focus was successful.
        :ReturnType: bool
        """
        if force_focus or self.canFocus():
            activeWidget = self.root.activeWidget()
            if activeWidget is None or activeWidget.blur(force=force_blur):
                self.__active = True
                return True
            else:
                return False
        else:
            return False
        return

    def canBlur(self):
        """
        Returns whether the widget can be blurred.
        
        Default returns ``True``.
        
        :ReturnType: bool
        """
        return True

    def blur(self, force=False):
        """
        Makes the widget inactive.
        
        .. Tip:: You may extend this implementation to perform custom handling,
                 but always call this implementation to actually blur the
                 widget.
        
        :Keywords:
            force : bool
                Whether to force the widget to blur.
        :Returns: Whether the blur was successful.
        :ReturnType: bool
        """
        if force or self.canBlur():
            self.__active = False
            return True
        else:
            return False

    def activeWidget(self):
        """
        Find the current active widget.
        
        .. Caution:: This only traverses from the receiver down.
        
        :Returns: The current active widget, or ``None`` if there is not one.
        :ReturnType: `Widget`
        """
        for child in self.childTree(include_self=True):
            if child.isActive():
                return child
        else:
            return

        return

    def isActive(self):
        """
        Returns whether the widget is active.
        
        :ReturnType: bool
        """
        return self.__active

    def display(self, surface=None, origin=(0, 0)):
        """
        Display the widget on the given surface.
        
        .. Note:: You *shouldn't* have to override this method.  Instead, you
                  should override the `draw` method.
        
        :Parameters:
            surface : ``pygame.Surface``
                The surface to display on.  If this is not specified, the
                current display surface is used.
            origin : tuple
                The point in local space to use as the origin.  If not given,
                (0, 0) is used.
        :Returns: A list of ``pygame.Rect`` objects that need to be
                  updated
        :ReturnType: list of ``pygame.Rect`` objects
        """
        screenUpdates = []
        if surface is None:
            surface = pygame.display.get_surface()
        if self.__oldRect != self.rect:
            if self.__oldRect is not None:
                screenUpdates.append(self.__oldRect.move(origin))
            self.rectChanged(self.__oldRect, Rect(self.rect))
            if self.hasCache():
                self.createCache()
            screenUpdates.append(self.rect.move(origin))
            self.__oldRect = Rect(self.rect)
        if self.__updates:
            region = self.__updates[0].unionall(self.__updates[1:])
            del self.__updates[:]
        else:
            region = None
        if self.hasCache():
            drawSurf = self.__cache
            if region is not None:
                self.draw(drawSurf, region)
        else:
            drawSurf = pygame.Surface(self.rect.size).convert_alpha(surface)
            self.draw(drawSurf, self.bounds())
        surface.blit(drawSurf, self.rect.move(origin))
        if region is not None:
            screenUpdates.append(self.btlrect(region, origin))
        childOrigin = self.rect.move(origin).topleft
        for child in self.__children:
            screenUpdates.extend(child.display(surface, childOrigin))

        return screenUpdates

    def draw(self, surface, rect):
        """
        Performs the actual drawing.
        
        Default implementation clears the surface to a transparent color.
        
        :Parameters:
            surface : ``pygame.Surface``
                Surface to draw onto.
            rect : ``pygame.Rect``
                Portion of the widget that needs to be refreshed.  This is only
                a guideline; you can update wherever you want.
        """
        surface.fill((0, 0, 0, 0), rect)

    def refresh(self, rect=None):
        """
        Inform the widget that a given portion needs to be refreshed.
        
        :Parameters:
            rect : ``pygame.Rect``
                The portion of the widget, in local space, that needs to be
                refreshed.  If not given, the entire widget will be refreshed.
        """
        if rect is None:
            rect = Rect(0, 0, self.rect.width, self.rect.height)
        self.__updates.append(Rect(rect))
        return

    def update(self):
        """
        Updates the widget.
        
        Default implementation calls `update` on child widgets.
        """
        for child in self.__children:
            child.update()

    def stlrect(self, rect, origin=(0, 0)):
        """
        Converts from a screen rectangle to a local rectangle.
        
        :Parameters:
            rect : ``pygame.Rect``
                Rectangle to convert
            origin : tuple
                The point to consider the origin; default is (0, 0).
        :Returns: The converted rectangle
        :ReturnType: ``pygame.Rect``
        """
        rect = Rect(rect)
        origin = self._localOrigin(origin)
        return rect.move(-origin[0], -origin[1])

    def stbrect(self, rect, origin=(0, 0)):
        """
        Converts from a screen rectangle to a bounds rectangle.
        
        :Parameters:
            rect : ``pygame.Rect``
                Rectangle to convert
            origin : tuple
                The point to consider the origin; default is (0, 0).
        :Returns: The converted rectangle
        :ReturnType: ``pygame.Rect``
        """
        rect = Rect(rect)
        origin = self._boundsOrigin(origin)
        return rect.move(-origin[0], -origin[1])

    def ltsrect(self, rect, origin=(0, 0)):
        """
        Converts from a local rectangle to a screen rectangle.
        
        :Parameters:
            rect : ``pygame.Rect``
                Rectangle to convert
            origin : tuple
                The point to consider the origin; default is (0, 0).
        :Returns: The converted rectangle
        :ReturnType: ``pygame.Rect``
        """
        rect = Rect(rect)
        origin = self._localOrigin(origin)
        return rect.move(origin[0], origin[1])

    def ltbrect(self, rect, origin=(0, 0)):
        """
        Converts from a local rectangle to a bounds rectangle.
        
        :Parameters:
            rect : ``pygame.Rect``
                Rectangle to convert
            origin : tuple
                The point to consider the origin; default is (0, 0).
        :Returns: The converted rectangle
        :ReturnType: ``pygame.Rect``
        """
        rect = Rect(rect)
        origin = self.rect.topleft
        return rect.move(-origin[0], -origin[1])

    def btsrect(self, rect, origin=(0, 0)):
        """
        Converts from a bounds rectangle to a screen rectangle.
        
        :Parameters:
            rect : ``pygame.Rect``
                Rectangle to convert
            origin : tuple
                The point to consider the origin; default is (0, 0).
        :Returns: The converted rectangle
        :ReturnType: ``pygame.Rect``
        """
        rect = Rect(rect)
        origin = self._boundsOrigin(origin)
        return rect.move(origin[0], origin[1])

    def btlrect(self, rect, origin=(0, 0)):
        """
        Converts from a bounds rectangle to a screen rectangle.
        
        :Parameters:
            rect : ``pygame.Rect``
                Rectangle to convert
            origin : tuple
                The point to consider the origin; default is (0, 0).
        :Returns: The converted rectangle
        :ReturnType: ``pygame.Rect``
        """
        rect = Rect(rect)
        origin = self.rect.topleft
        return rect.move(origin[0], origin[1])

    def stlpoint(self, point, origin=(0, 0)):
        """
        Converts from a screen point to a local point.
        
        :Parameters:
            point : tuple
                Point to convert
            origin : tuple
                The point to consider the origin; default is (0, 0).
        :Returns: The converted point
        :ReturnType: tuple
        """
        origin = self._localOrigin(origin)
        return (
         point[0] - origin[0], point[1] - origin[1])

    def stbpoint(self, point, origin=(0, 0)):
        """
        Converts from a screen point to a bounds point.
        
        :Parameters:
            point : tuple
                Point to convert
            origin : tuple
                The point to consider the origin; default is (0, 0).
        :Returns: The converted point
        :ReturnType: tuple
        """
        origin = self._boundsOrigin(origin)
        return (
         point[0] - origin[0], point[1] - origin[1])

    def ltspoint(self, point, origin=(0, 0)):
        """
        Converts from a local point to a screen point.
        
        :Parameters:
            point : tuple
                Point to convert
            origin : tuple
                The point to consider the origin; default is (0, 0).
        :Returns: The converted point
        :ReturnType: tuple
        """
        origin = self._localOrigin(origin)
        return (
         point[0] + origin[0], point[1] + origin[1])

    def ltbpoint(self, point, origin=(0, 0)):
        """
        Converts from a local point to a bounds point.
        
        :Parameters:
            point : tuple
                Point to convert
            origin : tuple
                The point to consider the origin; default is (0, 0).
        :Returns: The converted point
        :ReturnType: tuple
        """
        origin = self.rect.topleft
        return (
         point[0] - origin[0], point[1] - origin[1])

    def btspoint(self, point, origin=(0, 0)):
        """
        Converts from a bounds point to a screen point.
        
        :Parameters:
            point : tuple
                Point to convert
            origin : tuple
                The point to consider the origin; default is (0, 0).
        :Returns: The converted point
        :ReturnType: tuple
        """
        origin = self._boundsOrigin(origin)
        return (
         point[0] + origin[0], point[1] + origin[1])

    def btlpoint(self, point, origin=(0, 0)):
        """
        Converts from a bounds point to a local point.
        
        :Parameters:
            point : tuple
                Point to convert
            origin : tuple
                The point to consider the origin; default is (0, 0).
        :Returns: The converted point
        :ReturnType: tuple
        """
        origin = self.rect.topleft
        return (
         point[0] + origin[0], point[1] + origin[1])

    def _localOrigin(self, origin=(0, 0)):
        """Returns the local origin as screen coordinates."""
        origin = self.screenRect(origin).topleft
        return (
         origin[0] - self.rect.x, origin[1] - self.rect.y)

    def _boundsOrigin(self, origin=(0, 0)):
        """Returns the bounds origin as screen coordinates."""
        return self.screenRect(origin).topleft

    def screenRect(self, origin=(0, 0)):
        """
        Calculates the screen rectangle.
        
        :Parameters:
            origin : tuple
                The point to consider the origin; default is (0, 0).
        :Returns: The widget's rectangle in screen coordinates
        :ReturnType: ``pygame.Rect``
        """
        rect = Rect(self.rect)
        parent = self.parent
        while parent is not None:
            rect.move_ip(parent.rect.topleft)
            parent = parent.parent

        rect.move_ip(origin)
        return rect

    def bounds(self):
        """
        Returns the rectangle that can be drawn in.
        
        :ReturnType: ``pygame.Rect``
        """
        return Rect(0, 0, self.rect.width, self.rect.height)

    def optimalSize(self):
        """
        Returns the optimal size of the widget.
        
        Default returns ``None``, but subclasses can override to return an
        actual value.
        
        :Returns: The optimal size, or ``None`` if one cannot be calculated.
        :ReturnType: tuple
        """
        return

    def pack(self, anchor=None):
        """
        Changes the widget's rect to the optimal size.
        
        If `optimalSize` returns None, this does nothing.
        
        .. Tip:: For best results, specify a corner (e.g. topleft) for anchor.
        
        :Parameters:
            anchor : string
                A corner/edge attribute name that will remain constant after the
                resize.
        """
        if anchor is not None:
            anchorValue = getattr(self.rect, anchor)
        size = self.optimalSize()
        if size is not None:
            self.rect.size = size
            if anchor is not None:
                setattr(self.rect, anchor, anchorValue)
        return

    def rectChanged(self, old_rect, new_rect):
        """
        Hook method for the rectangle changing.
        
        This is called before `display` does any drawing.
        
        :Parameters:
            old_rect : ``pygame.Rect``
                The old rectangle in local coordinates
            new_rect : ``pygame.Rect``
                The new rectangle in local coordinates
        """
        pass

    def _getRect(self):
        return self.__rect

    def _setRect(self, new_rect):
        self.__rect = Rect(new_rect)

    rect = property(_getRect, _setRect)


class Container(Widget):
    """
    A widget that is designed to contain other widgets.
    
    :IVariables:
        border : int
            The border width (in pixels).
        borderColor : tuple
            The border color as an RGBA 0-255 tuple
        bgColor : tuple
            The background color as an RGBA 0-255 tuple
    """

    def __init__(self, border=0, border_color=(0, 0, 0, 255), bg_color=(0, 0, 0, 0), *args, **kw):
        super(Container, self).__init__(*args, **kw)
        self.border = border
        self.borderColor = border_color
        self.bgColor = bg_color

    def draw(self, surface, rect):
        surface.fill(self.bgColor, rect)
        if self.border > 0:
            pygame.draw.rect(surface, self.borderColor, self.bounds(), self.border)

    def optimalSize(self):
        childRects = [ child.rect for child in self.children() ]
        if childRects:
            allChildRect = childRects[0].union_all(childRects[1:])
            return (
             allChildRect.x + allChildRect.width,
             allChildRect.y + allChildRect.height)
        else:
            return
        return


class TextWidget(Widget):
    """
    A widget that can display a single line of text.
    
    :IVariables:
        text : string
            The text the widget displays.
        font : ``pygame.font.Font``
            The font the text is displayed as.  Default is the pygame default
            font at size 14.
        fgColor : tuple
            The text color as an RGBA 0-255 tuple.  Default is black.
        bgColor : tuple
            The background color as an RGBA 0-255 tuple.  Default is clear.
        antialias : bool
            Whether or not to antialias the text.  Default is ``True``.
        align : int
            The alignment as a constant (i.e. `left_align`, `center_align`, or
            `right_align`).  The default is left alignment.
        shadow : bool
            Whether or not to add a *cheap* shadow.  Default is ``False``.
        shadowColor : tuple
            The shadow color as an RGBA 0-255 tuple.  Default is a
            half-transparent black.
    """
    fgColor = (0, 0, 0, 255)
    bgColor = (0, 0, 0, 0)
    antialias = True
    shadow = False
    shadowColor = (0, 0, 0, 128)

    def __init__(self, text='', font=None, *args, **kw):
        """
        Initializes a text widget.
        
        The additional variables can be specified via keyword arguments.
        """
        self.fgColor = kw.pop('fgColor', self.fgColor)
        self.bgColor = kw.pop('bgColor', self.bgColor)
        self.antialias = kw.pop('antialias', self.antialias)
        self.align = kw.pop('align', left_align)
        self.shadow = kw.pop('shadow', self.shadow)
        super(TextWidget, self).__init__(*args, **kw)
        self.text = text
        if font is None:
            font = pygame.font.Font(None, 14)
        self.font = font
        return

    def draw(self, surface, rect):
        surface.fill(self.bgColor, rect)
        rendered = self.font.render(self.text, self.antialias, self.fgColor)
        textRect = rendered.get_rect()
        alignPoints = {left_align: 'topleft', center_align: 'midtop', 
           right_align: 'topright'}
        setattr(textRect, alignPoints[self.align], getattr(self.bounds(), alignPoints[self.align]))
        if self.shadow:
            renderedShadow = self.font.render(self.text, self.antialias, self.shadowColor)
            shadowRect = textRect.move(0, 2)
        else:
            renderedShadow = None
            shadowRect = None
        if renderedShadow is not None and shadowRect.colliderect(rect):
            surface.blit(renderedShadow, shadowRect)
        if textRect.colliderect(rect):
            surface.blit(rendered, textRect)
        return

    def optimalSize(self):
        return self.font.size(self.text)

    def _getText(self):
        """Retrieve text value."""
        return self._text

    def _setText(self, text):
        """Change text value and refresh."""
        self._text = text
        self.refresh()

    def _getFont(self):
        """Retrieve font."""
        return self._font

    def _setFont(self, font):
        """Change font and refresh."""
        self._font = font
        self.refresh()

    def _getAlign(self):
        """Retrieve alignment."""
        return self._align

    def _setAlign(self, align):
        """Change alignment and validate."""
        if align in (left_align, center_align, right_align):
            self._align = align
        else:
            raise ValueError('Alignment %r is not valid' % align)

    text = property(_getText, _setText)
    font = property(_getFont, _setFont)
    align = property(_getAlign, _setAlign)


class ImageWidget(Widget):
    """
    A widget that displays an image.
    
    :IVariables:
        image : ``pygame.Surface``
            The image the widget displays.
        stretch : bool
            Whether to stretch the image to fit the size.
    """

    def __init__(self, image, stretch=False, *args, **kw):
        super(ImageWidget, self).__init__(*args, **kw)
        self.image = image
        self.stretch = stretch

    def draw(self, surface, rect):
        super(ImageWidget, self).draw(surface, rect)
        image = self.image
        if self.stretch and self.rect.size != image.get_size():
            image = pygame.transform.scale(self.image, rect.size)
        surface.blit(image, (0, 0), rect)

    def getImage(self):
        """
        Retrieves the current image.
        
        You can also use the ``image`` property.
        """
        return self.__image

    def setImage(self, image, tryIM=True):
        """
        Changes the current image.
        
        You can also use the ``image`` property, but it always tries
        `sprites.ImageManager`.
        """
        self.__image = sprites.getImage(image, tryIM)
        self.refresh()

    def optimalSize(self):
        return self.image.get_size()

    image = property(getImage, setImage)


class CursorWidget(ImageWidget):
    """
    A widget that displays an image, following the cursor.
    
    :IVariables:
        hotspot : tuple
            The location of the cursor's "hotspot".  When the mouse is clicked,
            the hotspot is the place where the mouse position is registered.
    """

    def __init__(self, hotspot=(0, 0), *args, **kw):
        super(CursorWidget, self).__init__(*args, **kw)
        self.hotspot = hotspot
        self.followMouse()

    def handle(self, event):
        if event.type == MOUSEMOTION:
            self.followMouse(event.pos)
            return True
        else:
            return False

    def followMouse(self, pos=None):
        """
        Called to follow the mouse.
        
        :Parameters:
            pos : tuple
                The position where the mouse is.  If not given, the position is
                retrieved with ``pygame.mouse.get_pos``.
        """
        if pos is None:
            pos = pygame.mouse.get_pos()
        self.rect.topleft = self.stlpoint((pos[0] - self.hotspot[0],
         pos[1] - self.hotspot[1]))
        return


class ButtonState(object):
    """A button state."""

    def setState(self, button):
        """
        Called to change the button into the given state.
        
        :Parameters:
            button : `Button`
                The button whose state is changing.
        """
        pass

    def unsetState(self, button):
        """
        Called to undo the effects of `setState`.
        
        :Parameters:
            button : `Button`
                The button whose state is being undone.
        """
        pass

    def optimalSize(self):
        """Returns the optimal size of the button, or ``None``."""
        return


class StretchState(ButtonState):
    """
    A button state in which three images are used.
    
    Two are used for caps, and the center is stretched to fit the text.
    
    :IVariables:
        text : string
            The text being displayed on the button.
        textColor : tuple
            The text color as an RGBA 0-255 tuple.
        imgL : ``pygame.Surface``
            The left image cap.
        imgC : ``pygame.Surface``
            The stretched center image.
        imgR : ``pygame.Surface``
            The right image cap.
    """

    def __init__(self, text, textColor, imgL, imgC, imgR):
        self.text = text
        self.textColor = textColor
        self.imgL = sprites.getImage(imgL)
        self.imgC = sprites.getImage(imgC)
        self.imgR = sprites.getImage(imgR)

    def setState(self, button):
        lrect = Rect(0, 0, 0, 0)
        lrect.size = self.imgL.get_size()
        lrect.topleft = (0, 0)
        rrect = Rect(0, 0, 0, 0)
        rrect.size = self.imgR.get_size()
        rrect.topright = (button.rect.width, 0)
        crect = Rect(0, 0, 0, 0)
        crect.height = self.imgC.get_height()
        crect.width = rrect.left - lrect.right
        crect.topleft = lrect.topright
        ImageWidget(self.imgL, parent=button, rect=lrect)
        ImageWidget(self.imgC, stretch=True, parent=button, rect=crect)
        ImageWidget(self.imgR, parent=button, rect=rrect)
        TextWidget(self.text, font=self.getFont(), align=center_align, fgColor=self.textColor, parent=button, rect=crect)

    def unsetState(self, button):
        button.removeAllChildren()

    def getFont(self):
        return pygame.font.Font(None, self.imgC.get_height())

    def optimalSize(self):
        font = self.getFont()
        width = self.imgL.get_width() + font.size(self.text)[0] + self.imgR.get_width()
        height = self.imgC.get_height()
        return (
         width, height)


class Button(Widget):
    """
    Abstract superclass for buttons.
    
    :IVariables:
        state : `ButtonState`
            The button's current state
        callback : function
            The button's action callback
        callArgs : tuple
            Additional arguments passed to the button's callback
        callKw : dict
            Additional keyword arguments passed to the button's callback
        nav_up : `Widget`
            The widget activated by pressing the up arrow key.
        nav_down : `Widget`
            The widget activated by pressing the down arrow key.
        nav_left : `Widget`
            The widget activated by pressing the left arrow key.
        nav_right : `Widget`
            The widget activated by pressing the right arrow key.
    """

    def __init__(self, state, callback=None, args=[], kw={}, *initArgs, **initKw):
        """
        Initializes the button.
        
        :Parameters:
            state : `ButtonState`
                Initial button state.
            callback : function
                Button's action callback
            args : tuple
                Additional callback arguments
            kw : dict
                Additional callback keyword arguments
            parent : `Widget`
                Parent widget
            rect : ``pygame.Rect``
                Initial button size and position
            cache : bool
                Whether to cache the button
        :Keywords:
            up : `Widget`
                The widget activated by pressing the up arrow key.
            down : `Widget`
                The widget activated by pressing the down arrow key.
            left : `Widget`
                The widget activated by pressing the left arrow key.
            right : `Widget`
                The widget activated by pressing the right arrow key.
        """
        self.nav_up = initKw.pop('up', None)
        self.nav_down = initKw.pop('down', None)
        self.nav_left = initKw.pop('left', None)
        self.nav_right = initKw.pop('right', None)
        super(Button, self).__init__(*initArgs, **initKw)
        self.setState(state)
        self.callback = callback
        self.callArgs = args
        self.callKw = kw
        return

    def handle(self, event):
        keyButtons = {K_UP: self.nav_up, K_DOWN: self.nav_down, 
           K_LEFT: self.nav_left, 
           K_RIGHT: self.nav_right}
        hatButtons = {(0, 1): self.nav_up, (0, -1): self.nav_down, 
           (-1, 0): self.nav_left, 
           (1, 0): self.nav_right}
        if event.type == KEYUP and keyButtons.get(event.key) is not None:
            keyButtons[event.key].focus()
            return True
        elif event.type == JOYHATMOTION and hatButtons.get(event.value) is not None:
            hatButtons[event.value].focus()
            return True
        else:
            return False
        return

    def setState(self, new_state):
        try:
            oldState = self.state
        except AttributeError:
            pass
        else:
            if oldState == new_state:
                return
            oldState.unsetState(self)

        self.state = new_state
        self.state.setState(self)

    def perform(self):
        """Calls the button's callback."""
        if self.callback is not None:
            self.callback(self, *self.callArgs, **self.callKw)
        return

    def optimalSize(self):
        """Sizes the button to the optimum size."""
        return self.state.optimalSize()

    def rectChanged(self, old_rect, new_rect):
        self.state.unsetState(self)
        self.state.setState(self)

    def __getattribute__(self, name):
        value = super(Button, self).__getattribute__(name)
        if name.startswith('nav_') and value is not None:
            value = value()
            if value is None:
                setattr(self, name, None)
        return value

    def __setattr__(self, name, value):
        if name.startswith('nav_') and value is not None:
            value = weakref.ref(value)
        super(Button, self).__setattr__(name, value)
        return


class PushButton(Button):
    """
    Button activated by clicking or pressing Enter while active.
    
    :IVariables:
        normState : `ButtonState`
            The inactive state
        rollState : `ButtonState`
            The active state
    """

    def __init__(self, normState, rollState=None, *args, **kw):
        """
        Initializes the button.
        
        :Parameters:
            normState : `ButtonState`
                The inactive state
            rollState : `ButtonState`
                The active state
            callback : function
                Button's action callback
            args : tuple
                Additional callback arguments
            kw : dict
                Additional callback keyword arguments
            parent : `Widget`
                Parent widget
            rect : ``pygame.Rect``
                Initial button size and position
            cache : bool
                Whether to cache the button
        :Keywords:
            up : `Widget`
                The widget activated by pressing the up arrow key.
            down : `Widget`
                The widget activated by pressing the down arrow key.
            left : `Widget`
                The widget activated by pressing the left arrow key.
            right : `Widget`
                The widget activated by pressing the right arrow key.
        """
        super(PushButton, self).__init__(normState, *args, **kw)
        self.normState = normState
        if rollState is None:
            self.rollState = self.normState
        else:
            self.rollState = rollState
        self._lastMousePos = pygame.mouse.get_pos()
        return

    def handle(self, event):
        if super(PushButton, self).handle(event):
            return True
        elif event.type == MOUSEBUTTONUP and event.button == 1 or event.type == KEYUP and event.key == K_RETURN or event.type == JOYBUTTONUP and event.button == 0:
            self.perform()
            return True
        else:
            return False

    def update(self):
        mousePos = pygame.mouse.get_pos()
        if mousePos != self._lastMousePos:
            self._lastMousePos = mousePos
            mouseInButton = self.screenRect().collidepoint(mousePos)
            if not self.isActive() and mouseInButton:
                self.focus()
            elif self.isActive() and not mouseInButton:
                self.blur()

    def canFocus(self):
        return True

    def focus(self, *args, **kw):
        success = super(PushButton, self).focus(*args, **kw)
        if success:
            self.setState(self.rollState)
        return success

    def blur(self, *args, **kw):
        success = super(PushButton, self).blur(*args, **kw)
        if success:
            self.setState(self.normState)
        return success