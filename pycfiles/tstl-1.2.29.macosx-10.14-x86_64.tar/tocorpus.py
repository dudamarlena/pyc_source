# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/local/Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/tstl/tocorpus.py
# Compiled at: 2019-02-11 12:34:52
from __future__ import print_function
import sys, os
current_working_dir = os.getcwd()
sys.path.append(current_working_dir)
if '--help' not in sys.argv:
    import sut as SUT

def main():
    if '--help' in sys.argv:
        print('Usage:  tstl_toafl <outputdir> <files>')
        sys.exit(0)
    sut = SUT.sut()
    outputDir = sys.argv[1]
    files = sys.argv[2:]
    i = 0
    for f in files:
        t = sut.loadTest(f)
        sut.saveTest(t, outputDir + '/' + os.path.basename(f) + '.afl', afl=True)
        i += 1