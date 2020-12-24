# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\zhpy\info.py
# Compiled at: 2015-10-22 21:48:08
"""
zhpy package and plugin information

This is the MIT license:
http://www.opensource.org/licenses/mit-license.php

Copyright (c) 2007~ Fred Lin and contributors. zhpy is a trademark of Fred Lin.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following consditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""
import pkg_resources, sys
entrypoints = {'Traditional Chinese Keywords': 'plugtw.tools', 'Simplified Chinese Keywords': 'plugcn.tools'}

def retrieve_info():
    """
    retrieve package and plugins info
    """
    packages = [ '%s' % i for i in pkg_resources.require('zhpy') ]
    return packages


def info():
    """
    show zhpy informations including version and plugins

    ported from TurboGears2 tginfo command
    """
    print '\nComplete zhpy Version Information\n\nzhpy requires:\n'
    print '  * python', sys.version.split()[0]
    packages = retrieve_info()
    for p in packages:
        print '  *', p

    print ''