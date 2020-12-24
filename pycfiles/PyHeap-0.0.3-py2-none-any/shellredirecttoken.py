# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/shellredirecttoken.py
# Compiled at: 2015-12-15 13:15:46
from healthvaultlib.utils.xmlutils import XmlUtils

class ShellRedirectToken:

    def __init__(self, token_xml=None):
        self.token = None
        self.description = None
        self.querystring_parameters = []
        if token_xml is not None:
            self.parse_xml(token_xml)
        return

    def parse_xml(self, token_xml):
        xmlutils = XmlUtils(token_xml)
        self.token = xmlutils.get_string_by_xpath('token/text()')
        self.description = xmlutils.get_string_by_xpath('description/text()')
        self.querystring_parameters = xmlutils.get_string_by_xpath('querystring-parameters/text()').split(',')