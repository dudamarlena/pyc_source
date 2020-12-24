# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/smr/map.py
# Compiled at: 2014-08-02 17:16:38
from __future__ import absolute_import, division, print_function, unicode_literals
import os, sys
from .config import get_config, configure_job
from .uri import download, cleanup

def write_to_stderr(file_status, file_size, file_name):
    sys.stderr.write((b'{},{},{}\n').format(file_status, file_size, file_name))
    sys.stderr.flush()


def run(config):
    configure_job(config)
    try:
        for uri in iter(sys.stdin.readline, b''):
            uri = uri.rstrip()
            temp_filename = None
            try:
                try:
                    temp_filename = download(config, uri)
                    file_size = os.path.getsize(temp_filename)
                    config.MAP_FUNC(temp_filename)
                    write_to_stderr(b'+', file_size, uri)
                except (KeyboardInterrupt, SystemExit):
                    sys.stderr.write((b'map worker {} aborted\n').format(os.getpid()))
                    sys.exit(1)
                except Exception as e:
                    sys.stderr.write((b'{}\n').format(e))
                    write_to_stderr(b'!', 0, uri)

            finally:
                sys.stdout.flush()
                if temp_filename:
                    cleanup(uri, temp_filename)

    except (KeyboardInterrupt, SystemExit):
        sys.stderr.write((b'map worker {} aborted\n').format(os.getpid()))
        sys.exit(1)

    return


def main():
    config = get_config()
    run(config)