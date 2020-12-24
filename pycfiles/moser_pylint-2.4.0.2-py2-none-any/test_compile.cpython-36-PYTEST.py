# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/functional/test_compile.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 242 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar

class WrapperClass(object):

    def method(self):
        var = 4294967296
        self.method.__code__.co_consts