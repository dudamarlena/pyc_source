# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/thejoeejoee/projects/VUT-FIT-IFJ-2017-tests/ifj2017/test/base.py
# Compiled at: 2017-12-01 03:11:23
# Size of source mod 2**32: 662 bytes
from collections import namedtuple
from ..interpreter.state import State
TestInfo = namedtuple('TestInfo', 'name code stdin stdout compiler_exit_code interpreter_exit_code info section_dir extensions timeout')

class TestReport(object):
    compiler_stdout = None
    compiler_stderr = None
    compiler_exit_code = None
    interpreter_stdout = None
    interpreter_stderr = None
    interpreter_exit_code = None
    state = None
    test_info = None
    groot_price = None
    success = None
    skipped = None


__all__ = [
 'TestReport', 'TestInfo']