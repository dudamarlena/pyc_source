# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/scandb/importer.py
# Compiled at: 2019-09-17 10:08:37
# Size of source mod 2**32: 1876 bytes
from __future__ import print_function
import argparse, os
from termcolor import colored
from scandb.models import init_db
from scandb.nmap import import_nmap_file
from scandb.nessus import import_nessus_file

def importer():
    """
    Entry point for the console script scandb-importer. This script allows to import either a single nessus|nmap XML-file or
    several nessus|nmap XML-files within a given directory.
    :return:
    """
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--db', type=str, required=False, default='scandb.sqlite')
    parser.add_argument('--file', metavar='FILE', type=str, default=None, nargs='*', help='The nessus and/or nmap file(s)')
    parser.add_argument('--dir', metavar='DIR', type=str, default=None, help='Directory name with nessus and/or nmap files')
    args = parser.parse_args()
    db = args.db
    filename = args.file
    dir = args.dir
    database = init_db(db)
    if filename is None:
        if dir is None:
            parser.print_usage()
            return
    if filename is not None:
        for file in filename:
            if file.endswith('.nessus'):
                import_nessus_file(file)
            if file.endswith('.xml'):
                import_nmap_file(file)

    if dir is not None:
        for filename in os.listdir(dir):
            if filename.endswith('.nessus'):
                fullname = os.path.join(dir, filename)
                import_nessus_file(fullname)
            if filename.endswith('.xml'):
                fullname = os.path.join(dir, filename)
                import_nmap_file(fullname)

    database.close()