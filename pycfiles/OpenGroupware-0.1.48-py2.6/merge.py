# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/xml/merge.py
# Compiled at: 2012-10-12 07:02:39
import os, base64
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand

class XPathMerge(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'xpath-merge'
    __aliases__ = ['xpathMergeAction', 'xpathMerge']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        doc_a = etree.parse(self.rfile)
        message = self._ctx.run_command('message::get', process=self.process, label=self._input_label)
        self.log.debug(('Merging with message {0}').format(message.uuid))
        input_handle = self._ctx.run_command('message::get-handle', object=message)
        doc_b = etree.parse(input_handle)
        root_a = doc_a.getroot()
        elements = doc_b.xpath(self._xpath, namespaces=doc_b.getroot().nsmap)
        self.log.debug(('Merging {0} elements from message.').format(len(elements)))
        for element in elements:
            root_a.append(element)

        self.log.debug('Document merge complete, writing output.')
        self.wfile.write(etree.tostring(root_a))
        doc_b = None
        doc_a = None
        input_handle.close()
        return

    def parse_action_parameters(self):
        self._input_label = self.action_parameters.get('label', None)
        self._xpath = self.action_parameters.get('xpath', None)
        if self._xpath is None:
            raise CoilsException('No path provided for xpath query')
        else:
            self._xpath = self.decode_text(self._xpath)
        return

    def do_epilogue(self):
        pass