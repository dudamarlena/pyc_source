# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: dfuzz/core/target.py
# Compiled at: 2011-04-29 05:45:25
import shlex, logging, subprocess

class Target(object):

    def __init__(self, target, args=[]):
        self.target = target
        self.args = args
        self.stderr = ''
        self.stdout = ''
        self.code = 0

    def run(self, input_file):
        cmd = '%s %s' % (self.target,
         self.args % {'input': input_file})
        logging.debug('Running %s', cmd)
        proc = subprocess.Popen(shlex.split(cmd), env={'LIBC_FATAL_STDERR_': '1'}, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        (self.stdout, self.stderr) = proc.communicate()
        self.retcode = proc.poll()