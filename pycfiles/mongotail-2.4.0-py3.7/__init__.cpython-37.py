# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mongotail/__init__.py
# Compiled at: 2020-04-09 11:10:14
# Size of source mod 2**32: 1692 bytes
__author__ = 'Mariano Ruiz'
__version__ = '2.4.0'
__license__ = 'GPL-3'
__url__ = 'https://github.com/mrsarm/mongotail'
__doc__ = 'Mongotail, Log all MongoDB queries in a "tail"able way.'
__usage__ = '%(prog)s [db address] [options]\n\ndb address can be:\n  foo                   foo database on local machine (IPv4 connection)\n  :1234/foo             foo database on local machine on port 1234\n  192.169.0.5/foo       foo database on 192.168.0.5 machine\n  192.169.0.5:9999/foo  foo database on 192.168.0.5 machine on port 9999\n  remotehost/foo        foo database on remotehost machine\n  "[::1]:9999/foo"      foo database on ::1 machine on port 9999 (IPv6 connection)'