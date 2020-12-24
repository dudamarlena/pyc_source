# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/wordtex/cloudtb/spreadsheets.py
# Compiled at: 2013-11-12 16:48:22


class spreadsheet_index_counter(object):
    """can keep track of incrementing an spreadsheet notated number.
    can also be used to increment pre-existing spreadsheet notation"""

    def __init__(self, letters=None, count=0):
        self.count = count
        if letters == None:
            self.letters = [
             0]
        else:
            self.letters = letters
        return

    def increment(self, position=-1):
        if position == -1:
            self.count += 1
        if self.letters[position] > 24:
            self.letters[position] = 0
            try:
                return self.increment(position - 1)
            except IndexError:
                self.letters.insert(0, 0)
                self.letters = [ 0 for n in self.letters ]

        else:
            self.letters[position] += 1

    def get_spreadsheet_counter(self):
        return ('').join([ chr(ord('A') + n) for n in self.letters ])

    def get_count(self):
        return self.count


def stdindex_to_strindex(stdindex):
    """stdindex is just a simple (row, col) index NOT generators"""
    row, col = stdindex
    row += 1
    num_list = []
    col2 = col
    while col2 > 0:
        col = col2
        num_list.insert(0, (col - 1) % 26)
        col2 = (col - 1) // 26

    ec = spreadsheet_index_counter()
    ec.letters = num_list
    if num_list == []:
        return ('A', row)
    else:
        ec.increment()
        return (ec.get_spreadsheet_counter(), row)


def strindex_to_tuples(strindex):
    """conviencience function for converting from a string index
        i.e. "A2:B20" into a tuple form ('A', 2), ('B', 20)"""
    start, end = strindex.split(':')
    i = first_index_lt(start, 'A')
    start = (start[:i], int(start[i:]))
    i = first_index_lt(end, 'A')
    end = (end[:i], int(end[i:]))
    return (start, end)


def strindex_to_stdindex(strindex):
    """converts from standard spreadsheet string index into stdindex"""
    strindex = strindex.upper().replace(' ', '')
    n = first_index_lt(strindex, 'A')
    row = int(strindex[n:]) - 1
    col_list = list(strindex[:n])
    col_list.reverse()
    col = 0
    for n, c in enumerate(col_list):
        col += (ord(c) - ord('A') + 1) * 26 ** n

    col -= 1
    return (row, col)


def dev1():
    e = spreadsheet_index_counter()
    num = int(1000)
    for n in xrange(num, num + 100000):
        e_count = e.get_spreadsheet_counter()
        a = strindex_to_stdindex(e_count + '0')[1]
        if a != e.count:
            print 'ERROR1: ', e.count, e_count, a
        b = stdindex_to_strindex((0, e.count))[0]
        if b != e_count:
            print 'ERROR2: ', e.count, e_count, b
        e.increment()