# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thinman/__init__.py
# Compiled at: 2015-04-06 18:19:08
"""
    “Thin Man” backs up all metadata in your source tree of git repos.

    By recording the tree layout, ``git`` remotes and ‘refs’ of the typical
    ``~/src`` directory containing your cloned ``git`` repos, “Thin Man”
    can restore that structure later on, and also sync it to other machines.

    This can be also part of a backup strategy by only including that small
    amount of metadata in a backup set, instead of duplicating all the data
    that is available in remote locations anyway.

    That of course assumes that your repositories are usually clean and
    don't contain days of uncommitted work, and can be easily restored
    into working shape by bootstrap scripts and the like. But that's a
    given, right?

    Copyright ©  2015 Jürgen Hermann <jh@web.de>

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
from __future__ import absolute_import, unicode_literals, print_function
__url__ = b'https://github.com/jhermann/thin-man'
__version__ = b'0.1.0'
__license__ = b'Apache 2.0'
__author__ = b'Jürgen Hermann'
__author_email__ = b'jh@web.de'
__keywords__ = b'hosted.by.github python git tool backup metadata'
__all__ = []