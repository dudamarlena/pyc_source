# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syzygy/runparserscript.py
# Compiled at: 2010-10-12 17:55:40
import optparse
from mpgutils import utils
import sys, re
from optparse import OptionParser
import os, subprocess

def main(argv=None):
    if not argv:
        argv = sys.argv
    perlpath = os.path.join('/home/radon00/rivas/bin/syzygyfinal/trunk/playground/Syzygy/perl/', 'ParseAnnotationOutput.pl')
    perlp = os.path.join('/util/bin/', 'perl')
    lstArgs = [perlp, perlpath]
    check_call(lstArgs)


def findFiles(folder_root, pattern):
    Files = []
    for (root, dirs, files) in os.walk(folder_root, False):
        for name in files:
            match = pattern.search(name)
            if match:
                Files.append(os.path.join(root, name))

    return Files


def check_call(lstArgs):
    retcode = subprocess.Popen(lstArgs)
    retcode.wait()


if __name__ == '__main__':
    main()