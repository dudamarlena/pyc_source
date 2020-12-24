# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gnupg/_trust.py
# Compiled at: 2016-12-21 00:01:22
"""Functions for handling trustdb and trust calculations.

The functions within this module take an instance of :class:`gnupg.GPGBase` or
a suitable subclass as their first argument.
"""
from __future__ import absolute_import
import os
from . import _util
from ._util import log

def _create_trustdb(cls):
    """Create the trustdb file in our homedir, if it doesn't exist."""
    trustdb = os.path.join(cls.homedir, 'trustdb.gpg')
    if not os.path.isfile(trustdb):
        log.info('GnuPG complained that your trustdb file was missing. %s' % 'This is likely due to changing to a new homedir.')
        log.info('Creating trustdb.gpg file in your GnuPG homedir.')
        cls.fix_trustdb(trustdb)


def export_ownertrust(cls, trustdb=None):
    """Export ownertrust to a trustdb file.

    If there is already a file named :file:`trustdb.gpg` in the current GnuPG
    homedir, it will be renamed to :file:`trustdb.gpg.bak`.

    :param string trustdb: The path to the trustdb.gpg file. If not given,
                           defaults to ``'trustdb.gpg'`` in the current GnuPG
                           homedir.
    """
    if trustdb is None:
        trustdb = os.path.join(cls.homedir, 'trustdb.gpg')
    try:
        os.rename(trustdb, trustdb + '.bak')
    except (OSError, IOError) as err:
        log.debug(str(err))

    export_proc = cls._open_subprocess(['--export-ownertrust'])
    tdb = open(trustdb, 'wb')
    _util._threaded_copy_data(export_proc.stdout, tdb)
    return


def import_ownertrust(cls, trustdb=None):
    """Import ownertrust from a trustdb file.

    :param str trustdb: The path to the trustdb.gpg file. If not given,
                        defaults to :file:`trustdb.gpg` in the current GnuPG
                        homedir.
    """
    if trustdb is None:
        trustdb = os.path.join(cls.homedir, 'trustdb.gpg')
    import_proc = cls._open_subprocess(['--import-ownertrust'])
    try:
        tdb = open(trustdb, 'rb')
    except (OSError, IOError):
        log.error('trustdb file %s does not exist!' % trustdb)

    _util._threaded_copy_data(tdb, import_proc.stdin)
    return


def fix_trustdb(cls, trustdb=None):
    """Attempt to repair a broken trustdb.gpg file.

    GnuPG>=2.0.x has this magical-seeming flag: `--fix-trustdb`. You'd think
    it would fix the the trustdb. Hah! It doesn't. Here's what it does
    instead::

      (gpg)~/code/python-gnupg $ gpg2 --fix-trustdb
      gpg: You may try to re-create the trustdb using the commands:
      gpg:   cd ~/.gnupg
      gpg:   gpg2 --export-ownertrust > otrust.tmp
      gpg:   rm trustdb.gpg
      gpg:   gpg2 --import-ownertrust < otrust.tmp
      gpg: If that does not work, please consult the manual

    Brilliant piece of software engineering right there.

    :param str trustdb: The path to the trustdb.gpg file. If not given,
                        defaults to :file:`trustdb.gpg` in the current GnuPG
                        homedir.
    """
    if trustdb is None:
        trustdb = os.path.join(cls.homedir, 'trustdb.gpg')
    export_proc = cls._open_subprocess(['--export-ownertrust'])
    import_proc = cls._open_subprocess(['--import-ownertrust'])
    _util._threaded_copy_data(export_proc.stdout, import_proc.stdin)
    return