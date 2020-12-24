# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/pandasql/__init__.py
# Compiled at: 2016-02-01 12:11:24
from .sqldf import *
import os, pandas as pd
_ROOT = os.path.abspath(os.path.dirname(__file__))

def get_data(path):
    return os.path.join(_ROOT, 'data', path)


def load_meat():
    filename = get_data('meat.csv')
    df = pd.read_csv(filename, parse_dates=[0])
    return df


def load_births():
    filename = get_data('births_by_month.csv')
    df = pd.read_csv(filename, parse_dates=[0])
    return df