# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pybasic/__main__.py
# Compiled at: 2019-04-20 06:42:58
# Size of source mod 2**32: 1304 bytes
import argparse, pickle, sys
from .basic_yacc import ast, parser, root_stack
from .utils import BasicError
from .pybasic import *

def main():
    arg_parser = argparse.ArgumentParser(description='Execute pybasic programs, or start an REPL session.')
    arg_parser.add_argument('program_name', nargs='?', help='The path of the source program to execute. If not specified, an REPL session will be started.')
    arg_parser.add_argument('-a', '--ast', action='store_true', dest='ast', help='Execute a binary abstract syntax tree file rather than a source program. This will be ignored in REPL mode. ')
    arg_parser.add_argument('-s', '--save', action='store', dest='ast_path', help='Save the binary abstract syntax tree of the source program to the given path. The source program will not be executed. This will be ignored in REPL mode. ')
    args = arg_parser.parse_args()
    if not args.program_name:
        repl()
    else:
        if args.ast_path:
            save_ast(args.program_name, args.ast_path)
            return
        if args.ast:
            execute_ast(args.program_name)
            return
        execute(args.program_name)


if __name__ == '__main__':
    main()