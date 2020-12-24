# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pylxca/test/poc/interactive_argparse.py
# Compiled at: 2019-12-05 00:54:38
import ast
updateList = '[{"jobUID":"9","percentage":50}]'
rep = ast.literal_eval(updateList)
print rep