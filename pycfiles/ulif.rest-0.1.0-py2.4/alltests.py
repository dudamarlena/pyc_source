# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ulif/rest/tests/alltests.py
# Compiled at: 2008-02-24 09:47:59
"""'exec python -u "$0" "$@" #"""
__doc__ = "\nAll modules named 'test_*.py' in the current directory, and recursively in\nsubdirectories (packages) called 'test_*', are loaded and test suites within\nare run.\n"
import time
start = time.time()
import sys, os, DocutilsTestSupport, docutils

class Tee:
    """Write to a file and a stream (default: stdout) simultaneously."""
    __module__ = __name__

    def __init__(self, filename, stream=sys.__stdout__):
        self.file = open(filename, 'w')
        self.stream = stream

    def write(self, string):
        self.stream.write(string)
        self.file.write(string)

    def flush(self):
        self.stream.flush()
        self.file.flush()


def pformat(suite):
    step = 4
    suitestr = repr(suite).replace('=[<', '=[\n<').replace(', ', ',\n')
    indent = 0
    output = []
    for line in suitestr.splitlines():
        output.append(' ' * indent + line)
        if line[-1:] == '[':
            indent += step
        elif line[-5:] == ']>]>,':
            indent -= step * 2
        elif line[-3:] == ']>,':
            indent -= step

    return ('\n').join(output)


def suite():
    (path, script) = os.path.split(sys.argv[0])
    suite = package_unittest.loadTestModules(DocutilsTestSupport.testroot, 'test_', packages=1)
    sys.stdout.flush()
    return suite


sys.stdout = sys.stderr = Tee('alltests.out')
import package_unittest
test_suite = suite
if __name__ == '__main__':
    suite = suite()
    print 'Testing Docutils %s [%s] with Python %s on %s at %s' % (docutils.__version__, docutils.__version_details__, sys.version.split()[0], time.strftime('%Y-%m-%d'), time.strftime('%H:%M:%S'))
    print 'Working directory: %s' % os.getcwd()
    print 'Docutils package: %s' % os.path.dirname(docutils.__file__)
    sys.stdout.flush()
    package_unittest.main(suite)
    finish = time.time()
    print 'Elapsed time: %.3f seconds' % (finish - start)