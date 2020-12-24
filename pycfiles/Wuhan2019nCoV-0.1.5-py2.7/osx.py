# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/wuhanncov/osx.py
# Compiled at: 2020-01-28 02:50:08
"""
Copyright (C) 2020 Jacksgong.com.

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
import os

def notify_mac(title, subtitle, message):
    if os.name == 'posix':
        t = "-title '%s'" % title
        s = "-subtitle '%s'" % subtitle
        m = "-message '%s'" % message
        cmd = (' ').join(['terminal-notifier', m, t, s]).encode('utf-8').strip()
        os.system(cmd)