# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/Goban/lib/Board.py
# Compiled at: 2008-04-06 04:02:05


class Goban(dict):
    __module__ = __name__

    def __init__(self, size):
        dict.__init__(self)
        self.size = size
        for i in range(0, size):
            for j in range(0, size):
                self[(i, j)] = 0

    def __str__(self):
        s = ''
        for i in range(0, self.size):
            for j in range(0, self.size):
                if self[(i, j)] == 1:
                    s = s + 'B'
                elif self[(i, j)] == -1:
                    s = s + 'W'
                elif self[(i, j)] == 0:
                    s = s + '0'

            s = s + '\n'

        return s

    def checkForCaptures(self, coords, color):
        captureList = self.doCapture(coords[1], coords[0] - 1, color)
        captureList = captureList + self.doCapture(coords[1], coords[0] + 1, color)
        captureList = captureList + self.doCapture(coords[1] - 1, coords[0], color)
        captureList = captureList + self.doCapture(coords[1] + 1, coords[0], color)
        return captureList

    def capture(self, y, x, color, captureBoard):
        """
        recursive function to mark group (searches for liberties)
        returns 1 if a liberty was found, 0 otherwise
        """
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return False
        if self[(y, x)] == color:
            return False
        if self[(y, x)] == 0:
            return True
        if captureBoard[(y, x)] != 0:
            return False
        captureBoard[(y, x)] = 1
        if self.capture(y, x - 1, color, captureBoard):
            return True
        if self.capture(y, x + 1, color, captureBoard):
            return True
        if self.capture(y - 1, x, color, captureBoard):
            return True
        if self.capture(y + 1, x, color, captureBoard):
            return True
        return False

    def doCapture(self, y, x, color):
        if x < 0 or y < 0 or x >= self.size or y >= self.size:
            return []
        if self[(y, x)] != -1 * color:
            return []
        captureBoard = Goban(self.size)
        if self.capture(y, x, color, captureBoard):
            return []
        captureList = []
        for i in range(0, self.size):
            for j in range(0, self.size):
                if captureBoard[(i, j)] == 1:
                    captureList.append((j, i))

        return captureList