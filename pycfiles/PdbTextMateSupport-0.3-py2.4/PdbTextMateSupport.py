# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.1-i386/egg/PdbTextMateSupport.py
# Compiled at: 2007-02-17 18:45:15
from os.path import exists
from os import system

def mate(self):
    (frame, lineno) = self.stack[self.curindex]
    filename = self.canonic(frame.f_code.co_filename)
    if exists(filename):
        tm_url = 'txmt://open?url=file://%s&line=%d&column=2' % (filename, lineno)
        osa_cmd = 'tell application "TextMate" to get url "%s"' % tm_url
        system("osascript -e '%s'" % osa_cmd)


def preloop(self):
    mate(self)


def precmd(self, line):
    mate(self)
    return line