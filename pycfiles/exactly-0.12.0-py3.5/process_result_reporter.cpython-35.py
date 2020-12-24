# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/common/process_result_reporter.py
# Compiled at: 2019-12-27 10:07:29
# Size of source mod 2**32: 2752 bytes
from abc import ABC, abstractmethod
from exactly_lib.util import file_printer
from exactly_lib.util.file_printer import FilePrinter
from exactly_lib.util.process_execution.process_output_files import ProcOutputFile
from exactly_lib.util.std import StdOutputFiles

class StdOutputFilePrinters(tuple):

    def __new__(cls, out: FilePrinter, err: FilePrinter):
        return tuple.__new__(cls, (out, err))

    @staticmethod
    def new_with_color_if_supported_by_terminal(std_files: StdOutputFiles) -> 'StdOutputFilePrinters':
        return StdOutputFilePrinters(file_printer.file_printer_with_color_if_terminal(std_files.out), file_printer.file_printer_with_color_if_terminal(std_files.err))

    @staticmethod
    def new_plain(std_files: StdOutputFiles) -> 'StdOutputFilePrinters':
        return StdOutputFilePrinters(file_printer.plain(std_files.out), file_printer.plain(std_files.err))

    @property
    def out(self) -> FilePrinter:
        return self[0]

    @property
    def err(self) -> FilePrinter:
        return self[1]

    def get(self, file: ProcOutputFile) -> FilePrinter:
        if file is ProcOutputFile.STDOUT:
            return self.out
        return self.err


class Environment(tuple):

    def __new__(cls, std_files: StdOutputFiles, std_file_printers: StdOutputFilePrinters):
        return tuple.__new__(cls, (std_files, std_file_printers))

    @staticmethod
    def new_with_color_if_supported_by_terminal(std_files: StdOutputFiles) -> 'Environment':
        return Environment(std_files, StdOutputFilePrinters.new_with_color_if_supported_by_terminal(std_files))

    @staticmethod
    def new_plain(std_files: StdOutputFiles) -> 'Environment':
        return Environment(std_files, StdOutputFilePrinters.new_plain(std_files))

    @property
    def std_files(self) -> StdOutputFiles:
        return self[0]

    @property
    def std_file_printers(self) -> StdOutputFilePrinters:
        return self[1]

    @property
    def std_out_file(self):
        return self[0].out

    @property
    def std_err_file(self):
        return self[0].err

    @property
    def out_printer(self) -> FilePrinter:
        return self[1].out

    @property
    def err_printer(self) -> FilePrinter:
        return self[1].err


class ProcessResultReporter(ABC):

    @abstractmethod
    def report(self, environment: Environment) -> int:
        """
        :return: Exit code of process
        """
        pass