# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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