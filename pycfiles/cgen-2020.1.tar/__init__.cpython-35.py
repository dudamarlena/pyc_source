# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cgecore/__init__.py
# Compiled at: 2020-04-01 11:10:12
# Size of source mod 2**32: 736 bytes
__doc__ = '\nThe CGE functions module\n'
from .utility import adv_dict, copy_dir, copy_file, create_zip_dir, debug, open_, file_unzipper, file_zipper, mkpath, move_file, seqs_from_file, Reg, REGroup, sort2groups, load_json, sort_and_distribute
from .cmdline import Program, proglist, cmd2list
from .argumentparsing import check_file_type, get_arguments, get_string, make_file_list
__version__ = '1.5.4'
__all__ = [
 'argumentparsing',
 'cmdline',
 'utility']