# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/tests/testutils.py
# Compiled at: 2016-06-16 16:03:55
"""
Copyright (c) 2014-2015 Maciej Nabozny

This file is part of CloudOver project.

CloudOver is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
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
    return (p.returncode, stdout, stderr)