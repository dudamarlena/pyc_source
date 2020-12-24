# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pylxca/test/poc/interactive_argparse.py
# Compiled at: 2019-12-05 00:54:38
import ast
updateList = '[{"jobUID":"9","percentage":50}]'
rep = ast.literal_eval(updateList)
print rep