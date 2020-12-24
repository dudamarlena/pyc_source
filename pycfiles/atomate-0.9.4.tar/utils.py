# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ajain/Documents/code_matgen/atomate/atomate/vasp/builders/utils.py
# Compiled at: 2017-08-17 16:13:47
"""
This class contains common functions for builders
"""
__author__ = 'Anubhav Jain <ajain@lbl.gov>'

def dbid_to_str(prefix, dbid):
    return ('{}-{}').format(prefix, dbid)


def dbid_to_int(dbid):
    return int(dbid.split('-')[1])