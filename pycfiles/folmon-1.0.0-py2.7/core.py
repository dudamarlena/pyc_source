# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/folmond/core.py
# Compiled at: 2018-05-05 06:15:22
from filereader import CSVReader

class CoreAnalysis:

    def __init__(self, path):
        self.reader = CSVReader(path)

    def getCurrentUsage(self):
        df_recent = self.reader.getRecent()
        total = int(df_recent.loc[(df_recent['folder'] == '/log', 'size')].item())
        df_recent['percentage'] = df_recent['size'] / total * 100
        return df_recent


if __name__ == '__main__':
    ca = CoreAnalysis('/home/arun/Projects/bingoarun/folmon/sample-data')
    print ca.getCurrentUsage()