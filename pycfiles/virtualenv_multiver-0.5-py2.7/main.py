# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/virtualenv_multiver/main.py
# Compiled at: 2015-06-28 04:54:14
from __future__ import unicode_literals
import os, shutil, subprocess, sys
from virtualenv import mach_o_change

def main():
    if len(sys.argv) < 3:
        sys.stderr.write(b'Usage: virtualenv-multiver <path> <X.Y>...\n')
        sys.exit(1)
    path = sys.argv[1]
    versions = sys.argv[2:]
    bin_path = os.path.join(path, b'bin')
    python_bin_path = os.path.join(bin_path, b'python')
    for version in versions:
        pythonxy_bin = b'python%s' % version
        pythonxy_bin_path = os.path.join(bin_path, pythonxy_bin)
        for link_path in (os.path.join(bin_path, b'python'),
         os.path.join(bin_path, b'python%s' % version[0]),
         os.path.join(path, b'.Python')):
            try:
                os.unlink(link_path)
            except OSError:
                pass

        subprocess.call([b'virtualenv', b'-p', pythonxy_bin, path])
        if os.path.islink(pythonxy_bin_path):
            os.unlink(pythonxy_bin_path)
            shutil.move(python_bin_path, pythonxy_bin_path)
            os.symlink(pythonxy_bin, python_bin_path)
        mac_python_link = os.path.join(path, b'.Python')
        if os.path.exists(mac_python_link):
            new_mac_python_link = os.path.join(path, b'.Py%s' % version)
            shutil.move(mac_python_link, new_mac_python_link)
            orig_python_path = os.readlink(new_mac_python_link)
            old_python_exec_path = b'@executable_path/../.Python'
            new_python_exec_path = b'@executable_path/../.Py%s' % version
            try:
                mach_o_change(pythonxy_bin_path, old_python_exec_path, new_python_exec_path)
            except:
                try:
                    subprocess.call([b'install_name_tool', b'-change',
                     old_python_exec_path,
                     new_python_exec_path,
                     pythonxy_bin_path])
                except:
                    sys.stderr.write(b'Could not patch %s with the Python path. Make sure to install the Apple development tools.\n')
                    raise