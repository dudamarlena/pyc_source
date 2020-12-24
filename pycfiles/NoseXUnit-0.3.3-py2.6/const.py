# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/nosexunit/const.py
# Compiled at: 2009-09-22 16:55:25
import os
LOGGER = 'nose'
PANEL_TARGET_RIGHT = 'right_panel'
PANEL_TARGET_LEFT = 'left_panel'
HTML = 'html'
TEXT = 'text'
TARGET = os.path.join('target', 'NoseXUnit')
TARGET_CORE = os.path.join(TARGET, 'core')
TARGET_AUDIT = os.path.join(TARGET, 'audit')
TARGET_COVER = os.path.join(TARGET, 'cover')
PREFIX_CORE = 'TEST-'
EXT_CORE = 'xml'
SEARCH_EXCLUDE = [
 '.svn', 'CVS']
TEST_SUCCESS = 0
TEST_FAIL = 1
TEST_ERROR = 2
TEST_SKIP = 3
TEST_DEPRECATED = 4
UNK_TIME = 0
UNK_ERR_TYPE = 'unknown'
INIT = '__init__.py'
AUDIT_DEFAULT_REPORTER = 'nosexunit'
AUDIT_EXCHANGE_FILE = 'exchange.pkl'
AUDIT_EXCHANGE_ENTRY = 'NOSEXUNIT_EXCHANGE_FILE'
AUDIT_COVER_EXCLUDE = [
 'ez_setup', 'setup']
COVER_OUTPUT_BASE = '.coverage'