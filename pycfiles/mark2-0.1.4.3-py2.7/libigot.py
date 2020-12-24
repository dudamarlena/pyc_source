# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mk2/servers/libigot.py
# Compiled at: 2013-08-16 22:15:55
from . import JenkinsJarProvider

class Libigot(JenkinsJarProvider):
    name = 'Libigot'
    base = 'http://build.libigot.org/'
    project = 'Libigot'


ref = Libigot