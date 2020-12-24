# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/jinjarg.py
# Compiled at: 2020-01-21 16:04:21
# Size of source mod 2**32: 1034 bytes
"""CLI-template renderer like m4 but based on Jinja2 and argparse"""
from jinja2 import Template
from argparse import ArgumentParser

class Jinjarg:

    def __init__(self):
        self.parser = ArgumentParser()
        self._default_setup()
        self.setup()
        self.args = self.parser.parse_args()

    def _default_setup(self):
        self.parser.description = __doc__
        self.parser.add_argument('-t', '--template', required=True, help='Path to template-file')

    def setup(self):
        raise NotImplementedError('Do not use Jinjarg directly!\n        \nUsage example:\n```        \nfrom jinjarg import Jinjarg\n\n\nclass Example(Jinjarg):\n    def setup(self):\n        self.parser.add_argument("--example", type=str, help="Example variable passed to template", required=True)\n\n\nif __name__ == \'__main__\':\n    print(Example())\n```\n')

    def __str__(self):
        with open(self.args.template) as (fd):
            template = Template(fd.read())
            return template.render(args=(self.args))