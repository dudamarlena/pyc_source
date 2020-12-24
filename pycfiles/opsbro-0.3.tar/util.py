# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/ruamel/yaml/util.py
# Compiled at: 2017-07-27 07:36:53
"""
some helper functions that might be generally useful
"""
from __future__ import print_function
from __future__ import absolute_import
from .compat import text_type, binary_type
from .main import round_trip_load

def load_yaml_guess_indent(stream, **kw):
    """guess the indent and block sequence indent of yaml stream/string

    returns round_trip_loaded stream, indent level, block sequence indent
    - block sequence indent is the number of spaces before a dash relative to previous indent
    - if there are no block sequences, indent is taken from nested mappings, block sequence
      indent is unset (None) in that case
    """

    def leading_spaces(l):
        idx = 0
        while idx < len(l) and l[idx] == ' ':
            idx += 1

        return idx

    if isinstance(stream, text_type):
        yaml_str = stream
    else:
        if isinstance(stream, binary_type):
            yaml_str = stream.decode('utf-8')
        else:
            yaml_str = stream.read()
        map_indent = None
        indent = None
        block_seq_indent = None
        prev_line_key_only = None
        key_indent = 0
        for line in yaml_str.splitlines():
            rline = line.rstrip()
            lline = rline.lstrip()
            if lline.startswith('- '):
                l_s = leading_spaces(line)
                block_seq_indent = l_s - key_indent
                idx = l_s + 1
                while line[idx] == ' ':
                    idx += 1

                if line[idx] == '#':
                    continue
                indent = idx - key_indent
                break
            if map_indent is None and prev_line_key_only is not None and rline:
                idx = 0
                while line[idx] in ' -':
                    idx += 1

                if idx > prev_line_key_only:
                    map_indent = idx - prev_line_key_only
            if rline.endswith(':'):
                key_indent = leading_spaces(line)
                idx = 0
                while line[idx] == ' ':
                    idx += 1

                prev_line_key_only = idx
                continue
            prev_line_key_only = None

    if indent is None and map_indent is not None:
        indent = map_indent
    return (
     round_trip_load(yaml_str, **kw), indent, block_seq_indent)


def configobj_walker(cfg):
    """
    walks over a ConfigObj (INI file with comments) generating
    corresponding YAML output (including comments
    """
    from configobj import ConfigObj
    assert isinstance(cfg, ConfigObj)
    for c in cfg.initial_comment:
        if c.strip():
            yield c

    for s in _walk_section(cfg):
        if s.strip():
            yield s

    for c in cfg.final_comment:
        if c.strip():
            yield c


def _walk_section(s, level=0):
    from configobj import Section
    assert isinstance(s, Section)
    indent = '  ' * level
    for name in s.scalars:
        for c in s.comments[name]:
            yield indent + c.strip()

        x = s[name]
        if '\n' in x:
            i = indent + '  '
            x = '|\n' + i + x.strip().replace('\n', '\n' + i)
        elif ':' in x:
            x = "'" + x.replace("'", "''") + "'"
        line = ('{0}{1}: {2}').format(indent, name, x)
        c = s.inline_comments[name]
        if c:
            line += ' ' + c
        yield line

    for name in s.sections:
        for c in s.comments[name]:
            yield indent + c.strip()

        line = ('{0}{1}:').format(indent, name)
        c = s.inline_comments[name]
        if c:
            line += ' ' + c
        yield line
        for val in _walk_section(s[name], level=level + 1):
            yield val