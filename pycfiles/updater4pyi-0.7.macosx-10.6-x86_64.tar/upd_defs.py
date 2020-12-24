# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/updater4pyi/upd_defs.py
# Compiled at: 2014-12-07 08:43:19


class Updater4PyiError(Exception):
    """
    An exception class used to signify an error in the installation of a software update,
    for example.

    However, if you're not digging into the internals of the update interface, you
    probably won't even have to bother with catching these. See also
    :py:class:`~upd_core.Updater` and :py:class:`~upd_iface.UpdateInterface`.
    """

    def __init__(self, msg):
        self.updater_msg = msg
        Exception.__init__(self, 'Software Updater Error: ' + msg)


RELTYPE_UNKNOWN = 0
RELTYPE_EXE = 1
RELTYPE_ARCHIVE = 2
RELTYPE_BUNDLE_ARCHIVE = 3