# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/starwater/blowdrycss_venv/lib/python3.6/site-packages/blowdrycss/cssbuilder.py
# Compiled at: 2018-03-07 18:42:13
# Size of source mod 2**32: 5108 bytes
from __future__ import absolute_import, print_function, unicode_literals
from builtins import str
import logging
from cssutils.css import Selector, Property, CSSStyleRule, CSSStyleSheet
from xml.dom import SyntaxErr
from blowdrycss.classpropertyparser import ClassPropertyParser
__author__ = 'chad nelson'
__project__ = 'blowdrycss'

class CSSBuilder(object):
    __doc__ = ' Builds CSS text with the ``cssutils.css`` module.\n\n    **Note:** Removes invalid classes. A class is invalid for one of the following reasons:\n\n    - It is not valid CSS.\n    - It does not contain a valid ``blowdrycss`` encoding.\n\n    **Object initialization process:**\n\n    - Build CSS property rules\n    - Add to css_rules, OR remove invalid css_class from class_set.\n    - Build a CSS stylesheet based on the CSS ``css_rules`` set.\n\n    | **Parameters: property_parser** (*ClassPropertyParser object*) -- Contains a class property parser with a\n      populated class_set.\n    | **Returns:** None\n\n    '

    def __init__(self, property_parser=ClassPropertyParser()):
        message = 'CSSBuilder Running...'
        print(message)
        logging.debug(msg=message)
        self.property_parser = property_parser
        self.css_rules = set()
        self.css_stylesheet = CSSStyleSheet()
        invalid_css_classes = []
        reasons = []
        for css_class in self.property_parser.class_set:
            name = self.property_parser.get_property_name(css_class=css_class)
            try:
                encoded_property_value = self.property_parser.get_encoded_property_value(property_name=name,
                  css_class=css_class)
            except ValueError:
                invalid_css_classes.append(css_class)
                reasons.append(' (property_name not found in property_alias_dict.)')
                continue

            priority = self.property_parser.get_property_priority(css_class=css_class)
            value = self.property_parser.get_property_value(property_name=name,
              encoded_property_value=encoded_property_value)
            try:
                css_property = Property(name=name, value=value, priority=priority)
                if css_property.valid:
                    selector = self.build_selector(str(css_class))
                    css_rule = CSSStyleRule(selectorText=(selector.selectorText), style=(css_property.cssText))
                    self.css_rules.add(css_rule)
                else:
                    invalid_css_classes.append(css_class)
                    reasons.append(' (cssutils invalid property value: ' + value + ')')
                    continue
            except SyntaxErr:
                invalid_css_classes.append(css_class)
                reasons.append(' (cssutils SyntaxErr invalid property value: ' + value + ')')
                continue

        for i, invalid_css_class in enumerate(invalid_css_classes):
            self.property_parser.class_set.remove(invalid_css_class)
            self.property_parser.removed_class_set.add(invalid_css_class + reasons[i])

        self.build_stylesheet()

    def build_selector(self, css_class=''):
        """ Builds a CSS selector by prepending a ``'.'`` to ``css_class``, and appending an optional pseudo item.

        **Rules**

        - Always append a ``'.'`` to ``css_class``.

        - If a pseudo class is found append ``':' + pseuedo_class`` to ``css_class``.

        - If a pseudo element is found append ``'::' + pseudo_element`` to ``css_class``.

        :type css_class: str

        :param css_class: This value may or may not be identical to the property_value.
        :return: *str* -- The selector with a '.' prepended and an option pseudo item appended.

        """
        self.property_parser.set_pseudo_class(css_class)
        self.property_parser.set_pseudo_element(css_class)
        css_class = '.' + css_class
        if self.property_parser.pseudo_class:
            selector = Selector(css_class + ':' + self.property_parser.pseudo_class)
        else:
            if self.property_parser.pseudo_element:
                selector = Selector(css_class + '::' + self.property_parser.pseudo_element)
            else:
                selector = Selector(css_class)
        return selector

    def build_stylesheet(self):
        """ Builds the stylesheet by adding CSS rules to the CSS stylesheet.

        :return: None
        """
        for css_rule in self.css_rules:
            self.css_stylesheet.add(rule=css_rule)

    def get_css_text(self):
        """
        :return: str -- Returns CSS text.
        """
        return self.css_stylesheet.cssText