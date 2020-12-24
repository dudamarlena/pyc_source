# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/exactly_lib/definitions/primitives/file_or_dir_contents.py
# Compiled at: 2020-01-29 09:08:19
# Size of source mod 2**32: 503 bytes
from exactly_lib.definitions import instruction_arguments
from exactly_lib.util.cli_syntax.elements import argument as a
EMPTINESS_CHECK_ARGUMENT = 'empty'
RECURSIVE_OPTION = a.option('recursive')
MIN_DEPTH_OPTION = a.option('min-depth', argument=instruction_arguments.INTEGER_ARGUMENT.name)
MAX_DEPTH_OPTION = a.option('max-depth', argument=instruction_arguments.INTEGER_ARGUMENT.name)
DIR_FILE_SET_OPTIONS = a.Named('DIR-CONTENTS-OPTIONS')