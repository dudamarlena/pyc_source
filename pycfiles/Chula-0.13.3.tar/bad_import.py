# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./scripts/../apps/example/webapp/controller/bad_import.py
# Compiled at: 2011-03-19 21:05:04
"""
This module cannot be imported because it should itself raise an
import error.
"""
import intentionally_non_existent_module