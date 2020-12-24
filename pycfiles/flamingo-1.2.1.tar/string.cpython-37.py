# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/core/utils/string.py
# Compiled at: 2020-02-08 07:33:40
# Size of source mod 2**32: 624 bytes
import re
CLEAN_RE = re.compile('[^a-z0-9äöüßø]')
WHITESPACE_RE = re.compile('\\s+')
ESCAPE_TABLE = [
 ('ä', 'ae'),
 ('ö', 'oe'),
 ('ü', 'ue'),
 ('ø', 'oe'),
 ('ß', 'ss')]

def slugify(string):
    string = string.lower()
    string = CLEAN_RE.sub(' ', string)
    string = string.strip()
    string = WHITESPACE_RE.sub('-', string)
    for a, b in ESCAPE_TABLE:
        string = string.replace(a, b)

    return string


def split(string, delimiter=','):
    string = WHITESPACE_RE.sub(' ', string.strip())
    strings = [i.strip() for i in string.split(delimiter) if i]
    return strings