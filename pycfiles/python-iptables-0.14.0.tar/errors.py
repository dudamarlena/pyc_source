# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/vilmos/Projects/python-iptables/iptc/errors.py
# Compiled at: 2018-04-16 20:15:10


class XTablesError(Exception):
    """Raised when an xtables call fails for some reason."""
    pass


__all__ = [
 'XTablesError']