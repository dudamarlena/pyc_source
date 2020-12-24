# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/nielsen/files.py
# Compiled at: 2020-05-04 00:23:44
# Size of source mod 2**32: 1932 bytes
"""
System-level file operations needed by the API. These functions operate on the
various Path class objects provided by the pathlib library. These functions
probably won't ever need to be called directly by a client.
"""
import logging
from shutil import chown, move as su_move
from nielsen.config import CONFIG

def set_file_mode(file):
    """Set the mode of `file` to the value defined in `CONFIG`."""
    if CONFIG.get('Options', 'Mode'):
        try:
            file.chmod(int(CONFIG.get('Options', 'Mode'), 8))
        except PermissionError as err:
            try:
                logging.error('chmod failed. %s', err)
                raise
            finally:
                err = None
                del err


def set_file_ownership(file):
    """Set owner and group of `file` to the values defined in `CONFIG`."""
    if CONFIG.get('Options', 'User') or CONFIG.get('Options', 'Group'):
        try:
            chown(file, CONFIG.get('Options', 'User') or None, CONFIG.get('Options', 'Group') or None)
            status = True
        except PermissionError as err:
            try:
                logging.error('chown failed. %s', err)
                raise
            finally:
                err = None
                del err


def create_hierarchy(file):
    """Create the directory hierarchy for the given `file`."""
    try:
        file.parent.mkdir(mode=(int(CONFIG.get('Options', 'mode'), 8)), parents=True,
          exist_ok=True)
        logging.debug('Created: %s', file.parent)
        status = True
    except FileExistsError:
        logging.debug('%s already exists', file.parent)
    except PermissionError as err:
        try:
            logging.error(err)
            raise
        finally:
            err = None
            del err


def move(src, dst):
    """Move the file `src` to the path `dst`, but do not overwrite existing files."""
    if dst.exists() or src == dst:
        logging.debug('%s already in MediaPath. File will not be moved.', dst)
    try:
        su_move(src, dst)
    except PermissionError as err:
        try:
            logging.error(err)
            raise
        finally:
            err = None
            del err