# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyqart/qr/printer/string_printer.py
# Compiled at: 2016-08-01 03:38:45
# Size of source mod 2**32: 1327 bytes
from .base import QrBasePrinter
WHITE_ALL = '█'
WHITE_BLACK = '▀'
BLACK_WHITE = '▄'
BLACK_ALL = ' '
MAP = {(True, True): BLACK_ALL, 
 (True, False): BLACK_WHITE, 
 (False, True): WHITE_BLACK, 
 (False, False): WHITE_ALL}

class QrStringPrinter(QrBasePrinter):

    @classmethod
    def print(cls, obj, print_out=True, *args, **kwargs):
        """
        :param obj: See :any:`QrImagePrinter`
        :param bool print_out: Whether to print QrCode out.
        :return: The string that can be print out like a QrCode.
        :type: string
        """
        painter = cls._create_painter(obj)
        matrix = painter.as_bool_matrix
        matrix = [[False] + x + [False] for x in matrix]
        size = len(matrix) + 2
        matrix.insert(0, [False] * size)
        matrix.append([False] * size)
        matrix.append([True] * size)
        lines = []
        for row in range(0, size, 2):
            line = []
            for col in range(0, size):
                line.append(MAP[(matrix[row][col], matrix[(row + 1)][col])])

            lines.append(''.join(line))

        string = '\n'.join(lines)
        if print_out:
            print(string)
        return string