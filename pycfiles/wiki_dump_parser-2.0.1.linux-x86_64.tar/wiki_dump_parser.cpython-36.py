# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/akronix/.pyenv/versions/3.6.7/lib/python3.6/site-packages/wiki_dump_parser.py
# Compiled at: 2019-01-14 10:34:17
# Size of source mod 2**32: 5090 bytes
"""
  wiki_dump_parser.py

  Script to convert a xml mediawiki history dump to a csv file with readable useful data
for pandas processing.

  Copyright 2017-2019 Abel 'Akronix' Serrano Juste <akronix5@gmail.com>
"""
import xml.parsers.expat, sys
__version__ = '2.0.1'
Debug = False
csv_separator = ','

def xml_to_csv(filename):
    output_csv = None
    _parent = None
    _current_tag = ''
    page_id = page_title = page_ns = revision_id = timestamp = contributor_id = contributor_name = bytes_var = ''

    def start_tag(tag, attrs):
        nonlocal _current_tag
        nonlocal _parent
        nonlocal bytes_var
        _current_tag = tag
        if tag == 'text':
            if 'bytes' in attrs:
                bytes_var = attrs['bytes']
            else:
                bytes_var = '-1'
        else:
            if tag == 'page' or tag == 'revision' or tag == 'contributor':
                _parent = tag
        if tag == 'upload':
            print("!! Warning: '<upload>' element not being handled", file=(sys.stderr))

    def data_handler--- This code section failed: ---

 L.  54         0  LOAD_DEREF               '_current_tag'
                2  LOAD_STR                 ''
                4  COMPARE_OP               ==
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L.  55         8  LOAD_CONST               None
               10  RETURN_END_IF    
             12_0  COME_FROM             6  '6'

 L.  57        12  LOAD_DEREF               '_parent'
               14  POP_JUMP_IF_FALSE   186  'to 186'

 L.  58        16  LOAD_DEREF               '_parent'
               18  LOAD_STR                 'page'
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_FALSE    90  'to 90'

 L.  59        24  LOAD_DEREF               '_current_tag'
               26  LOAD_STR                 'title'
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    46  'to 46'

 L.  60        32  LOAD_STR                 '|'
               34  LOAD_FAST                'data'
               36  BINARY_ADD       
               38  LOAD_STR                 '|'
               40  BINARY_ADD       
               42  STORE_DEREF              'page_title'
               44  JUMP_ABSOLUTE       186  'to 186'
               46  ELSE                     '88'

 L.  61        46  LOAD_DEREF               '_current_tag'
               48  LOAD_STR                 'id'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    76  'to 76'

 L.  62        54  LOAD_FAST                'data'
               56  STORE_DEREF              'page_id'

 L.  63        58  LOAD_GLOBAL              Debug
               60  POP_JUMP_IF_FALSE    88  'to 88'

 L.  64        62  LOAD_GLOBAL              print
               64  LOAD_STR                 'Parsing page '
               66  LOAD_DEREF               'page_id'
               68  BINARY_ADD       
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  POP_TOP          
               74  JUMP_ABSOLUTE       186  'to 186'
               76  ELSE                     '88'

 L.  65        76  LOAD_DEREF               '_current_tag'
               78  LOAD_STR                 'ns'
               80  COMPARE_OP               ==
               82  POP_JUMP_IF_FALSE   186  'to 186'

 L.  66        84  LOAD_FAST                'data'
               86  STORE_DEREF              'page_ns'
             88_0  COME_FROM            60  '60'
               88  JUMP_FORWARD        186  'to 186'
               90  ELSE                     '186'

 L.  67        90  LOAD_DEREF               '_parent'
               92  LOAD_STR                 'revision'
               94  COMPARE_OP               ==
               96  POP_JUMP_IF_FALSE   126  'to 126'

 L.  68        98  LOAD_DEREF               '_current_tag'
              100  LOAD_STR                 'id'
              102  COMPARE_OP               ==
              104  POP_JUMP_IF_FALSE   112  'to 112'

 L.  69       106  LOAD_FAST                'data'
              108  STORE_DEREF              'revision_id'
              110  JUMP_ABSOLUTE       186  'to 186'
              112  ELSE                     '124'

 L.  70       112  LOAD_DEREF               '_current_tag'
              114  LOAD_STR                 'timestamp'
              116  COMPARE_OP               ==
              118  POP_JUMP_IF_FALSE   186  'to 186'

 L.  71       120  LOAD_FAST                'data'
              122  STORE_DEREF              'timestamp'
              124  JUMP_FORWARD        186  'to 186'
              126  ELSE                     '186'

 L.  72       126  LOAD_DEREF               '_parent'
              128  LOAD_STR                 'contributor'
              130  COMPARE_OP               ==
              132  POP_JUMP_IF_FALSE   186  'to 186'

 L.  73       134  LOAD_DEREF               '_current_tag'
              136  LOAD_STR                 'id'
              138  COMPARE_OP               ==
              140  POP_JUMP_IF_FALSE   148  'to 148'

 L.  74       142  LOAD_FAST                'data'
              144  STORE_DEREF              'contributor_id'
              146  JUMP_FORWARD        186  'to 186'
              148  ELSE                     '186'

 L.  75       148  LOAD_DEREF               '_current_tag'
              150  LOAD_STR                 'username'
              152  COMPARE_OP               ==
              154  POP_JUMP_IF_FALSE   170  'to 170'

 L.  76       156  LOAD_STR                 '|'
              158  LOAD_FAST                'data'
              160  BINARY_ADD       
              162  LOAD_STR                 '|'
              164  BINARY_ADD       
              166  STORE_DEREF              'contributor_name'
              168  JUMP_FORWARD        186  'to 186'
              170  ELSE                     '186'

 L.  77       170  LOAD_DEREF               '_current_tag'
              172  LOAD_STR                 'ip'
              174  COMPARE_OP               ==
              176  POP_JUMP_IF_FALSE   186  'to 186'

 L.  78       178  LOAD_FAST                'data'
              180  STORE_DEREF              'contributor_id'

 L.  79       182  LOAD_STR                 'Anonymous'
              184  STORE_DEREF              'contributor_name'
            186_0  COME_FROM           176  '176'
            186_1  COME_FROM           168  '168'
            186_2  COME_FROM           146  '146'
            186_3  COME_FROM           132  '132'
            186_4  COME_FROM           124  '124'
            186_5  COME_FROM           118  '118'
            186_6  COME_FROM            88  '88'
            186_7  COME_FROM            82  '82'
            186_8  COME_FROM            14  '14'

