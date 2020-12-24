# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/scandb/exporter.py
# Compiled at: 2019-09-17 10:08:37
# Size of source mod 2**32: 1911 bytes
import argparse, sqlite3, os
host_port_list = "\n    select address , group_concat(distinct port), protocol from port where protocol = 'tcp' and status='open' group by address\n    union\n    select address , group_concat(distinct port), protocol from port where protocol = 'udp' and status='open' group by address;"

def gen_host_port_list(db, outfile):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(host_port_list)
    rows = cur.fetchall()
    with open(outfile, 'w') as (f):
        for r in rows:
            f.write(';'.join(r))
            f.write('\n')

    conn.close()


def gen_host_list(db, status, delimiter):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute('SELECT distinct address FROM host WHERE status like ? ;', (status,))
    rows = cur.fetchall()
    ips = [x[0] for x in rows]
    conn.close()
    return ips


def scandb2hostlist():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--db', type=str, required=False, default='scandb.sqlite')
    parser.add_argument('--status', type=str, required=False, default='up', help='Status string stored in database (default: up)')
    parser.add_argument('-d', '--list-delimiter', required=False, default='\n', help='Delimiter used to separate hosts in the list output')
    args = parser.parse_args()
    gen_host_list(args.db, args.status, args.list_delimiter)


def scandb2hostportlist():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('--db', type=str, required=False, default='scandb.sqlite')
    parser.add_argument('-o', '--outfile', metavar='FILE', required=False, type=str, default='hostportlist.csv', help='')
    args = parser.parse_args()
    gen_host_port_list(args.db, args.outfile)
    print('Results written to : {0}'.format(args.outfile))