# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/sixel/cellsize.py
# Compiled at: 2014-09-12 21:50:28
import sys, os, termios, select

class CellSizeDetector:

    def __set_raw(self):
        fd = sys.stdin.fileno()
        backup = termios.tcgetattr(fd)
        try:
            new = termios.tcgetattr(fd)
            new[0] = 0
            new[3] = 0
            new[3] = new[3] & ~(termios.ECHO | termios.ICANON)
            termios.tcsetattr(fd, termios.TCSANOW, new)
        except Exception:
            termios.tcsetattr(fd, termios.TCSANOW, backup)

        return backup

    def __reset_raw(self, old):
        fd = sys.stdin.fileno()
        termios.tcsetattr(fd, termios.TCSAFLUSH, old)

    def __get_report(self, query):
        result = ''
        fd = sys.stdin.fileno()
        rfds = [fd]
        wfds = []
        xfds = []
        sys.stdout.write(query)
        sys.stdout.flush()
        (rfd, wfd, xfd) = select.select(rfds, wfds, xfds, 0.5)
        if rfd:
            result = os.read(fd, 1024)
            return result[:-1].split(';')[1:]
        else:
            return

    def get_size(self):
        backup_termios = self.__set_raw()
        try:
            (height, width) = self.__get_report('\x1b[14t')
            (row, column) = self.__get_report('\x1b[18t')
            char_width = int(width) / int(column)
            char_height = int(height) / int(row)
        finally:
            self.__reset_raw(backup_termios)

        return (char_width, char_height)