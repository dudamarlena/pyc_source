# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/utils/xmlutils.py
# Compiled at: 2016-01-03 05:52:37
from dateutil import parser
from datetime import datetime
from lxml import etree

class XmlUtils:

    def __init__(self, element=None):
        self.element = element

    def get_string_by_xpath(self, xpath):
        if self.element is None:
            return
        else:
            result = self.element.xpath(xpath)
            if len(result) > 0:
                out = result[0]
                if isinstance(out, str):
                    return out
                if hasattr(out, 'text'):
                    return out.text
            return

    def get_int_by_xpath(self, xpath):
        value = self.get_string_by_xpath(xpath)
        if value is not None:
            return int(value)
        else:
            return

    def get_bool_by_xpath(self, xpath):
        value = self.get_string_by_xpath(xpath)
        if value is not None:
            return value == 1
        else:
            return False

    def get_float_by_xpath(self, xpath):
        value = self.get_string_by_xpath(xpath)
        if value is not None:
            return float(value)
        else:
            return

    def get_datetime_by_xpath(self, xpath):
        value = self.get_string_by_xpath(xpath)
        if value is not None:
            return parser.parse(value)
        else:
            return

    def get_datetime_from_when(self, when_node):
        xmlutils = XmlUtils(when_node)
        y = xmlutils.get_int_by_xpath('date/y/text()')
        m = xmlutils.get_int_by_xpath('date/m/text()')
        d = xmlutils.get_int_by_xpath('date/d/text()')
        h = xmlutils.get_int_by_xpath('time/h/text()')
        _m = xmlutils.get_int_by_xpath('time/m/text()')
        s = xmlutils.get_int_by_xpath('time/s/text()')
        if h is None:
            return datetime(y, m, d)
        else:
            return datetime(y, m, d, h, _m, s)
            return

    def get_string(self, attributename):
        value = self.element.get(attributename)
        if value is not None:
            return value
        else:
            return

    def get_bool(self, attributename):
        value = self.get_string(attributename)
        return value == 1

    def get_int(self, attributename):
        value = self.get_string(attributename)
        if value is not None:
            return int(value)
        else:
            return

    def get_float(self, attributename):
        value = self.get_string(attributename)
        if value is not None:
            return float(value)
        else:
            return

    def get_datetime(self, attributename):
        value = self.get_string(attributename)
        if value is not None:
            return parser.parse(value)
        else:
            return

    def get_lang(self):
        XMLNS = '{http://www.w3.org/XML/1998/namespace}'
        lang = XMLNS + 'lang'
        return self.get_string(lang)