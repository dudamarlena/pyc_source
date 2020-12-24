# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/pybasic/pybasic.py
# Compiled at: 2019-04-20 06:39:38
# Size of source mod 2**32: 1811 bytes
import argparse, pickle, sys
from .basic_yacc import ast, parser, root_stack
from .utils import BasicError

def print_error(error):
    print(('ERROR: %s' % error), file=(sys.stderr))


def parse_line(cnt, in_block=False):
    prompt = '> ' if in_block else 'In [%d]: ' % cnt
    while 1:
        try:
            s = input(prompt)
        except (EOFError, KeyboardInterrupt):
            sys.exit(1)

        if s:
            break

    return parser.parse(s)


def repl():
    cnt = 1
    while True:
        try:
            result = parse_line(cnt)
            while len(root_stack) > 1:
                parse_line(cnt, in_block=True)

        except Exception as error:
            try:
                print_error(error)
                cnt += 1
                continue
            finally:
                error = None
                del error

        if result is not None:
            try:
                out = result.run()
                if out is not None:
                    print('Out [%d]: %s' % (cnt, out))
            except Exception as error:
                try:
                    print_error(error)
                finally:
                    error = None
                    del error

            print('')
        cnt += 1


def execute(program_name):
    f = open(program_name, 'r')
    lines = f.readlines()
    try:
        for line in lines:
            parser.parse(line)

        ast.run()
    except Exception as error:
        try:
            print_error(error)
        finally:
            error = None
            del error


def save_ast(input_name, output_name):
    with open(input_name, 'r') as (input_file):
        with open(output_name, 'wb') as (output_file):
            lines = input_file.readlines()
            for line in lines:
                parser.parse(line)

            pickle.dump(ast, output_file)


def execute_ast(ast_file_name):
    with open(ast_file_name, 'rb') as (input_file):
        new_ast = pickle.load(input_file)
    new_ast.run()