# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tkomiya/work/sphinx/.tox/py37/lib/python3.7/site-packages/docutils/parsers/rst/directives/tables.py
# Compiled at: 2018-11-25 06:19:18
# Size of source mod 2**32: 22360 bytes
"""
Directives for table elements.
"""
__docformat__ = 'reStructuredText'
import sys, os.path, csv
from docutils import io, nodes, statemachine, utils
from docutils.utils.error_reporting import SafeString
from docutils.utils import SystemMessagePropagation
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives

def align(argument):
    return directives.choice(argument, ('left', 'center', 'right'))


class Table(Directive):
    __doc__ = '\n    Generic table base class.\n    '
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {'class':directives.class_option,  'name':directives.unchanged, 
     'align':align, 
     'widths':directives.value_or(('auto', 'grid'), directives.positive_int_list)}
    has_content = True

    def make_title(self):
        if self.arguments:
            title_text = self.arguments[0]
            text_nodes, messages = self.state.inline_text(title_text, self.lineno)
            title = (nodes.title)(title_text, '', *text_nodes)
            title.source, title.line = self.state_machine.get_source_and_line(self.lineno)
        else:
            title = None
            messages = []
        return (
         title, messages)

    def process_header_option(self):
        source = self.state_machine.get_source(self.lineno - 1)
        table_head = []
        max_header_cols = 0
        if 'header' in self.options:
            rows, max_header_cols = self.parse_csv_data_into_rows(self.options['header'].split('\n'), self.HeaderDialect(), source)
            table_head.extend(rows)
        return (
         table_head, max_header_cols)

    def check_table_dimensions(self, rows, header_rows, stub_columns):
        if len(rows) < header_rows:
            error = self.state_machine.reporter.error(('%s header row(s) specified but only %s row(s) of data supplied ("%s" directive).' % (
             header_rows, len(rows), self.name)),
              (nodes.literal_block(self.block_text, self.block_text)),
              line=(self.lineno))
            raise SystemMessagePropagation(error)
        if len(rows) == header_rows > 0:
            error = self.state_machine.reporter.error(('Insufficient data supplied (%s row(s)); no data remaining for table body, required by "%s" directive.' % (
             len(rows), self.name)),
              (nodes.literal_block(self.block_text, self.block_text)),
              line=(self.lineno))
            raise SystemMessagePropagation(error)
        for row in rows:
            if len(row) < stub_columns:
                error = self.state_machine.reporter.error(('%s stub column(s) specified but only %s columns(s) of data supplied ("%s" directive).' % (
                 stub_columns, len(row), self.name)),
                  (nodes.literal_block(self.block_text, self.block_text)),
                  line=(self.lineno))
                raise SystemMessagePropagation(error)
            if len(row) == stub_columns > 0:
                error = self.state_machine.reporter.error(('Insufficient data supplied (%s columns(s)); no data remaining for table body, required by "%s" directive.' % (
                 len(row), self.name)),
                  (nodes.literal_block(self.block_text, self.block_text)),
                  line=(self.lineno))
                raise SystemMessagePropagation(error)

    @property
    def widths(self):
        return self.options.get('widths', '')

    def get_column_widths(self, max_cols):
        if type(self.widths) == list:
            if len(self.widths) != max_cols:
                error = self.state_machine.reporter.error(('"%s" widths do not match the number of columns in table (%s).' % (
                 self.name, max_cols)),
                  (nodes.literal_block(self.block_text, self.block_text)),
                  line=(self.lineno))
                raise SystemMessagePropagation(error)
            col_widths = self.widths
        else:
            if max_cols:
                col_widths = [
                 100 // max_cols] * max_cols
            else:
                error = self.state_machine.reporter.error('No table data detected in CSV file.',
                  (nodes.literal_block(self.block_text, self.block_text)),
                  line=(self.lineno))
                raise SystemMessagePropagation(error)
        return col_widths

    def extend_short_rows_with_empty_cells(self, columns, parts):
        for part in parts:
            for row in part:
                if len(row) < columns:
                    row.extend([(0, 0, 0, [])] * (columns - len(row)))


class RSTTable(Table):

    def run(self):
        if not self.content:
            warning = self.state_machine.reporter.warning(('Content block expected for the "%s" directive; none found.' % self.name),
              (nodes.literal_block(self.block_text, self.block_text)),
              line=(self.lineno))
            return [warning]
        else:
            title, messages = self.make_title()
            node = nodes.Element()
            self.state.nested_parse(self.content, self.content_offset, node)
            error = len(node) != 1 or isinstance(node[0], nodes.table) or self.state_machine.reporter.error(('Error parsing content block for the "%s" directive: exactly one table expected.' % self.name),
              (nodes.literal_block(self.block_text, self.block_text)),
              line=(self.lineno))
            return [error]
        table_node = node[0]
        table_node['classes'] += self.options.get('class', [])
        if 'align' in self.options:
            table_node['align'] = self.options.get('align')
        tgroup = table_node[0]
        if type(self.widths) == list:
            colspecs = [child for child in tgroup.children if child.tagname == 'colspec']
            for colspec, col_width in zip(colspecs, self.widths):
                colspec['colwidth'] = col_width

        if self.widths == 'auto':
            table_node['classes'] += ['colwidths-auto']
        else:
            if self.widths:
                table_node['classes'] += ['colwidths-given']
            self.add_name(table_node)
            if title:
                table_node.insert(0, title)
            return [
             table_node] + messages


class CSVTable(Table):
    option_spec = {'header-rows':directives.nonnegative_int, 
     'stub-columns':directives.nonnegative_int, 
     'header':directives.unchanged, 
     'widths':directives.value_or(('auto', ), directives.positive_int_list), 
     'file':directives.path, 
     'url':directives.uri, 
     'encoding':directives.encoding, 
     'class':directives.class_option, 
     'name':directives.unchanged, 
     'align':align, 
     'delim':directives.single_char_or_whitespace_or_unicode, 
     'keepspace':directives.flag, 
     'quote':directives.single_char_or_unicode, 
     'escape':directives.single_char_or_unicode}

    class DocutilsDialect(csv.Dialect):
        __doc__ = 'CSV dialect for `csv_table` directive.'
        delimiter = ','
        quotechar = '"'
        doublequote = True
        skipinitialspace = True
        strict = True
        lineterminator = '\n'
        quoting = csv.QUOTE_MINIMAL

        def __init__(self, options):
            if 'delim' in options:
                self.delimiter = CSVTable.encode_for_csv(options['delim'])
            if 'keepspace' in options:
                self.skipinitialspace = False
            if 'quote' in options:
                self.quotechar = CSVTable.encode_for_csv(options['quote'])
            if 'escape' in options:
                self.doublequote = False
                self.escapechar = CSVTable.encode_for_csv(options['escape'])
            csv.Dialect.__init__(self)

    class HeaderDialect(csv.Dialect):
        __doc__ = 'CSV dialect to use for the "header" option data.'
        delimiter = ','
        quotechar = '"'
        escapechar = '\\'
        doublequote = False
        skipinitialspace = True
        strict = True
        lineterminator = '\n'
        quoting = csv.QUOTE_MINIMAL

    def check_requirements(self):
        pass

    def run(self):
        try:
            if not self.state.document.settings.file_insertion_enabled:
                if not 'file' in self.options:
                    if 'url' in self.options:
                        warning = self.state_machine.reporter.warning(('File and URL access deactivated; ignoring "%s" directive.' % self.name),
                          (nodes.literal_block(self.block_text, self.block_text)),
                          line=(self.lineno))
                        return [warning]
            self.check_requirements()
            title, messages = self.make_title()
            csv_data, source = self.get_csv_data()
            table_head, max_header_cols = self.process_header_option()
            rows, max_cols = self.parse_csv_data_into_rows(csv_data, self.DocutilsDialect(self.options), source)
            max_cols = max(max_cols, max_header_cols)
            header_rows = self.options.get('header-rows', 0)
            stub_columns = self.options.get('stub-columns', 0)
            self.check_table_dimensions(rows, header_rows, stub_columns)
            table_head.extend(rows[:header_rows])
            table_body = rows[header_rows:]
            col_widths = self.get_column_widths(max_cols)
            self.extend_short_rows_with_empty_cells(max_cols, (
             table_head, table_body))
        except SystemMessagePropagation as detail:
            try:
                return [
                 detail.args[0]]
            finally:
                detail = None
                del detail

        except csv.Error as detail:
            try:
                message = str(detail)
                if sys.version_info < (3, ):
                    if '1-character string' in message:
                        message += '\nwith Python 2.x this must be an ASCII character.'
                error = self.state_machine.reporter.error(('Error with CSV data in "%s" directive:\n%s' % (
                 self.name, message)),
                  (nodes.literal_block(self.block_text, self.block_text)),
                  line=(self.lineno))
                return [error]
            finally:
                detail = None
                del detail

        table = (
         col_widths, table_head, table_body)
        table_node = self.state.build_table(table, (self.content_offset), stub_columns,
          widths=(self.widths))
        table_node['classes'] += self.options.get('class', [])
        if 'align' in self.options:
            table_node['align'] = self.options.get('align')
        self.add_name(table_node)
        if title:
            table_node.insert(0, title)
        return [
         table_node] + messages

    def get_csv_data--- This code section failed: ---

 L. 282         0  LOAD_FAST                'self'
                2  LOAD_ATTR                options
                4  LOAD_METHOD              get

 L. 283         6  LOAD_STR                 'encoding'
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                state
               12  LOAD_ATTR                document
               14  LOAD_ATTR                settings
               16  LOAD_ATTR                input_encoding
               18  CALL_METHOD_2         2  '2 positional arguments'
               20  STORE_FAST               'encoding'

 L. 284        22  LOAD_FAST                'self'
               24  LOAD_ATTR                state
               26  LOAD_ATTR                document
               28  LOAD_ATTR                settings
               30  LOAD_ATTR                input_encoding_error_handler
               32  STORE_FAST               'error_handler'

 L. 285        34  LOAD_FAST                'self'
               36  LOAD_ATTR                content
               38  POP_JUMP_IF_FALSE   130  'to 130'

 L. 287        40  LOAD_STR                 'file'
               42  LOAD_FAST                'self'
               44  LOAD_ATTR                options
               46  COMPARE_OP               in
               48  POP_JUMP_IF_TRUE     60  'to 60'
               50  LOAD_STR                 'url'
               52  LOAD_FAST                'self'
               54  LOAD_ATTR                options
               56  COMPARE_OP               in
               58  POP_JUMP_IF_FALSE   108  'to 108'
             60_0  COME_FROM            48  '48'

 L. 288        60  LOAD_FAST                'self'
               62  LOAD_ATTR                state_machine
               64  LOAD_ATTR                reporter
               66  LOAD_ATTR                error

 L. 289        68  LOAD_STR                 '"%s" directive may not both specify an external file and have content.'

 L. 290        70  LOAD_FAST                'self'
               72  LOAD_ATTR                name
               74  BINARY_MODULO    
               76  LOAD_GLOBAL              nodes
               78  LOAD_METHOD              literal_block

 L. 291        80  LOAD_FAST                'self'
               82  LOAD_ATTR                block_text
               84  LOAD_FAST                'self'
               86  LOAD_ATTR                block_text
               88  CALL_METHOD_2         2  '2 positional arguments'
               90  LOAD_FAST                'self'
               92  LOAD_ATTR                lineno
               94  LOAD_CONST               ('line',)
               96  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               98  STORE_FAST               'error'

 L. 292       100  LOAD_GLOBAL              SystemMessagePropagation
              102  LOAD_FAST                'error'
              104  CALL_FUNCTION_1       1  '1 positional argument'
              106  RAISE_VARARGS_1       1  'exception instance'
            108_0  COME_FROM            58  '58'

 L. 293       108  LOAD_FAST                'self'
              110  LOAD_ATTR                content
              112  LOAD_METHOD              source
              114  LOAD_CONST               0
              116  CALL_METHOD_1         1  '1 positional argument'
              118  STORE_FAST               'source'

 L. 294       120  LOAD_FAST                'self'
              122  LOAD_ATTR                content
              124  STORE_FAST               'csv_data'
          126_128  JUMP_FORWARD        682  'to 682'
            130_0  COME_FROM            38  '38'

 L. 295       130  LOAD_STR                 'file'
              132  LOAD_FAST                'self'
              134  LOAD_ATTR                options
              136  COMPARE_OP               in
          138_140  POP_JUMP_IF_FALSE   414  'to 414'

 L. 297       142  LOAD_STR                 'url'
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                options
              148  COMPARE_OP               in
              150  POP_JUMP_IF_FALSE   200  'to 200'

 L. 298       152  LOAD_FAST                'self'
              154  LOAD_ATTR                state_machine
              156  LOAD_ATTR                reporter
              158  LOAD_ATTR                error

 L. 299       160  LOAD_STR                 'The "file" and "url" options may not be simultaneously specified for the "%s" directive.'

 L. 300       162  LOAD_FAST                'self'
              164  LOAD_ATTR                name
              166  BINARY_MODULO    

 L. 301       168  LOAD_GLOBAL              nodes
              170  LOAD_METHOD              literal_block
              172  LOAD_FAST                'self'
              174  LOAD_ATTR                block_text
              176  LOAD_FAST                'self'
              178  LOAD_ATTR                block_text
              180  CALL_METHOD_2         2  '2 positional arguments'

 L. 302       182  LOAD_FAST                'self'
              184  LOAD_ATTR                lineno
              186  LOAD_CONST               ('line',)
              188  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              190  STORE_FAST               'error'

 L. 303       192  LOAD_GLOBAL              SystemMessagePropagation
              194  LOAD_FAST                'error'
              196  CALL_FUNCTION_1       1  '1 positional argument'
              198  RAISE_VARARGS_1       1  'exception instance'
            200_0  COME_FROM           150  '150'

 L. 304       200  LOAD_GLOBAL              os
              202  LOAD_ATTR                path
              204  LOAD_METHOD              dirname

 L. 305       206  LOAD_GLOBAL              os
              208  LOAD_ATTR                path
              210  LOAD_METHOD              abspath
              212  LOAD_FAST                'self'
              214  LOAD_ATTR                state
              216  LOAD_ATTR                document
              218  LOAD_ATTR                current_source
              220  CALL_METHOD_1         1  '1 positional argument'
              222  CALL_METHOD_1         1  '1 positional argument'
              224  STORE_FAST               'source_dir'

 L. 306       226  LOAD_GLOBAL              os
              228  LOAD_ATTR                path
              230  LOAD_METHOD              normpath
              232  LOAD_GLOBAL              os
              234  LOAD_ATTR                path
              236  LOAD_METHOD              join
              238  LOAD_FAST                'source_dir'

 L. 307       240  LOAD_FAST                'self'
              242  LOAD_ATTR                options
              244  LOAD_STR                 'file'
              246  BINARY_SUBSCR    
              248  CALL_METHOD_2         2  '2 positional arguments'
              250  CALL_METHOD_1         1  '1 positional argument'
              252  STORE_FAST               'source'

 L. 308       254  LOAD_GLOBAL              utils
              256  LOAD_METHOD              relative_path
              258  LOAD_CONST               None
              260  LOAD_FAST                'source'
              262  CALL_METHOD_2         2  '2 positional arguments'
              264  STORE_FAST               'source'

 L. 309       266  SETUP_EXCEPT        318  'to 318'

 L. 310       268  LOAD_FAST                'self'
              270  LOAD_ATTR                state
              272  LOAD_ATTR                document
              274  LOAD_ATTR                settings
              276  LOAD_ATTR                record_dependencies
              278  LOAD_METHOD              add
              280  LOAD_FAST                'source'
              282  CALL_METHOD_1         1  '1 positional argument'
              284  POP_TOP          

 L. 311       286  LOAD_GLOBAL              io
              288  LOAD_ATTR                FileInput
              290  LOAD_FAST                'source'

 L. 312       292  LOAD_FAST                'encoding'

 L. 313       294  LOAD_FAST                'error_handler'
              296  LOAD_CONST               ('source_path', 'encoding', 'error_handler')
              298  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              300  STORE_FAST               'csv_file'

 L. 314       302  LOAD_FAST                'csv_file'
              304  LOAD_METHOD              read
              306  CALL_METHOD_0         0  '0 positional arguments'
              308  LOAD_METHOD              splitlines
              310  CALL_METHOD_0         0  '0 positional arguments'
              312  STORE_FAST               'csv_data'
              314  POP_BLOCK        
              316  JUMP_FORWARD        682  'to 682'
            318_0  COME_FROM_EXCEPT    266  '266'

 L. 315       318  DUP_TOP          
              320  LOAD_GLOBAL              IOError
              322  COMPARE_OP               exception-match
          324_326  POP_JUMP_IF_FALSE   408  'to 408'
              328  POP_TOP          
              330  STORE_FAST               'error'
              332  POP_TOP          
              334  SETUP_FINALLY       396  'to 396'

 L. 316       336  LOAD_FAST                'self'
              338  LOAD_ATTR                state_machine
              340  LOAD_ATTR                reporter
              342  LOAD_ATTR                severe

 L. 317       344  LOAD_STR                 'Problems with "%s" directive path:\n%s.'

 L. 318       346  LOAD_FAST                'self'
              348  LOAD_ATTR                name
              350  LOAD_GLOBAL              SafeString
              352  LOAD_FAST                'error'
              354  CALL_FUNCTION_1       1  '1 positional argument'
              356  BUILD_TUPLE_2         2 
              358  BINARY_MODULO    

 L. 319       360  LOAD_GLOBAL              nodes
              362  LOAD_METHOD              literal_block
              364  LOAD_FAST                'self'
              366  LOAD_ATTR                block_text
              368  LOAD_FAST                'self'
              370  LOAD_ATTR                block_text
              372  CALL_METHOD_2         2  '2 positional arguments'

 L. 320       374  LOAD_FAST                'self'
              376  LOAD_ATTR                lineno
              378  LOAD_CONST               ('line',)
              380  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              382  STORE_FAST               'severe'

 L. 321       384  LOAD_GLOBAL              SystemMessagePropagation
              386  LOAD_FAST                'severe'
              388  CALL_FUNCTION_1       1  '1 positional argument'
              390  RAISE_VARARGS_1       1  'exception instance'
              392  POP_BLOCK        
              394  LOAD_CONST               None
            396_0  COME_FROM_FINALLY   334  '334'
              396  LOAD_CONST               None
              398  STORE_FAST               'error'
              400  DELETE_FAST              'error'
              402  END_FINALLY      
              404  POP_EXCEPT       
              406  JUMP_FORWARD        682  'to 682'
            408_0  COME_FROM           324  '324'
              408  END_FINALLY      
          410_412  JUMP_FORWARD        682  'to 682'
            414_0  COME_FROM           138  '138'

 L. 322       414  LOAD_STR                 'url'
              416  LOAD_FAST                'self'
              418  LOAD_ATTR                options
              420  COMPARE_OP               in
          422_424  POP_JUMP_IF_FALSE   634  'to 634'

 L. 327       426  LOAD_CONST               0
              428  LOAD_CONST               None
              430  IMPORT_NAME_ATTR         urllib.request
              432  STORE_FAST               'urllib'
              434  LOAD_CONST               0
              436  LOAD_CONST               None
              438  IMPORT_NAME_ATTR         urllib.error
              440  STORE_FAST               'urllib'
              442  LOAD_CONST               0
              444  LOAD_CONST               None
              446  IMPORT_NAME_ATTR         urllib.parse
              448  STORE_FAST               'urllib'

 L. 328       450  LOAD_FAST                'self'
              452  LOAD_ATTR                options
              454  LOAD_STR                 'url'
              456  BINARY_SUBSCR    
              458  STORE_FAST               'source'

 L. 329       460  SETUP_EXCEPT        482  'to 482'

 L. 330       462  LOAD_FAST                'urllib'
              464  LOAD_ATTR                request
              466  LOAD_METHOD              urlopen
              468  LOAD_FAST                'source'
              470  CALL_METHOD_1         1  '1 positional argument'
              472  LOAD_METHOD              read
              474  CALL_METHOD_0         0  '0 positional arguments'
              476  STORE_FAST               'csv_text'
              478  POP_BLOCK        
              480  JUMP_FORWARD        594  'to 594'
            482_0  COME_FROM_EXCEPT    460  '460'

 L. 331       482  DUP_TOP          
              484  LOAD_FAST                'urllib'
              486  LOAD_ATTR                error
              488  LOAD_ATTR                URLError
              490  LOAD_GLOBAL              IOError
              492  LOAD_GLOBAL              OSError
              494  LOAD_GLOBAL              ValueError
              496  BUILD_TUPLE_4         4 
              498  COMPARE_OP               exception-match
          500_502  POP_JUMP_IF_FALSE   592  'to 592'
              504  POP_TOP          
              506  STORE_FAST               'error'
              508  POP_TOP          
              510  SETUP_FINALLY       580  'to 580'

 L. 332       512  LOAD_FAST                'self'
              514  LOAD_ATTR                state_machine
              516  LOAD_ATTR                reporter
              518  LOAD_ATTR                severe

 L. 333       520  LOAD_STR                 'Problems with "%s" directive URL "%s":\n%s.'

 L. 334       522  LOAD_FAST                'self'
              524  LOAD_ATTR                name
              526  LOAD_FAST                'self'
              528  LOAD_ATTR                options
              530  LOAD_STR                 'url'
              532  BINARY_SUBSCR    
              534  LOAD_GLOBAL              SafeString
              536  LOAD_FAST                'error'
              538  CALL_FUNCTION_1       1  '1 positional argument'
              540  BUILD_TUPLE_3         3 
              542  BINARY_MODULO    

 L. 335       544  LOAD_GLOBAL              nodes
              546  LOAD_METHOD              literal_block
              548  LOAD_FAST                'self'
              550  LOAD_ATTR                block_text
              552  LOAD_FAST                'self'
              554  LOAD_ATTR                block_text
              556  CALL_METHOD_2         2  '2 positional arguments'

 L. 336       558  LOAD_FAST                'self'
              560  LOAD_ATTR                lineno
              562  LOAD_CONST               ('line',)
              564  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              566  STORE_FAST               'severe'

 L. 337       568  LOAD_GLOBAL              SystemMessagePropagation
              570  LOAD_FAST                'severe'
              572  CALL_FUNCTION_1       1  '1 positional argument'
              574  RAISE_VARARGS_1       1  'exception instance'
              576  POP_BLOCK        
              578  LOAD_CONST               None
            580_0  COME_FROM_FINALLY   510  '510'
              580  LOAD_CONST               None
              582  STORE_FAST               'error'
              584  DELETE_FAST              'error'
            586_0  COME_FROM           316  '316'
              586  END_FINALLY      
              588  POP_EXCEPT       
              590  JUMP_FORWARD        594  'to 594'
            592_0  COME_FROM           500  '500'
              592  END_FINALLY      
            594_0  COME_FROM           590  '590'
            594_1  COME_FROM           480  '480'

 L. 338       594  LOAD_GLOBAL              io
              596  LOAD_ATTR                StringInput

 L. 339       598  LOAD_FAST                'csv_text'
              600  LOAD_FAST                'source'
              602  LOAD_FAST                'encoding'

 L. 340       604  LOAD_FAST                'self'
              606  LOAD_ATTR                state
              608  LOAD_ATTR                document
              610  LOAD_ATTR                settings
              612  LOAD_ATTR                input_encoding_error_handler
              614  LOAD_CONST               ('source', 'source_path', 'encoding', 'error_handler')
              616  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              618  STORE_FAST               'csv_file'

 L. 342       620  LOAD_FAST                'csv_file'
              622  LOAD_METHOD              read
              624  CALL_METHOD_0         0  '0 positional arguments'
              626  LOAD_METHOD              splitlines
              628  CALL_METHOD_0         0  '0 positional arguments'
              630  STORE_FAST               'csv_data'
              632  JUMP_FORWARD        682  'to 682'
            634_0  COME_FROM           422  '422'

 L. 344       634  LOAD_FAST                'self'
              636  LOAD_ATTR                state_machine
              638  LOAD_ATTR                reporter
              640  LOAD_ATTR                warning

 L. 345       642  LOAD_STR                 'The "%s" directive requires content; none supplied.'

 L. 346       644  LOAD_FAST                'self'
              646  LOAD_ATTR                name
              648  BINARY_MODULO    
              650  LOAD_GLOBAL              nodes
              652  LOAD_METHOD              literal_block

 L. 347       654  LOAD_FAST                'self'
              656  LOAD_ATTR                block_text
              658  LOAD_FAST                'self'
              660  LOAD_ATTR                block_text
              662  CALL_METHOD_2         2  '2 positional arguments'
              664  LOAD_FAST                'self'
              666  LOAD_ATTR                lineno
              668  LOAD_CONST               ('line',)
              670  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              672  STORE_FAST               'error'

 L. 348       674  LOAD_GLOBAL              SystemMessagePropagation
            676_0  COME_FROM           406  '406'
              676  LOAD_FAST                'error'
              678  CALL_FUNCTION_1       1  '1 positional argument'
              680  RAISE_VARARGS_1       1  'exception instance'
            682_0  COME_FROM           632  '632'
            682_1  COME_FROM           410  '410'
            682_2  COME_FROM           126  '126'

 L. 349       682  LOAD_FAST                'csv_data'
              684  LOAD_FAST                'source'
              686  BUILD_TUPLE_2         2 
              688  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `END_FINALLY' instruction at offset 586

    if sys.version_info < (3, ):

        def decode_from_csv(s):
            return s.decode('utf-8')

        def encode_for_csv(s):
            return s.encode('utf-8')

    else:

        def decode_from_csv(s):
            return s

        def encode_for_csv(s):
            return s

    decode_from_csv = staticmethod(decode_from_csv)
    encode_for_csv = staticmethod(encode_for_csv)

    def parse_csv_data_into_rows(self, csv_data, dialect, source):
        csv_reader = csv.reader([self.encode_for_csv(line + '\n') for line in csv_data],
          dialect=dialect)
        rows = []
        max_cols = 0
        for row in csv_reader:
            row_data = []
            for cell in row:
                cell_text = self.decode_from_csv(cell)
                cell_data = (0, 0, 0,
                 statemachine.StringList((cell_text.splitlines()),
                   source=source))
                row_data.append(cell_data)

            rows.append(row_data)
            max_cols = max(max_cols, len(row))

        return (
         rows, max_cols)


class ListTable(Table):
    __doc__ = '\n    Implement tables whose data is encoded as a uniform two-level bullet list.\n    For further ideas, see\n    http://docutils.sf.net/docs/dev/rst/alternatives.html#list-driven-tables\n    '
    option_spec = {'header-rows':directives.nonnegative_int, 
     'stub-columns':directives.nonnegative_int, 
     'widths':directives.value_or(('auto', ), directives.positive_int_list), 
     'class':directives.class_option, 
     'name':directives.unchanged, 
     'align':align}

    def run(self):
        if not self.content:
            error = self.state_machine.reporter.error(('The "%s" directive is empty; content required.' % self.name),
              (nodes.literal_block(self.block_text, self.block_text)),
              line=(self.lineno))
            return [error]
        title, messages = self.make_title()
        node = nodes.Element()
        self.state.nested_parse(self.content, self.content_offset, node)
        try:
            num_cols, col_widths = self.check_list_content(node)
            table_data = [[item.children for item in row_list[0]] for row_list in node[0]]
            header_rows = self.options.get('header-rows', 0)
            stub_columns = self.options.get('stub-columns', 0)
            self.check_table_dimensions(table_data, header_rows, stub_columns)
        except SystemMessagePropagation as detail:
            try:
                return [
                 detail.args[0]]
            finally:
                detail = None
                del detail

        table_node = self.build_table_from_list(table_data, col_widths, header_rows, stub_columns)
        if 'align' in self.options:
            table_node['align'] = self.options.get('align')
        table_node['classes'] += self.options.get('class', [])
        self.add_name(table_node)
        if title:
            table_node.insert(0, title)
        return [
         table_node] + messages

    def check_list_content(self, node):
        if not (len(node) != 1 or isinstance(node[0], nodes.bullet_list)):
            error = self.state_machine.reporter.error(('Error parsing content block for the "%s" directive: exactly one bullet list expected.' % self.name),
              (nodes.literal_block(self.block_text, self.block_text)),
              line=(self.lineno))
            raise SystemMessagePropagation(error)
        list_node = node[0]
        for item_index in range(len(list_node)):
            item = list_node[item_index]
            if not len(item) != 1:
                error = isinstance(item[0], nodes.bullet_list) or self.state_machine.reporter.error(('Error parsing content block for the "%s" directive: two-level bullet list expected, but row %s does not contain a second-level bullet list.' % (
                 self.name, item_index + 1)),
                  (nodes.literal_block(self.block_text, self.block_text)),
                  line=(self.lineno))
                raise SystemMessagePropagation(error)
            elif item_index:
                if len(item[0]) != num_cols:
                    error = self.state_machine.reporter.error(('Error parsing content block for the "%s" directive: uniform two-level bullet list expected, but row %s does not contain the same number of items as row 1 (%s vs %s).' % (
                     self.name, item_index + 1, len(item[0]), num_cols)),
                      (nodes.literal_block(self.block_text, self.block_text)),
                      line=(self.lineno))
                    raise SystemMessagePropagation(error)
            else:
                num_cols = len(item[0])

        col_widths = self.get_column_widths(num_cols)
        return (num_cols, col_widths)

    def build_table_from_list(self, table_data, col_widths, header_rows, stub_columns):
        table = nodes.table()
        if self.widths == 'auto':
            table['classes'] += ['colwidths-auto']
        else:
            if self.widths:
                table['classes'] += ['colwidths-given']
        tgroup = nodes.tgroup(cols=(len(col_widths)))
        table += tgroup
        for col_width in col_widths:
            colspec = nodes.colspec()
            if col_width is not None:
                colspec.attributes['colwidth'] = col_width
            if stub_columns:
                colspec.attributes['stub'] = 1
                stub_columns -= 1
            tgroup += colspec

        rows = []
        for row in table_data:
            row_node = nodes.row()
            for cell in row:
                entry = nodes.entry()
                entry += cell
                row_node += entry

            rows.append(row_node)

        if header_rows:
            thead = nodes.thead()
            thead.extend(rows[:header_rows])
            tgroup += thead
        tbody = nodes.tbody()
        tbody.extend(rows[header_rows:])
        tgroup += tbody
        return table