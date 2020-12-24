# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xslcover/runners/dblatex.py
# Compiled at: 2016-11-26 11:29:20
import os, sys
from subprocess import Popen
from argparse import ArgumentParser
from xslcover.coverapi import TraceRunnerBase

class TraceDblatex(TraceRunnerBase):

    def __init__(self):
        self.dblatex = 'dblatex'
        self.cmd = []

    def _parse_args(self, args):
        parser = ArgumentParser(description='Run dblatex with traces')
        parser.add_argument('--script', help='Script to call', default='dblatex')
        options, remain_args = parser.parse_known_args(args)
        self.dblatex = options.script
        return remain_args

    def trace_generator(self):
        return 'saxon'

    def run(self, args, trace_dir=''):
        args = self._parse_args(args)
        cmd = [
         self.dblatex, '-T', 'xsltcover']
        cmd += args
        self.cmd = cmd
        config_dir = os.environ.get('DBLATEX_CONFIG_FILES', '')
        if config_dir:
            pathsep = os.pathsep
        else:
            pathsep = ''
        config_dir += pathsep + os.path.abspath(os.path.dirname(__file__))
        env = {}
        env.update(os.environ)
        env.update({'DBLATEX_CONFIG_FILES': config_dir})
        if trace_dir:
            env.update({'TRACE_DIRECTORY': trace_dir})
        try:
            p = Popen(cmd, env=env)
            rc = p.wait()
        except OSError as e:
            print >> sys.stderr, 'dblatex seems to be missing: %s' % e
            rc = -1

        return rc


class TraceRunner(TraceDblatex):
    """Plugin Class to load"""
    pass