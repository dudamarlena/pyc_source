# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pytestreport\__init__.py
# Compiled at: 2019-06-03 02:21:41
# Size of source mod 2**32: 1118 bytes
import sys, json
from .HTMLTestRunner import HTMLTestRunner as TestRunner, main
from .api import make_report
__all__ = [
 'TestRunner', 'main', 'shell', 'web']

def shell():
    arg_len = len(sys.argv)
    if arg_len == 1:
        print(f"\n        Usage:\n            {sys.argv[0]} data.json [reportfile theme, htmltemplate, stylesheet, javascript]\n        ")
        exit(1)
    data_file = 'data.json'
    report_file = 'PyTestReport.html'
    theme = htmltemplate = stylesheet = javascript = None
    if arg_len > 1:
        data_file = sys.argv[1]
    if arg_len > 2:
        report_file = sys.argv[2]
    if arg_len > 3:
        theme = sys.argv[3]
    if arg_len > 4:
        htmltemplate = sys.argv[4]
    if arg_len > 5:
        stylesheet = sys.argv[5]
    if arg_len > 6:
        javascript = sys.argv[6]
    with open(data_file, 'r', encoding='utf-8') as (f):
        data = json.load(f)
        with open(report_file, 'wb') as (fp):
            make_report(fp, data, theme=theme, htmltemplate=htmltemplate, stylesheet=stylesheet,
              javascript=javascript)


def web():
    pass