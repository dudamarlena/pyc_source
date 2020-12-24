# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/link.py
# Compiled at: 2013-04-04 15:36:35
"""Used to create external or internal URL links."""
from muntjac.ui.abstract_component import AbstractComponent
from muntjac.ui.window import Window

class Link(AbstractComponent):
    """Link is used to create external or internal URL links.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """
    CLIENT_WIDGET = None
    TARGET_BORDER_NONE = Window.BORDER_NONE
    TARGET_BORDER_MINIMAL = Window.BORDER_MINIMAL
    TARGET_BORDER_DEFAULT = Window.BORDER_DEFAULT

    def __init__(self, caption=None, resource=None, targetName=None, width=None, height=None, border=None):
        """Creates a new instance of Link.

        @param caption:
                   the Link text.
        @param resource:
        @param targetName:
                   the name of the target window where the link opens to. Empty
                   name of null implies that the target is opened to the window
                   containing the link.
        @param width:
                   the Width of the target window.
        @param height:
                   the Height of the target window.
        @param border:
                   the Border style of the target window.
        """
        super(Link, self).__init__()
        self._resource = None
        self._targetName = None
        self._targetBorder = self.TARGET_BORDER_DEFAULT
        self._targetWidth = -1
        self._targetHeight = -1
        if caption is not None:
            self.setCaption(caption)
        if resource is not None:
            self._resource = resource
        if targetName is not None:
            self.setTargetName(targetName)
        if width is not None:
            self.setTargetWidth(width)
        if height is not None:
            self.setTargetHeight(height)
        if border is not None:
            self.setTargetBorder(border)
        return

    def paintContent(self, target):
        """Paints the content of this component.

        @param target:
                   the Paint Event.
        @raise PaintException:
                    if the paint operation failed.
        """
        if self._resource is not None:
            target.addAttribute('src', self._resource)
        else:
            return
        name = self.getTargetName()
        if name is not None and len(name) > 0:
            target.addAttribute('name', name)
        if self.getTargetWidth() >= 0:
            target.addAttribute('targetWidth', self.getTargetWidth())
        if self.getTargetHeight() >= 0:
            target.addAttribute('targetHeight', self.getTargetHeight())
        test = self.getTargetBorder()
        if test == self.TARGET_BORDER_MINIMAL:
            target.addAttribute('border', 'minimal')
        elif test == self.TARGET_BORDER_NONE:
            target.addAttribute('border', 'none')
        return

    def getTargetBorder(self):
        """Returns the target window border.

        @return: the target window border.
        """
        return self._targetBorder

    def getTargetHeight(self):
        """Returns the target window height or -1 if not set.

        @return: the target window height.
        """
        if self._targetHeight < 0:
            return -1
        return self._targetHeight

    def getTargetName(self):
        """Returns the target window name. Empty name of null implies
        that the target is opened to the window containing the link.

        @return: the target window name.
        """
        return self._targetName

    def getTargetWidth(self):
        """Returns the target window width or -1 if not set.

        @return: the target window width.
        """
        if self._targetWidth < 0:
            return -1
        return self._targetWidth

    def setTargetBorder(self, targetBorder):
        """Sets the border of the target window.

        @param targetBorder:
                   the targetBorder to set.
        """
        if targetBorder == self.TARGET_BORDER_DEFAULT or targetBorder == self.TARGET_BORDER_MINIMAL or targetBorder == self.TARGET_BORDER_NONE:
            self._targetBorder = targetBorder
            self.requestRepaint()

    def setTargetHeight(self, targetHeight):
        """Sets the target window height.

        @param targetHeight:
                   the targetHeight to set.
        """
        self._targetHeight = targetHeight
        self.requestRepaint()

    def setTargetName(self, targetName):
        """Sets the target window name.

        @param targetName:
                   the targetName to set.
        """
        self._targetName = targetName
        self.requestRepaint()

    def setTargetWidth(self, targetWidth):
        """Sets the target window width.

        @param targetWidth:
                   the targetWidth to set.
        """
        self._targetWidth = targetWidth
        self.requestRepaint()

    def getResource(self):
        """Returns the resource this link opens.

        @return: the Resource.
        """
        return self._resource

    def setResource(self, resource):
        """Sets the resource this link opens.

        @param resource:
                   the resource to set.
        """
        self._resource = resource
        self.requestRepaint()