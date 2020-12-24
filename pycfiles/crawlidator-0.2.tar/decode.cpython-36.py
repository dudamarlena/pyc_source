# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/sanhehu/Documents/GitHub/crawlib-project/crawlib/decode.py
# Compiled at: 2019-04-23 16:11:59
# Size of source mod 2**32: 2284 bytes
__doc__ = '\nThis module provide extended power to decode HTML you crawled.\n'
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
    return (
     text, encoding, confidence)


class UrlSpecifiedDecoder(object):
    """UrlSpecifiedDecoder"""

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