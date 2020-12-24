# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ojcrawler/tests/test_get_problem.py
# Compiled at: 2018-12-28 09:36:25
from __future__ import print_function
from ojcrawler.control import Controller
if __name__ == '__main__':
    x = Controller()
    _, info = x.get_problem('hdu', '4114')
    print(_, info)
    _, info = x.get_problem('poj', '2114')
    print(_, info)
    _, info = x.get_problem('codeforces', '100a')
    print(_, info)