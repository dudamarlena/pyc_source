# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/iniparse.py
# Compiled at: 2015-11-29 05:52:18
from __future__ import unicode_literals
from __future__ import unicode_literals
from .compat import text_type, iteritems
from .containers import OrderedDict
import os, re
re_section = re.compile(b'\\[(.*?)\\]', re.UNICODE)

def sub_env(text, _re_env=re.compile(b'\\$(\\w+)', re.MULTILINE)):
    """Substition renvironment, in $ENV_VARIABLE syntax"""
    get_environ = os.environ.get

    def repl(match):
        return get_environ(match.group(1), match.group(0))

    return _re_env.sub(repl, text)


def parse(inifile, sections=None, section_class=OrderedDict, _sub_env=sub_env):
    """Parse an ini file in to nested dictionaries"""
    if hasattr(inifile, b'read'):
        ini = inifile.read()
    else:
        ini = inifile
    if not isinstance(ini, text_type):
        ini = ini.decode(b'utf-8')
    inilines = ini.splitlines()
    if sections is None:
        sections = section_class()
    current_section = b''
    current_section_data = section_class()
    current_key = None
    current_value = b''
    section_match = re_section.match
    for line in inilines:
        if line.startswith(b'#'):
            continue
        if not line.strip():
            current_key = None
            continue
        match = section_match(line)
        if match:
            sections[current_section] = current_section_data
            current_section_data = section_class()
            current_section = match.group(1)
        elif line[0] in b' \t':
            if current_key is not None:
                current_value += b'\n' + line.strip()
                current_section_data[current_key] = current_value
        elif b'=' in line:
            key, value = line.split(b'=', 1)
            key = key.rstrip()
            value = _sub_env(value.lstrip()).lstrip()
            current_key = key
            current_value = value
            current_section_data[key] = value
        else:
            current_section_data[line.strip()] = b''

    sections[current_section] = current_section_data
    return sections


def write(settings, comments=None):
    """Write an ini file from nested dictionaries"""
    if comments is None:
        comments = []
    if isinstance(comments, text_type):
        comments = comments.splitlines()
    lines = [ b'# ' + comment for comment in comments ]

    def write_section(name, section):
        if name:
            lines.append((b'[{}]').format(name))
        for k, v in iteritems(section):
            v = (b'\n    ').join(v.split(b'\n'))
            lines.append((b'{k} = {v}').format(k=k, v=v))

        lines.append(b'')

    if b'' in settings:
        write_section(b'', settings[b''])
    for name, section in iteritems(settings):
        if name:
            write_section(name, section)

    return (b'\n').join(lines)


if __name__ == b'__main__':
    ini = b"# -------------------------------------------------------------\n# Filesystems\n# -------------------------------------------------------------\n\nfoo=bar\n\n[fs:project]\nlocation = ./\nmultiline = long\n    line\n\n[templateengine:jinja2]\ncachefs = jinja2cache\n\n[templates:default]\nlocation = ./templates\npriority = 10\n\n[app:blog]\nname = Will's blog\nvalue = 3\n\nnoequal=\n\n"
    settings = parse(ini)
    settings[b'new'] = {b'foo': b'bar\nbaz'}
    print write(settings, comments=[b'Re-written ini file', b'comments'])