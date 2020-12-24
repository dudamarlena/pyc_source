# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alex/envs/purelyjs/lib/python2.7/site-packages/purelyjs/testmodule.py
# Compiled at: 2014-05-22 14:55:25
import os, tempfile

class TestModule(object):

    def __init__(self, testdir, interpreter, modules, test_case, keep_module=False):
        self.testdir = testdir
        self.interpreter = interpreter
        self.modules = modules
        self.test_case = test_case
        self.keep_module = keep_module
        self.passed = None
        self.stderr = None
        self.filepath = None
        return

    def assemble(self):
        fd, self.filepath = tempfile.mkstemp(dir=self.testdir, prefix='%s_' % self.test_case, suffix='.js', text=True)
        try:
            for module in self.modules:
                with open(module, 'rt') as (f):
                    content = f.read()
                content = '%s\n\n' % content
                content = content.encode('utf8')
                os.write(fd, content)

            content = '%s();\n' % self.test_case
            content = content.encode('utf8')
            os.write(fd, content)
        finally:
            os.close(fd)

    def run(self):
        self.assemble()
        try:
            passed, stderr = self.interpreter.run_module(self.filepath)
            if passed:
                self.passed = True
            else:
                self.passed = False
                self.stderr = stderr
        finally:
            if not self.keep_module:
                os.unlink(self.filepath)