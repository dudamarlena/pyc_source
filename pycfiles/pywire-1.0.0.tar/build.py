# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/2017-A/Dropbox/python_libraries/Pywire/pywire/build.py
# Compiled at: 2018-02-10 01:06:23
from pywire import *
import inspect, ast

def build(func, args, clock=True):
    source = inspect.getsource(func)
    top_node = ast.parse(source)
    func_args = [ x.id for x in top_node.body[0].args.args ]
    func_name = top_node.body[0].name
    assert len(args) == len(func_args)
    driven_indexes = []
    for line in source.split('\n'):
        if '=' in line:
            for arg_index in range(len(args)):
                if func_args[arg_index] in line[0:line.index('=')] and arg_index not in driven_indexes:
                    driven_indexes.append(arg_index)

    for index in driven_indexes:
        source_copy = source.split('\n')
        for line_id in range(len(source_copy)):
            line = source_copy[line_id]
            if '=' in line:
                if func_args[index] not in line[0:line.index('=')]:
                    source_copy[line_id] = '\t' * line.count('\t') + 'pass'
                else:
                    source_copy[line_id] = '\t' * line.count('\t') + 'return ' + line[line.index('=') + 1:]

        args[index].drive(('\n').join(source_copy), args, clock=clock)