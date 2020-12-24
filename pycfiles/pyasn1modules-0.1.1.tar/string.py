# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyasn1/compat/string.py
# Compiled at: 2019-10-17 01:00:19
from sys import version_info
if version_info[:2] <= (2, 5):

    def partition(string, sep):
        try:
            (a, c) = string.split(sep, 1)
        except ValueError:
            a, b, c = string, '', ''
        else:
            b = sep

        return (
         a, b, c)


else:

    def partition(string, sep):
        return string.partition(sep)