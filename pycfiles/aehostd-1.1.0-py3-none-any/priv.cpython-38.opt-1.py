# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aehostd/priv.py
# Compiled at: 2019-11-15 08:00:05
# Size of source mod 2**32: 2424 bytes
"""
aehostd.priv - privileged helper service module
"""
from __future__ import absolute_import
import os, logging, time
from .__about__ import __version__
from .cfg import CFG
from .service import init_service
LOG_NAME = 'aehostd.priv'
DESCRIPTION = 'Privileged helper service for AE-DIR'
REFRESH_INTERVAL = 2.0

def process_sudoers(last_sudoers_stat):
    """
    Process sudoers file exported by aehostd
    """
    try:
        sudoers_stat = os.stat(CFG.sudoers_file)
    except OSError:
        return last_sudoers_stat
    else:
        next_sudoers_stat = last_sudoers_stat
        if last_sudoers_stat != sudoers_stat:
            target_filename = os.path.join(CFG.sudoers_includedir, os.path.basename(CFG.sudoers_file))
            logging.debug('New sudoers file at %s to be moved to %s', CFG.sudoers_file, target_filename)
            try:
                os.chmod(CFG.sudoers_file, 288)
                os.chown(CFG.sudoers_file, 0, 0)
                os.rename(CFG.sudoers_file, target_filename)
            except Exception:
                logging.error('Moving sudoers file at %s to %s failed!',
                  (CFG.sudoers_file),
                  target_filename,
                  exc_info=True)
            else:
                logging.info('Successfully moved sudoers file at %s to %s', CFG.sudoers_file, target_filename)
                next_sudoers_stat = sudoers_stat
        return next_sudoers_stat


def main():
    """
    entry point for privileged helper service running as root
    """
    script_name, ctx = init_service(LOG_NAME, DESCRIPTION, service_uid=0, service_gid=0)
    last_sudoers_stat = None
    with ctx:
        try:
            logging.debug('Started privileged helper service')
            while True:
                if CFG.sudoers_file:
                    last_sudoers_stat = process_sudoers(last_sudoers_stat)
                time.sleep(REFRESH_INTERVAL)

        except (KeyboardInterrupt, SystemExit) as exit_exc:
            try:
                logging.debug('Exit exception received: %r', exit_exc)
            finally:
                exit_exc = None
                del exit_exc

        else:
            logging.info('Stopped %s %s', script_name, __version__)


if __name__ == '__main__':
    main()