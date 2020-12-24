# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/apacheconfig/error.py
# Compiled at: 2019-10-17 01:00:18


class ApacheConfigError(Exception):
    pass


class ConfigFileReadError(ApacheConfigError):
    pass