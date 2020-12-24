# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/help/entities/syntax_elements/objects/shell_command_line.py
# Compiled at: 2018-09-19 16:40:01
# Size of source mod 2**32: 1182 bytes
from exactly_lib.definitions import formatting
from exactly_lib.definitions.entity import syntax_elements
from exactly_lib.help.entities.syntax_elements.contents_structure import syntax_element_documentation
from exactly_lib.util.textformat.textformat_parser import TextParser
_MAIN_DESCRIPTION_REST = "A {SYNTAX_ELEMENT} is passed as a single string to the operating system's shell,\nso all features of the shell can be used.\n\n\nUs of the shell is of course not portable since it\ndepends on the current operating system environment's shell.\n\n\nOn POSIX, the shell defaults to /bin/sh.\n\nOn Windows, the COMSPEC environment variable specifies the default shell.\n"
_TEXT_PARSER = TextParser({'SYNTAX_ELEMENT': formatting.syntax_element_(syntax_elements.SHELL_COMMAND_LINE_SYNTAX_ELEMENT)})
DOCUMENTATION = syntax_element_documentation(None, syntax_elements.SHELL_COMMAND_LINE_SYNTAX_ELEMENT, _TEXT_PARSER.fnap(_MAIN_DESCRIPTION_REST), [], [], [])