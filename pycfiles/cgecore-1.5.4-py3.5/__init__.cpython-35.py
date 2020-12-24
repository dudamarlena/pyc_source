# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cgecore/__init__.py
# Compiled at: 2020-04-01 11:10:12
# Size of source mod 2**32: 736 bytes
"""
The CGE functions module
"""
from .utility import adv_dict, copy_dir, copy_file, create_zip_dir, debug, open_, file_unzipper, file_zipper, mkpath, move_file, seqs_from_file, Reg, REGroup, sort2groups, load_json, sort_and_distribute
from .cmdline import Program, proglist, cmd2list
from .argumentparsing import check_file_type, get_arguments, get_string, make_file_list
__version__ = '1.5.4'
__all__ = [
 'argumentparsing',
 'cmdline',
 'utility']