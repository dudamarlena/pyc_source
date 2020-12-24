# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/OpenDiscovery/runProcess.py
# Compiled at: 2014-08-19 20:12:50
import subprocess

class runProcess(object):
    """docstring for runProcess"""

    def __init__(self, verbose=False):
        self.verbose = verbose

    def run(self, command):
        if self.verbose:
            subprocess.call(command, shell=True)
        else:
            subprocess.call(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)