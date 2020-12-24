# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/file_printer.py
# Compiled at: 2019-12-27 10:07:29
# Size of source mod 2**32: 2487 bytes
import os
from abc import ABC
from typing import Optional, Sequence
from exactly_lib.util import ansi_terminal_color as ansi
from exactly_lib.util.ansi_terminal_color import ForegroundColor, FontStyle

class FilePrinter:
    __doc__ = '\n    Printer that prints text a sequence of text lines on\n    a file-like object.\n\n    Optional support of ansi colors.\n    '

    def __init__(self, file):
        """
        :param file: A file-like object.
        """
        self.file = file

    def flush(self):
        self.file.flush()

    def write(self, s: str, flush: bool=False):
        self.file.write(s)
        if flush:
            self.file.flush()

    def write_line(self, line: str, indent: str=''):
        self.file.write(indent)
        self.file.write(line)
        self.file.write(os.linesep)

    def set_color(self, color: ForegroundColor):
        pass

    def unset_color(self):
        pass

    def set_font_style(self, style: FontStyle):
        pass

    def unset_font_style(self):
        pass

    def write_colored_line(self, line: str, color: Optional[ForegroundColor]):
        if color is not None:
            self.set_color(color)
        self.file.write(line)
        if color is not None:
            self.unset_color()
        self.file.write(os.linesep)

    def write_empty_line(self):
        self.file.write(os.linesep)

    def write_line_if_present(self, line: str):
        if line:
            self.write_line(line)

    def write_lines(self, lines: Sequence[str], indent: str=''):
        for line in lines:
            self.write_line(indent)
            self.write_line(line)


class FilePrintable(ABC):
    __doc__ = '\n    Something that is able to print itself on a FilePrinter.\n    '

    def print_on(self, printer: FilePrinter):
        pass


class FilePrinterWithAnsiColor(FilePrinter):

    def set_color(self, color: ForegroundColor):
        self.file.write(ansi.set_color(color))

    def unset_color(self):
        self.file.write(ansi.unset_color())

    def set_font_style(self, style: FontStyle):
        self.file.write(ansi.set_font_style(style))

    def unset_font_style(self):
        self.file.write(ansi.unset_font_style())


def file_printer_with_color_if_terminal(file_object) -> FilePrinter:
    if ansi.is_file_object_with_color(file_object):
        return FilePrinterWithAnsiColor(file_object)
    return FilePrinter(file_object)


def plain(file_object) -> FilePrinter:
    return FilePrinter(file_object)