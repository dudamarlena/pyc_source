# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/esteban/PycharmProjects/emoji-unicode/emoji_unicode/data_parser.py
# Compiled at: 2017-10-10 17:01:05
# Size of source mod 2**32: 2479 bytes
from __future__ import unicode_literals
import os, io
from .utils import code_point_to_unicode
DIR = os.path.dirname(__file__)

def escape_unicode(txt):
    return txt.encode('unicode_escape').replace(b'\\', b'\\\\').decode('unicode_escape')


def _parse(line):
    code_point = line.split(';', 1)[0]
    return '-'.join(code_point_to_unicode(c) for c in code_point.strip().split('..'))


EMOJI_EXCLUDE = {str(n) for n in range(0, 10)} | {'#', '*'}

def parse():
    with io.open((os.path.join(DIR, 'emoji-data.txt')), mode='r', encoding='utf-8') as (fh):
        cps = []
        for line in fh.readlines():
            if line.startswith('#'):
                pass
            else:
                cp = _parse(line)
                if cp.split('-')[0] in EMOJI_EXCLUDE:
                    pass
                else:
                    cps.append(cp)

        return cps


def read_template():
    with io.open((os.path.join(DIR, 'pattern_template.py')), mode='r', encoding='utf-8') as (fh):
        return fh.read()


def render_template(template, code_points):
    code_points = escape_unicode(''.join(code_points))
    return template.replace('{{code_points}}', code_points)


def write_pattern_file(template_rendered):
    with io.open((os.path.join(DIR, 'pattern.py')), mode='w', encoding='utf-8') as (fh):
        fh.write(template_rendered)


def generate_pattern_file():
    code_points = parse()
    template = read_template()
    template_rendered = render_template(template, code_points)
    write_pattern_file(template_rendered)