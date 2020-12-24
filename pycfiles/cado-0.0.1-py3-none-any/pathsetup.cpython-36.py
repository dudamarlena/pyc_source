# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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