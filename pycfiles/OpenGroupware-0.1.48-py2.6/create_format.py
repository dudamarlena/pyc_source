# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/create_format.py
# Compiled at: 2012-10-12 07:02:39
import pickle, yaml
from sqlalchemy import *
from coils.core import *
from coils.foundation import Route, Process, Message
from coils.logic.workflow.formats import Format

class CreateFormat(Command):
    __domain__ = 'format'
    __operation__ = 'new'

    def parse_parameters(self, **params):
        Command.parse_parameters(self, **params)
        if 'description' in params:
            self.description = params.get('description')
            self.name = self.description.get('name')
            self.classname = self.description.get('class')
        elif 'yaml' in params:
            self.description = yaml.load(params.get('yaml'))
            self.name = self.description.get('name')
            self.classname = self.description.get('class')
        else:
            raise CoilsException('No description provided for data format')

    def run(self):
        format = Format.Marshall(self.classname)
        if format is None:
            self.log.warn(('No such format class as {0}').format(self.classname))
            raise CoilsException(('No such format class as {0}').format(self.classname))
        code = format.set_description(self.description)
        if code[0] < 0:
            self.log.warn(('Format description error#{0}: {1}').format(code[0], code[1]))
            raise CoilsException(code[1])
        format.save()
        self._result = format
        return