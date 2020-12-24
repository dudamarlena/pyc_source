# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysmi/parser/smiv1.py
# Compiled at: 2018-12-29 12:21:47
from pysmi.parser.smi import parserFactory
from pysmi.parser.dialect import smiV1
SmiV1Parser = parserFactory(**smiV1)