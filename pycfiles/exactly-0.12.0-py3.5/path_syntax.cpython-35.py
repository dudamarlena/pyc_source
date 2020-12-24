# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/definitions/argument_rendering/path_syntax.py
# Compiled at: 2018-08-03 07:19:58
# Size of source mod 2**32: 877 bytes
from typing import List
from exactly_lib.definitions.entity import syntax_elements
from exactly_lib.util.cli_syntax.elements import argument as a
from exactly_lib.util.cli_syntax.elements.argument import ArgumentUsage

def path_or_symbol_reference(multiplicity: a.Multiplicity, path_argument: a.Named) -> a.ArgumentUsage:
    return a.Single(multiplicity, path_argument)


def mandatory_path_with_optional_relativity(path_argument: a.Named, path_suffix_is_required: bool=True) -> List[ArgumentUsage]:
    multiplicity = a.Multiplicity.MANDATORY if path_suffix_is_required else a.Multiplicity.OPTIONAL
    path_part = a.Single(multiplicity, path_argument)
    return [path_part]


def the_path_of(a_file_description: str) -> str:
    return 'The ' + syntax_elements.PATH_SYNTAX_ELEMENT.argument.name + ' of ' + a_file_description