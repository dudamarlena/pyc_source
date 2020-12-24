# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/lotonumber/loto7_analysis.py
# Compiled at: 2017-09-12 02:19:51
# Size of source mod 2**32: 277 bytes
from analysis_basic import AnalysisBasic

class Loto7Analysis(AnalysisBasic):

    def __init__(self, loto7_data):
        super().__init__(loto7_data, 7)

    def __str__(self):
        return 'ロト7の当選番号を予想します。'


if __name__ == '__main__':
    pass