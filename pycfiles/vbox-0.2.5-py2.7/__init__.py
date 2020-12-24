# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\vbox\__init__.py
# Compiled at: 2013-03-20 09:41:35
"""The VBox structure is a three-layered one.

Bottommost layer is `cli` -- actual part that calls programs and parses their outputs (where possible);
Middle layer is `pyVb` -- it organises CLI bindings to pythonic object structures and performs final parsing and typecasting;
Topmost layer is `api` -- the one that actually gets exposed to the parent library. Should provide nice and consistent usage experience;
"""
from .api import *