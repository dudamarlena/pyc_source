# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-2.2.1-i686/egg/tvrenamer/core/renamer.py
# Compiled at: 2015-11-08 18:30:19
import logging, os, shutil
from oslo_config import cfg
LOG = logging.getLogger(__name__)

def execute(filename, formatted_name):
    """Renames a file based on the name generated using metadata.

    :param str filename: absolute path and filename of original file
    :param str formatted_name: absolute path and new filename
    """
    if os.path.isfile(formatted_name):
        if not cfg.CONF.overwrite_file_enabled:
            LOG.info('File %s already exists not forcefully moving %s', formatted_name, filename)
            return
    LOG.info('renaming [%s] to [%s]', filename, formatted_name)
    if not cfg.CONF.dryrun:
        shutil.move(filename, formatted_name)