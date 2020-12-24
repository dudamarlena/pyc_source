# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sorno/gitutil.py
# Compiled at: 2020-03-16 00:44:32
# Size of source mod 2**32: 1637 bytes
"""Utilities to deal with Git
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import git

def get_config_reader(filepath):
    """Gets an instance of GitConfigParser

  https://github.com/gitpython-developers/GitPython/blob/77e47bc313e42f9636e37ec94f2e0b366b492836/git/config.py#L194
  """
    return git.Repo(filepath).config_reader()


def get_sections(filepath):
    """Gets the sections from git config."""
    reader = get_config_reader(filepath)
    sections = {}
    for sec_name in reader.sections():
        sections[sec_name] = reader.items_all(sec_name)
    else:
        return sections


def get_remote_urls(filepath):
    sections = get_sections(filepath)
    urls = []
    for sec, section in sections.items():
        if sec.startswith('remote'):
            for option, values in section:
                if option == 'url':
                    urls.extend(values)

        return urls


def get_remote_urls_safe--- This code section failed: ---

 L.  57         0  SETUP_FINALLY        12  'to 12'

 L.  58         2  LOAD_GLOBAL              get_remote_urls
                4  LOAD_FAST                'filepath'
                6  CALL_FUNCTION_1       1  ''
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L.  59        12  DUP_TOP          
               14  LOAD_GLOBAL              git
               16  LOAD_ATTR                exc
               18  LOAD_ATTR                InvalidGitRepositoryError
               20  COMPARE_OP               exception-match
               22  POP_JUMP_IF_FALSE    38  'to 38'
               24  POP_TOP          
               26  POP_TOP          
               28  POP_TOP          

 L.  60        30  BUILD_LIST_0          0 
               32  ROT_FOUR         
               34  POP_EXCEPT       
               36  RETURN_VALUE     
             38_0  COME_FROM            22  '22'

 L.  61        38  DUP_TOP          
               40  LOAD_GLOBAL              git
               42  LOAD_ATTR                exc
               44  LOAD_ATTR                NoSuchPathError
               46  COMPARE_OP               exception-match
               48  POP_JUMP_IF_FALSE    64  'to 64'
               50  POP_TOP          
               52  POP_TOP          
               54  POP_TOP          

 L.  62        56  BUILD_LIST_0          0 
               58  ROT_FOUR         
               60  POP_EXCEPT       
               62  RETURN_VALUE     
             64_0  COME_FROM            48  '48'
               64  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 26