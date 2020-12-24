# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/soulmerge/projects/score/py/pyramid/score/pyramid/scaffolds/__init__.py
# Compiled at: 2015-05-06 04:10:03
# Size of source mod 2**32: 296 bytes
from pyramid.scaffolds import PyramidTemplate

class ScoreTemplate(PyramidTemplate):
    _template_dir = 'score'
    summary = 'Scaffold for projects by strg.at'


class ScoreNodbTemplate(PyramidTemplate):
    _template_dir = 'score-nodb'
    summary = 'Scaffold for design projects by strg.at'