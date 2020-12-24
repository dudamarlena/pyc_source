# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/seeing/__init__.py
# Compiled at: 2020-03-18 07:29:23
# Size of source mod 2**32: 1572 bytes
"""
monitor file modify then execute it.
support go, python, c++, c.
filename endswith .py .c .cpp .go
"""
__author__ = 'Mikele'
__version__ = '0.1.5'
import os, time, logging, argparse
logging.basicConfig(level=(logging.INFO))
help_text = 'monitor execute file every seconds.'
parser = argparse.ArgumentParser(description=(help_text + ' support go cpp c py'))
parser.add_argument(dest='filename', metavar='filename')
parser.add_argument('-s',
  '--seconds', metavar='seconds', action='store', default=1.0,
  help=help_text)
parser.add_argument('-c',
  '--cmd', metavar='cmd', action='store', default='', help='command to execute script, eg: seeing -c bash hello.sh')
commands = [
 'go', 'python', 'py', 'python3', 'g++', 'gcc']

def monitor_file_modify_every(seconds, filename, command):
    st = os.stat(filename).st_mtime
    while True:
        f = os.stat(filename)
        if st != f.st_mtime:
            if command not in commands:
                st = f.st_mtime
                if filename.endswith('.cpp'):
                    cmd = 'g++ {} && ./a.out'
                else:
                    if filename.endswith('.c'):
                        cmd = 'gcc {} && ./a.out'
                    else:
                        if filename.endswith('.py'):
                            cmd = 'python {}'
                        else:
                            if filename.endswith('.go'):
                                cmd = 'go run {}'
                            else:
                                cmd = command + ' {}'
                    os.system(cmd.format(filename))
                    logging.info(cmd.format(filename))
        try:
            time.sleep(seconds)
        except KeyboardInterrupt:
            os._exit(0)