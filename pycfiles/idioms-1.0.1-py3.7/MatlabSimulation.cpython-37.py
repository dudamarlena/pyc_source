# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/idioms/models/MatlabSimulation.py
# Compiled at: 2019-05-09 22:07:13
# Size of source mod 2**32: 1378 bytes
import sys, re
from idioms.utils.matlab import gen_header, gen_signature, extract_atomic_variables, boilerplate_end, boilerplate_start
from idioms.utils.pathutils import realpath
from idioms.utils.stringutils import tabs_to_spaces
import os

class MatlabSimulation:

    def __init__(self, filepath, boilerplate_start=boilerplate_start, boilerplate_end=boilerplate_end):
        self.filepath = realpath(filepath)
        self.boilerplate = (boilerplate_start, boilerplate_end)
        self.name, ext = os.path.splitext(os.path.basename(self.filepath))
        with open(self.filepath, 'r') as (f):
            self.input = f.read()
            extracted = extract_atomic_variables(self.input)
            self.body = extracted.body
            self.vars = extracted.vars
        self.formatted = self._adjust_indentation()
        self.preamble = gen_header(self.vars)
        self.signature = gen_signature(self.filepath)
        self.output = f"{self.preamble}\n{self.signature}\n{self.boilerplate[0]}{self.formatted}{self.boilerplate[1]}"

    def _adjust_indentation(self):
        last_line = self.boilerplate[0].split('\n')[(-1)]
        leftpad = re.findall('^([ ]*)', last_line)[0]
        indented = []
        for line in self.body.split('\n'):
            line = f"{leftpad}{line}"
            indented.append(line)

        return '\n'.join(indented)