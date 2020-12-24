# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/indra/util/llsubprocess.py
# Compiled at: 2008-07-21 18:56:18
"""@file llsubprocess.py
@author Phoenix
@date 2008-01-18
@brief The simplest possible wrapper for a common sub-process paradigm.

$LicenseInfo:firstyear=2007&license=mit$

Copyright (c) 2007-2008, Linden Research, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
$/LicenseInfo$
"""
import os, popen2, time, select

class Timeout(RuntimeError):
    """Exception raised when a subprocess times out."""
    __module__ = __name__


def run(command, args=None, data=None, timeout=None):
    """@brief Run command with arguments

This is it. This is the function I want to run all the time when doing
subprocces, but end up copying the code everywhere. none of the
standard commands are secure and provide a way to specify input, get
all the output, and get the result.
@param command A string specifying a process to launch.
@param args Arguments to be passed to command. Must be list, tuple or None.
@param data input to feed to the command.
@param timeout Maximum number of many seconds to run.
@return Returns (result, stdout, stderr) from process.
"""
    cmd = [
     command]
    if args:
        cmd.extend([ str(arg) for arg in args ])
    child = popen2.Popen3(cmd, True)
    out = []
    err = []
    result = -1
    time_left = timeout
    tochild = [child.tochild.fileno()]
    while True:
        time_start = time.time()
        (p_in, p_out, p_err) = select.select([child.fromchild.fileno(), child.childerr.fileno()], tochild, [], time_left)
        if p_in:
            new_line = os.read(child.fromchild.fileno(), 32 * 1024)
            if new_line:
                out.append(new_line)
            new_line = os.read(child.childerr.fileno(), 32 * 1024)
            if new_line:
                err.append(new_line)
        if p_out:
            if data:
                bytes = os.write(child.tochild.fileno(), data)
                data = data[bytes:]
                if len(data) == 0:
                    data = None
                    tochild = []
                    child.tochild.close()
        result = child.poll()
        if result != -1:
            child.tochild.close()
            child.fromchild.close()
            child.childerr.close()
            break
        if time_left is not None:
            time_left -= time.time() - time_start
            if time_left < 0:
                raise Timeout

    out = ('').join(out)
    err = ('').join(err)
    return (
     result, out, err)