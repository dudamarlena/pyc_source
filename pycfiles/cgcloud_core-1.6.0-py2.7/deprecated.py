# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/core/deprecated.py
# Compiled at: 2016-11-22 15:21:45


def deprecated(artifact):
    artifact.__cgcloud_core_deprecated__ = True
    return artifact


def is_deprecated(artifact):
    return getattr(artifact, '__cgcloud_core_deprecated__ ', False)