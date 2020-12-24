# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/pylox/__init__.py
# Compiled at: 2017-01-19 19:08:53
# Size of source mod 2**32: 908 bytes
__version__ = '0.0.1'
import sys
from .scanner import Scanner

class Lox(object):

    def __init__(self):
        self.had_error = False

    def error_code(self):
        if self.had_error:
            return 1
        else:
            return 0

    def run_file(self, filename):
        with open(filename, 'r') as (f):
            self.run(f.read())
            if self.had_error:
                sys.exit(65)

    def run_prompt(self):
        while True:
            s = input('> ')
            self.run(s)
            self.had_error = False

    def run(self, source):
        scanner = Scanner(source)
        tokens = scanner.scan_tokens()
        for token in tokens:
            print(token)

    def error(self, line, message):
        self.report(line, '', message)

    def report(self, line, where, message):
        text = f"[line {line}] Error {where}: {message}"
        print(text, file=(sys.stderr))
        self.had_error = True