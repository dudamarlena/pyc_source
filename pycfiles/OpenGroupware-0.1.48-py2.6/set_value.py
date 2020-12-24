# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/xml/set_value.py
# Compiled at: 2012-10-12 07:02:39
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand

class SetValueAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'set-value'
    __aliases__ = ['setValue', 'setValueAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        doc = etree.parse(self.rfile)
        for element in doc.xpath(self._xpath, namespaces=doc.getroot().nsmap):
            source.text = self._value

        self.wfile.write(etree.tostring(doc))

    def parse_action_parameters(self):
        self._xpath = self.action_parameters.get('xpath', None)
        if self._xpath is not None:
            self._xpath = self.decode_text(self._xpath)
            self._xpath = self.process_label_substitutions(self._xpath)
        else:
            self._value = self.action_parameters.get('value', None)
            if self._value is None:
                raise CoilsException('No value or xpath provided for setValueAction.')
            else:
                self._value = self.process_label_substitutions(self._value)
        return

    def do_epilogue(self):
        pass