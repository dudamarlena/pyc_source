# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/torchrs/shell/shell.py
# Compiled at: 2014-09-17 23:39:20
__author__ = 'Binh Vu <binh@toan2.com>'
import subprocess

def func(line):
    pass


class Shell(object):

    @staticmethod
    def call(args, callback=func):
        process = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = []
        for line in process.stdout:
            callback(line)
            output.append(line)

        process.wait()
        return output