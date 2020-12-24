# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shawn/Desktop/projects/cadnano2.5/cadnano/tests/pathsetup.py
# Compiled at: 2018-01-15 17:51:29
# Size of source mod 2**32: 270 bytes
import sys, os
pjoin, opd, opr = os.path.join, os.path.dirname, os.path.realpath
TEST_PATH = os.path.abspath(opd(__file__))
CN_PATH = opd(TEST_PATH)
PROJECT_PATH = opd(CN_PATH)
sys.path.insert(0, PROJECT_PATH)
sys.path.insert(0, TEST_PATH)