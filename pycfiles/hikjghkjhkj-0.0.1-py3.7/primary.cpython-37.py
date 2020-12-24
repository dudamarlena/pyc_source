# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\main\primary.py
# Compiled at: 2020-04-29 10:26:05
# Size of source mod 2**32: 363 bytes
import pandas as pd

class Hello:

    def __init__(self):
        self.test = 'welcome!'

    def output(self):
        df = pd.DataFrame({'first':[1, 2, 3],  'seconde':[
          6, 7, 8], 
         'third':[
          9, 0, 5]})
        print(df)
        return self.test


if __name__ == '__main__':
    a = Hello()
    a.output()