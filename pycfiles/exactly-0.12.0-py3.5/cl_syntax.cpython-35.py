# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/definitions/argument_rendering/cl_syntax.py
# Compiled at: 2018-04-20 07:05:01
# Size of source mod 2**32: 639 bytes
from typing import Sequence
from exactly_lib.util.cli_syntax.elements import argument as a
from exactly_lib.util.cli_syntax.render import cli_program_syntax
CL_SYNTAX_RENDERER = cli_program_syntax.CommandLineSyntaxRenderer()
ARG_SYNTAX_RENDERER = cli_program_syntax.ArgumentInArgumentDescriptionRenderer()

def cl_syntax_for_args(argument_usages: Sequence[a.ArgumentUsage]) -> str:
    cl = a.CommandLine(argument_usages)
    return cl_syntax(cl)


def cl_syntax(command_line: a.CommandLine) -> str:
    return CL_SYNTAX_RENDERER.as_str(command_line)


def arg_syntax(arg: a.Argument) -> str:
    return ARG_SYNTAX_RENDERER.visit(arg)