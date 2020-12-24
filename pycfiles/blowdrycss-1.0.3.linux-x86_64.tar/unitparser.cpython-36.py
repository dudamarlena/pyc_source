# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starwater/blowdrycss_venv/lib/python3.6/site-packages/blowdrycss/unitparser.py
# Compiled at: 2018-03-07 18:42:13
# Size of source mod 2**32: 10224 bytes
from __future__ import absolute_import
from string import digits
import blowdrycss_settings as settings
__author__ = 'chad nelson'
__project__ = 'blowdrycss'

class UnitParser(object):
    __doc__ = '\n    **Used in these cases:**\n\n    - No units are provided and default units need to be added to make it valid css.\n    - The user wants their pixel (px) based units to be converted to em or root em (rem)\n      so that their page scales / zooms properly.\n\n    **Assumption:** The value provided already has negative signs and decimal points. There are no dashes or\n    underscores present in the value e.g. -1.25 can be processed, but n1_25 cannot be processed.\n\n    **Contains a ``default_property_units_dict``** which maps property names to their default units.\n\n    **Note:** Shorthand properties are not supported.\n\n    **Why do I want to use em (named after the sound for the letter \'M\') or root em (rem)?:**\n\n        *Because your webpage will scale with browser and device size.*\n\n    |\n\n    .. http://snook.ca/archives/html_and_css/font-size-with-rem\n       https://css-tricks.com/rems-ems/\n\n    **What does (em) actually stand for?:**\n        **Source:** W3C -- http://www.w3.org/WAI/GL/css2em.htm\n\n        The foremost tool for writing scalable style sheets is the "em" unit, and it therefore goes on top of\n        the list of guidelines that we will compile throughout this chapter: use ems to make scalable style sheets.\n        Named after the letter "M", the em unit has a long-standing tradition in typography where it has been used\n        to measure horizontal widths.\n        ...\n        In CSS, the em unit is a general unit for measuring lengths, for example page margins and padding\n        around elements. You can use it both horizontally and vertically, and this shocks traditional\n        typographers who always have used em exclusively for horizontal measurements. By extending the em unit\n        to also work vertically, it has become a very powerful unit - so powerful that you seldom have to\n        use other length units.\n\n        **Source:** Wikipedia -- https://en.wikipedia.org/wiki/Em_%28typography%29\n\n        An em is a unit in the field of typography, equal to the currently specified point size. For example,\n        one em in a 16-point typeface is 16 points. Therefore, this unit is the same for all typefaces at a\n        given point size.\n\n    '

    def __init__(self, property_name=''):
        self.property_name = property_name
        self.allowed = set(digits + '-.px')
        self.default_property_units_dict = {'background-position':'%', 
         'border-top':'px', 
         'border-right':'px', 
         'border-bottom':'px', 
         'border-left':'px', 
         'border-spacing':'px', 
         'border-width':'px', 
         'border-top-width':'px', 
         'border-right-width':'px', 
         'border-bottom-width':'px', 
         'border-left-width':'px', 
         'border-radius':'px', 
         'border-top-left-radius':'px', 
         'border-top-right-radius':'px', 
         'border-bottom-right-radius':'px', 
         'border-bottom-left-radius':'px', 
         'elevation':'deg', 
         'font-size':'px', 
         'height':'px', 
         'max-height':'px', 
         'min-height':'px', 
         'letter-spacing':'px', 
         'word-spacing':'px', 
         'line-height':'px', 
         'top':'px', 
         'right':'px', 
         'bottom':'px', 
         'left':'px', 
         'margin':'px', 
         'margin-top':'px', 
         'margin-right':'px', 
         'margin-bottom':'px', 
         'margin-left':'px', 
         'outline-width':'px', 
         'padding':'px', 
         'padding-top':'px', 
         'padding-right':'px', 
         'padding-bottom':'px', 
         'padding-left':'px', 
         'pause':'ms', 
         'pause-after':'ms', 
         'pause-before':'ms', 
         'pitch':'Hz', 
         'text-indent':'px', 
         'text-shadow':'px', 
         'vertical-align':'%', 
         'volume':'%', 
         'width':'px', 
         'max-width':'px', 
         'min-width':'px'}

    def default_units(self):
        """ Returns the default units "if any" for the assigned ``self.property_name``.

        :return: (*str*) -- Returns default units for the assigned ``self.property_name`` if they exist. Otherwise,
            return an empty string ``''``.

        """
        if self.property_name in self.default_property_units_dict:
            return self.default_property_units_dict[self.property_name]
        else:
            return ''

    def add_units(self, property_value=''):
        """ If the property_name requires units, then apply the default units defined in default_property_units_dict.

        **Rules:**

        - If use_em is False apply the default units for the property name by looking it up in
          default_property_units_dict.
        - Unit that have default units of ``px`` are converted to ``em`` if use_em is True.
        - If ``property_value`` has multiple property values, then split it apart.
        - If the value already has units, then pass it through unchanged.
        - The value provided shall possess negative signs and decimal points.
        - Mixed units are allowed, but **not recommended**.
        - Values shall only contain [] e.g. -1.25 can be processed, but n1_25 cannot be processed.

        :type property_value: str

        :param property_value: A string containing one or more space delimited alphanumeric characters.
        :return: (str) -- Returns the property value with the default or converted units added.

        >>> # Convert 'px' to 'em'
        >>> unit_parser = UnitParser(property_name='padding', use_em=True)
        >>> unit_parser.add_units('1 2 1 2')
        0.0625em 0.125em 0.0625em 0.125em
        >>> # Use default units
        >>> unit_parser.use_em = False
        >>> unit_parser.add_units('1 2 1 2')
        1px 2px 1px 2px
        >>> # Values already have units or are not parsable pass through
        >>> # True produces the same output.
        >>> unit_parser.use_em = False
        >>> unit_parser.add_units('55zp')
        55zp
        >>> unit_parser.add_units('17rem')
        17rem
        >>> # Unitless ``property_name``
        >>> # causes ``property_value`` to pass through.
        >>> unit_parser.property_name = 'font-weight'
        >>> unit_parser.add_units('200')
        200
        >>> # Mixed units cases - Not a Recommended Practice,
        >>> # but represent valid CSS. Be careful.
        >>> unit_parser.use_em = False
        >>> unit_parser.add_units('5em 6 5em 6')
        5em 6px 5em 6px
        >>> unit_parser.use_em = True
        >>> unit_parser.add_units('1em 100 4cm 9rem')
        1em 6.25em 4cm 9rem

        """
        new_value = []
        try:
            default_units = self.default_property_units_dict[self.property_name]
            for val in property_value.split():
                if set(val) <= self.allowed:
                    val = val.replace('px', '')
                    if settings.use_em:
                        if default_units == 'px':
                            new_value.append(settings.px_to_em(pixels=val))
                    new_value.append(val + default_units)
                else:
                    new_value.append(val)

            property_value = ' '.join(new_value)
        except KeyError:
            pass

        return property_value