# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pydirduplicatefinder/interface_texts.py
# Compiled at: 2009-06-28 06:13:34
STARTING_CHECKING_MSG = 'Starting checking directories %s'
ENDING_NORMALLY_MSG = '\nCompleted'
FILE_IS_DUPLICATE = 'The file %s is a duplicate of %s'
PATH_IS_NOT_VALID_DIR = "The path %s doesn't match a valid directory; ignoring it."
RENAMING_DUPLICATE = '  Renaming duplicate %s to %s'
MOVING_DUPLICATE = '  moving duplicate %s to %s'
SKIPPING_EMPTY = 'skipping "%s"; is an empty file'
SKIPPING_TOO_SMALL = 'skipping "%s"; is too small (%s bytes).'
ASK_MESSAGE_OPTION = 'Do you want to:\n  (s) - Skip and continue\n  (d) - Delete one of the two files\n  (r) - Rename one of the two files\n  (m) - Move one of the two files\n  (q) - Quit\n'
ASK_INPUT = 'Insert your choice: '
NON_VALID_CHOICE = 'Choice %s is invalid. Please retry.'
ASK_MESSAGE_SELECTION = 'Select one of the files:\n  (1) - %s\n  (2) - %s\n'
NON_VALID_SELECTION = 'Selection %s is invalid. Please insert 1 for the original file, 2 for the duplicate.'
ASK_INPUT_RENAME = "Insert the new name for '%s' file: "
ERROR_FILE_EXISTS = "  ERROR. File '%s' already exists. Rename operation failed."
ASK_INPUT_MOVE = "Insert the new path for '%s' file: "
DIRECTORY_NOT_EXISTS = "  ERROR. Directory '%s' not exists. Move operation failed."
NO_DIRS_TO_CHECK_LEFT = 'No directories to check. Nothing done.'
HELP_FINAL_INFOS = '\nReport bugs (and suggestions) to <luca@keul.it>.\n'