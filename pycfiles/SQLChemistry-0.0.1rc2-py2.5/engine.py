# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sqlchemistry/alchemy/engine.py
# Compiled at: 2008-04-15 11:11:07
"""Module for creating SQLAlchemy engine objects

Copyright (C) 2008 Emanuel Gardaya Calso <egcalso@gmail.com>

This module is part of SQLChemistry and is is released under
the LGPL License
"""
from sqlalchemy.engine import create_engine

def get_engine(uri):
    return create_engine(uri)