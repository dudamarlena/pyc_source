# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/std.py
# Compiled at: 2019-12-27 10:07:29
# Size of source mod 2**32: 1650 bytes
import subprocess, sys
from exactly_lib.util.process_execution.process_output_files import ProcOutputFile

class StdOutputFiles:

    def __init__(self, stdout_file=sys.stdout, stderr_file=sys.stderr):
        self._stdout_file = stdout_file
        self._stderr_file = stderr_file

    @property
    def out(self):
        return self._stdout_file

    @property
    def err(self):
        return self._stderr_file

    def get(self, file: ProcOutputFile):
        if file is ProcOutputFile.STDOUT:
            return self.out
        return self.err


class StdOutputFilesContents:

    def __init__(self, stdout_file: str, stderr_file: str):
        self._stdout_file = stdout_file
        self._stderr_file = stderr_file

    @property
    def out(self) -> str:
        return self._stdout_file

    @property
    def err(self) -> str:
        return self._stderr_file


def new_std_output_files_dev_null() -> StdOutputFiles:
    return StdOutputFiles(subprocess.DEVNULL, subprocess.DEVNULL)


class StdFiles:

    def __init__(self, stdin_file=sys.stdin,
                 output_files: StdOutputFiles=StdOutputFiles()):
        self._stdin_file = stdin_file
        self._output_files = output_files

    @property
    def stdin(self):
        return self._stdin_file

    @property
    def output(self) -> StdOutputFiles:
        return self._output_files


def std_files_dev_null() -> StdFiles:
    return StdFiles(subprocess.DEVNULL, new_std_output_files_dev_null())