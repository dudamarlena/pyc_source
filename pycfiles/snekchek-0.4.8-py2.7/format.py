# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snekchek/format.py
# Compiled at: 2020-03-03 07:34:32
"""Formatting functions for each linter"""
from __future__ import print_function, unicode_literals
import typing

def flake8_format(data):
    for row in data:
        print((b'{path}:{line}:{col}: {errcode} {msg}').format(**row))


def vulture_format(data):
    for row in data:
        print((b'{path}:{line}: {err} ({conf}% confidence)').format(**row))


def pylint_format(data):
    last_path = b''
    for row in data:
        if row[b'path'] != last_path:
            print((b'File: {0}').format(row[b'path']))
            last_path = row[b'path']
        print((b'{type_}:{line:>3}, {column:>2}: {message} ({symbol})').format(type_=row[b'type'][0].upper(), **row))


def pyroma_format(data):
    for row in list(data[b'modules'].values())[0]:
        print(row)


def isort_format(data):
    for diff in data:
        print(diff)


def yapf_format(data):
    for row in data:
        print(row)


def pypi_format(data):
    for row in data:
        print(row)


def safety_format(data):
    for row in data:
        print((b'[{row[4]}] ({row[0]}{row[1]}) {row[3]}').format(row=row))


def dodgy_format(data):
    for row in data:
        print((b'{row[1]}:{row[0]}: {row[2]}').format(row=row))


def pytest_format(data):
    for test in data:
        print(test[b'name'])
        print(test[b'call'][b'longrepr'])


def unittest_format(data):
    for test in data:
        print((b"Test '{0}'").format(test[0]._testMethodName))
        print(test[1])