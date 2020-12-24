# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tims/moxel/moxel/moxel-clients/python/moxel/bin/command_line.py
# Compiled at: 2017-09-21 03:30:55
import os, sys, moxel
try:
    from shlex import quote as cmd_quote
except ImportError:
    from pipes import quote as cmd_quote

def get_script_path():
    return os.path.dirname(os.path.realpath(sys.argv[0]))


_p = sys.platform
if _p.startswith('linux'):
    bin_path = 'linux'
elif _p == 'darwin':
    bin_path = 'osx'
elif _p == 'win32':
    bin_path = 'windows'
moxel_install_dir = os.path.dirname(os.path.abspath(moxel.__file__))
bin_path = os.path.join(moxel_install_dir, 'bin', bin_path, 'moxel')

def main():
    cmd = ('{} ' * len(sys.argv)).format(bin_path, *[ cmd_quote(arg) for arg in sys.argv[1:] ])
    os.system(cmd)


if __name__ == '__main__':
    main()