# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/sorno/consoleutil.py
# Compiled at: 2020-03-16 00:44:32
# Size of source mod 2**32: 14306 bytes
"""Utilities related to console applications

Copyright 2015 Heung Ming Tai

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import sys, six, threading
from sorno import mathlib

def input--- This code section failed: ---

 L.  39         0  LOAD_FAST                'file'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    20  'to 20'

 L.  40         8  LOAD_GLOBAL              six
               10  LOAD_ATTR                moves
               12  LOAD_METHOD              input
               14  LOAD_FAST                'prompt'
               16  CALL_METHOD_1         1  ''
               18  RETURN_VALUE     
             20_0  COME_FROM             6  '6'

 L.  42        20  LOAD_GLOBAL              sys
               22  LOAD_ATTR                stdout
               24  STORE_FAST               'old_stdout'

 L.  43        26  SETUP_FINALLY        50  'to 50'

 L.  44        28  LOAD_FAST                'file'
               30  LOAD_GLOBAL              sys
               32  STORE_ATTR               stdout

 L.  45        34  LOAD_GLOBAL              six
               36  LOAD_ATTR                moves
               38  LOAD_METHOD              input
               40  LOAD_FAST                'prompt'
               42  CALL_METHOD_1         1  ''
               44  POP_BLOCK        
               46  CALL_FINALLY         50  'to 50'
               48  RETURN_VALUE     
             50_0  COME_FROM            46  '46'
             50_1  COME_FROM_FINALLY    26  '26'

 L.  47        50  LOAD_FAST                'old_stdout'
               52  LOAD_GLOBAL              sys
               54  STORE_ATTR               stdout
               56  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 46


def pick_items(items):
    for i, item in enumerate(items, 1):
        print(('%d)' % i), item, file=(sys.stderr))
    else:
        reply = input('Please choose:', file=(sys.stderr))
        intervals = parse_intervals(reply)
        nums = []
        for interval in intervals:
            nums.extendrange(interval.start, interval.end + 1)
        else:
            chosens = [items[(num - 1)] for num in nums]
            return chosens


def num_str_to_nums(num_str):
    if num_str:
        if '-' in num_str:
            start, end = num_str.split'-'
            return list(range(int(start), int(end) + 1))
        return [int(num_str)]
    else:
        return []


class DataPrinter(object):
    PRINT_STYLE_HTML_TABLE = 'html'
    PRINT_STYLE_PLAIN = 'plain'
    PRINT_STYLE_R = 'R'
    PRINT_STYLE_TABLE = 'table'
    PRINT_STYLE_VERBOSE = 'verbose'
    NICETABLE_COL_LEN = 80
    PRINT_STYLE_R = 'R'
    PRINT_STYLE_NICETABLE = 'nicetable'
    PRINT_STYLE_STREAMING_PLAIN = 'streaming-plan'
    OPTION_TITLE = 'title'
    OPTION_ADDITIONAL_TRAILING_CONTENT = 'additional-trailing-content'

    def __init__(self, data, headers=(), header_types=None, delimiter='\t', max_col_len=NICETABLE_COL_LEN, print_func=print, streaming=False):
        """Constructs a DataPrinter object

        Args:
          data: A list of dict's or a list of lists. Each dict or list
              represents a row of data. If it's a dict, the keys are the
              column names in strings and the values are the column values in
              strings.  If it's a list, then each item is the value of a
              column of the row. Each value should be a string properly
              formatted, since DataPrinter does not do any special formatting
              of each value.

              If streaming is True, data should be a Queue with
              the sentinel value None.

          headers: Optionally supply a list of headers in strings to control
              what columns are printed out and what order are the columns
              printed.

          header_types: A list of strings representing the types of the
              headers. It's currently used for PRINT_STYLE_R form. This is not
              needed if you are not using PRINT_STYLE_R.

          delimiter: The delimiter in string for separating column values. By
              default it's a tab character.

          max_col_len: An integer to indicate the maximum column length when
              the data is printed in PRINT_STYLE_NICETABLE. By default it's
              80.

          print_func: A function that takes a string as an argument. The
              function is used for printing the data. By default it uses the
              built-in print function.

          streaming: The data will come as a stream. This should
              be used if PRINT_STYLE_STREAMING_PLAIN is used for
              printing result.
        """
        if streaming:
            self.data = iter(data.get, None)
        else:
            if not hasattr(data, '__getitem__'):
                data = list(data)
            else:
                if not headers:
                    if data:
                        if isinstance(data[0], dict):
                            headers = sorted(data[0].keys())
                if data and isinstance(data[0], dict):
                    self.data = self._convert_list_of_dicts(headers, data)
                else:
                    self.data = data
        self.headers = headers
        self.header_types = header_types
        self.delimiter = delimiter
        self.max_col_len = max_col_len
        self.print_func = print_func

    def _convert_list_of_dicts(self, headers, ls_of_dicts):
        """
        Convert list of dicts to list of lists.
        """
        data = [[d[header] for header in headers] for d in ls_of_dicts]
        return data

    def print_result(self, style=PRINT_STYLE_TABLE, options=None):
        if options is None:
            options = {}
        elif style == DataPrinter.PRINT_STYLE_R:
            json_headers = []
            for header, t in zip(self.headers, self.header_types):
                h = {'name':header, 
                 'type':t}
                json_headers.appendjson.dumpsh.replace('\t', '').replace('\n', '')
            else:
                self.print_funcself.delimiter.joinjson_headers
                self.print_data()

        else:
            if style == DataPrinter.PRINT_STYLE_PLAIN:
                self.print_data()
            else:
                if style == DataPrinter.PRINT_STYLE_STREAMING_PLAIN:
                    self.print_data_streaming()
                else:
                    if style == DataPrinter.PRINT_STYLE_VERBOSE:
                        self.print_verbose()
                    else:
                        if style == DataPrinter.PRINT_STYLE_HTML_TABLE:
                            self.print_html_tableoptions
                        else:
                            if style == DataPrinter.PRINT_STYLE_NICETABLE:
                                self.print_table(is_nicetable=True)
                            else:
                                self.print_table()

    def print_data_streaming(self):
        threading.Thread(target=(self.print_data)).start()

    def print_data(self):
        for row in self.data:
            self.print_funcself.delimiter.joinrow

    def print_table(self, is_nicetable=False):
        max_widths = [len(header) for header in self.headers]
        for row in self.data:
            for i, col in enumerate(row):
                max_widths[i] = max(max_widths[i], self.get_lencol)

        else:
            if is_nicetable:
                max_widths = [min(self.max_col_len, width) for width in max_widths]
                print_data_row = self.print_nice_data_row
            else:
                print_data_row = self.print_data_row
            self.print_horizontal_linemax_widths
            print_data_row(max_widths, self.headers)
            self.print_horizontal_linemax_widths

        for row in self.data:
            print_data_row(max_widths, row)
        else:
            self.print_horizontal_linemax_widths

    def print_horizontal_line(self, widths):
        segments = ['-' * (width + 2) for width in widths]
        self.print_func('+%s+' % '+'.joinsegments)

    def print_data_row(self, widths, data_row):
        formatted_row = [' %-*s ' % (width, col) for width, col in zip(widths, data_row)]
        self.print_func('|%s|' % '|'.joinformatted_row)

    def print_verbose(self):
        if self.headers:
            max_header_len = max([len(header) for header in self.headers])
        else:
            max_header_len = 0
        for i, row in enumerate(self.data):
            self.print_func('***************************' + ' %1d. row ' % (i + 1) + '***************************')
            for header, col in zip(self.headers, row):
                self.print_func('%*s: %s' % (max_header_len, header, col))

    def print_nice_data_row(self, widths, data_row):
        count_line = 1
        for width, col in zip(widths, data_row):
            col_len = self.get_lencol
            if col_len > width:
                tmp = int(col_len / width)
                if col_len % width != 0:
                    tmp += 1
                count_line = max(count_line, tmp)
        else:
            for i in range(count_line):
                cells = []
                for width, col in zip(widths, data_row):
                    col_len = self.get_lencol
                    spaces_used = i * width
                    if col_len > spaces_used:
                        len_to_display = min(col_len - width * i, width)
                        text = col[spaces_used:spaces_used + len_to_display]
                        cells.appendtext.replace('\t', ' ').replace('\n', ' ')
                    else:
                        cells.append''
                else:
                    formatted = [' %-*s ' % (width, col) for width, col in zip(widths, cells)]
                    self.print_func('|%s|' % '|'.joinformatted)

    def print_html_table(self, options):
        html = '\n<html>\n<head>\n    <title>{title}</title>\n    <style>\n    table {{\n        border-collapse:collapse;\n    }}\n    table, tr, td, th {{\n        border: 1px solid black;\n        padding: 3px;\n    }}\n    th {{\n        background: #333;\n        color: white;\n        font-size: 80%;\n    }}\n    tr:nth-child(even) {{\n        background: #ccc;\n    }}\n    tr:nth-child(odd) {{\n        background: #fff;\n    }}\n\n    </style>\n</head>\n<body>\n<table style="border: 1px solid black">\n{headers}\n{rows}\n</table>\n{trailing_content}\n<p>Created at {timestamp}</p>\n</body>\n</html>\n        '
        title = options.get(self.OPTION_TITLE, '')
        trailing_content = options.get(self.OPTION_ADDITIONAL_TRAILING_CONTENT, '')
        headers = '<tr><th>' + '</th><th>'.joinself.headers + '</th></tr>\n'
        html_rows = []
        for row in self.data:
            partial_html_row = '</td><td>'.joinrow
            html_row = '<tr><td>' + partial_html_row + '</td></tr>'
            html_rows.appendhtml_row
        else:
            rows = '\n'.joinhtml_rows
            timestamp = time.ctime()
            self.print_func(html.format)(**locals())

    def get_len(self, value):
        if not value:
            return 0
        return len(value)


def parse_intervals(s):
    """
    Parse a string to return the intervals the string represents.

    Example:
        >>> parse_intervals("1,2")
        [Interval(start=1,end=1,is_start_opened=False,is_end_opened=False), Interval(start=2,end=2,is_start_opened=False,is_end_opened=False)]
    """
    s = s.strip()
    if not s:
        return []
    interval_strs = [segment.strip() for segment in s.split',']
    intervals = []
    for interval_str in interval_strs:
        num_or_interval = interval_str.split('-', 1)
        if len(num_or_interval) == 1:
            s = e = int(num_or_interval[0])
        else:
            s = int(num_or_interval[0])
            e = int(num_or_interval[1])
        interval = mathlib.Interval(s,
          e,
          is_start_opened=False,
          is_end_opened=False)
        intervals.appendinterval
    else:
        return intervals


def confirm--- This code section failed: ---

 L. 386         0  LOAD_CONST               None
                2  STORE_FAST               'old_stdout'

 L. 387         4  LOAD_FAST                'file'
                6  LOAD_CONST               None
                8  COMPARE_OP               is-not
               10  POP_JUMP_IF_FALSE    24  'to 24'

 L. 388        12  LOAD_GLOBAL              sys
               14  LOAD_ATTR                stdout
               16  STORE_FAST               'old_stdout'

 L. 389        18  LOAD_FAST                'file'
               20  LOAD_GLOBAL              sys
               22  STORE_ATTR               stdout
             24_0  COME_FROM            10  '10'

 L. 391        24  SETUP_FINALLY        84  'to 84'
             26_0  COME_FROM            68  '68'

 L. 393        26  LOAD_GLOBAL              six
               28  LOAD_ATTR                moves
               30  LOAD_METHOD              input
               32  LOAD_FAST                'prompt'
               34  LOAD_STR                 ' [y/N/t/F] '
               36  BINARY_ADD       
               38  CALL_METHOD_1         1  ''
               40  LOAD_METHOD              lower
               42  CALL_METHOD_0         0  ''
               44  STORE_FAST               'ans'

 L. 395        46  LOAD_FAST                'ans'
               48  LOAD_CONST               ('y', 'yes', 't', 'true')
               50  COMPARE_OP               in
               52  POP_JUMP_IF_FALSE    62  'to 62'

 L. 396        54  POP_BLOCK        
               56  CALL_FINALLY         84  'to 84'
               58  LOAD_CONST               True
               60  RETURN_VALUE     
             62_0  COME_FROM            52  '52'

 L. 397        62  LOAD_FAST                'ans'
               64  LOAD_CONST               ('n', 'no', 'f', 'false')
               66  COMPARE_OP               in
               68  POP_JUMP_IF_FALSE    26  'to 26'

 L. 398        70  POP_BLOCK        
               72  CALL_FINALLY         84  'to 84'
               74  LOAD_CONST               False
               76  RETURN_VALUE     
               78  JUMP_BACK            26  'to 26'
               80  POP_BLOCK        
               82  BEGIN_FINALLY    
             84_0  COME_FROM            72  '72'
             84_1  COME_FROM            56  '56'
             84_2  COME_FROM_FINALLY    24  '24'

 L. 400        84  LOAD_FAST                'old_stdout'
               86  POP_JUMP_IF_FALSE    94  'to 94'

 L. 401        88  LOAD_FAST                'old_stdout'
               90  LOAD_GLOBAL              sys
               92  STORE_ATTR               stdout
             94_0  COME_FROM            86  '86'
               94  END_FINALLY      

Parse error at or near `CALL_FINALLY' instruction at offset 56


def choose_item--- This code section failed: ---

 L. 416         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'items'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_FAST               'n'

 L. 417         8  LOAD_CONST               0
               10  STORE_FAST               'num_of_digits'

 L. 418        12  LOAD_FAST                'n'
               14  POP_JUMP_IF_FALSE    34  'to 34'

 L. 419        16  LOAD_FAST                'n'
               18  LOAD_CONST               10
               20  INPLACE_FLOOR_DIVIDE
               22  STORE_FAST               'n'

 L. 420        24  LOAD_FAST                'num_of_digits'
               26  LOAD_CONST               1
               28  INPLACE_ADD      
               30  STORE_FAST               'num_of_digits'
               32  JUMP_BACK            12  'to 12'
             34_0  COME_FROM            14  '14'

 L. 423        34  LOAD_GLOBAL              enumerate
               36  LOAD_FAST                'items'
               38  CALL_FUNCTION_1       1  ''
               40  GET_ITER         
               42  FOR_ITER             74  'to 74'
               44  UNPACK_SEQUENCE_2     2 
               46  STORE_FAST               'i'
               48  STORE_FAST               'item'

 L. 424        50  LOAD_GLOBAL              print
               52  LOAD_STR                 '%*s) %s'
               54  LOAD_FAST                'num_of_digits'
               56  LOAD_FAST                'i'
               58  LOAD_CONST               1
               60  BINARY_ADD       
               62  LOAD_FAST                'item'
               64  BUILD_TUPLE_3         3 
               66  BINARY_MODULO    
               68  CALL_FUNCTION_1       1  ''
               70  POP_TOP          
               72  JUMP_BACK            42  'to 42'

 L. 426        74  LOAD_GLOBAL              six
               76  LOAD_ATTR                moves
               78  LOAD_METHOD              input
               80  LOAD_FAST                'prompt'
               82  CALL_METHOD_1         1  ''
               84  STORE_FAST               'ans'

 L. 428        86  SETUP_FINALLY       144  'to 144'

 L. 429        88  LOAD_GLOBAL              int
               90  LOAD_FAST                'ans'
               92  CALL_FUNCTION_1       1  ''
               94  STORE_FAST               'choice'

 L. 430        96  LOAD_FAST                'choice'
               98  LOAD_CONST               1
              100  COMPARE_OP               <
              102  POP_JUMP_IF_TRUE    116  'to 116'
              104  LOAD_FAST                'choice'
              106  LOAD_GLOBAL              len
              108  LOAD_FAST                'items'
              110  CALL_FUNCTION_1       1  ''
              112  COMPARE_OP               >
              114  POP_JUMP_IF_FALSE   134  'to 134'
            116_0  COME_FROM           102  '102'

 L. 431       116  LOAD_GLOBAL              print
              118  LOAD_STR                 'Choose items between 1 to %d'
              120  LOAD_GLOBAL              len
              122  LOAD_FAST                'items'
              124  CALL_FUNCTION_1       1  ''
              126  CALL_FUNCTION_2       2  ''
              128  POP_TOP          

 L. 432       130  POP_BLOCK        
              132  JUMP_BACK            34  'to 34'
            134_0  COME_FROM           114  '114'

 L. 434       134  LOAD_FAST                'choice'
              136  LOAD_CONST               1
              138  BINARY_SUBTRACT  
              140  POP_BLOCK        
              142  RETURN_VALUE     
            144_0  COME_FROM_FINALLY    86  '86'

 L. 435       144  DUP_TOP          
              146  LOAD_GLOBAL              ValueError
              148  COMPARE_OP               exception-match
              150  POP_JUMP_IF_FALSE   176  'to 176'
              152  POP_TOP          
              154  POP_TOP          
              156  POP_TOP          

 L. 436       158  LOAD_GLOBAL              print
              160  LOAD_STR                 'Choose items between 1 to %d'
              162  LOAD_GLOBAL              len
              164  LOAD_FAST                'items'
              166  CALL_FUNCTION_1       1  ''
              168  CALL_FUNCTION_2       2  ''
              170  POP_TOP          
              172  POP_EXCEPT       
              174  JUMP_BACK            34  'to 34'
            176_0  COME_FROM           150  '150'
              176  END_FINALLY      
              178  JUMP_BACK            34  'to 34'

Parse error at or near `JUMP_BACK' instruction at offset 132


class Capturing(list):
    __doc__ = '\n    Captures the standard out in a context, so you can do something like:\n\n    with Capturing() as output:\n        subprocess.check_call("echo blah", shell=True)\n\n    print(str(output).contains("blah")) # true\n    '

    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extendself._stringio.getvalue().splitlines()
        sys.stdout = self._stdout


if __name__ == '__main__':
    rows = [{'a':'apple',  'b':'boy'},
     {'a':'one', 
      'b':'two'}]
    DataPrinter(rows).print_result()