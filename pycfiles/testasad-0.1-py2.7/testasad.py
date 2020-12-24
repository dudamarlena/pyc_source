# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\testasad\testasad.py
# Compiled at: 2018-03-15 10:10:08
import csv
output_buffer = []

def add_row(rows):
    output_buffer.append(rows)


def add_rows(rows):
    for row in rows:
        add_row(row)


def save():
    for row in output_buffer:
        print row


def save_csv(string):
    reader = csv.reader(string.split('\n'), delimiter=',')
    for row in reader:
        print row