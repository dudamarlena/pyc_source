# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starwater/blowdrycss_venv/lib/python3.6/site-packages/blowdrycss/scalingparser.py
# Compiled at: 2018-03-07 18:42:13
# Size of source mod 2**32: 9272 bytes
from __future__ import absolute_import
from cssutils.css import Property
from blowdrycss.utilities import deny_empty_or_whitespace
from blowdrycss.unitparser import UnitParser
from blowdrycss_settings import small, medium, large
__author__ = 'chad nelson'
__project__ = 'blowdrycss'

class ScalingParser(object):
    __doc__ = " Enables powerful responsive @media query generation via screen size suffixes.\n\n    **Scaling Flag:**\n\n    Append ``'-s'`` to the end of an encoded property values to scale the value up and down based on screen size.\n\n    Note: This only works on property values containing distance--based units (pixels, em, etc).\n\n    - General format: ``<name>-<value>-s``\n\n    - Specific case: ``font-size-24-s``\n\n    - Priority ``!important`` case: ``font-size-24-s-i``\n\n        - (``'-i'`` *is always last*)\n\n    **Responsive Scaling Ratios:**\n\n    - Assuming ``font-size-24-s`` is the encoded css class, the font-size will respond to the screen size according\n      to the following table:\n\n        +-------------+-------------------+----------------+------+-------+\n        | Screen Size |   Trigger Range   | Scaling Factor |  px  | em    |\n        +-------------+-------------------+----------------+------+-------+\n        | XLarge      | > 1024 or 64.0em  |        1       |  24  | 1.5   |\n        +-------------+-------------------+----------------+------+-------+\n        | Large       | > 720px & <= 1024 |      1.043     | 23.0 | 1.438 |\n        +-------------+-------------------+----------------+------+-------+\n        | Medium      | < 720px or 45.0em |      1.125     | 21.3 | 1.333 |\n        +-------------+-------------------+----------------+------+-------+\n        | Small       | < 480px or 30.0em |      1.25      | 19.2 | 1.2   |\n        +-------------+-------------------+----------------+------+-------+\n\n    **Important Note about cssutils**\n\n    Currently, ``cssutils`` does not support parsing media queries. Therefore, media queries need to be built, minified,\n    and appended separately.\n\n    :type css_class: str\n    :type css_property: Property()\n\n    :param css_class: Potentially encoded css class that may or may not be parsable. May not be empty or None.\n    :param css_property: Valid CSS Property as defined by ``cssutils.css.Property``.\n    :return: None\n\n    **Examples:**\n\n    >>> scaling_parser = ScalingParser(css_class='font-weight-24-s')\n\n    "

    def __init__(self, css_class='', css_property=Property()):
        deny_empty_or_whitespace(css_class, variable_name='css_class')
        deny_empty_or_whitespace((css_property.cssText), variable_name='css_property')
        self.css_class = css_class
        self.css_property = css_property
        self.scale_dict = {'large':1.043, 
         'medium':1.125, 
         'small':1.25}
        self.scaling_flag = '-s'
        self.is_scaling = self._is_scaling()

    def _is_scaling(self):
        """ Return False if ``self.property_name`` does not have default units of ``'px'``.
        Test if ``self.css_class`` contains the scaling flag ``-s``. Returns True if ``-s`` is found and
        False otherwise.

        **Rules:**

        - The ``self.property_name`` must possess units of pixels ``'px'``.
        - If no property priority is set the encoded ``css_class`` must end with ``-s``.
        - If priority is set the encoded ``css_class`` must end with ``-s-i``.

        :return: (*bool*) -- Returns True if ``-s`` is found and False otherwise.

        **Examples**

        >>> scaling_parser = ScalingParser(css_class='font-weight-24-s')
        >>> scaling_parser._is_scaling()
        True
        >>> scaling_parser.css_class = 'font-weight-24-s-i'
        >>> scaling_parser._is_scaling()
        True
        >>> scaling_parser.css_class = 'font-weight-24'
        >>> scaling_parser._is_scaling()
        False

        """
        unit_parser = UnitParser(property_name=(self.css_property.name))
        if unit_parser.default_units() != 'px':
            return False
        else:
            return self.css_class.endswith(self.scaling_flag) or self.css_class.endswith(self.scaling_flag + '-i')

    def strip_scaling_flag(self):
        """ Remove the ``scaling_flag`` from ``css_class`` if possible and return the clean css class. Otherwise,
        return the ``css_class`` unchanged.

        **Rules**

        - Remove ``-s`` if found at end of a string
        - Remove ``-s`` if ``-s-i`` is found at the end of the string.

        :return: (*str*) -- If the ``css_class`` is scaling remove the ``scaling_flag`` and return the clean
            css class. Otherwise, return the ``css_class`` unchanged.

        **Examples:**

        >>> scaling_parser = ScalingParser(css_class='font-size-32-s', name='font-size')
        >>> scaling_parser.strip_scaling_flag()
        font-size-32
        >>> scaling_parser.css_class = 'font-size-56-s-i'
        >>> scaling_parser.strip_scaling_flag()
        font-size-56-i
        >>> scaling_parser.css_class = 'font-size-14'
        >>> scaling_parser.strip_scaling_flag()
        font-size-14

        """
        if self.css_class.endswith(self.scaling_flag):
            return self.css_class[:-2]
        else:
            if self.css_class.endswith(self.scaling_flag + '-i'):
                return self.css_class[:-4] + '-i'
            return self.css_class

    def build_media_query(self):
        """ Returns CSS media queries that scales pixel / em values in response to screen size changes.

        **Generated CSS for ``font-size-24-s`` minus the inline comments & line breaks**::

            // Default size above medium
            .font-size-24-s { font-size: 24px; }

            // medium screen font size reduction
            @media only screen and (max-width: 64.0em) {
                .font-size-24-s { font-size: 23.0px; }
            }

            // medium screen font size reduction
            @media only screen and (max-width: 45.0em) {
                .font-size-24-s { font-size: 21.3px; }
            }

            // small screen font size reduction
            @media only screen and (max-width: 30.0em) {
                .font-size-24-s { font-size: 19.2px; }
            }

        **Priority !important -- Generated CSS for ``font-size-24-s-i`` minus the inline comments & line breaks**::

            // Default size above the maximum 'medium' width breakpoint.
            .font-size-24-s-i { font-size: 24px !important; }

            // medium screen font size reduction
            @media only screen and (max-width: 64.0em) {
                .font-size-24-s-i { font-size: 23.0px !important; }
            }

            // Apply 'medium' screen font size reduction.
            @media only screen and (max-width: 45.0em) {
                .font-size-24-s-i { font-size: 21.3px !important; }
            }

            // Apply 'small' screen font size reduction.
            @media only screen and (max-width: 30.0em) {
                .font-size-24-s-i { font-size: 19.2px !important; }
            }

        :return: (*str*) -- Returns CSS media queries that scales pixel / em values in response to screen size changes.

        """
        if not self.is_scaling:
            return ''
        else:
            name = self.css_property.name
            value = self.css_property.value
            units = ''.join(filter(lambda x: x.isalpha(), value))
            priority = self.css_property.priority
            deny_empty_or_whitespace((str(value)), variable_name='value')
            float_value = float(value.replace(units, ''))
            _max = 1
            large_property = Property(name=name, value=value, priority=priority)
            medium_property = Property(name=name, value=value, priority=priority)
            small_property = Property(name=name, value=value, priority=priority)
            large_value = round(float_value / self.scale_dict['large'], 4)
            large_property.value = str(large_value) + units
            medium_value = round(float_value / self.scale_dict['medium'], 4)
            medium_property.value = str(medium_value) + units
            small_value = round(float_value / self.scale_dict['small'], 4)
            small_property.value = str(small_value) + units
            return '.' + self.css_class + ' { ' + self.css_property.cssText + '; }\n\n' + '@media only screen and (max-width: ' + large[_max] + ') {\n' + '\t.' + self.css_class + ' { ' + large_property.cssText + '; }\n' + '}\n\n' + '@media only screen and (max-width: ' + medium[_max] + ') {\n' + '\t.' + self.css_class + ' { ' + medium_property.cssText + '; }\n' + '}\n\n' + '@media only screen and (max-width: ' + small[_max] + ') {\n' + '\t.' + self.css_class + ' { ' + small_property.cssText + '; }\n' + '}\n\n'