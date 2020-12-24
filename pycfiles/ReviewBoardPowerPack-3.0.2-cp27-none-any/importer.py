# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /rbpowerpack/sshdb/importer.py
# Compiled at: 2019-06-17 15:11:31
from __future__ import unicode_literals
import logging
from reviewboard.site.models import LocalSite
from reviewboard.ssh.storage import FileSSHStorage
from rbpowerpack.sshdb.storage import DBSSHStorage

def _import_data(counts, namespace=None):
    file_storage = FileSSHStorage(namespace=namespace)
    db_storage = DBSSHStorage(namespace=namespace)
    key = file_storage.read_user_key()
    if key is not None:
        db_storage.write_user_key(key)
        counts[b'keys'] += 1
    host_keys = file_storage.read_host_keys()
    if host_keys:
        db_storage.import_host_keys(host_keys)
        counts[b'host_keys'] += 1
    return


def import_sshdb_keys():
    """Imports local filesystem SSH key information into the database.

    This will override any keys and host key lists that already exist in
    the database.
    """
    counts = {b'keys': 0, 
       b'host_keys': 0}
    _import_data(counts)
    for site in LocalSite.objects.all():
        _import_data(counts, site.name)

    logging.info(b'Imported %(keys)d SSH key(s) and %(host_keys)d known host key list(s)' % counts)