Parse error at or near `COME_FROM' instruction at offset 186_7

    def end_tag(tag):
        nonlocal _current_tag
        nonlocal _parent
        nonlocal bytes_var
        nonlocal contributor_id
        nonlocal contributor_name
        nonlocal revision_id
        nonlocal timestamp

        def has_empty_field(l):
            field_empty = False
            i = 0
            while not field_empty and i < len(l):
                field_empty = l[i] == ''
                i = i + 1

            return field_empty

        if tag == 'page':
            _parent = None
        else:
            if tag == 'revision':
                _parent = 'page'
            else:
                if tag == 'contributor':
                    _parent = 'revision'
        if tag == 'revision':
            revision_row = [page_id, page_title, page_ns,
             revision_id, timestamp,
             contributor_id, contributor_name,
             bytes_var]
            if not has_empty_field(revision_row):
                output_csv.write(csv_separator.join(revision_row) + '\n')
            else:
                print("The following line has imcomplete info and therefore it's been removed from the dataset:")
                print(revision_row)
            if Debug:
                print(csv_separator.join(revision_row))
            revision_id = timestamp = contributor_id = contributor_name = bytes_var = ''
        _current_tag = ''

    parser = xml.parsers.expat.ParserCreate()
    input_file = open(filename, 'rb')
    parser.StartElementHandler = start_tag
    parser.EndElementHandler = end_tag
    parser.CharacterDataHandler = data_handler
    parser.buffer_text = True
    parser.buffer_size = 1024
    output_csv = open((filename[0:-3] + 'csv'), 'w', encoding='utf8')
    output_csv.write(csv_separator.join(['page_id', 'page_title', 'page_ns', 'revision_id', 'timestamp', 'contributor_id', 'contributor_name', 'bytes']))
    output_csv.write('\n')
    print('Processing...')
    parser.ParseFile(input_file)
    print('Done processing')
    input_file.close()
    output_csv.close()
    return True


if __name__ == '__main__':
    if len(sys.argv) >= 2:
        print('Dump files to process: {}'.format(sys.argv[1:]))
        for xmlfile in sys.argv[1:]:
            print('Starting to parse file ' + xmlfile)
            if xml_to_csv(xmlfile):
                print('Data dump {} parsed succesfully'.format(xmlfile))

    else:
        print('Error: Invalid number of arguments. Please specify one or more .xml file to parse', file=(sys.stderr))