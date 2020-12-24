# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/irk/util/storage/database.py
# Compiled at: 2018-06-21 18:58:03
# Size of source mod 2**32: 1541 bytes
from bisect import bisect_left
from . import etcfile
installed_database = []
packages = []
DB_FILE = etcfile.EtcFile('instdb')

def search_entry(package):
    global installed_database
    global packages
    i = bisect_left(packages, package)
    if i != len(packages):
        if packages[i] == package:
            return (
             installed_database[i], i)


def delete_entry(package):
    i = bisect_left(packages, package)
    if i != len(packages):
        if packages[i] == package:
            del installed_database[i]
            del packages[i]
    else:
        raise ValueError()


def insert_entry(e):
    i = bisect_left(packages, e[0])
    packages.insert(i, e[0])
    installed_database.insert(i, e)


def load_installed_database():
    global installed_database
    global packages
    packages = []
    installed_database = []
    if not DB_FILE.fullpath.exists():
        write_database()
    print('(Reading database... ', end='')
    with DB_FILE.open('r') as (f):
        i = 0
        while True:
            line = f.readline()
            if line == '':
                break
            i += 1
            line = line[:-1]
            line = line.split(' ')
            packages.append(line[0])
            installed_database.append(line)

    print(f" {i} packages installed.)")


def write_database():
    print('Writing package database... ', end='')
    with DB_FILE.open('w') as (f):
        for i in installed_database:
            f.write(' '.join(i))
            f.write('\n')

    print('done.')