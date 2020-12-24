# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/folmond/presentation.py
# Compiled at: 2018-05-05 06:15:22
import prettytable
from StringIO import StringIO
from core import CoreAnalysis

class Presentation:

    def __init__(self, path):
        self.ca = CoreAnalysis(path)

    def getRecentStatus(self):
        df = self.ca.getCurrentUsage()
        df['size'] = df['size'] / 1048576
        df = df.rename(columns={'size': 'size(MB)'})
        df = df.round(3)
        output = StringIO()
        df.to_csv(output)
        output.seek(0)
        pt = prettytable.from_csv(output)
        print pt


if __name__ == '__main__':
    presentation_obj = Presentation('/home/arun/Projects/bingoarun/folmon/sample-data')
    presentation_obj.getRecentStatus()