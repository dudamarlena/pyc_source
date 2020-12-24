# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/annogesiclib/extract_sec_info.py
# Compiled at: 2019-01-22 09:59:27
# Size of source mod 2**32: 1217 bytes
import os, shutil

def mod_file(input_file, out, indexs):
    with open(input_file) as (fh):
        for line in fh:
            line = line.strip()
            if line.startswith('>'):
                out.write(indexs[line] + '\n')
            else:
                out.write(line + '\n')

    out.close()


def extract_info_sec(sec_file, seq_file, index_file):
    out_sec = open(sec_file + 'tmp', 'w')
    out_seq = open(seq_file + 'tmp', 'w')
    indexs = {}
    with open(index_file) as (hi):
        for line in hi:
            line = line.strip()
            if line.startswith('>'):
                tag = line.split('|')[0]
                indexs[tag] = line

    mod_file(sec_file, out_sec, indexs)
    mod_file(seq_file, out_seq, indexs)
    os.remove(sec_file)
    shutil.move(sec_file + 'tmp', sec_file)
    os.remove(seq_file)
    shutil.move(seq_file + 'tmp', seq_file)


def modify_header(seq_file, index_file):
    out = open(seq_file, 'w')
    with open(index_file) as (fh):
        for line in fh:
            line = line.strip()
            if line.startswith('>'):
                tag = line.split('|')[0]
                out.write(tag + '\n')
            else:
                out.write(line + '\n')