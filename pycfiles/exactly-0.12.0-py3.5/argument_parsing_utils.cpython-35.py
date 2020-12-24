# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/util/argument_parsing_utils.py
# Compiled at: 2019-01-29 09:32:34
# Size of source mod 2**32: 2428 bytes
import argparse, pathlib
from typing import List, Callable, TypeVar, Tuple

class ArgumentParsingError(Exception):
    __doc__ = '\n    Indicates an invalid command line - a command line that the\n    ArgumentParser cannot parse.\n    '

    def __init__(self, error_message: str):
        self.error_message = error_message


def resolve_existing_path(path_to_resolve: pathlib.Path) -> pathlib.Path:
    """
    raises ArgumentParsingError: path_to_resolve is not an existing file
    """
    try:
        resolved = path_to_resolve.resolve()
        if not resolved.exists():
            raise ArgumentParsingError('File does not exist: ' + str(resolved))
        return resolved
    except FileNotFoundError as ex:
        raise ArgumentParsingError(str(ex))


def parse_args__raise_exception_instead_of_exiting_on_error--- This code section failed: ---

 L.  37         0  LOAD_GLOBAL              argparse
                3  LOAD_ATTR                Namespace
                6  LOAD_CONST               ('return',)
                9  LOAD_CLOSURE             'arguments'
               12  LOAD_CLOSURE             'parser'
               15  BUILD_TUPLE_2         2 
               18  LOAD_CODE                <code_object do_parse>
               21  LOAD_STR                 'parse_args__raise_exception_instead_of_exiting_on_error.<locals>.do_parse'
               24  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
               30  STORE_FAST               'do_parse'

 L.  40        33  LOAD_GLOBAL              _raise_exception_instead_of_exiting_on_error
               36  LOAD_FAST                'do_parse'
               39  CALL_FUNCTION_1       1  '1 positional, 0 named'
               42  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


def parse_known_args__raise_exception_instead_of_exiting_on_error--- This code section failed: ---

 L.  53         0  LOAD_GLOBAL              Tuple
                3  LOAD_GLOBAL              argparse
                6  LOAD_ATTR                Namespace
                9  LOAD_GLOBAL              List
               12  LOAD_GLOBAL              str
               15  BINARY_SUBSCR    
               16  BUILD_TUPLE_2         2 
               19  BINARY_SUBSCR    
               20  LOAD_CONST               ('return',)
               23  LOAD_CLOSURE             'arguments'
               26  LOAD_CLOSURE             'parser'
               29  BUILD_TUPLE_2         2 
               32  LOAD_CODE                <code_object do_parse>
               35  LOAD_STR                 'parse_known_args__raise_exception_instead_of_exiting_on_error.<locals>.do_parse'
               38  MAKE_CLOSURE_A_2_0        '0 positional, 0 keyword only, 2 annotated'
               44  STORE_FAST               'do_parse'

 L.  56        47  LOAD_GLOBAL              _raise_exception_instead_of_exiting_on_error
               50  LOAD_FAST                'do_parse'
               53  CALL_FUNCTION_1       1  '1 positional, 0 named'
               56  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


PARSE_RESULT = TypeVar('PARSE_RESULT')

def _raise_exception_instead_of_exiting_on_error(parse_action: Callable[([], PARSE_RESULT)]) -> PARSE_RESULT:
    """
    Corresponds to argparse.ArgumentParser.parse_args.

    But instead of exiting on error, a ArgumentParsingException is raised.
    """
    original_error_handler = argparse.ArgumentParser.error

    def error_handler(the_parser: argparse.ArgumentParser, the_message: str):
        raise ArgumentParsingError(the_message)

    try:
        argparse.ArgumentParser.error = error_handler
        return parse_action()
    finally:
        argparse.ArgumentParser.error = original_error_handler