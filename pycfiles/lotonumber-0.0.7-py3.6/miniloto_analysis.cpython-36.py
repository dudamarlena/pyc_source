# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lotonumber/miniloto_analysis.py
# Compiled at: 2017-09-12 02:07:04
# Size of source mod 2**32: 291 bytes
from analysis_basic import AnalysisBasic

class MinilotoAnalysis(AnalysisBasic):

    def __init__(self, miniloto_data):
        super().__init__(miniloto_data, 5)

    def __str__(self):
        return 'ミニロトの当選番号を予想します。'


if __name__ == '__main__':
    pass