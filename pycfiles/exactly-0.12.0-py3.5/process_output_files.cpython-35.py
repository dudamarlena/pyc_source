# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/process_execution/process_output_files.py
# Compiled at: 2018-04-04 04:20:26
# Size of source mod 2**32: 696 bytes
from enum import Enum
EXIT_CODE_FILE_NAME = 'exitcode'
STDOUT_FILE_NAME = 'stdout'
STDERR_FILE_NAME = 'stderr'

class ProcOutputFile(Enum):
    STDOUT = 1
    STDERR = 2


PROC_OUTPUT_FILE_NAMES = {ProcOutputFile.STDOUT: STDOUT_FILE_NAME, 
 ProcOutputFile.STDERR: STDERR_FILE_NAME}

class FileNames:

    @property
    def exit_code(self) -> str:
        return EXIT_CODE_FILE_NAME

    @property
    def stdout(self) -> str:
        return STDOUT_FILE_NAME

    @property
    def stderr(self) -> str:
        return STDERR_FILE_NAME

    @staticmethod
    def name_of(output_file: ProcOutputFile) -> str:
        return PROC_OUTPUT_FILE_NAMES[output_file]


FILE_NAMES = FileNames()