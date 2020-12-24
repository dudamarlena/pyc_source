# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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