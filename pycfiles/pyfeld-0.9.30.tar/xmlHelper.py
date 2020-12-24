# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pyfeld/xmlHelper.py
# Compiled at: 2017-11-23 08:41:51
from __future__ import unicode_literals

class XmlHelper:

    @staticmethod
    def xml_extract_dict(xml, extract_keys):
        result_dict = {}
        for k in extract_keys:
            try:
                element = xml.getElementsByTagName(k)
                result_dict[k] = element[0].firstChild.nodeValue
            except Exception as e:
                result_dict[k] = b''

        return result_dict

    def xml_extract_dict_by_val(xml, extract_keys):
        result_dict = {}
        for k in extract_keys:
            try:
                element = xml.getElementsByTagName(k)
                result_dict[k] = element[0].getAttribute(b'val')
            except Exception as e:
                pass

        return result_dict