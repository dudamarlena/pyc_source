# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/db/maintenance.py
# Compiled at: 2015-06-14 13:30:57
"""Provides the ability to perform maintenance on a database."""
import logging, os, shutil, six.moves.urllib.parse as urlparse
LOG = logging.getLogger(__name__)
MAX_BACKUP_COUNT = 8

def backup(conf):
    """create a backup copy of the database file.

    :param oslo_config.cfg.ConfigOpts conf: an instance of configuration
    """
    LOG.debug('starting database backup process')
    default_db_name = urlparse.urlparse(conf.database.connection).path.replace('//', '/')
    LOG.debug('location of database: [%s]', default_db_name)
    if os.path.exists(default_db_name):
        for i in range(MAX_BACKUP_COUNT - 1, 0, -1):
            sfn = '%s.%d' % (default_db_name, i)
            dfn = '%s.%d' % (default_db_name, i + 1)
            if os.path.exists(sfn):
                if os.path.exists(dfn):
                    os.remove(dfn)
                os.rename(sfn, dfn)

        dfn = default_db_name + '.1'
        LOG.info('backing up db [%s] to [%s]', default_db_name, dfn)
        shutil.copy2(default_db_name, dfn)
        LOG.info('backup complete')
    else:
        LOG.warning('Database [%s] does not exist, no backup taken.', default_db_name)