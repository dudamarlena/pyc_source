# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/nyancat/nyancat.py
# Compiled at: 2015-03-17 08:46:04
from frame import frames
import subprocess, time

class Nyancat(object):
    FRAME_HEIGHT = FRAME_WIDTH = 64
    COLORS = {',': '\x1b[48;5;17m', 
       '.': '\x1b[48;5;231m', 
       "'": '\x1b[48;5;16m', 
       '@': '\x1b[48;5;230m', 
       '$': '\x1b[48;5;175m', 
       '-': '\x1b[48;5;162m', 
       '>': '\x1b[48;5;196m', 
       '&': '\x1b[48;5;214m', 
       '+': '\x1b[48;5;226m', 
       '#': '\x1b[48;5;118m', 
       '=': '\x1b[48;5;33m', 
       ';': '\x1b[48;5;19m', 
       '*': '\x1b[48;5;240m', 
       '%': '\x1b[48;5;175m'}

    def __init__(self):
        self.terminal_height, self.terminal_width = self.linesnum()
        self.min_col = (self.FRAME_WIDTH - self.terminal_width / 2) / 2
        self.max_col = (self.FRAME_WIDTH + self.terminal_width / 2) / 2
        self.min_row = (self.FRAME_HEIGHT - (self.terminal_height - 1)) / 2
        self.max_row = (self.FRAME_HEIGHT + (self.terminal_height - 1)) / 2
        self.output = ' '
        self.clear_screen = 1
        self.always_escape = 0

    def linesnum(self):
        u"""测试屏幕显示行数,每行字符数"""
        num = subprocess.check_output('stty size', shell=True).split(' ')
        return (int(num[0]), int(num[1]))

    def run(self):
        rainbow = ',,>>&&&+++###==;;;,,'
        i = 0
        last = 0
        while True:
            print '\x1b[?25l]'
            for y in range(self.min_row, self.max_row):
                for x in range(self.min_col, self.max_col):
                    if 23 < y < 43 and x < 0:
                        mod_x = (-x + 2) % 16 / 8
                        if i / 2 % 2:
                            mod_x = 1 - mod_x
                        tmp = mod_x + y - 23
                        if -1 < tmp < len(rainbow):
                            color = rainbow[tmp]
                        else:
                            color = ','
                    elif x < 0 or y < 0 or y >= self.FRAME_HEIGHT or x >= self.FRAME_WIDTH:
                        color = ','
                    else:
                        color = frames[i][y][x]
                    if self.always_escape:
                        print self.COLORS[color],
                    elif color != last and self.COLORS.has_key(color):
                        last = color
                        print self.COLORS[color] + self.output,
                    else:
                        print self.output,

                print

            i += 1
            if i == 11:
                i = 0
            last = 0
            time.sleep(0.1)

    def __del__(self):
        print '\x1b[?25h]'


def main():
    nyancat = Nyancat()
    nyancat.run()


if __name__ == '__main__':
    main()