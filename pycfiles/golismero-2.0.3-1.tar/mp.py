# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/golismero/patches/mp.py
# Compiled at: 2013-12-10 19:44:47
"""
Internally used submodule that contains runtime patches
to the standard multiprocessing library.

.. warning: Do not import this submodule in your code!
            This is only meant to be imported from the
            processmanager submodule!
"""
__license__ = '\nGoLismero 2.0 - The web knife - Copyright (C) 2011-2013\n\nAuthors:\n  Daniel Garcia Garcia a.k.a cr0hn | cr0hn<@>cr0hn.com\n  Mario Vilas | mvilas<@>gmail.com\n\nGolismero project site: https://github.com/golismero\nGolismero project mail: golismero.project<@>gmail.com\n\nThis program is free software; you can redistribute it and/or\nmodify it under the terms of the GNU General Public License\nas published by the Free Software Foundation; either version 2\nof the License, or (at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program; if not, write to the Free Software\nFoundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.\n'
__all__ = []
import sys
from os import path
from signal import signal, SIGINT

def __suicide(signum, frame):
    exit(1)


signal(SIGINT, __suicide)

class __FakeFile(object):

    def write(self, s):
        pass

    def flush(self):
        pass

    def close(self):
        pass


def __patched_bootstrap(self):
    signal(SIGINT, __suicide)
    stdout, stderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = __FakeFile(), __FakeFile()
    try:
        return __original_bootstrap(self)
    finally:
        sys.stdout, sys.stderr = stdout, stderr


if sys.platform == 'win32':

    def __patched_get_command_line():
        args = _original_get_command_line()
        assert args[(-3)] == '-c', 'internal error, are you sure this is Python 2.7?'
        assert args[(-2)] == 'from multiprocessing.forking import main; main()', 'internal error, are you sure this is Python 2.7?'
        assert args[(-1)] == '--multiprocessing-fork', 'internal error, are you sure this is Python 2.7?'
        here = path.abspath(path.join(path.split(__file__)[0], '..', '..'))
        tpl = path.join(here, 'thirdparty_libs')
        code = 'import sys; '
        if path.exists(tpl):
            ehere = here.replace("'", "\\'").replace('"', '\\x%.2x' % ord('"'))
            etpl = tpl.replace("'", "\\'").replace('"', '\\x%.2x' % ord('"'))
            code += "here = '%s'; " % ehere
            code += 'sys.path.insert(0, here); '
            code += "tpl = '%s'; " % etpl
            code += 'sys.path.insert(0, tpl); '
        code += 'from golismero.patches.mp import main; main()'
        args[-2] = code
        return args


    def __patched_prepare(data):
        golismero = sys.modules['golismero']
        try:
            del sys.modules['golismero']
            return _original_prepare(data)
        finally:
            sys.modules['golismero'] = golismero


    def main():
        from multiprocessing.forking import main as original_main
        from multiprocessing import Process
        __original_bootstrap = Process._bootstrap
        Process._bootstrap = __patched_bootstrap
        stdout, stderr = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = __FakeFile(), __FakeFile()
        try:
            original_main()
        finally:
            sys.stdout, sys.stderr = stdout, stderr


if __name__ != '__parents_main__' and __name__ != '__main__':
    from multiprocessing import Process
    __original_bootstrap = Process._bootstrap
    Process._bootstrap = __patched_bootstrap
    if sys.platform == 'win32':
        from multiprocessing import forking
        from multiprocessing.forking import get_command_line as _original_get_command_line
        forking.get_command_line = __patched_get_command_line
        from multiprocessing.forking import prepare as _original_prepare
        forking.prepare = __patched_prepare