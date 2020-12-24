# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/command/sub/templatebuilder.py
# Compiled at: 2016-12-08 16:29:22
"""A system to create a directory tree from a template.

The format is very simple. A line beginning with @ should be a path to a file. Subsequent lines after that line will be appended to the specified file.

The template is passed through moya templates, creating a very flexible system for dynamically creating file trees.

In order to allow these fs templates to generate moya templates, the syntax is slightly different.
The filesystem template syntax should be {{% %}} for logic, and ${{ }} for substitution.

"""
from __future__ import unicode_literals
from __future__ import print_function
from ...context import Context
from ...template.moyatemplates import Template
from fs.path import dirname, join, relpath
import re

def compile_fs_template(fs, template_text, data=None, path=None):
    """Compile a fs template structure in to a filesystem object"""
    if data is None:
        data = {}
    template = Template(template_text)
    template.re_special = re.compile(b'\\{\\{\\%((?:\\".*?\\"|\\\'.*?\\\'|.|\\s)*?)\\%\\}\\}|(\\{\\{\\#)|(\\#\\}\\})')
    context = Context(re_sub=b'\\$\\{\\{(.*?)\\}\\}')
    fs_template = template.render(data, context=context)
    out_type = None
    out_filename = None
    file_lines = []

    def write_file(filename, file_type):
        if filename:
            if file_type.lower() == b'text':
                with fs.open(filename, b'wt') as (f):
                    f.write((b'\n').join(file_lines) + b'\n')
            elif file_type.lower() == b'wraptext':
                import textwrap
                with fs.open(filename, b'wt') as (f):
                    for line in file_lines:
                        f.write((b'\n').join(textwrap.wrap(line, 79)) + b'\n')

            elif file_type.lower() == b'bin':
                with fs.open(filename, b'wb') as (f):
                    for line in file_lines:
                        chunk = (b'').join(chr(int(a + b, 16)) for a, b in zip(line[::2], line[1::2]))
                        f.write(chunk)

            del file_lines[:]

    for line in fs_template.splitlines():
        line = line.rstrip()
        if line.startswith(b'@'):
            write_file(out_filename, out_type)
            out_filename = None
            out_type, path_spec = line[1:].split(b' ', 1)
            if path:
                path_spec = join(path, relpath(path_spec))
            if path_spec.endswith(b'/'):
                fs.makedirs(path_spec, recreate=True)
                out_filename = None
            else:
                fs.makedirs(dirname(path_spec), recreate=True)
                out_filename = path_spec
            continue
        if out_filename:
            file_lines.append(line)

    if out_filename:
        write_file(out_filename, out_type)
    return


if __name__ == b'__main__':
    template = b'\n@test.txt\nThis\nis a test file\n{{%- if readme %}}\n@readme.txt\nReadme file\n-----------\n${{message}}\n{{%- endif %}}\n@templates/base.html\n<h1>${title}</h1>\n<ul>\n    {% for fruit in fruits %}\n    <li>${fruit}</li>\n    {% endfor %}\n</ul>\n@settings/production.ini\n@foo/bar/baz/\n@author\nBob\n    '
    from fs.osfs import OSFS
    from fs.memoryfs import MemoryFS
    fs = OSFS(b'__test__', create=True)
    fs = MemoryFS()
    td = dict(message=b'Hello, World!', readme=True)
    compile_fs_template(fs, template, td)
    fs.tree()