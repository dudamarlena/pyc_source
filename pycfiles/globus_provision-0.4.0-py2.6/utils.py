# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/globus/provision/common/utils.py
# Compiled at: 2012-03-02 22:17:19
"""
Miscellaneous utility functions.
"""
import glob, os
from os import environ
from boto.ec2.connection import EC2Connection, RegionInfo
from boto import connect_ec2
from passlib.hosts import linux_context

def create_ec2_connection(hostname=None, path=None, port=None):
    if hostname == None:
        if not (environ.has_key('AWS_ACCESS_KEY_ID') and environ.has_key('AWS_SECRET_ACCESS_KEY')):
            return
        else:
            return EC2Connection()
    else:
        if not (environ.has_key('EC2_ACCESS_KEY') and environ.has_key('EC2_SECRET_KEY')):
            return
        else:
            print 'Setting region'
            region = RegionInfo(name='eucalyptus', endpoint=hostname)
            return connect_ec2(aws_access_key_id=environ['EC2_ACCESS_KEY'], aws_secret_access_key=environ['EC2_SECRET_KEY'], is_secure=False, region=region, port=port, path=path)
    return


def parse_extra_files_files(f):
    l = []
    extra_f = open(f)
    for line in extra_f:
        (srcglob, dst) = line.split()
        srcs = glob.glob(os.path.expanduser(srcglob))
        srcs = [ s for s in srcs if os.path.isfile(s) ]
        dst_isdir = os.path.basename(dst) == ''
        for src in srcs:
            full_dst = dst
            if dst_isdir:
                full_dst += os.path.basename(src)
            l.append((src, full_dst))

    return l


def rest_table(col_names, rows):

    def gen_line(lens, char):
        return '+' + char + (char + '+' + char).join([ char * l for l in lens ]) + char + '+\n'

    num_cols = len(col_names)
    len_cols = [0] * num_cols
    height_row = [0] * len(rows)
    table = ''
    for (i, name) in enumerate(col_names):
        len_cols[i] = max(len(name), len_cols[i])

    for (i, row) in enumerate(rows):
        for j in range(num_cols):
            lines = row[j].split('\n')
            row_len = max([ len(l) for l in lines ])
            len_cols[j] = max(row_len, len_cols[j])
            height_row[i] = max(len(lines), height_row[i])

    table += gen_line(len_cols, '-')
    table += '|'
    for (i, name) in enumerate(col_names):
        table += ' '
        table += col_names[i].ljust(len_cols[i])
        table += ' |'

    table += '\n'
    table += gen_line(len_cols, '=')
    for (i, row) in enumerate(rows):
        for j in range(height_row[i]):
            table += '|'
            for (k, col) in enumerate(row):
                lines = col.split('\n')
                if len(lines) < j + 1:
                    col_txt = ' ' * len_cols[k]
                else:
                    col_txt = lines[j].ljust(len_cols[k])
                table += ' '
                table += col_txt
                table += ' |'

            table += '\n'

        table += gen_line(len_cols, '-')

    return table


def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)


def gen_sha512(passwd):
    return linux_context.encrypt(passwd)