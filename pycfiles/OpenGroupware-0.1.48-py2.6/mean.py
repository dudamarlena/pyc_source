# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/math/mean.py
# Compiled at: 2012-10-12 07:02:39
import os, base64
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand

class XPathAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'mean'
    __aliases__ = ['meanAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def _calculate_arithmatic_mean(self, values):
        total = 0.0
        count = 0.0
        for value in values:
            total = total + float(value)
            count = count + 1.0

        return total / count

    @property
    def result_mimetype(self):
        return 'text/plain'

    def do_action(self):
        result = None
        doc = etree.parse(self.rfile)
        values = doc.xpath(self._xpath)
        if isinstance(result, list):
            if self._kind == 'ARITHMATIC':
                result = self._calculate_arithmatic_mean(values)
        self.wfile.write(str(result))
        return

    def parse_action_parameters(self):
        self._xpath = self.action_parameters.get('xpath', None)
        self._kind = self.action_parameters.get('kind', 'ARITHMATIC').upper()
        if self._xslt is None:
            raise CoilsException('No path provided for xpath query')
        else:
            self._xpath = self.decode_text(self._xpath)
        return

    def do_epilogue(self):
        pass