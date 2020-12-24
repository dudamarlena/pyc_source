# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tkomiya/work/sphinx/.tox/py37/lib/python3.7/site-packages/docutils/writers/null.py
# Compiled at: 2018-11-25 06:19:18
# Size of source mod 2**32: 450 bytes
"""
A do-nothing Writer.
"""
from docutils import writers

class Writer(writers.UnfilteredWriter):
    supported = ('null', )
    config_section = 'null writer'
    config_section_dependencies = ('writers', )

    def translate(self):
        pass