# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maciejczyzewski/teax/repository/teax/engines/latex.py
# Compiled at: 2016-02-03 14:19:14
import os, re, sys, subprocess
from teax.system.engine import EngineObject, EngineFacade

@EngineFacade.register
class LatexEngine(EngineObject):
    parseable_extensions = {'.latex', '.tex'}
    flags = [
     '-interaction nonstopmode',
     '-halt-on-error',
     '-file-line-error']

    def __init__(self, filename):
        self.filename = filename

    def start(self):
        _ftex = os.path.basename(self.filename)
        _cmd = (' ').join(['pdflatex'] + self.flags + [_ftex])
        p = subprocess.Popen(_cmd, shell=True, stdout=subprocess.PIPE)
        while p.poll() is None:
            self.parser(p.stdout.readline())

        print p.stdout.read()
        return

    def parser(self, line):
        """
        Interprets the line of LaTeX/TeX output. Each line has assigned
        symbol (i.e., 'W' means something is wrong, something missing).
        """
        if re.search('(?i)(.)rerun (.*)', line):
            pass
        if re.search('(?i)(.)warning(.*)', line):
            sys.stdout.write('W')
        elif re.search('(?i)(.)error(.*)', line):
            sys.stdout.write('E')
        else:
            sys.stdout.write('.')

    @classmethod
    def match(cls, filename, points=0):
        source = open(filename, 'rt').read()
        if filename.endswith(tuple(cls.parseable_extensions)):
            points += 1
        if '\\documentclass' in source:
            points += 1
        return points