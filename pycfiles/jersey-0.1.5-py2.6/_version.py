# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jersey/_version.py
# Compiled at: 2010-11-11 16:27:22
try:
    from twisted.python.versions import Version
except ImportError:

    class Version(object):

        def __init__(self, package, major, minor, nano, pre=None):
            self.package = package
            self.major = major
            self.minor = minor
            self.nano = nano
            self.pre = pre

        def short(self):
            fmt = '{0.major}.{0.minor}.{0.nano}'
            if self.pre:
                fmt += 'pre{0.pre}'
            return fmt.format(self)


version = Version('jersey', 0, 1, 5)
copyright = 'Copyright 2010, Yahoo! Inc.  All rights reserved.'
license = '\nSoftware Copyright License Agreement (BSD License)\n\nCopyright (c) 2010, Yahoo! Inc.\nAll rights reserved.\n\nWritten by Oliver V. Gould for Yahoo!, Inc.\n\nRedistribution and use of this software in source and binary forms, with or\nwithout modification, are permitted provided that the following conditions are\nmet:\n\n* Redistributions of source code must retain the above\n  copyright notice, this list of conditions and the\n  following disclaimer.\n\n* Redistributions in binary form must reproduce the above\n  copyright notice, this list of conditions and the\n  following disclaimer in the documentation and/or other\n  materials provided with the distribution.\n\n* Neither the name of Yahoo! Inc. nor the names of its\n  contributors may be used to endorse or promote products\n  derived from this software without specific prior\n  written permission of Yahoo! Inc.\n\nTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND\nANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED\nWARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE\nDISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR\nANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES\n(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;\nLOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON\nANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT\n(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS\nSOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n'