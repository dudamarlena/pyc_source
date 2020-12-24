# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/alanr/monitor/ctypesgen-davidjamesca/ctypesgen/ctypesgen/options.py
# Compiled at: 2019-08-18 21:39:19
__doc__ = '\nAll of the components of ctypegencore require an argument called "options".\nIn command-line usage, this would be an optparser.Values object. However, if\nctypesgen is used as a standard Python module, constructing this object\nwould be a pain. So this module exists to provide a "default" options object\nfor convenience.\n'
import optparse, copy
default_values = {'other_headers': [], 'modules': [], 'include_search_paths': [], 'compile_libdirs': [], 'runtime_libdirs': [], 'cpp': 'gcc -E', 
   'save_preprocessed_headers': None, 
   'all_headers': False, 
   'builtin_symbols': False, 
   'include_symbols': None, 
   'exclude_symbols': None, 
   'show_all_errors': False, 
   'show_long_errors': False, 
   'show_macro_warnings': True, 
   'header_template': None, 
   'inserted_files': [], 'other_known_names': [], 'include_macros': True, 
   'libraries': [], 'strip_build_path': None, 
   'output_language': 'py', 
   'no_stddef_types': False, 
   'no_gnu_types': False, 
   'no_python_types': False}

def get_default_options():
    return optparse.Values(copy.deepcopy(default_values))