# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/re/find.py
# Compiled at: 2012-10-12 07:02:39
import os, re
from coils.core import *
from coils.core.logic import ActionCommand

class FindAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 're-find'
    __aliases__ = ['regularExpressionFind', 'regularExpressionFindAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        self.log.debug(('Expression: {0}').format(self._expression))
        text = self.rfile.read()
        try:
            result = re.findall(self._expression, text)
        except Exception, e:
            self.log.error('Failure processing regular expression')
            self.log.exception(e)
            raise e

        if len(result):
            if self._singleton:
                result = result[0]
                if self._strip_value:
                    result = result.strip()
                self.wfile.write(result)
            else:
                self.wfile.write('<?xml version="1.0" encoding="utf-8"?>')
                self.wfile.write('<ResultSet>')
                for value in result:
                    if self._strip_value:
                        value = value.strip()
                    self.wfile.write(('<value>{0}</value>').format(self.encode_text(value)))

                self.wfile.write('</ResultSet>')
        elif self._singleton:
            self.wfile.write('<?xml version="1.0" encoding="utf-8"?>')
            self.wfile.write('<ResultSet/>')

    def parse_action_parameters(self):
        self._expression = self.action_parameters.get('expression', None)
        self._strip_value = self.action_parameters.get('trimValue', 'NO')
        self._singleton = self.action_parameters.get('singleton', 'YES').upper()
        if self._expression is None:
            raise CoilsException('No expression specified for re action')
        self._expression = self.decode_text(self._expression)
        self._expression = self.process_label_substitutions(self._expression)
        if self._strip_value.upper() == 'YES':
            self._strip_value = True
        else:
            self._strip_value = False
        if self._singleton.upper() in ('YES', 'TRUE'):
            self._singleton = True
        else:
            self._singleton = False
        return