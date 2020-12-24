# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/pyasn1/pyasn1/compat/string.py
# Compiled at: 2018-07-11 18:15:32
from sys import version_info
if version_info[:2] <= (2, 5):

    def partition(string, sep):
        try:
            a, c = string.split(sep, 1)
        except ValueError:
            a, b, c = string, '', ''
        else:
            b = sep

        return (a, b, c)


else:

    def partition(string, sep):
        return string.partition(sep)