# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_import_parser_mt940.py
# Compiled at: 2014-10-09 13:38:05
import datetime, os, tempfile
from decimal import Decimal
from nose.tools import eq_, ok_
from bdgt.importer.parsers import Mt940Parser