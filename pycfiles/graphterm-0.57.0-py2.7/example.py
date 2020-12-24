# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-x86_64/egg/graphterm/bin/pytutor/example-code/example.py
# Compiled at: 2014-02-02 09:23:11


def listSum(numbers):
    if not numbers:
        return 0
    else:
        f, rest = numbers
        return f + listSum(rest)


myList = (1, (2, (3, None)))
total = listSum(myList)