# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\CODE\VScode\autowork\ymm-automation\ymmuim-library\YmmuimLibrary\action\actioner.py
# Compiled at: 2019-07-01 08:19:32
# Size of source mod 2**32: 3215 bytes
from AppiumLibrary import utils
from robot.api import logger

class Actioner(object):

    def __init__(self):
        self._strategies = {'id':self._find_by_identifier, 
         'default':self._find_by_identifier}

    def find(self, browser, locator, tag=None):
        assert browser is not None
        if not (locator is not None and len(locator) > 0):
            raise AssertionError
        prefix, criteria = self._parse_locator(locator)
        prefix = 'default' if prefix is None else prefix
        strategy = self._strategies.get(prefix)
        if strategy is None:
            raise ValueError("Element locator with prefix '" + prefix + "' is not supported")
        tag, constraints = self._get_tag_and_constraints(tag)
        return strategy(browser, criteria, tag, constraints)

    def _find_by_identifier(self, browser, criteria, tag, constraints):
        elements = self._normalize_result(browser.find_elements_by_id(criteria))
        elements.extend(self._normalize_result(browser.find_elements_by_name(criteria)))
        return self._filter_elements(elements, tag, constraints)

    def _parse_locator(self, locator):
        prefix = None
        criteria = locator
        if not locator.startswith('//'):
            locator_parts = locator.partition('=')
            if len(locator_parts[1]) > 0:
                prefix = locator_parts[0].strip().lower()
                criteria = locator_parts[2].strip()
        return (
         prefix, criteria)

    def _get_tag_and_constraints(self, tag):
        if tag is None:
            return (
             None, {})
        else:
            tag = tag.lower()
            constraints = {}
            if tag == 'link':
                tag = 'a'
            else:
                if tag == 'image':
                    tag = 'img'
                else:
                    if tag == 'list':
                        tag = 'select'
                    else:
                        if tag == 'radio button':
                            tag = 'input'
                            constraints['type'] = 'radio'
                        else:
                            if tag == 'checkbox':
                                tag = 'input'
                                constraints['type'] = 'checkbox'
                            else:
                                if tag == 'text field':
                                    tag = 'input'
                                    constraints['type'] = 'text'
                                else:
                                    if tag == 'file upload':
                                        tag = 'input'
                                        constraints['type'] = 'file'
        return (
         tag, constraints)

    def _normalize_result(self, elements):
        if not isinstance(elements, list):
            logger.debug('WebDriver find returned %s' % elements)
            return []
        return elements

    def _filter_elements(self, elements, tag, constraints):
        elements = self._normalize_result(elements)
        if tag is None:
            return elements
        return filter(lambda element: self._element_matches(element, tag, constraints), elements)

    def _element_matches(self, element, tag, constraints):
        if not element.tag_name.lower() == tag:
            return False
        for name in constraints:
            if not element.get_attribute(name) == constraints[name]:
                return False

        return True