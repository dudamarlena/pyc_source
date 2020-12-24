# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bmiller/Runestone/RunestoneComponents/runestone/codelens/htmlexample_module.py
# Compiled at: 2019-11-02 08:12:59
# Size of source mod 2**32: 2088 bytes
"""
from htmlexample_module import ColorTable

t = ColorTable(3, 4)

t.set_color(0, 0, 'red')
t.render_HTML()

t.set_color(1, 1, 'green')
t.render_HTML()

t.set_color(2, 2, 'blue')
t.render_HTML()

for i in range(3):
    for j in range(4):
        t.set_color(i, j, 'gray')
        t.render_HTML()
"""

class ColorTable:

    def __init__(self, num_rows, num_columns):
        self.num_rows = num_rows
        self.num_columns = num_columns
        self.table = []
        for i in range(self.num_rows):
            new_lst = ['' for e in range(self.num_columns)]
            self.table.append(new_lst)

    def set_color(self, row, column, color):
        assert 0 <= row < self.num_rows
        assert 0 <= column < self.num_columns
        self.table[row][column] = color

    def render_HTML(self):
        html_string = '<table>'
        for i in range(self.num_rows):
            html_string += '<tr>'
            for j in range(self.num_columns):
                color = self.table[i][j]
                if not color:
                    color = 'white'
                html_string += '<td style="width: 30px; height: 30px; border: 1px solid black;\n                                  background-color: %s;"></td>' % color

            html_string += '</tr>'

        html_string += '</table>'
        setHTML(html_string)