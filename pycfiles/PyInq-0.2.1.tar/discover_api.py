# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\Auzzy\Documents\git\pyinq\examples\discover_api.py
# Compiled at: 2013-10-27 20:36:12
from pyinq import discover_tests
from pyinq import printers
suite = discover_tests('examples', suite_name='hello')
if suite:
    report = suite()
    printers.print_report(report)