# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ahayes/.virtualenvs/roicrm-django1.7/local/lib/python2.7/site-packages/django_toolkit/table/console.py
# Compiled at: 2013-03-19 00:20:36


class ConsoleTable:
    """
    Output a table in plain text format. 
    """

    def __init__(self, headers, rows):
        self.headers = headers
        self.rows = rows
        self.nrows = len(self.rows)
        self.fieldlen = []
        ncols = len(headers)
        for i in range(ncols):
            max = 0
            for j in rows:
                if j:
                    if len(str(j[i])) > max:
                        max = len(str(j[i]))

            self.fieldlen.append(max)

        for i in range(len(headers)):
            if i:
                if len(str(headers[i])) > self.fieldlen[i]:
                    self.fieldlen[i] = len(str(headers[i]))

        self.width = sum(self.fieldlen) + (ncols - 1) * 3 + 4

    def __str__(self):
        bar = ''
        for i in range(len(self.headers)):
            bar += '+%s' % ('-' * (self.fieldlen[i] + 2))

        bar += '+'
        out = [bar]
        header = ''
        for i in range(len(self.headers)):
            header += '| %s' % str(self.headers[i]) + ' ' * (self.fieldlen[i] - len(str(self.headers[i]))) + ' '

        header += '|'
        out.append(header)
        out.append(bar)
        for i in self.rows:
            if not i:
                out.append(bar)
            else:
                line = ''
                for j in range(len(i)):
                    line += '| %s' % str(i[j]) + ' ' * (self.fieldlen[j] - len(str(i[j]))) + ' '

                out.append(line + '|')

        out.append(bar)
        return ('\r\n').join(out)