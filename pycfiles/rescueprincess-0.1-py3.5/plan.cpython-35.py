# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/rescueprincess/plan.py
# Compiled at: 2016-10-24 21:53:35
# Size of source mod 2**32: 520 bytes
"""
Michael duPont
Proposed Solution to:
https://assets.toggl.com/images/toggl-how-to-save-the-princess-in-8-programming-languages.jpg
"""

class Plan:

    @staticmethod
    def execute():
        print('You saved the princess without having to write any code!')

    @staticmethod
    def party():
        raise Exception('Partied too hard with all that extra time you had')


if __name__ == '__main__':
    try:
        Plan.execute()
        Plan.party()
    except Exception as e:
        print(e)