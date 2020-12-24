# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/reviewday/util.py
# Compiled at: 2011-11-20 20:04:50
import os, shutil, html_helper
from Cheetah.Template import Template

def prep_out_dir(out_dir='out_report'):
    src_dir = os.path.dirname(__file__)
    report_files_dir = os.path.join(src_dir, 'report_files')
    if os.path.exists(out_dir):
        print 'WARNING: output directory "%s" already exists' % out_dir
    else:
        shutil.copytree(report_files_dir, out_dir)


def create_report(name_space={}):
    filename = os.path.join(os.path.dirname(__file__), 'report.html')
    report_text = open(filename).read()
    name_space['helper'] = html_helper
    t = Template(report_text, searchList=[name_space])
    out_dir = 'out_report'
    prep_out_dir(out_dir)
    out_file = open(os.path.join(out_dir, 'index.html'), 'w')
    out_file.write(str(t))
    out_file.close()