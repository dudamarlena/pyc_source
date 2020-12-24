# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alex/envs/purelyjs/lib/python2.7/site-packages/purelyjs/interpreter.py
# Compiled at: 2014-10-19 05:40:32
import os, tempfile
from .io import invoke

class Interpreter(object):
    known_engines = [
     'js', 'rhino']

    def __init__(self, exes=None):
        engines = exes if exes else self.known_engines
        self.exe = self.detect(engines)
        if not self.exe:
            raise RuntimeError('No js engine could be found, tried: %s' % (', ').join(engines))

    def detect(self, engines):
        found = None
        for engine in engines:
            success, stdout, stderr = invoke(['which', engine])
            exe = stdout.decode('utf8')
            if success:
                if self.run_test_module(exe):
                    found = exe
                    break

        return found

    def run_test_module(self, exe):
        fd, filepath = tempfile.mkstemp()
        try:
            content = 'try {  print;} catch (e) {  if (e.name !== "ReferenceError") {    throw e;  }  print = console.log;}print(1 + 3);'
            content = content.encode('utf8')
            os.write(fd, content)
            success, stdout, stderr = invoke([exe, filepath])
            content = stdout.decode('utf8')
            if success and '4' == content:
                return True
        finally:
            os.close(fd)
            os.unlink(filepath)

    def run_module(self, filepath):
        success, stdout, stderr = invoke([self.exe, filepath])
        return (
         success, stderr)