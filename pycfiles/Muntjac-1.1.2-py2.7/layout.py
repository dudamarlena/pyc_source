# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/ui/layout.py
# Compiled at: 2013-04-04 15:36:35
"""Defines an extension to the C{IComponentContainer} interface which adds the
layouting control to the elements in the container."""
from muntjac.ui.component_container import IComponentContainer
from muntjac.terminal.gwt.client.ui.v_margin_info import VMarginInfo
from muntjac.terminal.gwt.client.ui.alignment_info import Bits

class ILayout(IComponentContainer):
    """Extension to the L{IComponentContainer} interface which adds the
    layouting control to the elements in the container. This is required by
    the various layout components to enable them to place other components in
    specific locations in the UI.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def setMargin(self, *args):
        """Enable layout margins. Affects all four sides of the layout. This
        will tell the client-side implementation to leave extra space around
        the layout. The client-side implementation decides the actual amount,
        and it can vary between themes.

        Alternatively, enable specific layout margins. This will tell the
        client-side implementation to leave extra space around the layout in
        specified edges, clockwise from top (top, right, bottom, left). The
        client-side implementation decides the actual amount, and it can vary
        between themes.

        @param args: tuple of the form
            - (enabled)
            - (top, right, bottom, left)
        """
        raise NotImplementedError


class IAlignmentHandler(object):
    """IAlignmentHandler is most commonly an advanced L{ILayout} that
    can align its components.
    """
    ALIGNMENT_LEFT = Bits.ALIGNMENT_LEFT
    ALIGNMENT_RIGHT = Bits.ALIGNMENT_RIGHT
    ALIGNMENT_TOP = Bits.ALIGNMENT_TOP
    ALIGNMENT_BOTTOM = Bits.ALIGNMENT_BOTTOM
    ALIGNMENT_HORIZONTAL_CENTER = Bits.ALIGNMENT_HORIZONTAL_CENTER
    ALIGNMENT_VERTICAL_CENTER = Bits.ALIGNMENT_VERTICAL_CENTER

    def setComponentAlignment(self, *args):
        """Set alignment for one contained component in this layout. Alignment
        is calculated as a bit mask of the two passed values or predefined
        alignments from Alignment class.

        Example::
             layout.setComponentAlignment(myComponent, Alignment.TOP_RIGHT)

        @deprecated: Use L{setComponentAlignment} instead

        @param args: tuple of the form
            - (childComponent, horizontalAlignment, verticalAlignment)
              1. the component to align within it's layout cell.
              2. the horizontal alignment for the child component (left,
                 center, right). Use ALIGNMENT constants.
              3. the vertical alignment for the child component (top,
                 center, bottom). Use ALIGNMENT constants.
            - (childComponent, alignment)
              1. the component to align within it's layout cell.
              2. the Alignment value to be set
        """
        raise NotImplementedError

    def getComponentAlignment(self, childComponent):
        """Returns the current Alignment of given component.

        @return: the L{Alignment}
        """
        raise NotImplementedError


class ISpacingHandler(object):
    """This type of layout supports automatic addition of space between its
    components.
    """

    def setSpacing(self, enabled):
        """Enable spacing between child components within this layout.

        B{NOTE:} This will only affect the space between
        components, not the space around all the components in the layout
        (i.e. do not confuse this with the cellspacing attribute of a HTML
        Table). Use L{setMargin} to add space around the layout.

        See the reference manual for more information about CSS rules for
        defining the amount of spacing to use.

        @param enabled:
                   true if spacing should be turned on, false if it should be
                   turned off
        """
        raise NotImplementedError

    def isSpacingEnabled(self):
        """@return: true if spacing between child components within this layout
                    is enabled, false otherwise
        @deprecated: Use L{isSpacing} instead.
        """
        raise NotImplementedError

    def isSpacing(self):
        """@return: true if spacing between child components within this layout
                    is enabled, false otherwise
        """
        raise NotImplementedError


class IMarginHandler(object):
    """This type of layout supports automatic addition of margins (space around
    its components).
    """

    def setMargin(self, marginInfo):
        """Enable margins for this layout.

        B{NOTE:} This will only affect the space around the
        components in the layout, not space between the components in the
        layout. Use L{setSpacing} to add space between the components in
        the layout.

        See the reference manual for more information about CSS rules for
        defining the size of the margin.

        @param marginInfo:
                   MarginInfo object containing the new margins.
        """
        raise NotImplementedError

    def getMargin(self):
        """@return: MarginInfo containing the currently enabled margins."""
        raise NotImplementedError


class MarginInfo(VMarginInfo):

    def __init__(self, *args):
        super(MarginInfo, self).__init__(*args)