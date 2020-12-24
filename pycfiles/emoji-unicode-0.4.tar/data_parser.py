# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/esteban/PycharmProjects/emoji-awesome/emoji_unicode/data_parser.py
# Compiled at: 2015-11-18 15:40:31
from __future__ import unicode_literals
import os, io
from .utils import code_point_to_unicode
DIR = os.path.dirname(__file__)

def escape_unicode(txt):
    return txt.encode(b'unicode_escape').replace(b'\\', b'\\\\').decode(b'unicode_escape')


def _parse(line):
    code_point = line.split(b';', 1)[0]
    return (b'-').join(code_point_to_unicode(c) for c in code_point.strip().split(b'..'))


def parse():
    with io.open(os.path.join(DIR, b'emoji-data.txt'), mode=b'r', encoding=b'utf-8') as (fh):
        return [ _parse(line) for line in fh.readlines() if not line.startswith(b'#')
               ]


def read_template():
    with io.open(os.path.join(DIR, b'pattern_template.py'), mode=b'r', encoding=b'utf-8') as (fh):
        return fh.read()


def render_template(template, code_points):
    code_points = escape_unicode((b'').join(code_points))
    return template.replace(b'{{code_points}}', code_points)


def write_pattern_file(template_rendered):
    with io.open(os.path.join(DIR, b'pattern.py'), mode=b'w', encoding=b'utf-8') as (fh):
        fh.write(template_rendered)


def generate_pattern_file():
    code_points = parse()
    template = read_template()
    template_rendered = render_template(template, code_points)
    write_pattern_file(template_rendered)