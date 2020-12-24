# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lotonumber/loto6_analysis.py
# Compiled at: 2017-09-12 02:06:59
# Size of source mod 2**32: 278 bytes
from analysis_basic import AnalysisBasic

class Loto6Analysis(AnalysisBasic):

    def __init__(self, loto6_data):
        super().__init__(loto6_data, 6)

    def __str__(self):
        return 'ロト6の当選番号を予想します。'


if __name__ == '__main__':
    pass