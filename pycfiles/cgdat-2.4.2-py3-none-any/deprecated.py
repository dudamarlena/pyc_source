# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgcloud/core/deprecated.py
# Compiled at: 2016-11-22 15:21:45


def deprecated(artifact):
    artifact.__cgcloud_core_deprecated__ = True
    return artifact


def is_deprecated(artifact):
    return getattr(artifact, '__cgcloud_core_deprecated__ ', False)