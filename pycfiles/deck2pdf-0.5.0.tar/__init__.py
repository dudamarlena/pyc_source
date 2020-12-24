# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/attakei/workspace/MyOSS/deck2pdf/tests/__init__.py
# Compiled at: 2015-12-22 23:31:52
import os
from pytest import mark
current_dir = os.path.abspath(os.getcwd())
test_dir = os.path.abspath(os.path.dirname(__file__))
skip_in_ci = mark.skipif("'FULL_TEST' not in os.environ")