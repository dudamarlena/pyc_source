# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/xml/xpathtest.py
# Compiled at: 2012-10-12 07:02:39
import base64
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand

class XPathTestAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'xpath-test'
    __aliases__ = ['xpathTestAction', 'xpathTest']

    def __init__(self):
        ActionCommand.__init__(self)

    @property
    def result_mimetype(self):
        return 'text/plain'

    def do_action(self):
        doc = etree.parse(self.rfile)
        result = doc.xpath(self._xpath, namespaces=doc.getroot().nsmap)
        if len(result) > 0:
            self.wfile.write('YES')
        else:
            self.wfile.write('NO')
        result = None
        doc = None
        return

    def parse_action_parameters(self):
        self._xpath = self.action_parameters.get('xpath', None)
        self._b64 = self.action_parameters.get('isBase64', 'NO').upper()
        if self._xpath is None:
            raise CoilsException('No path provided for xpath query')
        elif self._b64 == 'YES':
            self.xpath = base64.decodestring(self._xpath.strip())
        else:
            self.xpath = self.decode_text(self._xpath)
        self._xpath = self.process_label_substitutions(self._xpath)
        return

    def do_epilogue(self):
        pass