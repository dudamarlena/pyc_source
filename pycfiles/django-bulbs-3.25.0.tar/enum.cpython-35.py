# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/infographics/enum.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 350 bytes
from django_enumfield import enum

class InfographicType(enum.Enum):
    LIST = 0
    TIMELINE = 1
    STRONGSIDE_WEAKSIDE = 2
    PRO_CON = 3
    COMPARISON = 4
    labels = {LIST: 'List', 
     TIMELINE: 'Timeline', 
     STRONGSIDE_WEAKSIDE: 'Strongside_Weakside', 
     PRO_CON: 'Pro_Con', 
     COMPARISON: 'Comparison'}