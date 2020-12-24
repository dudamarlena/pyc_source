# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /src/colin/core/constant.py
# Compiled at: 2018-08-17 09:32:41
# Size of source mod 2**32: 1018 bytes
RULESET_DIRECTORY_NAME = 'rulesets'
RULESET_DIRECTORY = 'share/colin/' + RULESET_DIRECTORY_NAME
EXTS = ['.yaml', '.yml', '.json']
PASSED = 'PASS'
FAILED = 'FAIL'
ERROR = 'ERROR'
COLOURS = {PASSED: 'green', 
 FAILED: 'red', 
 ERROR: 'red'}
OUTPUT_CHARS = {PASSED: '.', 
 FAILED: 'x', 
 ERROR: '#'}
COLIN_CHECKS_PATH = 'CHECKS_PATH'