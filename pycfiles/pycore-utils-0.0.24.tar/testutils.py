# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/testutils.py
# Compiled at: 2016-06-16 16:03:55
__doc__ = '\nCopyright (c) 2014-2015 Maciej Nabozny\n\nThis file is part of CloudOver project.\n\nCloudOver is free software: you can redistribute it and/or modify\nit under the terms of the GNU General Public License as published by\nthe Free Software Foundation, either version 3 of the License, or\n(at your option) any later version.\n\nThis program is distributed in the hope that it will be useful,\nbut WITHOUT ANY WARRANTY; without even the implied warranty of\nMERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\nGNU General Public License for more details.\n\nYou should have received a copy of the GNU General Public License\nalong with this program.  If not, see <http://www.gnu.org/licenses/>.\n'
import subprocess

def ssh_call(hostname, username, command, expect_code=None):
    p = subprocess.Popen(['ssh', '%s@%s' % (username, hostname), command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    p.wait()
    stdout = p.stdout.read()
    stderr = p.stderr.read()
    print '%s@%s' % (username, hostname) + ': ' + command + ': ' + stdout
    if expect_code != None and p.returncode != expect_code:
        print 'STDOUT: ' + stdout
        print '##################'
        print 'STDERR: ' + stderr
        print '##################'
        raise Exception('command %s failed' % command)
    return (
     p.returncode, stdout, stderr)