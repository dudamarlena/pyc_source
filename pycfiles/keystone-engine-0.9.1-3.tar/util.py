# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/me/projects/keystone.git/tmp/keystone.git/llvm/utils/llvm-build/llvmbuild/util.py
# Compiled at: 2016-06-04 06:22:29
import os, sys

def _write_message(kind, message):
    program = os.path.basename(sys.argv[0])
    sys.stderr.write('%s: %s: %s\n' % (program, kind, message))


note = lambda message: _write_message('note', message)
warning = lambda message: _write_message('warning', message)
error = lambda message: _write_message('error', message)
fatal = lambda message: (_write_message('fatal error', message), sys.exit(1))
__all__ = [
 'note', 'warning', 'error', 'fatal']