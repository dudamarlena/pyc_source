# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/terminal/sizeable.py
# Compiled at: 2013-04-04 15:36:36
"""Defines an interface to be implemented by components wishing to display
some object that may be dynamically resized."""

class ISizeable(object):
    """Interface to be implemented by components wishing to display some
    object that may be dynamically resized during runtime.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """
    UNITS_PIXELS = 0
    UNITS_POINTS = 1
    UNITS_PICAS = 2
    UNITS_EM = 3
    UNITS_EX = 4
    UNITS_MM = 5
    UNITS_CM = 6
    UNITS_INCH = 7
    UNITS_PERCENTAGE = 8
    SIZE_UNDEFINED = -1
    UNIT_SYMBOLS = [
     'px', 'pt', 'pc', 'em', 'ex', 'mm', 'cm', 'in', '%']

    def getWidth(self):
        """Gets the width of the object. Negative number implies unspecified
        size (terminal is free to set the size).

        @return: width of the object in units specified by widthUnits property.
        """
        raise NotImplementedError

    def setWidth(self, *args):
        """Sets the width of the object. Negative number implies unspecified
        size (terminal is free to set the size).

        @param args: tuple of the form
                - (width)
                  1. the width of the object in units specified by widthUnits
                     propertyor in CSS style string representation, null or
                     empty string to reset
                - (width, unit)
                  1. the width of the object.
                  2. the unit used for the width. Possible values include
                     L{UNITS_PIXELS}, L{UNITS_POINTS},
                     L{UNITS_PICAS}, L{UNITS_EM}, L{UNITS_EX},
                     L{UNITS_MM}, L{UNITS_CM}, L{UNITS_INCH},
                     L{UNITS_PERCENTAGE}.

        See U{CSS specification
        <http://www.w3.org/TR/REC-CSS2/syndata.html#value-def-length>} for
        more details.
        """
        raise NotImplementedError

    def getHeight(self):
        """Gets the height of the object. Negative number implies unspecified
        size (terminal is free to set the size).

        @return: height of the object in units specified by heightUnits
                property.
        """
        raise NotImplementedError

    def setHeight(self, *args):
        """Sets the height of the object. Negative number implies unspecified
        size (terminal is free to set the size).

        @param args: tuple of the form
                - (height)
                   1. the height of the object in units specified by
                      heightUnits property or the height of the component using
                      string presentation. String presentation is similar to
                      what is used in Cascading Style Sheets. Size can be
                      length or percentage of available size.
                - (height, unit)
                  1. the height of the object.
                  2. the unit used for the width. Possible values include
                     L{UNITS_PIXELS}, L{UNITS_POINTS},
                     L{UNITS_PICAS}, L{UNITS_EM}, L{UNITS_EX},
                     L{UNITS_MM}, L{UNITS_CM}, L{UNITS_INCH},
                     L{UNITS_PERCENTAGE}.
        """
        raise NotImplementedError

    def getWidthUnits(self):
        """Gets the width property units.

        @return: units used in width property.
        """
        raise NotImplementedError

    def setWidthUnits(self, units):
        """Sets the width property units.

        @param units:
                   the units used in width property.
        @deprecated: Consider setting width and unit simultaneously using
                    L{setWidth}, which is less error-prone.
        """
        raise NotImplementedError

    def getHeightUnits(self):
        """Gets the height property units.

        @return: units used in height property.
        """
        raise NotImplementedError

    def setHeightUnits(self, units):
        """Sets the height property units.

        @param units:
                   the units used in height property.
        @deprecated: Consider setting height and unit simultaneously using
                    L{setHeight} or which is less error-prone.
        """
        raise NotImplementedError

    def setSizeFull(self):
        """Sets the size to 100% x 100%."""
        raise NotImplementedError

    def setSizeUndefined(self):
        """Clears any size settings."""
        raise NotImplementedError