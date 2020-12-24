# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/actions/format/row_template.py
# Compiled at: 2012-10-12 07:02:39
import re, datetime
from lxml import etree
from coils.core import *
from coils.core.logic import ActionCommand

class RowTemplateAction(ActionCommand):
    __domain__ = 'action'
    __operation__ = 'row-template'
    __aliases__ = ['rowTemplate', 'rowTemplateAction']

    def __init__(self):
        ActionCommand.__init__(self)

    def do_action(self):
        rows = StandardXML.Read_Rows(self.rfile)
        for row in rows:
            text = self._template
            fields = row[0]
            fields.update(row[1])
            labels = re.findall('{:[A-z].[A-z0-9=:,]*}', text)
            for label in labels:
                components = label[2:-1].split(':')
                name = components[0]
                params = {}
                if len(components) > 1:
                    kind = components[1].lower()
                if len(components) > 2:
                    for param in components[2].lower().split(','):
                        params[param.split('=')[0]] = param.split('=')[1]

                else:
                    kind = 's'
                if name in fields:
                    value = fields[name]
                    if kind in ('string', 's'):
                        if isinstance(value, datetime.datetime):
                            value = value.strftime(self._dt_format)
                        elif isinstance(value, float):
                            if 'precision' in params:
                                value = '%.*f' % (int(params['precision']), value)
                            else:
                                value = unicode(value)
                        else:
                            value = unicode(value)
                        if 'ljust' in params:
                            value = value.ljust(int(params['ljust']))
                        elif 'rjust' in params:
                            value = value.rjust(int(params['rjust']))
                        elif 'center' in params:
                            value = value.center(int(params['center']))
                    text = text.replace(label, value)

            self.wfile.write(text)

    @property
    def result_mimetype(self):
        return self._mime_type

    def parse_action_parameters(self):
        self._template = self.action_parameters.get('template')
        self._dt_format = self.action_parameters.get('datetimeFormat', '%Y-%m-%d')
        self._mime_type = self.action_parameters.get('mimeType', 'text/plain')
        self._template = self.process_label_substitutions(self._template)

    def do_epilogue(self):
        pass