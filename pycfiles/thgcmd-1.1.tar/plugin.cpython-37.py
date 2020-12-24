# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tools/tmp/cmd2/thgcmd/plugin.py
# Compiled at: 2019-07-17 15:13:03
# Size of source mod 2**32: 378 bytes
"""Classes for the thgcmd plugin system"""
import attr

@attr.s
class PostparsingData:
    stop = attr.ib()
    statement = attr.ib()


@attr.s
class PrecommandData:
    statement = attr.ib()


@attr.s
class PostcommandData:
    stop = attr.ib()
    statement = attr.ib()


@attr.s
class CommandFinalizationData:
    stop = attr.ib()
    statement = attr.ib()