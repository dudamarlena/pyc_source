# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/pymobiledevice/util/asciitables.py
# Compiled at: 2019-03-03 16:57:38


def print_table(title, headers, rows):
    widths = []
    for i in range(len(headers)):
        z = list(map(len, [ row[i] for row in rows ]))
        z.append(len(headers[i]))
        widths.append(max(z))

    width = sum(widths) + len(headers) + 1
    print '-' * width
    print '|' + title.center(width - 2) + '|'
    print '-' * width
    hline = '|'
    for i in range(len(headers)):
        hline += headers[i].ljust(widths[i]) + '|'

    print hline
    print '-' * width
    for row in rows:
        line = '|'
        for i in range(len(row)):
            line += row[i].ljust(widths[i]) + '|'

        print line

    if len(rows) == 0:
        print '|' + ('No entries').center(width - 2) + '|'
    print '-' * width
    print ''