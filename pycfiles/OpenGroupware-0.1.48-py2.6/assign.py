# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/xml/assign.py
# Compiled at: 2012-10-12 07:02:39
import os, base64
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand

class AssignAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'assign'
    __aliases__ = ['assignAction']

    def __init__(self):
        ActionCommand.__init__(self)

    @property
    def result_mimetype(self):
        return self._output_mimetype

    def prepare_xpath_namespaces(self, namespaces):
        namespaces = dict((prefix, namespaces[prefix]) for prefix in namespaces if prefix)
        if 'OGo' not in namespaces:
            namespaces['OGo'] = 'http://www.opengroupware.us/model'
        if 'OIE' not in namespaces:
            namespaces['OIE'] = 'http://www.opengroupware.us/oie'
        if 'OGoLegacy' not in namespaces:
            namespaces['OGoLegacy'] = 'http://www.opengroupware.org/'
        if 'OGoDAV' not in namespaces:
            namespaces['OGoDAV'] = '57c7fc84-3cea-417d-af54-b659eb87a046'
        if 'OGoCloud' not in namespaces:
            namespaces['OGoCloud'] = '2f85ddbe-28f5-4de3-8de9-c96bdd5230dd'
        return namespaces

    def do_action(self):
        if self._xpath is None:
            self.wfile.write(self._default)
        else:
            value = self._default
            doc = etree.parse(self.rfile)
            self.log.debug(etree.tostring(doc))
            namespaces = self.prepare_xpath_namespaces(doc.getroot().nsmap)
            try:
                result = doc.xpath(self._xpath, namespaces=namespaces)
            except TypeError, e:
                self.log.error(('TypeError with namespaces of: {0}').format(namespaces))
                raise e

            if isinstance(result, list):
                if len(result):
                    if result[0] is not None:
                        value = str(result[0])
            self.wfile.write(value)
        return

    def parse_action_parameters(self):
        self._xpath = self.action_parameters.get('xpath', None)
        self._default = self.action_parameters.get('default', '')
        self._output_mimetype = self.action_parameters.get('mimetype', 'application/xml')
        if self._xpath is not None:
            self._xpath = self.decode_text(self._xpath)
            if self._xpath:
                self._xpath = self.process_label_substitutions(self._xpath)
            else:
                self._xpath = None
        if self._default:
            self._default = self.process_label_substitutions(self._default)
        return

    def do_epilogue(self):
        pass