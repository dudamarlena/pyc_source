# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/shell.py
# Compiled at: 2015-12-15 14:26:00
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.objects.shellredirecttoken import ShellRedirectToken

class Shell:

    def __init__(self, shell_xml=None):
        self.url = None
        self.redirect_url = None
        self.redirect_token = []
        if shell_xml is not None:
            self.parse_xml(shell_xml)
        return

    def parse_xml(self, shell_xml):
        xmlutils = XmlUtils(shell_xml)
        self.url = xmlutils.get_string_by_xpath('url/text()')
        self.redirect_url = xmlutils.get_string_by_xpath('redirect-url/text()')
        for i in shell_xml.xpath('redirect-token'):
            self.redirect_token.append(ShellRedirectToken(i))