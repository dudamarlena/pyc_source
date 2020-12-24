# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nuclio/export.py
# Compiled at: 2018-07-26 10:52:30
# Size of source mod 2**32: 2869 bytes
from os.path import join, dirname, abspath
from textwrap import indent
import re
from nbconvert.filters import ipython2python
from nbconvert.exporters.html import HTMLExporter
here = dirname(abspath(__file__))
is_ignore = re.compile('#\\s*nuclio:\\s*ignore').search
is_handler = re.compile('^\\s*#\\s*nuclio:\\s*handler').search
is_return = re.compile('#\\s*nuclio:\\s*return').search
handler_decl = 'def handler(context, event):'
indent_prefix = '    '

class NuclioExporter(HTMLExporter):
    __doc__ = 'Export to nuclio handler'
    export_from_notebook = 'Nuclio'

    def _file_extension_default(self):
        """Return default file extension"""
        return '.py'

    @property
    def template_path(self):
        return super().template_path + [join(here, 'templates')]

    def _template_file_default(self):
        """Name of default template"""
        return 'nuclio'

    def default_filters(self):
        for pair in super().default_filters():
            yield pair

        yield ('nuclio', self.convert)

    def convert(self, text):
        code = ipython2python(text)
        if is_ignore(code):
            return indent(code, '# ')
        else:
            return is_handler(code) or code
        lines = [handler_decl]
        code = indent(code, indent_prefix)
        for line in code.splitlines():
            if is_return(line):
                line = self.add_return(line)
            lines.append(line)

        last_idx = len(lines) - 1
        for i, line in enumerate(reversed(lines[1:])):
            if not self.is_code_line(line):
                continue
            if 'return' not in line:
                lines[last_idx - i] = self.add_return(line)
            break

        return '\n'.join(lines)

    def is_code_line(self, line):
        """A code line is a non empty line that don't start with #"""
        line = line.strip()
        return line and line[0] != '#'

    def add_return(self, line, prefix=indent_prefix):
        """Add return to a line"""
        return line.replace(prefix, prefix + 'return ', 1)