# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: _build/bdist.macosx-10.15-x86_64/egg/sphinx_intl/catalog.py
# Compiled at: 2020-04-19 02:09:17
# Size of source mod 2**32: 2072 bytes
import os, io
from babel.messages import pofile, mofile

def load_po--- This code section failed: ---

 L.  16         0  LOAD_GLOBAL              io
                2  LOAD_METHOD              open
                4  LOAD_FAST                'filename'
                6  LOAD_STR                 'rb'
                8  CALL_METHOD_2         2  ''
               10  SETUP_WITH           28  'to 28'
               12  STORE_FAST               'f'

 L.  17        14  LOAD_GLOBAL              pofile
               16  LOAD_METHOD              read_po
               18  LOAD_FAST                'f'
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'cat'
               24  POP_BLOCK        
               26  BEGIN_FINALLY    
             28_0  COME_FROM_WITH       10  '10'
               28  WITH_CLEANUP_START
               30  WITH_CLEANUP_FINISH
               32  END_FINALLY      

 L.  18        34  LOAD_FAST                'cat'
               36  LOAD_ATTR                charset
               38  JUMP_IF_TRUE_OR_POP    42  'to 42'
               40  LOAD_STR                 'utf-8'
             42_0  COME_FROM            38  '38'
               42  STORE_FAST               'charset'

 L.  22        44  LOAD_GLOBAL              io
               46  LOAD_METHOD              open
               48  LOAD_FAST                'filename'
               50  LOAD_STR                 'rb'
               52  CALL_METHOD_2         2  ''
               54  SETUP_WITH           84  'to 84'
               56  STORE_FAST               'f'

 L.  23        58  LOAD_GLOBAL              pofile
               60  LOAD_ATTR                read_po
               62  LOAD_FAST                'f'
               64  LOAD_FAST                'charset'
               66  LOAD_CONST               ('charset',)
               68  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               70  POP_BLOCK        
               72  ROT_TWO          
               74  BEGIN_FINALLY    
               76  WITH_CLEANUP_START
               78  WITH_CLEANUP_FINISH
               80  POP_FINALLY           0  ''
               82  RETURN_VALUE     
             84_0  COME_FROM_WITH       54  '54'
               84  WITH_CLEANUP_START
               86  WITH_CLEANUP_FINISH
               88  END_FINALLY      

Parse error at or near `ROT_TWO' instruction at offset 72


def dump_po(filename, catalog, line_width=76):
    """write po/pot file from catalog object

    :param unicode filename: path to po file
    :param catalog: catalog object
    :param line_width: maximum line wdith of po files
    :return: None
    """
    dirname = os.path.dirnamefilename
    if not os.path.existsdirname:
        os.makedirsdirname
    with io.openfilename'wb' as (f):
        pofile.write_po(f, catalog, line_width)


def write_mo(filename, catalog):
    """write mo file from catalog object

    :param unicode filename: path to mo file
    :param catalog: catalog object
    :return: None
    """
    dirname = os.path.dirnamefilename
    if not os.path.existsdirname:
        os.makedirsdirname
    with io.openfilename'wb' as (f):
        mofile.write_mofcatalog


def translated_entries(catalog):
    return [m for m in catalog if m.id if m.string]


def fuzzy_entries(catalog):
    return [m for m in catalog if m.id if m.fuzzy]


def untranslated_entries(catalog):
    return [m for m in catalog if m.id if not m.string]


def update_with_fuzzy(catalog, catalog_source):
    """update catalog by template catalog with fuzzy flag.

    :param catalog: catalog object to be updated
    :param catalog_source: catalog object as a template to update 'catalog'
    :return: None
    """
    catalog.updatecatalog_source