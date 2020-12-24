# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/scripts-2.7/ml-initdb.py
# Compiled at: 2018-06-11 10:19:13
import argparse
from m_librarian.config import get_config
from m_librarian.db import open_db, init_db
from m_librarian.glst import import_glst
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Init')
    parser.add_argument('-C', '--config', help='configuration file')
    parser.add_argument('-D', '--database', help='database URI')
    args = parser.parse_args()
    if args.config:
        get_config(args.config)
    open_db(args.database)
    init_db()
    count_old, count_new = import_glst()
    if count_old:
        print 'Imported %d genres (ignored %d existing)' % (
         count_new, count_old)
    else:
        print 'Imported %d genres' % count_new