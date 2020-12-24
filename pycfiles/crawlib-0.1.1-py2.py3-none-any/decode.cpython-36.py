# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/decode.py
# Compiled at: 2019-04-23 16:11:59
# Size of source mod 2**32: 2284 bytes
"""
This module provide extended power to decode HTML you crawled.
"""
import six, chardet
from . import util

def smart_decode(binary, errors='strict'):
    """
    Automatically find the right codec to decode binary data to string.

    :type binary: six.binary_type
    :param binary: binary data

    :type errors: str
    :param errors: one of 'strict', 'ignore' and 'replace'

    :rtype: str
    :return: decoded string
    """
    d = chardet.detect(binary)
    encoding = d['encoding']
    confidence = d['confidence']
    text = binary.decode(encoding, errors=errors)
    return (text, encoding, confidence)


class UrlSpecifiedDecoder(object):
    __doc__ = "\n    Designed for automatically decoding html from binary content of an url.\n\n    First, `chardet.detect` is very expensive in time.\n    Second, usually each website (per domain) only use one encoding algorithm.\n\n    This class avoid perform `chardet.detect` twice on the same domain.\n\n    :param domain_encoding_table: dict, key is root domain, and value is the\n        domain's default encoding.\n    "

    class ErrorsHandle(object):
        strict = 'strict'
        ignore = 'ignore'
        replace = 'replace'

    def __init__(self):
        self.domain_encoding_table = dict()

    def decode(self, binary, url, encoding=None, errors='strict'):
        """
        Decode binary to string.

        :param binary: binary content of a http request.
        :param url: endpoint of the request.
        :param encoding: manually specify the encoding.
        :param errors: errors handle method.

        :return: str
        """
        if encoding is None:
            domain = util.get_domain(url)
            if domain in self.domain_encoding_table:
                encoding = self.domain_encoding_table[domain]
                html = binary.decode(encoding, errors=errors)
            else:
                html, encoding, confidence = smart_decode(binary,
                  errors=errors)
                self.domain_encoding_table[domain] = encoding
        else:
            html = binary.decode(encoding, errors=errors)
        return html


url_specified_decoder = UrlSpecifiedDecoder()
decoder = url_specified_decoder