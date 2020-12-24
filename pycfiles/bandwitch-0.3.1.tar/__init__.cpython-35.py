# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/valentin/Documents/EGF/bandwitch_project/bandwitch/bandwitch/enzymes_infos/__init__.py
# Compiled at: 2017-07-28 15:55:20
# Size of source mod 2**32: 608 bytes
"""Loads REBASE enzymes infos (mehtylation sensitivity and providers)"""
__all__ = [
 'enzymes_infos']
import os.path as osp
csv_path = osp.join(osp.dirname(osp.realpath(__file__)), 'enzymes_infos.csv')
with open(csv_path, 'r') as (f):
    _lines = f.read().split('\n')
    _fields = _lines[0].split(';')
    _replacements = dict([('N/A', False), ('+', True), ('-', True)] + [(str(i), i) for i in range(50)])
    enzymes_infos = {_line.split(';')[0]:dict(zip(_fields, [_replacements.get(e, e) for e in _line.split(';')])) for _line in _lines[1:]}