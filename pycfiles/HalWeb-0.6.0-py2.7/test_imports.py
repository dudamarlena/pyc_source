# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/halicea/tests/test_imports.py
# Compiled at: 2011-12-25 05:31:43
import os
from os.path import dirname, join as pjoin
PROJECT_LOC = os.path.abspath(pjoin(dirname(__file__), 'testProjectV1_Actual'))
INSTALL_LOC = os.path.abspath(dirname(dirname(dirname(__file__))))
TEMPLATE_LOC = pjoin(INSTALL_LOC, 'Templates')
print PROJECT_LOC, INSTALL_LOC, TEMPLATE_LOC