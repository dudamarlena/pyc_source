# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tim/Projects/django_kss/VENV/lib/python2.7/site-packages/django_kss/pykss/section.py
# Compiled at: 2014-12-20 07:06:42
import re
from .modifier import Modifier
CLASS_MODIFIER = '.'
PSEUDO_CLASS_MODIFIER = ':'
MODIFIER_DESCRIPTION_SEPARATOR = ' - '
EXAMPLE_START = 'Example:'
REFERENCE_START = 'Styleguide'
reference_re = re.compile('%s ([\\d\\.]+)' % REFERENCE_START)
optional_re = re.compile('\\[(.*)\\]\\?')

class Section(object):

    def __init__(self, comment=None, filename=None):
        self.comment = comment or ''
        self.filename = filename

    def parse(self):
        self._description_lines = []
        self._modifiers = []
        self._example_lines = []
        self._reference = None
        in_example = False
        for line in self.comment.splitlines():
            if line.startswith(CLASS_MODIFIER) or line.startswith(PSEUDO_CLASS_MODIFIER):
                try:
                    modifier, description = line.split(MODIFIER_DESCRIPTION_SEPARATOR)
                except ValueError:
                    pass
                else:
                    self._modifiers.append(Modifier(modifier.strip(), description.strip()))

            elif line.startswith(EXAMPLE_START):
                in_example = True
            elif line.startswith(REFERENCE_START):
                in_example = False
                self._reference = reference_re.match(line).groups()[0].rstrip('.')
            elif in_example is True:
                self._example_lines.append(line)
            else:
                self._description_lines.append(line)

        self._description = ('\n').join(self._description_lines).strip()
        self.add_example(('\n').join(self._example_lines).strip())
        return

    @property
    def description(self):
        if not hasattr(self, '_description'):
            self.parse()
        return self._description

    @property
    def modifiers(self):
        if not hasattr(self, '_modifiers'):
            self.parse()
        return self._modifiers

    @property
    def example(self):
        if not hasattr(self, '_modifiers'):
            self.parse()
        return self._example

    @property
    def section(self):
        if not hasattr(self, '_reference'):
            self.parse()
        return self._reference

    def add_example(self, example):
        self._example = optional_re.sub('', example).replace('$modifier_class', '')
        for modifier in self._modifiers:
            modifier.add_example(optional_re.sub('\\1', example))