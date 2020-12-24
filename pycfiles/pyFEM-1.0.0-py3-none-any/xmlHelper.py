# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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