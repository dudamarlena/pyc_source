# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/actors/source_interpreter/python3.py
# Compiled at: 2019-09-20 02:11:23
# Size of source mod 2**32: 862 bytes
import sys
from exactly_lib.actors.source_interpreter import source_file_management
from exactly_lib.actors.source_interpreter.executable_file import Parser
from exactly_lib.actors.source_interpreter.source_file_management import StandardSourceFileManager
from exactly_lib.test_case.actor import Actor

def source_interpreter_setup() -> source_file_management.SourceInterpreterSetup:
    return source_file_management.SourceInterpreterSetup(_file_manager())


def _file_manager() -> source_file_management.SourceFileManager:
    if not sys.executable:
        raise ValueError('Cannot execute since name of executable not found in sys.executable.')
    return StandardSourceFileManager('py', sys.executable, [])


def new_actor() -> Actor:
    return Parser(source_interpreter_setup())