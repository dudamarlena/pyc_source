# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\clement_besnier\PycharmProjects\old_norse_runes_db\runesdb\reader.py
# Compiled at: 2019-09-20 10:48:50
# Size of source mod 2**32: 620 bytes
"""

"""
import csv, codecs
__author__ = [
 'Clément Besnier <clemsciences@aol.com>']

def read(filename):
    with codecs.open(filename, 'r', encoding='utf-8-sig') as (f):
        reader = csv.DictReader(f, dialect=(csv.unix_dialect), delimiter=';', quoting=(csv.QUOTE_ALL))
        return [row for row in reader]


def extract_year(text):
    if '-' in text:
        beginning, end = text.split('-')
        return int((int(end) + int(beginning)) / 2)
    else:
        return int(text)


if __name__ == '__main__':
    runes_db_filename = 'runes_data.csv'
    read(runes_db_filename)