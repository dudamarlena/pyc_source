# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\dev\pylib\visvis\utils\ssdf\tests\test_simple.py
# Compiled at: 2017-05-31 18:20:46
# Size of source mod 2**32: 223 bytes
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, ssdf
s1 = ssdf.load('test1.ssdf')
tmp = ssdf.saves(s1)
s2 = ssdf.loads(tmp)
print(s2)