# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nemweb/__init__.py
# Compiled at: 2018-06-24 05:43:50
# Size of source mod 2**32: 209 bytes
"""Initialises nemweb package, loads config"""
import configparser, os
MODULE_DIR = os.path.dirname(__file__)
CONFIG = configparser.RawConfigParser()
CONFIG.read(os.path.join(MODULE_DIR, 'config.ini'))