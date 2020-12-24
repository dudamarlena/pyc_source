# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/search.py
# Compiled at: 2020-03-18 17:27:39
# Size of source mod 2**32: 42359 bytes
"""
web2ldap.app.search: do a search and return results in several formats

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2019 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import time, csv, urllib.parse, binascii, xlwt, ldap0, ldap0.cidict, ldap0.filter, ldap0.schema.models
from ldap0.controls.openldap import SearchNoOpControl
from ldap0.schema.models import AttributeType
from ldap0.base import decode_list
from ldap0.res import SearchReference, SearchResultEntry
import web2ldap.web.forms
from web2ldap.web import escape_html
import web2ldap.ldaputil.asynch, web2ldap.msbase, web2ldap.ldaputil, web2ldap.app.core, web2ldap.app.cnf, web2ldap.app.gui, web2ldap.app.read, web2ldap.app.searchform
from web2ldap.ldaputil.extldapurl import ExtendedLDAPUrl
from web2ldap.msbase import GrabKeys
from web2ldap.app.schema.syntaxes import syntax_registry
from web2ldap.app.searchform import SEARCH_OPT_ATTR_EXISTS, SEARCH_OPT_ATTR_NOT_EXISTS
from web2ldap.ldapsession import LDAPLimitErrors
from web2ldap.msbase import CaseinsensitiveStringKeyDict
from web2ldap.wsgi import WSGIBytesWrapper
import web2ldap.__about__
SEARCH_NOOP_TIMEOUT = 5.0
PAGE_COMMAND_TMPL = '\n<nav><table>\n  <tr>\n    <td width="20%">{0}</td>\n    <td width="20%">{1}</td>\n    <td width="20%">{2}</td>\n    <td width="20%">{3}</td>\n    <td width="20%">{4}</td>\n  </tr>\n</table></nav>\n'
LDAPERROR_SIZELIMIT_MSG = '\n<p class="ErrorMessage">\n  <strong>\n    Only partial results received. Try to refine search.\n  </strong><br>\n  {error_msg}\n</p>\n'
LDIF1_HEADER = '########################################################################\n# LDIF export by web2ldap %s, see https://www.web2ldap.de\n# Date and time: %s\n# Bind-DN: %s\n# LDAP-URL of search:\n# %s\n########################################################################\nversion: 1\n\n'
is_search_result = {
 ldap0.RES_SEARCH_ENTRY,
 ldap0.RES_SEARCH_RESULT}
is_search_reference = {
 ldap0.RES_SEARCH_REFERENCE}

class excel_semicolon(csv.excel):
    __doc__ = 'Describe the usual properties of Excel-generated TAB-delimited files.'
    delimiter = ';'


csv.register_dialect('excel-semicolon', excel_semicolon)

class LDIFWriter(web2ldap.ldaputil.asynch.LDIFWriter):

    def pre_processing(self):
        pass

    def after_first(self):
        self._ldif_writer._output_file.set_headers(web2ldap.app.gui.gen_headers(content_type='text/plain',
          charset='utf-8',
          more_headers=[
         ('Content-Disposition', 'inline; filename=web2ldap-export.ldif')]))
        web2ldap.ldaputil.asynch.LDIFWriter.pre_processing(self)


class PrintableHTMLWriter(web2ldap.ldaputil.asynch.List):
    __doc__ = '\n    Class for writing a stream LDAP search results to a printable file\n    '
    _entryResultTypes = is_search_result

    def __init__(self, app, dn, sub_schema, print_template_str_dict):
        web2ldap.ldaputil.asynch.List.__init__(self, app.ls.l)
        self._app = app
        self._dn = dn
        self._s = sub_schema
        self._p = print_template_str_dict

    def process_results(self, ignoreResultsNumber=0, processResultsCount=0):
        web2ldap.ldaputil.asynch.List.process_results(self)
        utf2display = self._app.form.utf2display
        print_cols = self._app.cfg_param('print_cols', '4')
        table = []
        for r in self.allResults:
            if not isinstance(r, SearchResultEntry):
                pass
            else:
                objectclasses = r.entry_s.get('objectclass', r.entry_s.get('objectClass', []))
                template_oc = list(set([o.lower() for o in objectclasses]).intersection([s.lower() for s in self._p.keys()]))
                if template_oc:
                    tableentry = CaseinsensitiveStringKeyDict(default='')
                    attr_list = r.entry_s.keys()
                    for attr in attr_list:
                        tableentry[attr] = ', '.join([utf2display(attr_value) for attr_value in r.entry_s[attr]])
                    else:
                        table.append(self._p[template_oc[0]] % tableentry)

                web2ldap.app.gui.top_section(self._app, 'Printable Search Results', [])
                self._app.outf.write('\n            <table\n              class="PrintSearchResults"\n              rules="rows"\n              id="PrintTable"\n              summary="Table with search results formatted for printing">\n            ')
                for i in range(0, len(table), print_cols):
                    td_list = ['<td>%s</td>' % tc for tc in table[i:i + print_cols]]
                    self._app.outf.write('<tr>\n%s</tr>\n' % '\n'.join(td_list))
                else:
                    self._app.outf.write('</table>\n')
                    web2ldap.app.gui.footer(self._app)


class CSVWriter(web2ldap.ldaputil.asynch.AsyncSearchHandler):
    __doc__ = '\n    Class for writing a stream LDAP search results to a CSV file\n    '
    _entryResultTypes = is_search_result
    _formular_prefixes = frozenset('@+-=|%')

    def __init__(self, l, f, sub_schema, attr_types, ldap_charset='utf-8'):
        web2ldap.ldaputil.asynch.AsyncSearchHandler.__init__(self, l)
        self._output_file = f
        self._csv_writer = csv.writer(f, dialect='excel-semicolon')
        self._s = sub_schema
        self._attr_types = attr_types
        self._ldap_charset = ldap_charset

    def after_first(self):
        self._output_file.set_headers(web2ldap.app.gui.gen_headers(content_type='text/csv',
          charset='utf-8',
          more_headers=[
         ('Content-Disposition', 'inline; filename=web2ldap-export.csv')]))
        self._csv_writer.writerow(self._attr_types)

    def _process_result(self, resultItem):
        if not isinstance(resultItem, SearchResultEntry):
            return
        entry = ldap0.schema.models.Entry(self._s, resultItem.dn_s, resultItem.entry_as)
        csv_row_list = []
        for attr_type in self._attr_types:
            csv_col_value_list = []
            for attr_value in entry.get(attr_type, [b'']):
                try:
                    csv_col_value = attr_value.decode(self._ldap_charset)
                except UnicodeError:
                    csv_col_value = binascii.b2a_base64(attr_value).decode('ascii').replace('\r', '').replace('\n', '')
                else:
                    if csv_col_value and csv_col_value[0] in self._formular_prefixes:
                        csv_col_value_list.append("'" + csv_col_value)
                    else:
                        csv_col_value_list.append(csv_col_value)
            else:
                csv_row_list.append('|'.join(csv_col_value_list))

        else:
            self._csv_writer.writerow(csv_row_list)


class ExcelWriter(web2ldap.ldaputil.asynch.AsyncSearchHandler):
    __doc__ = '\n    Class for writing a stream LDAP search results to a Excel file\n    '
    _entryResultTypes = is_search_result

    def __init__(self, l, f, sub_schema, attr_types, ldap_charset='utf-8'):
        web2ldap.ldaputil.asynch.AsyncSearchHandler.__init__(self, l)
        self._f = f
        self._s = sub_schema
        self._attr_types = attr_types
        self._ldap_charset = ldap_charset
        self._workbook = xlwt.Workbook(encoding='cp1251')
        self._worksheet = self._workbook.add_sheet('web2ldap_export')
        self._row_counter = 0

    def after_first(self):
        self._f.set_headers(web2ldap.app.gui.gen_headers(content_type='application/vnd.ms-excel',
          charset='utf-8',
          more_headers=[
         ('Content-Disposition', 'inline; filename=web2ldap-export.xls')]))
        for col in range(len(self._attr_types)):
            self._worksheet.write(0, col, self._attr_types[col])
        else:
            self._row_counter += 1

    def post_processing(self):
        self._workbook.save(self._f)

    def _process_result(self, resultItem):
        if not isinstance(resultItem, SearchResultEntry):
            return
        entry = ldap0.schema.models.Entry(self._s, resultItem.dn_s, resultItem.entry_as)
        csv_row_list = []
        for attr_type in self._attr_types:
            csv_col_value_list = []
            for attr_value in entry.get(attr_type, [b'']):
                try:
                    csv_col_value = attr_value.decode(self._ldap_charset)
                except UnicodeError:
                    csv_col_value = binascii.b2a_base64(attr_value).decode('ascii').replace('\r', '').replace('\n', '')
                else:
                    csv_col_value_list.append(csv_col_value)
            else:
                csv_row_list.append('\r\n'.join(csv_col_value_list))

        else:
            for col in range(len(csv_row_list)):
                self._worksheet.write(self._row_counter, col, csv_row_list[col])
            else:
                self._row_counter += 1


def w2l_search--- This code section failed: ---

 L. 287         0  LOAD_CLOSURE             'scope'
                2  LOAD_CLOSURE             'search_attrs'
                4  BUILD_TUPLE_2         2 
                6  LOAD_CODE                <code_object page_appl_anchor>
                8  LOAD_STR                 'w2l_search.<locals>.page_appl_anchor'
               10  MAKE_FUNCTION_8          'closure'
               12  STORE_FAST               'page_appl_anchor'

 L. 321        14  LOAD_DEREF               'app'
               16  LOAD_ATTR                ldap_url
               18  LOAD_ATTR                scope
               20  STORE_DEREF              'scope'

 L. 322        22  LOAD_DEREF               'app'
               24  LOAD_ATTR                ldap_url
               26  LOAD_ATTR                filterstr
               28  STORE_FAST               'filterstr'

 L. 324        30  LOAD_DEREF               'app'
               32  LOAD_ATTR                form
               34  LOAD_METHOD              getInputValue
               36  LOAD_STR                 'search_submit'
               38  LOAD_STR                 'Search'
               40  BUILD_LIST_1          1 
               42  CALL_METHOD_2         2  ''
               44  LOAD_CONST               0
               46  BINARY_SUBSCR    
               48  STORE_FAST               'search_submit'

 L. 325        50  LOAD_DEREF               'app'
               52  LOAD_ATTR                form
               54  LOAD_METHOD              getInputValue
               56  LOAD_STR                 'searchform_mode'
               58  LOAD_STR                 'exp'
               60  BUILD_LIST_1          1 
               62  CALL_METHOD_2         2  ''
               64  LOAD_CONST               0
               66  BINARY_SUBSCR    
               68  STORE_FAST               'searchform_mode'

 L. 327        70  LOAD_FAST                'search_submit'
               72  LOAD_STR                 'Search'
               74  COMPARE_OP               !=
               76  POP_JUMP_IF_FALSE   112  'to 112'
               78  LOAD_FAST                'searchform_mode'
               80  LOAD_STR                 'adv'
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE   112  'to 112'

 L. 328        86  LOAD_GLOBAL              web2ldap
               88  LOAD_ATTR                app
               90  LOAD_ATTR                searchform
               92  LOAD_ATTR                w2l_searchform

 L. 329        94  LOAD_DEREF               'app'

 L. 330        96  LOAD_STR                 ''

 L. 331        98  LOAD_STR                 ''

 L. 332       100  LOAD_DEREF               'scope'

 L. 328       102  LOAD_CONST               ('Msg', 'filterstr', 'scope')
              104  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              106  POP_TOP          

 L. 334       108  LOAD_CONST               None
              110  RETURN_VALUE     
            112_0  COME_FROM            84  '84'
            112_1  COME_FROM            76  '76'

 L. 337       112  LOAD_DEREF               'app'
              114  LOAD_ATTR                form
              116  LOAD_ATTR                utf2display
              118  STORE_FAST               'utf2display'

 L. 339       120  LOAD_DEREF               'app'
              122  LOAD_ATTR                form
              124  LOAD_METHOD              getInputValue
              126  LOAD_STR                 'search_output'
              128  LOAD_STR                 'table'
              130  BUILD_LIST_1          1 
              132  CALL_METHOD_2         2  ''
              134  LOAD_CONST               0
              136  BINARY_SUBSCR    
              138  STORE_FAST               'search_output'

 L. 340       140  LOAD_DEREF               'app'
              142  LOAD_ATTR                form
              144  LOAD_METHOD              getInputValue
              146  LOAD_STR                 'search_opattrs'
              148  LOAD_STR                 'no'
              150  BUILD_LIST_1          1 
              152  CALL_METHOD_2         2  ''
              154  LOAD_CONST               0
              156  BINARY_SUBSCR    
              158  LOAD_STR                 'yes'
              160  COMPARE_OP               ==
              162  STORE_FAST               'search_opattrs'

 L. 341       164  LOAD_DEREF               'app'
              166  LOAD_ATTR                form
              168  LOAD_METHOD              getInputValue
              170  LOAD_STR                 'search_root'
              172  LOAD_DEREF               'app'
              174  LOAD_ATTR                dn
              176  BUILD_LIST_1          1 
              178  CALL_METHOD_2         2  ''
              180  LOAD_CONST               0
              182  BINARY_SUBSCR    
              184  STORE_FAST               'search_root'

 L. 343       186  LOAD_DEREF               'scope'
              188  LOAD_CONST               None
              190  COMPARE_OP               is
              192  POP_JUMP_IF_FALSE   200  'to 200'

 L. 344       194  LOAD_GLOBAL              ldap0
              196  LOAD_ATTR                SCOPE_SUBTREE
              198  STORE_DEREF              'scope'
            200_0  COME_FROM           192  '192'

 L. 346       200  LOAD_DEREF               'app'
              202  LOAD_ATTR                form
              204  LOAD_METHOD              getInputValue
              206  LOAD_STR                 'filterstr'
              208  LOAD_FAST                'filterstr'
              210  BUILD_LIST_1          1 
              212  CALL_METHOD_2         2  ''
              214  STORE_FAST               'search_filter'

 L. 348       216  LOAD_DEREF               'app'
              218  LOAD_ATTR                form
              220  LOAD_METHOD              getInputValue
              222  LOAD_STR                 'search_mode'
              224  LOAD_STR                 '(&%s)'
              226  BUILD_LIST_1          1 
              228  CALL_METHOD_2         2  ''
              230  LOAD_CONST               0
              232  BINARY_SUBSCR    
              234  STORE_FAST               'search_mode'

 L. 349       236  LOAD_DEREF               'app'
              238  LOAD_ATTR                form
              240  LOAD_METHOD              getInputValue
              242  LOAD_STR                 'search_option'
              244  BUILD_LIST_0          0 
              246  CALL_METHOD_2         2  ''
              248  STORE_FAST               'search_option'

 L. 350       250  LOAD_DEREF               'app'
              252  LOAD_ATTR                form
              254  LOAD_METHOD              getInputValue
              256  LOAD_STR                 'search_attr'
              258  BUILD_LIST_0          0 
              260  CALL_METHOD_2         2  ''
              262  STORE_FAST               'search_attr'

 L. 351       264  LOAD_DEREF               'app'
              266  LOAD_ATTR                form
              268  LOAD_METHOD              getInputValue
              270  LOAD_STR                 'search_mr'
              272  LOAD_CONST               None
              274  BUILD_LIST_1          1 
              276  LOAD_GLOBAL              len
              278  LOAD_FAST                'search_attr'
              280  CALL_FUNCTION_1       1  ''
              282  BINARY_MULTIPLY  
              284  CALL_METHOD_2         2  ''
              286  STORE_FAST               'search_mr'

 L. 352       288  LOAD_DEREF               'app'
              290  LOAD_ATTR                form
              292  LOAD_METHOD              getInputValue
              294  LOAD_STR                 'search_string'
              296  BUILD_LIST_0          0 
              298  CALL_METHOD_2         2  ''
              300  STORE_FAST               'search_string'

 L. 354       302  LOAD_GLOBAL              len
              304  LOAD_FAST                'search_option'
              306  CALL_FUNCTION_1       1  ''
              308  LOAD_GLOBAL              len
              310  LOAD_FAST                'search_attr'
              312  CALL_FUNCTION_1       1  ''
              314  DUP_TOP          
              316  ROT_THREE        
              318  COMPARE_OP               ==
          320_322  POP_JUMP_IF_FALSE   354  'to 354'
              324  LOAD_GLOBAL              len
              326  LOAD_FAST                'search_mr'
              328  CALL_FUNCTION_1       1  ''
              330  DUP_TOP          
              332  ROT_THREE        
              334  COMPARE_OP               ==
          336_338  POP_JUMP_IF_FALSE   354  'to 354'
              340  LOAD_GLOBAL              len
              342  LOAD_FAST                'search_string'
              344  CALL_FUNCTION_1       1  ''
              346  COMPARE_OP               ==
          348_350  POP_JUMP_IF_TRUE    370  'to 370'
              352  JUMP_FORWARD        356  'to 356'
            354_0  COME_FROM           336  '336'
            354_1  COME_FROM           320  '320'
              354  POP_TOP          
            356_0  COME_FROM           352  '352'

 L. 355       356  LOAD_GLOBAL              web2ldap
              358  LOAD_ATTR                app
              360  LOAD_ATTR                core
              362  LOAD_METHOD              ErrorExit
              364  LOAD_STR                 'Invalid search form data.'
              366  CALL_METHOD_1         1  ''
              368  RAISE_VARARGS_1       1  'exception instance'
            370_0  COME_FROM           348  '348'

 L. 358       370  LOAD_GLOBAL              range
              372  LOAD_GLOBAL              len
              374  LOAD_FAST                'search_attr'
              376  CALL_FUNCTION_1       1  ''
              378  CALL_FUNCTION_1       1  ''
              380  GET_ITER         
            382_0  COME_FROM           530  '530'
              382  FOR_ITER            584  'to 584'
              384  STORE_FAST               'i'

 L. 359       386  LOAD_FAST                'search_attr'
              388  LOAD_FAST                'i'
              390  BINARY_SUBSCR    
          392_394  POP_JUMP_IF_TRUE    400  'to 400'

 L. 361   396_398  JUMP_BACK           382  'to 382'
            400_0  COME_FROM           392  '392'

 L. 362       400  LOAD_FAST                'search_string'
              402  LOAD_FAST                'i'
              404  BINARY_SUBSCR    
              406  STORE_FAST               'search_av_string'

 L. 363       408  LOAD_STR                 '*'
              410  LOAD_FAST                'search_option'
              412  LOAD_FAST                'i'
              414  BINARY_SUBSCR    
              416  COMPARE_OP               not-in
          418_420  POP_JUMP_IF_FALSE   482  'to 482'

 L. 365       422  LOAD_GLOBAL              syntax_registry
              424  LOAD_ATTR                get_at

 L. 366       426  LOAD_DEREF               'app'

 L. 366       428  LOAD_DEREF               'app'
              430  LOAD_ATTR                dn

 L. 366       432  LOAD_DEREF               'app'
              434  LOAD_ATTR                schema

 L. 366       436  LOAD_FAST                'search_attr'
              438  LOAD_FAST                'i'
              440  BINARY_SUBSCR    

 L. 366       442  LOAD_CONST               None

 L. 366       444  LOAD_CONST               None

 L. 365       446  LOAD_CONST               ('entry',)
              448  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
              450  STORE_FAST               'attr_instance'

 L. 368       452  LOAD_FAST                'attr_instance'
              454  LOAD_METHOD              sanitize
              456  LOAD_FAST                'search_av_string'
              458  LOAD_METHOD              encode
              460  LOAD_DEREF               'app'
              462  LOAD_ATTR                ls
              464  LOAD_ATTR                charset
              466  CALL_METHOD_1         1  ''
              468  CALL_METHOD_1         1  ''
              470  LOAD_METHOD              decode
              472  LOAD_DEREF               'app'
              474  LOAD_ATTR                ls
              476  LOAD_ATTR                charset
              478  CALL_METHOD_1         1  ''
              480  STORE_FAST               'search_av_string'
            482_0  COME_FROM           418  '418'

 L. 369       482  LOAD_FAST                'search_mr'
              484  LOAD_FAST                'i'
              486  BINARY_SUBSCR    
          488_490  POP_JUMP_IF_FALSE   506  'to 506'

 L. 370       492  LOAD_STR                 ':%s:'
              494  LOAD_FAST                'search_mr'
              496  LOAD_FAST                'i'
              498  BINARY_SUBSCR    
              500  BINARY_MODULO    
              502  STORE_FAST               'search_mr_string'
              504  JUMP_FORWARD        510  'to 510'
            506_0  COME_FROM           488  '488'

 L. 372       506  LOAD_STR                 ''
              508  STORE_FAST               'search_mr_string'
            510_0  COME_FROM           504  '504'

 L. 373       510  LOAD_FAST                'search_av_string'
          512_514  POP_JUMP_IF_TRUE    534  'to 534'

 L. 374       516  LOAD_FAST                'search_option'
              518  LOAD_FAST                'i'
              520  BINARY_SUBSCR    
              522  LOAD_GLOBAL              SEARCH_OPT_ATTR_EXISTS
              524  LOAD_GLOBAL              SEARCH_OPT_ATTR_NOT_EXISTS
              526  BUILD_SET_2           2 
              528  COMPARE_OP               in

 L. 373   530_532  POP_JUMP_IF_FALSE   382  'to 382'
            534_0  COME_FROM           512  '512'

 L. 375       534  LOAD_FAST                'search_filter'
              536  LOAD_METHOD              append
              538  LOAD_FAST                'search_option'
              540  LOAD_FAST                'i'
              542  BINARY_SUBSCR    
              544  LOAD_ATTR                format

 L. 376       546  LOAD_STR                 ''
              548  LOAD_METHOD              join
              550  LOAD_FAST                'search_attr'
              552  LOAD_FAST                'i'
              554  BINARY_SUBSCR    
              556  LOAD_FAST                'search_mr_string'
              558  BUILD_TUPLE_2         2 
              560  CALL_METHOD_1         1  ''

 L. 377       562  LOAD_GLOBAL              ldap0
              564  LOAD_ATTR                filter
              566  LOAD_METHOD              escape_str
              568  LOAD_FAST                'search_av_string'
              570  CALL_METHOD_1         1  ''

 L. 375       572  LOAD_CONST               ('at', 'av')
              574  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              576  CALL_METHOD_1         1  ''
              578  POP_TOP          
          580_582  JUMP_BACK           382  'to 382'

 L. 381       584  LOAD_GLOBAL              list
              586  LOAD_GLOBAL              filter
              588  LOAD_CONST               None
              590  LOAD_FAST                'search_filter'
              592  CALL_FUNCTION_2       2  ''
              594  CALL_FUNCTION_1       1  ''
              596  STORE_FAST               'search_filter'

 L. 383       598  LOAD_FAST                'search_filter'
          600_602  POP_JUMP_IF_TRUE    630  'to 630'

 L. 384       604  LOAD_GLOBAL              web2ldap
              606  LOAD_ATTR                app
              608  LOAD_ATTR                searchform
              610  LOAD_ATTR                w2l_searchform

 L. 385       612  LOAD_DEREF               'app'

 L. 386       614  LOAD_STR                 'Empty search values.'

 L. 387       616  LOAD_STR                 ''

 L. 388       618  LOAD_DEREF               'scope'

 L. 384       620  LOAD_CONST               ('Msg', 'filterstr', 'scope')
              622  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              624  POP_TOP          

 L. 390       626  LOAD_CONST               None
              628  RETURN_VALUE     
            630_0  COME_FROM           600  '600'

 L. 391       630  LOAD_GLOBAL              len
              632  LOAD_FAST                'search_filter'
              634  CALL_FUNCTION_1       1  ''
              636  LOAD_CONST               1
              638  COMPARE_OP               ==
          640_642  POP_JUMP_IF_FALSE   654  'to 654'

 L. 392       644  LOAD_FAST                'search_filter'
              646  LOAD_CONST               0
              648  BINARY_SUBSCR    
              650  STORE_FAST               'filterstr'
              652  JUMP_FORWARD        682  'to 682'
            654_0  COME_FROM           640  '640'

 L. 393       654  LOAD_GLOBAL              len
              656  LOAD_FAST                'search_filter'
              658  CALL_FUNCTION_1       1  ''
              660  LOAD_CONST               1
              662  COMPARE_OP               >
          664_666  POP_JUMP_IF_FALSE   682  'to 682'

 L. 394       668  LOAD_FAST                'search_mode'
              670  LOAD_STR                 ''
              672  LOAD_METHOD              join
              674  LOAD_FAST                'search_filter'
              676  CALL_METHOD_1         1  ''
              678  BINARY_MODULO    
              680  STORE_FAST               'filterstr'
            682_0  COME_FROM           664  '664'
            682_1  COME_FROM           652  '652'

 L. 396       682  LOAD_GLOBAL              int
              684  LOAD_DEREF               'app'
              686  LOAD_ATTR                form
              688  LOAD_METHOD              getInputValue
              690  LOAD_STR                 'search_resminindex'
              692  LOAD_STR                 '0'
              694  BUILD_LIST_1          1 
              696  CALL_METHOD_2         2  ''
              698  LOAD_CONST               0
              700  BINARY_SUBSCR    
              702  CALL_FUNCTION_1       1  ''
              704  STORE_FAST               'search_resminindex'

 L. 397       706  LOAD_GLOBAL              int

 L. 398       708  LOAD_DEREF               'app'
              710  LOAD_ATTR                form
              712  LOAD_METHOD              getInputValue

 L. 399       714  LOAD_STR                 'search_resnumber'

 L. 400       716  LOAD_GLOBAL              str
              718  LOAD_DEREF               'app'
              720  LOAD_METHOD              cfg_param
              722  LOAD_STR                 'search_resultsperpage'
              724  LOAD_CONST               10
              726  CALL_METHOD_2         2  ''
              728  CALL_FUNCTION_1       1  ''
              730  BUILD_LIST_1          1 

 L. 398       732  CALL_METHOD_2         2  ''

 L. 401       734  LOAD_CONST               0

 L. 398       736  BINARY_SUBSCR    

 L. 397       738  CALL_FUNCTION_1       1  ''
              740  STORE_FAST               'search_resnumber'

 L. 404       742  LOAD_GLOBAL              int
              744  LOAD_DEREF               'app'
              746  LOAD_ATTR                form
              748  LOAD_METHOD              getInputValue
              750  LOAD_STR                 'search_lastmod'
              752  LOAD_CONST               -1
              754  BUILD_LIST_1          1 
              756  CALL_METHOD_2         2  ''
              758  LOAD_CONST               0
              760  BINARY_SUBSCR    
              762  CALL_FUNCTION_1       1  ''
              764  STORE_FAST               'search_lastmod'

 L. 405       766  LOAD_FAST                'search_lastmod'
              768  LOAD_CONST               0
              770  COMPARE_OP               >
          772_774  POP_JUMP_IF_FALSE   870  'to 870'

 L. 406       776  LOAD_GLOBAL              time
              778  LOAD_METHOD              strftime
              780  LOAD_STR                 '%Y%m%d%H%M%S'
              782  LOAD_GLOBAL              time
              784  LOAD_METHOD              gmtime
              786  LOAD_GLOBAL              time
              788  LOAD_METHOD              time
              790  CALL_METHOD_0         0  ''
              792  LOAD_FAST                'search_lastmod'
              794  BINARY_SUBTRACT  
              796  CALL_METHOD_1         1  ''
              798  CALL_METHOD_2         2  ''
              800  STORE_FAST               'timestamp_str'

 L. 407       802  LOAD_STR                 '1.2.840.113556.1.2.2'
              804  LOAD_DEREF               'app'
              806  LOAD_ATTR                schema
              808  LOAD_ATTR                sed
              810  LOAD_GLOBAL              AttributeType
              812  BINARY_SUBSCR    
              814  COMPARE_OP               in
          816_818  POP_JUMP_IF_FALSE   854  'to 854'

 L. 408       820  LOAD_STR                 '1.2.840.113556.1.2.3'
              822  LOAD_DEREF               'app'
              824  LOAD_ATTR                schema
              826  LOAD_ATTR                sed
              828  LOAD_GLOBAL              AttributeType
              830  BINARY_SUBSCR    
              832  COMPARE_OP               in

 L. 407   834_836  POP_JUMP_IF_FALSE   854  'to 854'

 L. 410       838  LOAD_STR                 '(&(|(whenCreated>=%s.0Z)(whenChanged>=%s.0Z))%s)'

 L. 411       840  LOAD_FAST                'timestamp_str'

 L. 411       842  LOAD_FAST                'timestamp_str'

 L. 411       844  LOAD_FAST                'filterstr'

 L. 410       846  BUILD_TUPLE_3         3 
              848  BINARY_MODULO    
              850  STORE_FAST               'filterstr2'
              852  JUMP_FORWARD        868  'to 868'
            854_0  COME_FROM           834  '834'
            854_1  COME_FROM           816  '816'

 L. 415       854  LOAD_STR                 '(&(|(createTimestamp>=%sZ)(modifyTimestamp>=%sZ))%s)'

 L. 416       856  LOAD_FAST                'timestamp_str'

 L. 416       858  LOAD_FAST                'timestamp_str'

 L. 416       860  LOAD_FAST                'filterstr'

 L. 415       862  BUILD_TUPLE_3         3 
              864  BINARY_MODULO    
              866  STORE_FAST               'filterstr2'
            868_0  COME_FROM           852  '852'
              868  JUMP_FORWARD        874  'to 874'
            870_0  COME_FROM           772  '772'

 L. 419       870  LOAD_FAST                'filterstr'
              872  STORE_FAST               'filterstr2'
            874_0  COME_FROM           868  '868'

 L. 421       874  LOAD_DEREF               'app'
              876  LOAD_METHOD              cfg_param
              878  LOAD_STR                 'requested_attrs'
              880  BUILD_LIST_0          0 
              882  CALL_METHOD_2         2  ''
              884  STORE_FAST               'requested_attrs'

 L. 423       886  LOAD_LISTCOMP            '<code_object <listcomp>>'
              888  LOAD_STR                 'w2l_search.<locals>.<listcomp>'
              890  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'

 L. 425       892  LOAD_DEREF               'app'
              894  LOAD_ATTR                form
              896  LOAD_METHOD              getInputValue

 L. 426       898  LOAD_STR                 'search_attrs'

 L. 427       900  LOAD_STR                 ','
              902  LOAD_METHOD              join
              904  LOAD_DEREF               'app'
              906  LOAD_ATTR                ldap_url
              908  LOAD_ATTR                attrs
          910_912  JUMP_IF_TRUE_OR_POP   916  'to 916'
              914  BUILD_LIST_0          0 
            916_0  COME_FROM           910  '910'
              916  CALL_METHOD_1         1  ''
              918  BUILD_LIST_1          1 

 L. 425       920  CALL_METHOD_2         2  ''

 L. 428       922  LOAD_CONST               0

 L. 425       924  BINARY_SUBSCR    
              926  LOAD_METHOD              split

 L. 428       928  LOAD_STR                 ','

 L. 425       930  CALL_METHOD_1         1  ''

 L. 423       932  GET_ITER         
              934  CALL_FUNCTION_1       1  ''
              936  STORE_DEREF              'search_attrs'

 L. 432       938  LOAD_GLOBAL              ldap0
              940  LOAD_ATTR                schema
              942  LOAD_ATTR                models
              944  LOAD_METHOD              SchemaElementOIDSet
              946  LOAD_DEREF               'app'
              948  LOAD_ATTR                schema
              950  LOAD_GLOBAL              AttributeType
              952  LOAD_DEREF               'search_attrs'
              954  CALL_METHOD_3         3  ''
              956  STORE_FAST               'search_attr_set'

 L. 433       958  LOAD_FAST                'search_attr_set'
              960  LOAD_ATTR                names
              962  STORE_DEREF              'search_attrs'

 L. 435       964  LOAD_DEREF               'app'
              966  LOAD_ATTR                ls
              968  LOAD_ATTR                ldapUrl
              970  LOAD_FAST                'search_root'
          972_974  JUMP_IF_TRUE_OR_POP   984  'to 984'
              976  LOAD_GLOBAL              str
              978  LOAD_DEREF               'app'
              980  LOAD_ATTR                naming_context
              982  CALL_FUNCTION_1       1  ''
            984_0  COME_FROM           972  '972'
              984  LOAD_CONST               ('dn',)
              986  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              988  STORE_FAST               'search_ldap_url'

 L. 436       990  LOAD_FAST                'filterstr2'
              992  LOAD_FAST                'search_ldap_url'
              994  STORE_ATTR               filterstr

 L. 437       996  LOAD_DEREF               'scope'
              998  LOAD_FAST                'search_ldap_url'
             1000  STORE_ATTR               scope

 L. 438      1002  LOAD_DEREF               'search_attrs'
             1004  LOAD_FAST                'search_ldap_url'
             1006  STORE_ATTR               attrs

 L. 440      1008  LOAD_FAST                'search_ldap_url'
             1010  LOAD_METHOD              ldapsearch_cmd
             1012  CALL_METHOD_0         0  ''
             1014  STORE_FAST               'ldap_search_command'

 L. 442      1016  LOAD_GLOBAL              ldap0
             1018  LOAD_ATTR                schema
             1020  LOAD_ATTR                models
             1022  LOAD_METHOD              SchemaElementOIDSet
             1024  LOAD_DEREF               'app'
             1026  LOAD_ATTR                schema
             1028  LOAD_GLOBAL              AttributeType
             1030  LOAD_DEREF               'search_attrs'
             1032  CALL_METHOD_3         3  ''
             1034  STORE_FAST               'read_attr_set'

 L. 443      1036  LOAD_FAST                'search_output'
             1038  LOAD_CONST               {'table', 'print'}
             1040  COMPARE_OP               in
         1042_1044  POP_JUMP_IF_FALSE  1056  'to 1056'

 L. 444      1046  LOAD_FAST                'read_attr_set'
             1048  LOAD_METHOD              add
             1050  LOAD_STR                 'objectClass'
             1052  CALL_METHOD_1         1  ''
             1054  POP_TOP          
           1056_0  COME_FROM          1042  '1042'

 L. 446      1056  LOAD_FAST                'search_output'
             1058  LOAD_STR                 'print'
             1060  COMPARE_OP               ==
         1062_1064  POP_JUMP_IF_FALSE  1236  'to 1236'

 L. 447      1066  LOAD_DEREF               'app'
             1068  LOAD_METHOD              cfg_param
             1070  LOAD_STR                 'print_template'
             1072  LOAD_CONST               None
             1074  CALL_METHOD_2         2  ''
             1076  STORE_FAST               'print_template_filenames_dict'

 L. 448      1078  LOAD_FAST                'print_template_filenames_dict'
             1080  LOAD_CONST               None
             1082  COMPARE_OP               is
         1084_1086  POP_JUMP_IF_FALSE  1102  'to 1102'

 L. 449      1088  LOAD_GLOBAL              web2ldap
             1090  LOAD_ATTR                app
             1092  LOAD_ATTR                core
             1094  LOAD_METHOD              ErrorExit
             1096  LOAD_STR                 'No templates for printing defined.'
             1098  CALL_METHOD_1         1  ''
             1100  RAISE_VARARGS_1       1  'exception instance'
           1102_0  COME_FROM          1084  '1084'

 L. 450      1102  LOAD_GLOBAL              CaseinsensitiveStringKeyDict
             1104  CALL_FUNCTION_0       0  ''
             1106  STORE_FAST               'print_template_str_dict'

 L. 451      1108  LOAD_FAST                'print_template_filenames_dict'
             1110  LOAD_METHOD              keys
             1112  CALL_METHOD_0         0  ''
             1114  GET_ITER         
             1116  FOR_ITER           1210  'to 1210'
             1118  STORE_FAST               'oc'

 L. 452      1120  SETUP_FINALLY      1164  'to 1164'

 L. 453      1122  LOAD_GLOBAL              open
             1124  LOAD_FAST                'print_template_filenames_dict'
             1126  LOAD_FAST                'oc'
             1128  BINARY_SUBSCR    
             1130  LOAD_STR                 'r'
             1132  CALL_FUNCTION_2       2  ''
             1134  SETUP_WITH         1154  'to 1154'
             1136  STORE_FAST               'template_file'

 L. 454      1138  LOAD_FAST                'template_file'
             1140  LOAD_METHOD              read
             1142  CALL_METHOD_0         0  ''
             1144  LOAD_FAST                'print_template_str_dict'
             1146  LOAD_FAST                'oc'
             1148  STORE_SUBSCR     
             1150  POP_BLOCK        
             1152  BEGIN_FINALLY    
           1154_0  COME_FROM_WITH     1134  '1134'
             1154  WITH_CLEANUP_START
             1156  WITH_CLEANUP_FINISH
             1158  END_FINALLY      
             1160  POP_BLOCK        
             1162  JUMP_FORWARD       1186  'to 1186'
           1164_0  COME_FROM_FINALLY  1120  '1120'

 L. 455      1164  DUP_TOP          
             1166  LOAD_GLOBAL              IOError
             1168  COMPARE_OP               exception-match
         1170_1172  POP_JUMP_IF_FALSE  1184  'to 1184'
             1174  POP_TOP          
             1176  POP_TOP          
             1178  POP_TOP          

 L. 456      1180  POP_EXCEPT       
             1182  JUMP_BACK          1116  'to 1116'
           1184_0  COME_FROM          1170  '1170'
             1184  END_FINALLY      
           1186_0  COME_FROM          1162  '1162'

 L. 458      1186  LOAD_FAST                'read_attr_set'
             1188  LOAD_METHOD              update
             1190  LOAD_GLOBAL              GrabKeys
             1192  LOAD_FAST                'print_template_str_dict'
             1194  LOAD_FAST                'oc'
             1196  BINARY_SUBSCR    
             1198  CALL_FUNCTION_1       1  ''
             1200  LOAD_ATTR                keys
             1202  CALL_METHOD_1         1  ''
             1204  POP_TOP          
         1206_1208  JUMP_BACK          1116  'to 1116'

 L. 459      1210  LOAD_FAST                'read_attr_set'
             1212  LOAD_ATTR                names
             1214  STORE_FAST               'read_attrs'

 L. 460      1216  LOAD_GLOBAL              PrintableHTMLWriter
             1218  LOAD_DEREF               'app'
             1220  LOAD_FAST                'search_root'
             1222  LOAD_DEREF               'app'
             1224  LOAD_ATTR                schema
             1226  LOAD_FAST                'print_template_str_dict'
             1228  CALL_FUNCTION_4       4  ''
             1230  STORE_FAST               'result_handler'
         1232_1234  JUMP_FORWARD       1720  'to 1720'
           1236_0  COME_FROM          1062  '1062'

 L. 462      1236  LOAD_FAST                'search_output'
             1238  LOAD_CONST               {'raw', 'table'}
             1240  COMPARE_OP               in
         1242_1244  POP_JUMP_IF_FALSE  1426  'to 1426'

 L. 464      1246  LOAD_GLOBAL              ldap0
             1248  LOAD_ATTR                cidict
             1250  LOAD_METHOD              CIDict
             1252  LOAD_DEREF               'app'
             1254  LOAD_METHOD              cfg_param
             1256  LOAD_STR                 'search_tdtemplate'
             1258  BUILD_MAP_0           0 
             1260  CALL_METHOD_2         2  ''
             1262  CALL_METHOD_1         1  ''
             1264  STORE_FAST               'search_tdtemplate'

 L. 465      1266  LOAD_FAST                'search_tdtemplate'
             1268  LOAD_METHOD              keys
             1270  CALL_METHOD_0         0  ''
             1272  STORE_FAST               'search_tdtemplate_keys'

 L. 466      1274  LOAD_GLOBAL              ldap0
             1276  LOAD_ATTR                cidict
             1278  LOAD_METHOD              CIDict
             1280  CALL_METHOD_0         0  ''
             1282  STORE_FAST               'search_tdtemplate_attrs_lower'

 L. 467      1284  LOAD_FAST                'search_tdtemplate_keys'
             1286  GET_ITER         
             1288  FOR_ITER           1314  'to 1314'
             1290  STORE_FAST               'oc'

 L. 468      1292  LOAD_GLOBAL              GrabKeys
             1294  LOAD_FAST                'search_tdtemplate'
             1296  LOAD_FAST                'oc'
             1298  BINARY_SUBSCR    
             1300  CALL_FUNCTION_1       1  ''
             1302  LOAD_ATTR                keys
             1304  LOAD_FAST                'search_tdtemplate_attrs_lower'
             1306  LOAD_FAST                'oc'
             1308  STORE_SUBSCR     
         1310_1312  JUMP_BACK          1288  'to 1288'

 L. 472      1314  LOAD_FAST                'read_attr_set'
             1316  LOAD_METHOD              update

 L. 473      1318  LOAD_STR                 'subschemaSubentry'

 L. 473      1320  LOAD_STR                 'displayName'

 L. 473      1322  LOAD_STR                 'description'

 L. 473      1324  LOAD_STR                 'structuralObjectClass'

 L. 474      1326  LOAD_STR                 'hasSubordinates'

 L. 474      1328  LOAD_STR                 'subordinateCount'

 L. 475      1330  LOAD_STR                 'numSubordinates'

 L. 476      1332  LOAD_STR                 'numAllSubordinates'

 L. 477      1334  LOAD_STR                 'countImmSubordinates'

 L. 477      1336  LOAD_STR                 'countTotSubordinates'

 L. 478      1338  LOAD_STR                 'msDS-Approx-Immed-Subordinates'

 L. 472      1340  BUILD_LIST_11        11 
             1342  CALL_METHOD_1         1  ''
             1344  POP_TOP          

 L. 482      1346  LOAD_FAST                'search_output'
             1348  LOAD_STR                 'table'
             1350  COMPARE_OP               ==
         1352_1354  POP_JUMP_IF_FALSE  1388  'to 1388'

 L. 483      1356  LOAD_FAST                'search_tdtemplate_keys'
             1358  GET_ITER         
             1360  FOR_ITER           1388  'to 1388'
             1362  STORE_FAST               'oc'

 L. 484      1364  LOAD_FAST                'read_attr_set'
             1366  LOAD_METHOD              update
             1368  LOAD_GLOBAL              GrabKeys
             1370  LOAD_FAST                'search_tdtemplate'
             1372  LOAD_FAST                'oc'
             1374  BINARY_SUBSCR    
             1376  CALL_FUNCTION_1       1  ''
             1378  LOAD_ATTR                keys
             1380  CALL_METHOD_1         1  ''
             1382  POP_TOP          
         1384_1386  JUMP_BACK          1360  'to 1360'
           1388_0  COME_FROM          1352  '1352'

 L. 485      1388  LOAD_FAST                'read_attr_set'
             1390  LOAD_METHOD              discard
             1392  LOAD_STR                 'entryDN'
             1394  CALL_METHOD_1         1  ''
             1396  POP_TOP          

 L. 486      1398  LOAD_FAST                'read_attr_set'
             1400  LOAD_ATTR                names
             1402  STORE_FAST               'read_attrs'

 L. 489      1404  LOAD_GLOBAL              web2ldap
             1406  LOAD_ATTR                ldaputil
             1408  LOAD_ATTR                asynch
             1410  LOAD_METHOD              List
             1412  LOAD_DEREF               'app'
             1414  LOAD_ATTR                ls
             1416  LOAD_ATTR                l
             1418  CALL_METHOD_1         1  ''
             1420  STORE_FAST               'result_handler'
         1422_1424  JUMP_FORWARD       1720  'to 1720'
           1426_0  COME_FROM          1242  '1242'

 L. 491      1426  LOAD_FAST                'search_output'
             1428  LOAD_CONST               {'ldif', 'ldif1'}
             1430  COMPARE_OP               in
         1432_1434  POP_JUMP_IF_FALSE  1560  'to 1560'

 L. 494      1436  LOAD_DEREF               'search_attrs'
         1438_1440  JUMP_IF_TRUE_OR_POP  1474  'to 1474'

 L. 495      1442  LOAD_CONST               ('*',)
             1444  LOAD_CONST               ('*', '+')
             1446  LOAD_CONST               (False, True)
             1448  BUILD_CONST_KEY_MAP_2     2 
             1450  LOAD_DEREF               'app'
             1452  LOAD_ATTR                ls
             1454  LOAD_ATTR                supportsAllOpAttr
         1456_1458  JUMP_IF_FALSE_OR_POP  1462  'to 1462'
             1460  LOAD_FAST                'search_opattrs'
           1462_0  COME_FROM          1456  '1456'
             1462  BINARY_SUBSCR    
             1464  LOAD_FAST                'requested_attrs'
             1466  BINARY_ADD       

 L. 494  1468_1470  JUMP_IF_TRUE_OR_POP  1474  'to 1474'

 L. 496      1472  LOAD_CONST               None
           1474_0  COME_FROM          1468  '1468'
           1474_1  COME_FROM          1438  '1438'

 L. 493      1474  STORE_FAST               'read_attrs'

 L. 498      1476  LOAD_GLOBAL              LDIFWriter
             1478  LOAD_DEREF               'app'
             1480  LOAD_ATTR                ls
             1482  LOAD_ATTR                l
             1484  LOAD_GLOBAL              WSGIBytesWrapper
             1486  LOAD_DEREF               'app'
             1488  LOAD_ATTR                outf
             1490  CALL_FUNCTION_1       1  ''
             1492  CALL_FUNCTION_2       2  ''
             1494  STORE_FAST               'result_handler'

 L. 499      1496  LOAD_FAST                'search_output'
             1498  LOAD_STR                 'ldif1'
             1500  COMPARE_OP               ==
         1502_1504  POP_JUMP_IF_FALSE  1720  'to 1720'

 L. 500      1506  LOAD_GLOBAL              LDIF1_HEADER

 L. 501      1508  LOAD_GLOBAL              web2ldap
             1510  LOAD_ATTR                __about__
             1512  LOAD_ATTR                __version__

 L. 502      1514  LOAD_GLOBAL              time
             1516  LOAD_METHOD              strftime

 L. 503      1518  LOAD_STR                 '%A, %Y-%m-%d %H:%M:%S GMT'

 L. 504      1520  LOAD_GLOBAL              time
             1522  LOAD_METHOD              gmtime
             1524  LOAD_GLOBAL              time
             1526  LOAD_METHOD              time
             1528  CALL_METHOD_0         0  ''
             1530  CALL_METHOD_1         1  ''

 L. 502      1532  CALL_METHOD_2         2  ''

 L. 506      1534  LOAD_GLOBAL              repr
             1536  LOAD_DEREF               'app'
             1538  LOAD_ATTR                ls
             1540  LOAD_ATTR                who
             1542  CALL_FUNCTION_1       1  ''

 L. 507      1544  LOAD_GLOBAL              str
             1546  LOAD_FAST                'search_ldap_url'
             1548  CALL_FUNCTION_1       1  ''

 L. 500      1550  BUILD_TUPLE_4         4 
             1552  BINARY_MODULO    
             1554  LOAD_FAST                'result_handler'
             1556  STORE_ATTR               header
             1558  JUMP_FORWARD       1720  'to 1720'
           1560_0  COME_FROM          1432  '1432'

 L. 510      1560  LOAD_FAST                'search_output'
             1562  LOAD_CONST               {'csv', 'excel'}
             1564  COMPARE_OP               in
         1566_1568  POP_JUMP_IF_FALSE  1720  'to 1720'

 L. 512      1570  LOAD_LISTCOMP            '<code_object <listcomp>>'
             1572  LOAD_STR                 'w2l_search.<locals>.<listcomp>'
             1574  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             1576  LOAD_DEREF               'search_attrs'
             1578  GET_ITER         
             1580  CALL_FUNCTION_1       1  ''
             1582  STORE_FAST               'read_attrs'

 L. 513      1584  LOAD_FAST                'read_attrs'
         1586_1588  POP_JUMP_IF_TRUE   1634  'to 1634'

 L. 514      1590  LOAD_FAST                'searchform_mode'
             1592  LOAD_STR                 'base'
             1594  COMPARE_OP               ==
         1596_1598  POP_JUMP_IF_FALSE  1604  'to 1604'

 L. 515      1600  LOAD_STR                 'adv'
             1602  STORE_FAST               'searchform_mode'
           1604_0  COME_FROM          1596  '1596'

 L. 516      1604  LOAD_GLOBAL              web2ldap
             1606  LOAD_ATTR                app
             1608  LOAD_ATTR                searchform
             1610  LOAD_ATTR                w2l_searchform

 L. 517      1612  LOAD_DEREF               'app'

 L. 518      1614  LOAD_STR                 'For table-structured export you have to define the attributes to be read!'

 L. 519      1616  LOAD_FAST                'filterstr'

 L. 520      1618  LOAD_DEREF               'scope'

 L. 521      1620  LOAD_FAST                'search_root'

 L. 522      1622  LOAD_FAST                'searchform_mode'

 L. 516      1624  LOAD_CONST               ('Msg', 'filterstr', 'scope', 'search_root', 'searchform_mode')
             1626  CALL_FUNCTION_KW_6     6  '6 total positional and keyword args'
             1628  POP_TOP          

 L. 524      1630  LOAD_CONST               None
             1632  RETURN_VALUE     
           1634_0  COME_FROM          1586  '1586'

 L. 525      1634  LOAD_FAST                'search_output'
             1636  LOAD_STR                 'csv'
             1638  COMPARE_OP               ==
         1640_1642  POP_JUMP_IF_FALSE  1676  'to 1676'

 L. 526      1644  LOAD_GLOBAL              CSVWriter
             1646  LOAD_DEREF               'app'
             1648  LOAD_ATTR                ls
             1650  LOAD_ATTR                l
             1652  LOAD_DEREF               'app'
             1654  LOAD_ATTR                outf
             1656  LOAD_DEREF               'app'
             1658  LOAD_ATTR                schema
             1660  LOAD_FAST                'read_attrs'
             1662  LOAD_DEREF               'app'
             1664  LOAD_ATTR                ls
             1666  LOAD_ATTR                charset
             1668  LOAD_CONST               ('ldap_charset',)
             1670  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1672  STORE_FAST               'result_handler'
             1674  JUMP_FORWARD       1720  'to 1720'
           1676_0  COME_FROM          1640  '1640'

 L. 527      1676  LOAD_FAST                'search_output'
             1678  LOAD_STR                 'excel'
             1680  COMPARE_OP               ==
         1682_1684  POP_JUMP_IF_FALSE  1720  'to 1720'

 L. 528      1686  LOAD_GLOBAL              ExcelWriter
             1688  LOAD_DEREF               'app'
             1690  LOAD_ATTR                ls
             1692  LOAD_ATTR                l
             1694  LOAD_GLOBAL              WSGIBytesWrapper
             1696  LOAD_DEREF               'app'
             1698  LOAD_ATTR                outf
             1700  CALL_FUNCTION_1       1  ''
             1702  LOAD_DEREF               'app'
             1704  LOAD_ATTR                schema
             1706  LOAD_FAST                'read_attrs'
             1708  LOAD_DEREF               'app'
             1710  LOAD_ATTR                ls
             1712  LOAD_ATTR                charset
             1714  LOAD_CONST               ('ldap_charset',)
             1716  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1718  STORE_FAST               'result_handler'
           1720_0  COME_FROM          1682  '1682'
           1720_1  COME_FROM          1674  '1674'
           1720_2  COME_FROM          1566  '1566'
           1720_3  COME_FROM          1558  '1558'
           1720_4  COME_FROM          1502  '1502'
           1720_5  COME_FROM          1422  '1422'
           1720_6  COME_FROM          1232  '1232'

 L. 530      1720  LOAD_FAST                'search_resnumber'
         1722_1724  POP_JUMP_IF_FALSE  1736  'to 1736'

 L. 531      1726  LOAD_FAST                'search_resminindex'
             1728  LOAD_FAST                'search_resnumber'
             1730  BINARY_ADD       
             1732  STORE_FAST               'search_size_limit'
             1734  JUMP_FORWARD       1740  'to 1740'
           1736_0  COME_FROM          1722  '1722'

 L. 533      1736  LOAD_CONST               -1
             1738  STORE_FAST               'search_size_limit'
           1740_0  COME_FROM          1734  '1734'

 L. 535      1740  SETUP_FINALLY      1772  'to 1772'

 L. 537      1742  LOAD_FAST                'result_handler'
             1744  LOAD_ATTR                start_search

 L. 538      1746  LOAD_FAST                'search_root'

 L. 539      1748  LOAD_DEREF               'scope'

 L. 540      1750  LOAD_FAST                'filterstr2'

 L. 541      1752  LOAD_FAST                'read_attrs'
         1754_1756  JUMP_IF_TRUE_OR_POP  1760  'to 1760'
             1758  LOAD_CONST               None
           1760_0  COME_FROM          1754  '1754'

 L. 542      1760  LOAD_FAST                'search_size_limit'

 L. 537      1762  LOAD_CONST               ('attrList', 'sizelimit')
             1764  CALL_FUNCTION_KW_5     5  '5 total positional and keyword args'
             1766  POP_TOP          
             1768  POP_BLOCK        
             1770  JUMP_FORWARD       1912  'to 1912'
           1772_0  COME_FROM_FINALLY  1740  '1740'

 L. 544      1772  DUP_TOP          

 L. 545      1774  LOAD_GLOBAL              ldap0
             1776  LOAD_ATTR                FILTER_ERROR

 L. 546      1778  LOAD_GLOBAL              ldap0
             1780  LOAD_ATTR                INAPPROPRIATE_MATCHING

 L. 544      1782  BUILD_TUPLE_2         2 
             1784  COMPARE_OP               exception-match
         1786_1788  POP_JUMP_IF_FALSE  1862  'to 1862'
             1790  POP_TOP          
             1792  STORE_FAST               'e'
             1794  POP_TOP          
             1796  SETUP_FINALLY      1850  'to 1850'

 L. 549      1798  LOAD_GLOBAL              web2ldap
             1800  LOAD_ATTR                app
             1802  LOAD_ATTR                searchform
             1804  LOAD_ATTR                w2l_searchform

 L. 550      1806  LOAD_DEREF               'app'

 L. 551      1808  LOAD_STR                 ' '
             1810  LOAD_METHOD              join

 L. 552      1812  LOAD_DEREF               'app'
             1814  LOAD_METHOD              ldap_error_msg
             1816  LOAD_FAST                'e'
             1818  CALL_METHOD_1         1  ''

 L. 553      1820  LOAD_FAST                'utf2display'
             1822  LOAD_FAST                'filterstr2'
             1824  CALL_FUNCTION_1       1  ''

 L. 551      1826  BUILD_TUPLE_2         2 
             1828  CALL_METHOD_1         1  ''

 L. 555      1830  LOAD_FAST                'filterstr'

 L. 556      1832  LOAD_DEREF               'scope'

 L. 549      1834  LOAD_CONST               ('Msg', 'filterstr', 'scope')
             1836  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             1838  POP_TOP          

 L. 558      1840  POP_BLOCK        
             1842  POP_EXCEPT       
             1844  CALL_FINALLY       1850  'to 1850'
             1846  LOAD_CONST               None
             1848  RETURN_VALUE     
           1850_0  COME_FROM          1844  '1844'
           1850_1  COME_FROM_FINALLY  1796  '1796'
             1850  LOAD_CONST               None
             1852  STORE_FAST               'e'
             1854  DELETE_FAST              'e'
             1856  END_FINALLY      
             1858  POP_EXCEPT       
             1860  JUMP_FORWARD       1912  'to 1912'
           1862_0  COME_FROM          1786  '1786'

 L. 559      1862  DUP_TOP          
             1864  LOAD_GLOBAL              ldap0
             1866  LOAD_ATTR                NO_SUCH_OBJECT
             1868  COMPARE_OP               exception-match
         1870_1872  POP_JUMP_IF_FALSE  1910  'to 1910'
             1874  POP_TOP          
             1876  STORE_FAST               'e'
             1878  POP_TOP          
             1880  SETUP_FINALLY      1898  'to 1898'

 L. 560      1882  LOAD_DEREF               'app'
             1884  LOAD_ATTR                dn
         1886_1888  POP_JUMP_IF_FALSE  1894  'to 1894'

 L. 561      1890  LOAD_FAST                'e'
             1892  RAISE_VARARGS_1       1  'exception instance'
           1894_0  COME_FROM          1886  '1886'
             1894  POP_BLOCK        
             1896  BEGIN_FINALLY    
           1898_0  COME_FROM_FINALLY  1880  '1880'
             1898  LOAD_CONST               None
             1900  STORE_FAST               'e'
             1902  DELETE_FAST              'e'
             1904  END_FINALLY      
             1906  POP_EXCEPT       
             1908  JUMP_FORWARD       1912  'to 1912'
           1910_0  COME_FROM          1870  '1870'
             1910  END_FINALLY      
           1912_0  COME_FROM          1908  '1908'
           1912_1  COME_FROM          1860  '1860'
           1912_2  COME_FROM          1770  '1770'

 L. 563      1912  LOAD_FAST                'search_output'
             1914  LOAD_CONST               {'raw', 'table'}
             1916  COMPARE_OP               in
         1918_1920  POP_JUMP_IF_FALSE  4800  'to 4800'

 L. 565      1922  LOAD_STR                 ''
             1924  STORE_FAST               'SearchWarningMsg'

 L. 566      1926  LOAD_STR                 ''
             1928  STORE_FAST               'max_result_msg'

 L. 567      1930  LOAD_CONST               (None, None)
             1932  UNPACK_SEQUENCE_2     2 
             1934  STORE_FAST               'num_all_search_results'
             1936  STORE_FAST               'num_all_search_continuations'

 L. 568      1938  LOAD_CONST               None
             1940  STORE_FAST               'num_result_all'

 L. 569      1942  LOAD_CONST               0
             1944  STORE_FAST               'partial_results'

 L. 571      1946  SETUP_FINALLY      1978  'to 1978'

 L. 572      1948  LOAD_FAST                'result_handler'
             1950  LOAD_METHOD              process_results

 L. 573      1952  LOAD_FAST                'search_resminindex'

 L. 573      1954  LOAD_FAST                'search_resnumber'
             1956  LOAD_GLOBAL              int
             1958  LOAD_FAST                'search_resnumber'
             1960  LOAD_CONST               0
             1962  COMPARE_OP               >
             1964  CALL_FUNCTION_1       1  ''
             1966  BINARY_ADD       

 L. 572      1968  CALL_METHOD_2         2  ''
             1970  POP_TOP          
             1972  POP_BLOCK        
         1974_1976  JUMP_FORWARD       2358  'to 2358'
           1978_0  COME_FROM_FINALLY  1946  '1946'

 L. 575      1978  DUP_TOP          
             1980  LOAD_GLOBAL              ldap0
             1982  LOAD_ATTR                SIZELIMIT_EXCEEDED
             1984  LOAD_GLOBAL              ldap0
             1986  LOAD_ATTR                ADMINLIMIT_EXCEEDED
             1988  BUILD_TUPLE_2         2 
             1990  COMPARE_OP               exception-match
         1992_1994  POP_JUMP_IF_FALSE  2176  'to 2176'
             1996  POP_TOP          
             1998  STORE_FAST               'e'
             2000  POP_TOP          
             2002  SETUP_FINALLY      2164  'to 2164'

 L. 576      2004  LOAD_FAST                'search_size_limit'
             2006  LOAD_CONST               0
             2008  COMPARE_OP               <
         2010_2012  POP_JUMP_IF_TRUE   2026  'to 2026'
             2014  LOAD_FAST                'result_handler'
             2016  LOAD_ATTR                endResultBreak
             2018  LOAD_FAST                'search_size_limit'
             2020  COMPARE_OP               <
         2022_2024  POP_JUMP_IF_FALSE  2040  'to 2040'
           2026_0  COME_FROM          2010  '2010'

 L. 577      2026  LOAD_DEREF               'app'
             2028  LOAD_ATTR                ldap_error_msg
             2030  LOAD_FAST                'e'
             2032  LOAD_GLOBAL              LDAPERROR_SIZELIMIT_MSG
             2034  LOAD_CONST               ('template',)
             2036  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2038  STORE_FAST               'SearchWarningMsg'
           2040_0  COME_FROM          2022  '2022'

 L. 578      2040  LOAD_CONST               1
             2042  STORE_FAST               'partial_results'

 L. 579      2044  LOAD_FAST                'result_handler'
             2046  LOAD_ATTR                endResultBreak
             2048  STORE_FAST               'resind'

 L. 582      2050  LOAD_GLOBAL              SearchNoOpControl
             2052  LOAD_ATTR                controlType
             2054  LOAD_DEREF               'app'
             2056  LOAD_ATTR                ls
             2058  LOAD_ATTR                supportedControl
             2060  COMPARE_OP               in
         2062_2064  POP_JUMP_IF_FALSE  2160  'to 2160'

 L. 583      2066  SETUP_FINALLY      2138  'to 2138'

 L. 584      2068  LOAD_DEREF               'app'
             2070  LOAD_ATTR                ls
             2072  LOAD_ATTR                l
             2074  LOAD_ATTR                noop_search

 L. 585      2076  LOAD_FAST                'search_root'

 L. 586      2078  LOAD_DEREF               'scope'

 L. 587      2080  LOAD_FAST                'filterstr2'

 L. 588      2082  LOAD_GLOBAL              SEARCH_NOOP_TIMEOUT

 L. 584      2084  LOAD_CONST               ('filterstr', 'timeout')
             2086  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2088  UNPACK_SEQUENCE_2     2 
             2090  STORE_FAST               'num_all_search_results'
             2092  STORE_FAST               'num_all_search_continuations'

 L. 590      2094  LOAD_FAST                'num_all_search_results'
             2096  LOAD_CONST               None
             2098  COMPARE_OP               is-not
         2100_2102  POP_JUMP_IF_FALSE  2134  'to 2134'
             2104  LOAD_FAST                'num_all_search_continuations'
             2106  LOAD_CONST               None
             2108  COMPARE_OP               is-not
         2110_2112  POP_JUMP_IF_FALSE  2134  'to 2134'

 L. 591      2114  LOAD_FAST                'num_all_search_results'
             2116  LOAD_FAST                'num_all_search_continuations'
             2118  BINARY_ADD       
             2120  STORE_FAST               'num_result_all'

 L. 592      2122  LOAD_STR                 '(of %d / %d) '
             2124  LOAD_FAST                'num_all_search_results'
             2126  LOAD_FAST                'num_all_search_continuations'
             2128  BUILD_TUPLE_2         2 
             2130  BINARY_MODULO    
             2132  STORE_FAST               'max_result_msg'
           2134_0  COME_FROM          2110  '2110'
           2134_1  COME_FROM          2100  '2100'
             2134  POP_BLOCK        
             2136  JUMP_FORWARD       2160  'to 2160'
           2138_0  COME_FROM_FINALLY  2066  '2066'

 L. 593      2138  DUP_TOP          
             2140  LOAD_GLOBAL              LDAPLimitErrors
             2142  COMPARE_OP               exception-match
         2144_2146  POP_JUMP_IF_FALSE  2158  'to 2158'
             2148  POP_TOP          
             2150  POP_TOP          
             2152  POP_TOP          

 L. 594      2154  POP_EXCEPT       
             2156  JUMP_FORWARD       2160  'to 2160'
           2158_0  COME_FROM          2144  '2144'
             2158  END_FINALLY      
           2160_0  COME_FROM          2156  '2156'
           2160_1  COME_FROM          2136  '2136'
           2160_2  COME_FROM          2062  '2062'
             2160  POP_BLOCK        
             2162  BEGIN_FINALLY    
           2164_0  COME_FROM_FINALLY  2002  '2002'
             2164  LOAD_CONST               None
             2166  STORE_FAST               'e'
             2168  DELETE_FAST              'e'
             2170  END_FINALLY      
             2172  POP_EXCEPT       
             2174  JUMP_FORWARD       2384  'to 2384'
           2176_0  COME_FROM          1992  '1992'

 L. 595      2176  DUP_TOP          
             2178  LOAD_GLOBAL              ldap0
             2180  LOAD_ATTR                FILTER_ERROR
             2182  LOAD_GLOBAL              ldap0
             2184  LOAD_ATTR                INAPPROPRIATE_MATCHING
             2186  BUILD_TUPLE_2         2 
             2188  COMPARE_OP               exception-match
         2190_2192  POP_JUMP_IF_FALSE  2252  'to 2252'
             2194  POP_TOP          
             2196  STORE_FAST               'e'
             2198  POP_TOP          
             2200  SETUP_FINALLY      2240  'to 2240'

 L. 597      2202  LOAD_GLOBAL              web2ldap
             2204  LOAD_ATTR                app
             2206  LOAD_ATTR                searchform
             2208  LOAD_ATTR                w2l_searchform

 L. 598      2210  LOAD_DEREF               'app'

 L. 599      2212  LOAD_DEREF               'app'
             2214  LOAD_METHOD              ldap_error_msg
             2216  LOAD_FAST                'e'
             2218  CALL_METHOD_1         1  ''

 L. 600      2220  LOAD_FAST                'filterstr'

 L. 601      2222  LOAD_DEREF               'scope'

 L. 597      2224  LOAD_CONST               ('Msg', 'filterstr', 'scope')
             2226  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2228  POP_TOP          

 L. 603      2230  POP_BLOCK        
             2232  POP_EXCEPT       
             2234  CALL_FINALLY       2240  'to 2240'
             2236  LOAD_CONST               None
             2238  RETURN_VALUE     
           2240_0  COME_FROM          2234  '2234'
           2240_1  COME_FROM_FINALLY  2200  '2200'
             2240  LOAD_CONST               None
             2242  STORE_FAST               'e'
             2244  DELETE_FAST              'e'
             2246  END_FINALLY      
             2248  POP_EXCEPT       
             2250  JUMP_FORWARD       2384  'to 2384'
           2252_0  COME_FROM          2190  '2190'

 L. 604      2252  DUP_TOP          
             2254  LOAD_GLOBAL              ldap0
             2256  LOAD_ATTR                NO_SUCH_OBJECT
             2258  LOAD_GLOBAL              ldap0
             2260  LOAD_ATTR                UNWILLING_TO_PERFORM
             2262  BUILD_TUPLE_2         2 
             2264  COMPARE_OP               exception-match
         2266_2268  POP_JUMP_IF_FALSE  2356  'to 2356'
             2270  POP_TOP          
             2272  STORE_FAST               'e'
             2274  POP_TOP          
             2276  SETUP_FINALLY      2344  'to 2344'

 L. 605      2278  LOAD_FAST                'result_handler'
             2280  LOAD_ATTR                endResultBreak
             2282  STORE_FAST               'resind'

 L. 606      2284  LOAD_FAST                'search_root'
         2286_2288  POP_JUMP_IF_TRUE   2302  'to 2302'
             2290  LOAD_DEREF               'scope'
             2292  LOAD_GLOBAL              ldap0
             2294  LOAD_ATTR                SCOPE_ONELEVEL
             2296  COMPARE_OP               !=
         2298_2300  POP_JUMP_IF_FALSE  2340  'to 2340'
           2302_0  COME_FROM          2286  '2286'

 L. 608      2302  LOAD_GLOBAL              web2ldap
             2304  LOAD_ATTR                app
             2306  LOAD_ATTR                searchform
             2308  LOAD_ATTR                w2l_searchform

 L. 609      2310  LOAD_DEREF               'app'

 L. 610      2312  LOAD_DEREF               'app'
             2314  LOAD_METHOD              ldap_error_msg
             2316  LOAD_FAST                'e'
             2318  CALL_METHOD_1         1  ''

 L. 611      2320  LOAD_FAST                'filterstr'

 L. 612      2322  LOAD_DEREF               'scope'

 L. 608      2324  LOAD_CONST               ('Msg', 'filterstr', 'scope')
             2326  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2328  POP_TOP          

 L. 614      2330  POP_BLOCK        
             2332  POP_EXCEPT       
             2334  CALL_FINALLY       2344  'to 2344'
             2336  LOAD_CONST               None
             2338  RETURN_VALUE     
           2340_0  COME_FROM          2298  '2298'
             2340  POP_BLOCK        
             2342  BEGIN_FINALLY    
           2344_0  COME_FROM          2334  '2334'
           2344_1  COME_FROM_FINALLY  2276  '2276'
             2344  LOAD_CONST               None
             2346  STORE_FAST               'e'
             2348  DELETE_FAST              'e'
             2350  END_FINALLY      
             2352  POP_EXCEPT       
             2354  JUMP_FORWARD       2384  'to 2384'
           2356_0  COME_FROM          2266  '2266'
             2356  END_FINALLY      
           2358_0  COME_FROM          1974  '1974'

 L. 616      2358  LOAD_FAST                'search_size_limit'
             2360  LOAD_CONST               0
             2362  COMPARE_OP               >=
         2364_2366  JUMP_IF_FALSE_OR_POP  2376  'to 2376'
             2368  LOAD_FAST                'result_handler'
             2370  LOAD_ATTR                endResultBreak
             2372  LOAD_FAST                'search_size_limit'
             2374  COMPARE_OP               >
           2376_0  COME_FROM          2364  '2364'
             2376  STORE_FAST               'partial_results'

 L. 617      2378  LOAD_FAST                'result_handler'
             2380  LOAD_ATTR                endResultBreak
             2382  STORE_FAST               'resind'
           2384_0  COME_FROM          2354  '2354'
           2384_1  COME_FROM          2250  '2250'
           2384_2  COME_FROM          2174  '2174'

 L. 619      2384  LOAD_FAST                'result_handler'
             2386  LOAD_ATTR                beginResultsDropped
             2388  STORE_FAST               'search_resminindex'

 L. 620      2390  LOAD_FAST                'result_handler'
             2392  LOAD_ATTR                allResults
             2394  STORE_FAST               'result_dnlist'

 L. 624      2396  LOAD_FAST                'search_root'
         2398_2400  POP_JUMP_IF_TRUE   2456  'to 2456'
             2402  LOAD_FAST                'result_dnlist'
         2404_2406  POP_JUMP_IF_TRUE   2456  'to 2456'
             2408  LOAD_DEREF               'scope'
             2410  LOAD_GLOBAL              ldap0
             2412  LOAD_ATTR                SCOPE_ONELEVEL
             2414  COMPARE_OP               ==
         2416_2418  POP_JUMP_IF_FALSE  2456  'to 2456'

 L. 625      2420  LOAD_FAST                'result_dnlist'
             2422  LOAD_METHOD              extend
             2424  LOAD_CLOSURE             'app'
             2426  BUILD_TUPLE_1         1 
             2428  LOAD_LISTCOMP            '<code_object <listcomp>>'
             2430  LOAD_STR                 'w2l_search.<locals>.<listcomp>'
             2432  MAKE_FUNCTION_8          'closure'

 L. 627      2434  LOAD_DEREF               'app'
             2436  LOAD_ATTR                ls
             2438  LOAD_ATTR                namingContexts

 L. 625      2440  GET_ITER         
             2442  CALL_FUNCTION_1       1  ''
             2444  CALL_METHOD_1         1  ''
             2446  POP_TOP          

 L. 629      2448  LOAD_GLOBAL              len
             2450  LOAD_FAST                'result_dnlist'
             2452  CALL_FUNCTION_1       1  ''
             2454  STORE_FAST               'resind'
           2456_0  COME_FROM          2416  '2416'
           2456_1  COME_FROM          2404  '2404'
           2456_2  COME_FROM          2398  '2398'

 L. 634      2456  LOAD_DEREF               'app'
             2458  LOAD_METHOD              anchor

 L. 635      2460  LOAD_STR                 'searchform'

 L. 635      2462  LOAD_STR                 'Edit Filter'

 L. 637      2464  LOAD_STR                 'dn'
             2466  LOAD_DEREF               'app'
             2468  LOAD_ATTR                dn
             2470  BUILD_TUPLE_2         2 

 L. 638      2472  LOAD_CONST               ('searchform_mode', 'exp')

 L. 639      2474  LOAD_STR                 'search_root'
             2476  LOAD_FAST                'search_root'
             2478  BUILD_TUPLE_2         2 

 L. 640      2480  LOAD_STR                 'filterstr'
             2482  LOAD_FAST                'filterstr'
             2484  BUILD_TUPLE_2         2 

 L. 641      2486  LOAD_STR                 'search_lastmod'
             2488  LOAD_GLOBAL              str
             2490  LOAD_FAST                'search_lastmod'
             2492  CALL_FUNCTION_1       1  ''
             2494  BUILD_TUPLE_2         2 

 L. 642      2496  LOAD_STR                 'search_attrs'
             2498  LOAD_STR                 ','
             2500  LOAD_METHOD              join
             2502  LOAD_DEREF               'search_attrs'
             2504  CALL_METHOD_1         1  ''
             2506  BUILD_TUPLE_2         2 

 L. 643      2508  LOAD_STR                 'scope'
             2510  LOAD_GLOBAL              str
             2512  LOAD_DEREF               'scope'
             2514  CALL_FUNCTION_1       1  ''
             2516  BUILD_TUPLE_2         2 

 L. 636      2518  BUILD_LIST_7          7 

 L. 634      2520  CALL_METHOD_3         3  ''

 L. 646      2522  LOAD_DEREF               'app'
             2524  LOAD_ATTR                anchor

 L. 647      2526  LOAD_STR                 'search'

 L. 647      2528  LOAD_STR                 'Negate search'

 L. 649      2530  LOAD_STR                 'dn'
             2532  LOAD_DEREF               'app'
             2534  LOAD_ATTR                dn
             2536  BUILD_TUPLE_2         2 

 L. 650      2538  LOAD_STR                 'search_root'
             2540  LOAD_FAST                'search_root'
             2542  BUILD_TUPLE_2         2 

 L. 651      2544  LOAD_STR                 'search_output'
             2546  LOAD_STR                 'raw'
             2548  LOAD_STR                 'table'
             2550  LOAD_CONST               (False, True)
             2552  BUILD_CONST_KEY_MAP_2     2 
             2554  LOAD_FAST                'search_output'
             2556  LOAD_STR                 'table'
             2558  COMPARE_OP               ==
             2560  BINARY_SUBSCR    
             2562  BUILD_TUPLE_2         2 

 L. 652      2564  LOAD_STR                 'scope'
             2566  LOAD_GLOBAL              str
             2568  LOAD_DEREF               'scope'
             2570  CALL_FUNCTION_1       1  ''
             2572  BUILD_TUPLE_2         2 

 L. 653      2574  LOAD_STR                 'filterstr'
             2576  LOAD_GLOBAL              ldap0
             2578  LOAD_ATTR                filter
             2580  LOAD_METHOD              negate_filter
             2582  LOAD_FAST                'filterstr'
             2584  CALL_METHOD_1         1  ''
             2586  BUILD_TUPLE_2         2 

 L. 654      2588  LOAD_STR                 'search_resminindex'
             2590  LOAD_GLOBAL              str
             2592  LOAD_FAST                'search_resminindex'
             2594  CALL_FUNCTION_1       1  ''
             2596  BUILD_TUPLE_2         2 

 L. 655      2598  LOAD_STR                 'search_resnumber'
             2600  LOAD_GLOBAL              str
             2602  LOAD_FAST                'search_resnumber'
             2604  CALL_FUNCTION_1       1  ''
             2606  BUILD_TUPLE_2         2 

 L. 656      2608  LOAD_STR                 'search_lastmod'
             2610  LOAD_GLOBAL              str
             2612  LOAD_FAST                'search_lastmod'
             2614  CALL_FUNCTION_1       1  ''
             2616  BUILD_TUPLE_2         2 

 L. 657      2618  LOAD_STR                 'search_attrs'
             2620  LOAD_STR                 ','
             2622  LOAD_METHOD              join
             2624  LOAD_DEREF               'search_attrs'
             2626  CALL_METHOD_1         1  ''
             2628  BUILD_TUPLE_2         2 

 L. 648      2630  BUILD_LIST_9          9 

 L. 659      2632  LOAD_STR                 'Search with negated search filter'

 L. 646      2634  LOAD_CONST               ('title',)
             2636  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 633      2638  BUILD_LIST_2          2 
             2640  STORE_FAST               'ContextMenuList'

 L. 663      2642  LOAD_FAST                'searchform_mode'
             2644  LOAD_CONST               {'base', 'adv'}
             2646  COMPARE_OP               in
         2648_2650  POP_JUMP_IF_FALSE  2698  'to 2698'

 L. 664      2652  LOAD_FAST                'ContextMenuList'
             2654  LOAD_METHOD              append

 L. 665      2656  LOAD_DEREF               'app'
             2658  LOAD_ATTR                anchor

 L. 666      2660  LOAD_STR                 'searchform'

 L. 666      2662  LOAD_STR                 'Modify Search'

 L. 667      2664  LOAD_DEREF               'app'
             2666  LOAD_ATTR                form
             2668  LOAD_ATTR                allInputFields

 L. 669      2670  LOAD_STR                 'dn'
             2672  LOAD_DEREF               'app'
             2674  LOAD_ATTR                dn
             2676  BUILD_TUPLE_2         2 

 L. 670      2678  LOAD_CONST               ('searchform_mode', 'adv')

 L. 668      2680  BUILD_LIST_2          2 

 L. 672      2682  LOAD_CONST               ('dn', 'searchform_mode')

 L. 667      2684  LOAD_CONST               ('fields', 'ignore_fields')
             2686  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 674      2688  LOAD_STR                 'Modify search parameters'

 L. 665      2690  LOAD_CONST               ('title',)
             2692  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 664      2694  CALL_METHOD_1         1  ''
             2696  POP_TOP          
           2698_0  COME_FROM          2648  '2648'

 L. 678      2698  LOAD_STR                 '\n            <table>\n              <tr>\n                <td>Scope:</td>\n                <td>%s</td>\n              </tr>\n              <tr>\n                <td>Base DN:</td>\n                <td>%s</td>\n              </tr>\n              <tr>\n                <td>Filter string:</td>\n                <td>%s</td>\n              </tr>\n            </table>\n            '

 L. 694      2700  LOAD_GLOBAL              ldap0
             2702  LOAD_ATTR                ldapurl
             2704  LOAD_ATTR                SEARCH_SCOPE_STR
             2706  LOAD_DEREF               'scope'
             2708  BINARY_SUBSCR    

 L. 695      2710  LOAD_FAST                'utf2display'
             2712  LOAD_FAST                'search_root'
             2714  CALL_FUNCTION_1       1  ''

 L. 696      2716  LOAD_FAST                'utf2display'
             2718  LOAD_FAST                'filterstr2'
             2720  CALL_FUNCTION_1       1  ''

 L. 693      2722  BUILD_TUPLE_3         3 

 L. 678      2724  BINARY_MODULO    
             2726  STORE_FAST               'search_param_html'

 L. 699      2728  LOAD_FAST                'result_dnlist'
         2730_2732  POP_JUMP_IF_TRUE   2770  'to 2770'

 L. 703      2734  LOAD_DEREF               'app'
             2736  LOAD_ATTR                simple_message

 L. 704      2738  LOAD_STR                 'No Search Results'

 L. 705      2740  LOAD_STR                 '<p class="WarningMessage">No entries found.</p>%s'
             2742  LOAD_FAST                'search_param_html'
             2744  BINARY_MODULO    

 L. 706      2746  LOAD_GLOBAL              web2ldap
             2748  LOAD_ATTR                app
             2750  LOAD_ATTR                gui
             2752  LOAD_METHOD              main_menu
             2754  LOAD_DEREF               'app'
             2756  CALL_METHOD_1         1  ''

 L. 707      2758  LOAD_FAST                'ContextMenuList'

 L. 703      2760  LOAD_CONST               ('main_menu_list', 'context_menu_list')
             2762  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             2764  POP_TOP          
         2766_2768  JUMP_ABSOLUTE      4852  'to 4852'
           2770_0  COME_FROM          2730  '2730'

 L. 715      2770  LOAD_CONST               None
             2772  STORE_FAST               'page_command_list'

 L. 717      2774  LOAD_FAST                'ContextMenuList'
             2776  LOAD_METHOD              extend

 L. 718      2778  LOAD_DEREF               'app'
             2780  LOAD_ATTR                anchor

 L. 719      2782  LOAD_STR                 'search'

 L. 720      2784  LOAD_STR                 'Raw'
             2786  LOAD_STR                 'Table'
             2788  LOAD_CONST               (False, True)
             2790  BUILD_CONST_KEY_MAP_2     2 
             2792  LOAD_FAST                'search_output'
             2794  LOAD_STR                 'raw'
             2796  COMPARE_OP               ==
             2798  BINARY_SUBSCR    

 L. 722      2800  LOAD_STR                 'dn'
             2802  LOAD_DEREF               'app'
             2804  LOAD_ATTR                dn
             2806  BUILD_TUPLE_2         2 

 L. 723      2808  LOAD_STR                 'search_root'
             2810  LOAD_FAST                'search_root'
             2812  BUILD_TUPLE_2         2 

 L. 724      2814  LOAD_STR                 'search_output'
             2816  LOAD_STR                 'raw'
             2818  LOAD_STR                 'table'
             2820  LOAD_CONST               (False, True)
             2822  BUILD_CONST_KEY_MAP_2     2 
             2824  LOAD_FAST                'search_output'
             2826  LOAD_STR                 'raw'
             2828  COMPARE_OP               ==
             2830  BINARY_SUBSCR    
             2832  BUILD_TUPLE_2         2 

 L. 725      2834  LOAD_STR                 'scope'
             2836  LOAD_GLOBAL              str
             2838  LOAD_DEREF               'scope'
             2840  CALL_FUNCTION_1       1  ''
             2842  BUILD_TUPLE_2         2 

 L. 726      2844  LOAD_STR                 'filterstr'
             2846  LOAD_FAST                'filterstr'
             2848  BUILD_TUPLE_2         2 

 L. 727      2850  LOAD_STR                 'search_resminindex'
             2852  LOAD_GLOBAL              str
             2854  LOAD_FAST                'search_resminindex'
             2856  CALL_FUNCTION_1       1  ''
             2858  BUILD_TUPLE_2         2 

 L. 728      2860  LOAD_STR                 'search_resnumber'
             2862  LOAD_GLOBAL              str
             2864  LOAD_FAST                'search_resnumber'
             2866  CALL_FUNCTION_1       1  ''
             2868  BUILD_TUPLE_2         2 

 L. 729      2870  LOAD_STR                 'search_lastmod'
             2872  LOAD_GLOBAL              str
             2874  LOAD_FAST                'search_lastmod'
             2876  CALL_FUNCTION_1       1  ''
             2878  BUILD_TUPLE_2         2 

 L. 730      2880  LOAD_STR                 'search_attrs'
             2882  LOAD_STR                 ','
             2884  LOAD_METHOD              join
             2886  LOAD_DEREF               'search_attrs'
             2888  CALL_METHOD_1         1  ''
             2890  BUILD_TUPLE_2         2 

 L. 721      2892  BUILD_LIST_9          9 

 L. 732      2894  LOAD_STR                 'Display %s of search results'

 L. 733      2896  LOAD_STR                 'distinguished names'
             2898  LOAD_STR                 'attributes'
             2900  LOAD_CONST               (False, True)
             2902  BUILD_CONST_KEY_MAP_2     2 
             2904  LOAD_FAST                'search_output'
             2906  LOAD_STR                 'raw'
             2908  COMPARE_OP               ==
             2910  BINARY_SUBSCR    

 L. 732      2912  BINARY_MODULO    

 L. 718      2914  LOAD_CONST               ('title',)
             2916  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 736      2918  LOAD_DEREF               'app'
             2920  LOAD_METHOD              anchor

 L. 737      2922  LOAD_STR                 'delete'

 L. 737      2924  LOAD_STR                 'Delete'

 L. 739      2926  LOAD_STR                 'dn'
             2928  LOAD_FAST                'search_root'
             2930  BUILD_TUPLE_2         2 

 L. 740      2932  LOAD_STR                 'filterstr'
             2934  LOAD_FAST                'filterstr2'
             2936  BUILD_TUPLE_2         2 

 L. 741      2938  LOAD_STR                 'scope'
             2940  LOAD_GLOBAL              str
             2942  LOAD_DEREF               'scope'
             2944  CALL_FUNCTION_1       1  ''
             2946  BUILD_TUPLE_2         2 

 L. 738      2948  BUILD_LIST_3          3 

 L. 736      2950  CALL_METHOD_3         3  ''

 L. 744      2952  LOAD_DEREF               'app'
             2954  LOAD_METHOD              anchor

 L. 745      2956  LOAD_STR                 'bulkmod'

 L. 745      2958  LOAD_STR                 'Bulk modify'

 L. 747      2960  LOAD_STR                 'dn'
             2962  LOAD_FAST                'search_root'
             2964  BUILD_TUPLE_2         2 

 L. 748      2966  LOAD_STR                 'filterstr'
             2968  LOAD_FAST                'filterstr2'
             2970  BUILD_TUPLE_2         2 

 L. 749      2972  LOAD_STR                 'scope'
             2974  LOAD_GLOBAL              str
             2976  LOAD_DEREF               'scope'
             2978  CALL_FUNCTION_1       1  ''
             2980  BUILD_TUPLE_2         2 

 L. 746      2982  BUILD_LIST_3          3 

 L. 744      2984  CALL_METHOD_3         3  ''

 L. 717      2986  BUILD_LIST_3          3 
             2988  CALL_METHOD_1         1  ''
             2990  POP_TOP          

 L. 754      2992  LOAD_FAST                'partial_results'
         2994_2996  POP_JUMP_IF_FALSE  3008  'to 3008'
             2998  LOAD_FAST                'search_size_limit'
             3000  LOAD_CONST               0
             3002  COMPARE_OP               >
         3004_3006  POP_JUMP_IF_TRUE   3014  'to 3014'
           3008_0  COME_FROM          2994  '2994'
             3008  LOAD_FAST                'search_resminindex'
         3010_3012  POP_JUMP_IF_FALSE  3266  'to 3266'
           3014_0  COME_FROM          3004  '3004'

 L. 756      3014  LOAD_CONST               5
             3016  LOAD_STR                 '&nbsp;'
             3018  BUILD_LIST_1          1 
             3020  BINARY_MULTIPLY  
             3022  STORE_FAST               'page_command_list'

 L. 757      3024  LOAD_GLOBAL              max
             3026  LOAD_CONST               0
             3028  LOAD_FAST                'search_resminindex'
             3030  LOAD_FAST                'search_resnumber'
             3032  BINARY_SUBTRACT  
             3034  CALL_FUNCTION_2       2  ''
             3036  STORE_FAST               'prev_resminindex'

 L. 759      3038  LOAD_FAST                'search_resminindex'
             3040  LOAD_FAST                'search_resnumber'
             3042  COMPARE_OP               >
         3044_3046  POP_JUMP_IF_FALSE  3076  'to 3076'

 L. 760      3048  LOAD_FAST                'page_appl_anchor'

 L. 761      3050  LOAD_DEREF               'app'

 L. 762      3052  LOAD_STR                 '|&larr;{0}…{1}'

 L. 763      3054  LOAD_FAST                'search_root'

 L. 763      3056  LOAD_FAST                'filterstr'

 L. 763      3058  LOAD_FAST                'search_output'

 L. 764      3060  LOAD_CONST               0

 L. 764      3062  LOAD_FAST                'search_resnumber'

 L. 765      3064  LOAD_FAST                'search_lastmod'

 L. 765      3066  LOAD_FAST                'num_result_all'

 L. 760      3068  CALL_FUNCTION_9       9  ''
             3070  LOAD_FAST                'page_command_list'
             3072  LOAD_CONST               0
             3074  STORE_SUBSCR     
           3076_0  COME_FROM          3044  '3044'

 L. 768      3076  LOAD_FAST                'search_resminindex'
             3078  LOAD_CONST               0
             3080  COMPARE_OP               >
         3082_3084  POP_JUMP_IF_FALSE  3120  'to 3120'

 L. 769      3086  LOAD_FAST                'page_appl_anchor'

 L. 770      3088  LOAD_DEREF               'app'

 L. 771      3090  LOAD_STR                 '&larr;{0}…{1}'

 L. 772      3092  LOAD_FAST                'search_root'

 L. 772      3094  LOAD_FAST                'filterstr'

 L. 772      3096  LOAD_FAST                'search_output'

 L. 773      3098  LOAD_GLOBAL              max
             3100  LOAD_CONST               0
             3102  LOAD_FAST                'prev_resminindex'
             3104  CALL_FUNCTION_2       2  ''

 L. 773      3106  LOAD_FAST                'search_resnumber'

 L. 774      3108  LOAD_FAST                'search_lastmod'

 L. 774      3110  LOAD_FAST                'num_result_all'

 L. 769      3112  CALL_FUNCTION_9       9  ''
             3114  LOAD_FAST                'page_command_list'
             3116  LOAD_CONST               1
             3118  STORE_SUBSCR     
           3120_0  COME_FROM          3082  '3082'

 L. 777      3120  LOAD_FAST                'page_appl_anchor'

 L. 778      3122  LOAD_DEREF               'app'

 L. 779      3124  LOAD_STR                 'all'

 L. 780      3126  LOAD_FAST                'search_root'

 L. 780      3128  LOAD_FAST                'filterstr'

 L. 780      3130  LOAD_FAST                'search_output'

 L. 781      3132  LOAD_CONST               0

 L. 781      3134  LOAD_CONST               0

 L. 782      3136  LOAD_FAST                'search_lastmod'

 L. 782      3138  LOAD_FAST                'num_result_all'

 L. 777      3140  CALL_FUNCTION_9       9  ''
             3142  LOAD_FAST                'page_command_list'
             3144  LOAD_CONST               2
             3146  STORE_SUBSCR     

 L. 785      3148  LOAD_FAST                'partial_results'
         3150_3152  POP_JUMP_IF_FALSE  3266  'to 3266'

 L. 787      3154  LOAD_FAST                'page_appl_anchor'

 L. 788      3156  LOAD_DEREF               'app'

 L. 789      3158  LOAD_STR                 '{0}…{1}&rarr;'

 L. 790      3160  LOAD_FAST                'search_root'

 L. 790      3162  LOAD_FAST                'filterstr'

 L. 790      3164  LOAD_FAST                'search_output'

 L. 791      3166  LOAD_FAST                'search_resminindex'
             3168  LOAD_FAST                'search_resnumber'
             3170  BINARY_ADD       

 L. 791      3172  LOAD_FAST                'search_resnumber'

 L. 792      3174  LOAD_FAST                'search_lastmod'

 L. 792      3176  LOAD_FAST                'num_result_all'

 L. 787      3178  CALL_FUNCTION_9       9  ''
             3180  STORE_FAST               'page_next_link'

 L. 795      3182  LOAD_FAST                'num_result_all'
             3184  LOAD_CONST               None
             3186  COMPARE_OP               is-not
         3188_3190  POP_JUMP_IF_FALSE  3244  'to 3244'
             3192  LOAD_FAST                'resind'
             3194  LOAD_FAST                'num_result_all'
             3196  COMPARE_OP               <
         3198_3200  POP_JUMP_IF_FALSE  3244  'to 3244'

 L. 796      3202  LOAD_FAST                'page_next_link'
             3204  LOAD_FAST                'page_command_list'
             3206  LOAD_CONST               3
             3208  STORE_SUBSCR     

 L. 797      3210  LOAD_FAST                'page_appl_anchor'

 L. 798      3212  LOAD_DEREF               'app'

 L. 799      3214  LOAD_STR                 '{0}…{1}&rarr;|'

 L. 800      3216  LOAD_FAST                'search_root'

 L. 800      3218  LOAD_FAST                'filterstr'

 L. 800      3220  LOAD_FAST                'search_output'

 L. 801      3222  LOAD_FAST                'num_result_all'
             3224  LOAD_FAST                'search_resnumber'
             3226  BINARY_SUBTRACT  

 L. 801      3228  LOAD_FAST                'search_resnumber'

 L. 802      3230  LOAD_FAST                'search_lastmod'

 L. 802      3232  LOAD_FAST                'num_result_all'

 L. 797      3234  CALL_FUNCTION_9       9  ''
             3236  LOAD_FAST                'page_command_list'
             3238  LOAD_CONST               4
             3240  STORE_SUBSCR     
             3242  JUMP_FORWARD       3266  'to 3266'
           3244_0  COME_FROM          3198  '3198'
           3244_1  COME_FROM          3188  '3188'

 L. 804      3244  LOAD_FAST                'search_resminindex'
             3246  LOAD_FAST                'search_resnumber'
             3248  BINARY_ADD       
             3250  LOAD_FAST                'resind'
             3252  COMPARE_OP               <=
         3254_3256  POP_JUMP_IF_FALSE  3266  'to 3266'

 L. 805      3258  LOAD_FAST                'page_next_link'
             3260  LOAD_FAST                'page_command_list'
             3262  LOAD_CONST               3
             3264  STORE_SUBSCR     
           3266_0  COME_FROM          3254  '3254'
           3266_1  COME_FROM          3242  '3242'
           3266_2  COME_FROM          3150  '3150'
           3266_3  COME_FROM          3010  '3010'

 L. 807      3266  LOAD_STR                 '\n                <a\n                  href="{baseUrl}?{ldapUrl}"\n                  target="_blank"\n                  rel="bookmark"\n                  title="Bookmark for these search results"\n                >\n                  Bookmark\n                </a>\n                '
             3268  LOAD_ATTR                format

 L. 817      3270  LOAD_GLOBAL              escape_html
             3272  LOAD_DEREF               'app'
             3274  LOAD_ATTR                form
             3276  LOAD_ATTR                script_name
             3278  CALL_FUNCTION_1       1  ''

 L. 818      3280  LOAD_GLOBAL              str
             3282  LOAD_FAST                'search_ldap_url'
             3284  CALL_FUNCTION_1       1  ''

 L. 807      3286  LOAD_CONST               ('baseUrl', 'ldapUrl')
             3288  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             3290  STORE_FAST               'search_bookmark'

 L. 820      3292  LOAD_STR                 '\n<p>Search results %d - %d %s / <a href="#params" title="See search parameters and export options">Params</a> / %s</p>\n'

 L. 821      3294  LOAD_FAST                'search_resminindex'
             3296  LOAD_CONST               1
             3298  BINARY_ADD       

 L. 822      3300  LOAD_FAST                'resind'

 L. 823      3302  LOAD_FAST                'max_result_msg'

 L. 824      3304  LOAD_FAST                'search_bookmark'

 L. 820      3306  BUILD_TUPLE_4         4 
             3308  BINARY_MODULO    
             3310  STORE_FAST               'result_message'

 L. 827      3312  LOAD_GLOBAL              web2ldap
             3314  LOAD_ATTR                app
             3316  LOAD_ATTR                gui
             3318  LOAD_ATTR                top_section

 L. 828      3320  LOAD_DEREF               'app'

 L. 829      3322  LOAD_STR                 'Search Results'

 L. 830      3324  LOAD_GLOBAL              web2ldap
             3326  LOAD_ATTR                app
             3328  LOAD_ATTR                gui
             3330  LOAD_METHOD              main_menu
             3332  LOAD_DEREF               'app'
             3334  CALL_METHOD_1         1  ''

 L. 831      3336  LOAD_FAST                'ContextMenuList'

 L. 827      3338  LOAD_CONST               ('context_menu_list',)
             3340  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             3342  POP_TOP          

 L. 834      3344  LOAD_GLOBAL              web2ldap
             3346  LOAD_ATTR                app
             3348  LOAD_ATTR                form
             3350  LOAD_METHOD              ExportFormatSelect
             3352  CALL_METHOD_0         0  ''
             3354  STORE_FAST               'export_field'

 L. 835      3356  LOAD_DEREF               'app'
             3358  LOAD_ATTR                form
             3360  LOAD_ATTR                accept_charset
             3362  LOAD_FAST                'export_field'
             3364  STORE_ATTR               charset

 L. 837      3366  LOAD_DEREF               'app'
             3368  LOAD_ATTR                outf
             3370  LOAD_METHOD              write
             3372  LOAD_STR                 '\n'
             3374  LOAD_METHOD              join
             3376  LOAD_FAST                'SearchWarningMsg'
             3378  LOAD_FAST                'result_message'
             3380  BUILD_TUPLE_2         2 
             3382  CALL_METHOD_1         1  ''
             3384  CALL_METHOD_1         1  ''
             3386  POP_TOP          

 L. 839      3388  LOAD_FAST                'search_resminindex'
             3390  LOAD_CONST               0
             3392  COMPARE_OP               ==
         3394_3396  POP_JUMP_IF_FALSE  3530  'to 3530'
             3398  LOAD_FAST                'partial_results'
         3400_3402  POP_JUMP_IF_TRUE   3530  'to 3530'

 L. 840      3404  LOAD_GLOBAL              set
             3406  CALL_FUNCTION_0       0  ''
             3408  STORE_FAST               'mailtolist'

 L. 841      3410  LOAD_FAST                'result_dnlist'
             3412  GET_ITER         
           3414_0  COME_FROM          3426  '3426'
             3414  FOR_ITER           3464  'to 3464'
             3416  STORE_FAST               'r'

 L. 842      3418  LOAD_GLOBAL              isinstance
             3420  LOAD_FAST                'r'
             3422  LOAD_GLOBAL              SearchResultEntry
             3424  CALL_FUNCTION_2       2  ''
         3426_3428  POP_JUMP_IF_FALSE  3414  'to 3414'

 L. 843      3430  LOAD_FAST                'mailtolist'
             3432  LOAD_METHOD              update
             3434  LOAD_FAST                'r'
             3436  LOAD_ATTR                entry_s
             3438  LOAD_METHOD              get
             3440  LOAD_STR                 'mail'
             3442  LOAD_FAST                'r'
             3444  LOAD_ATTR                entry_s
             3446  LOAD_METHOD              get
             3448  LOAD_STR                 'rfc822Mailbox'
             3450  BUILD_LIST_0          0 
             3452  CALL_METHOD_2         2  ''
             3454  CALL_METHOD_2         2  ''
             3456  CALL_METHOD_1         1  ''
             3458  POP_TOP          
         3460_3462  JUMP_BACK          3414  'to 3414'

 L. 844      3464  LOAD_FAST                'mailtolist'
         3466_3468  POP_JUMP_IF_FALSE  3530  'to 3530'

 L. 845      3470  LOAD_LISTCOMP            '<code_object <listcomp>>'
             3472  LOAD_STR                 'w2l_search.<locals>.<listcomp>'
             3474  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
             3476  LOAD_FAST                'mailtolist'
             3478  GET_ITER         
             3480  CALL_FUNCTION_1       1  ''
             3482  STORE_FAST               'mailtolist'

 L. 846      3484  LOAD_DEREF               'app'
             3486  LOAD_ATTR                outf
             3488  LOAD_METHOD              write
             3490  LOAD_STR                 'Mail to all <a href="mailto:%s?cc=%s">Cc:-ed</a> - <a href="mailto:?bcc=%s">Bcc:-ed</a>'

 L. 847      3492  LOAD_FAST                'mailtolist'
             3494  LOAD_CONST               0
             3496  BINARY_SUBSCR    

 L. 848      3498  LOAD_STR                 ','
             3500  LOAD_METHOD              join
             3502  LOAD_FAST                'mailtolist'
             3504  LOAD_CONST               1
             3506  LOAD_CONST               None
             3508  BUILD_SLICE_2         2 
             3510  BINARY_SUBSCR    
             3512  CALL_METHOD_1         1  ''

 L. 849      3514  LOAD_STR                 ','
             3516  LOAD_METHOD              join
             3518  LOAD_FAST                'mailtolist'
             3520  CALL_METHOD_1         1  ''

 L. 846      3522  BUILD_TUPLE_3         3 
             3524  BINARY_MODULO    
             3526  CALL_METHOD_1         1  ''
             3528  POP_TOP          
           3530_0  COME_FROM          3466  '3466'
           3530_1  COME_FROM          3400  '3400'
           3530_2  COME_FROM          3394  '3394'

 L. 852      3530  LOAD_FAST                'page_command_list'
         3532_3534  POP_JUMP_IF_FALSE  3554  'to 3554'

 L. 854      3536  LOAD_DEREF               'app'
             3538  LOAD_ATTR                outf
             3540  LOAD_METHOD              write
             3542  LOAD_GLOBAL              PAGE_COMMAND_TMPL
             3544  LOAD_ATTR                format
             3546  LOAD_FAST                'page_command_list'
             3548  CALL_FUNCTION_EX      0  'positional arguments only'
             3550  CALL_METHOD_1         1  ''
             3552  POP_TOP          
           3554_0  COME_FROM          3532  '3532'

 L. 856      3554  LOAD_DEREF               'app'
             3556  LOAD_ATTR                outf
             3558  LOAD_METHOD              write
             3560  LOAD_STR                 '<table id="SrchResList">\n'
             3562  CALL_METHOD_1         1  ''
             3564  POP_TOP          

 L. 858      3566  LOAD_FAST                'result_dnlist'
             3568  LOAD_CONST               0
             3570  LOAD_FAST                'resind'
             3572  BUILD_SLICE_2         2 
             3574  BINARY_SUBSCR    
             3576  GET_ITER         
         3578_3580  FOR_ITER           4588  'to 4588'
             3582  STORE_FAST               'r'

 L. 860      3584  LOAD_GLOBAL              isinstance
             3586  LOAD_FAST                'r'
             3588  LOAD_GLOBAL              SearchReference
             3590  CALL_FUNCTION_2       2  ''
         3592_3594  POP_JUMP_IF_FALSE  3874  'to 3874'

 L. 863      3596  LOAD_GLOBAL              ldap0
             3598  LOAD_ATTR                cidict
             3600  LOAD_METHOD              CIDict
             3602  BUILD_MAP_0           0 
             3604  CALL_METHOD_1         1  ''
             3606  STORE_FAST               'entry'

 L. 864      3608  SETUP_FINALLY      3628  'to 3628'

 L. 865      3610  LOAD_GLOBAL              ExtendedLDAPUrl
             3612  LOAD_FAST                'r'
             3614  LOAD_ATTR                ref_url_strings
             3616  LOAD_CONST               0
             3618  BINARY_SUBSCR    
             3620  CALL_FUNCTION_1       1  ''
             3622  STORE_FAST               'refUrl'
             3624  POP_BLOCK        
             3626  JUMP_FORWARD       3682  'to 3682'
           3628_0  COME_FROM_FINALLY  3608  '3608'

 L. 866      3628  DUP_TOP          
             3630  LOAD_GLOBAL              ValueError
             3632  COMPARE_OP               exception-match
         3634_3636  POP_JUMP_IF_FALSE  3680  'to 3680'
             3638  POP_TOP          
             3640  POP_TOP          
             3642  POP_TOP          

 L. 867      3644  BUILD_LIST_0          0 
             3646  STORE_FAST               'command_table'

 L. 868      3648  LOAD_STR                 'Search reference (NON-LDAP-URI) =&gt; %s'
             3650  LOAD_FAST                'utf2display'
             3652  LOAD_GLOBAL              str
             3654  LOAD_FAST                'r'
             3656  LOAD_CONST               1
             3658  BINARY_SUBSCR    
             3660  LOAD_CONST               1
             3662  BINARY_SUBSCR    
             3664  LOAD_CONST               0
             3666  BINARY_SUBSCR    
             3668  CALL_FUNCTION_1       1  ''
             3670  CALL_FUNCTION_1       1  ''
             3672  BINARY_MODULO    
             3674  STORE_FAST               'result_dd_str'
             3676  POP_EXCEPT       
             3678  JUMP_FORWARD       4558  'to 4558'
           3680_0  COME_FROM          3634  '3634'
             3680  END_FINALLY      
           3682_0  COME_FROM          3626  '3626'

 L. 870      3682  LOAD_STR                 'Search reference =&gt; %s'
             3684  LOAD_FAST                'refUrl'
             3686  LOAD_ATTR                htmlHREF
             3688  LOAD_CONST               None
             3690  LOAD_CONST               ('hrefTarget',)
             3692  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             3694  BINARY_MODULO    
             3696  STORE_FAST               'result_dd_str'

 L. 871      3698  LOAD_DEREF               'scope'
             3700  LOAD_GLOBAL              ldap0
             3702  LOAD_ATTR                SCOPE_SUBTREE
             3704  COMPARE_OP               ==
         3706_3708  POP_JUMP_IF_FALSE  3776  'to 3776'

 L. 872      3710  LOAD_FAST                'refUrl'
             3712  LOAD_ATTR                scope
         3714_3716  JUMP_IF_TRUE_OR_POP  3720  'to 3720'
             3718  LOAD_DEREF               'scope'
           3720_0  COME_FROM          3714  '3714'
             3720  LOAD_FAST                'refUrl'
             3722  STORE_ATTR               scope

 L. 873      3724  LOAD_FAST                'refUrl'
             3726  LOAD_ATTR                filterstr
         3728_3730  JUMP_IF_TRUE_OR_POP  3740  'to 3740'
             3732  LOAD_STR                 ''
         3734_3736  JUMP_IF_TRUE_OR_POP  3740  'to 3740'
             3738  LOAD_FAST                'filterstr'
           3740_0  COME_FROM          3734  '3734'
           3740_1  COME_FROM          3728  '3728'
             3740  LOAD_FAST                'refUrl'
             3742  STORE_ATTR               filterstr

 L. 875      3744  LOAD_DEREF               'app'
             3746  LOAD_ATTR                anchor

 L. 876      3748  LOAD_STR                 'search'

 L. 876      3750  LOAD_STR                 'Continue search'

 L. 877      3752  LOAD_STR                 'ldapurl'
             3754  LOAD_FAST                'refUrl'
             3756  LOAD_METHOD              unparse
             3758  CALL_METHOD_0         0  ''
             3760  BUILD_TUPLE_2         2 
             3762  BUILD_LIST_1          1 

 L. 878      3764  LOAD_STR                 'Follow this search continuation'

 L. 875      3766  LOAD_CONST               ('title',)
             3768  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'

 L. 874      3770  BUILD_LIST_1          1 
             3772  STORE_FAST               'command_table'
             3774  JUMP_FORWARD       4558  'to 4558'
           3776_0  COME_FROM          3706  '3706'

 L. 882      3776  BUILD_LIST_0          0 
             3778  STORE_FAST               'command_table'

 L. 883      3780  LOAD_FAST                'filterstr'
             3782  LOAD_FAST                'refUrl'
             3784  STORE_ATTR               filterstr

 L. 884      3786  LOAD_GLOBAL              ldap0
             3788  LOAD_ATTR                SCOPE_BASE
             3790  LOAD_FAST                'refUrl'
             3792  STORE_ATTR               scope

 L. 885      3794  LOAD_FAST                'command_table'
             3796  LOAD_METHOD              append
             3798  LOAD_DEREF               'app'
             3800  LOAD_ATTR                anchor

 L. 886      3802  LOAD_STR                 'read'

 L. 886      3804  LOAD_STR                 'Read'

 L. 887      3806  LOAD_STR                 'ldapurl'
             3808  LOAD_FAST                'refUrl'
             3810  LOAD_METHOD              unparse
             3812  CALL_METHOD_0         0  ''
             3814  BUILD_TUPLE_2         2 
             3816  BUILD_LIST_1          1 

 L. 888      3818  LOAD_STR                 'Display single entry following search continuation'

 L. 885      3820  LOAD_CONST               ('title',)
             3822  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             3824  CALL_METHOD_1         1  ''
             3826  POP_TOP          

 L. 890      3828  LOAD_GLOBAL              ldap0
             3830  LOAD_ATTR                SCOPE_ONELEVEL
             3832  LOAD_FAST                'refUrl'
             3834  STORE_ATTR               scope

 L. 891      3836  LOAD_FAST                'command_table'
             3838  LOAD_METHOD              append
             3840  LOAD_DEREF               'app'
             3842  LOAD_ATTR                anchor

 L. 892      3844  LOAD_STR                 'search'

 L. 892      3846  LOAD_STR                 'Down'

 L. 893      3848  LOAD_STR                 'ldapurl'
             3850  LOAD_FAST                'refUrl'
             3852  LOAD_METHOD              unparse
             3854  CALL_METHOD_0         0  ''
             3856  BUILD_TUPLE_2         2 
             3858  BUILD_LIST_1          1 

 L. 894      3860  LOAD_STR                 'Descend into tree following search continuation'

 L. 891      3862  LOAD_CONST               ('title',)
             3864  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             3866  CALL_METHOD_1         1  ''
             3868  POP_TOP          
         3870_3872  JUMP_FORWARD       4558  'to 4558'
           3874_0  COME_FROM          3592  '3592'

 L. 897      3874  LOAD_GLOBAL              isinstance
             3876  LOAD_FAST                'r'
             3878  LOAD_GLOBAL              SearchResultEntry
             3880  CALL_FUNCTION_2       2  ''
         3882_3884  POP_JUMP_IF_FALSE  4544  'to 4544'

 L. 900      3886  LOAD_GLOBAL              ldap0
             3888  LOAD_ATTR                schema
             3890  LOAD_ATTR                models
             3892  LOAD_METHOD              Entry
             3894  LOAD_DEREF               'app'
             3896  LOAD_ATTR                schema
             3898  LOAD_FAST                'r'
             3900  LOAD_ATTR                dn_s
             3902  LOAD_FAST                'r'
             3904  LOAD_ATTR                entry_as
             3906  CALL_METHOD_3         3  ''
             3908  STORE_FAST               'entry'

 L. 902      3910  LOAD_FAST                'search_output'
             3912  LOAD_STR                 'raw'
             3914  COMPARE_OP               ==
         3916_3918  POP_JUMP_IF_FALSE  3932  'to 3932'

 L. 905      3920  LOAD_FAST                'utf2display'
             3922  LOAD_FAST                'r'
             3924  LOAD_ATTR                dn_s
             3926  CALL_FUNCTION_1       1  ''
             3928  STORE_FAST               'result_dd_str'
             3930  JUMP_FORWARD       4186  'to 4186'
           3932_0  COME_FROM          3916  '3916'

 L. 909      3932  LOAD_GLOBAL              ldap0
             3934  LOAD_ATTR                schema
             3936  LOAD_ATTR                models
             3938  LOAD_METHOD              SchemaElementOIDSet

 L. 910      3940  LOAD_DEREF               'app'
             3942  LOAD_ATTR                schema

 L. 911      3944  LOAD_GLOBAL              ldap0
             3946  LOAD_ATTR                schema
             3948  LOAD_ATTR                models
             3950  LOAD_ATTR                ObjectClass

 L. 912      3952  LOAD_GLOBAL              decode_list
             3954  LOAD_FAST                'entry'
             3956  LOAD_METHOD              get
             3958  LOAD_STR                 'objectClass'
             3960  BUILD_LIST_0          0 
             3962  CALL_METHOD_2         2  ''
             3964  LOAD_STR                 'ascii'
             3966  LOAD_CONST               ('encoding',)
             3968  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L. 909      3970  CALL_METHOD_3         3  ''
             3972  STORE_FAST               'oc_set'

 L. 914      3974  LOAD_FAST                'oc_set'
             3976  LOAD_METHOD              intersection
             3978  LOAD_FAST                'search_tdtemplate_keys'
             3980  CALL_METHOD_1         1  ''
             3982  LOAD_ATTR                names
             3984  STORE_FAST               'tdtemplate_oc'

 L. 915      3986  LOAD_CONST               None
             3988  STORE_FAST               'tableentry_attrs'

 L. 917      3990  LOAD_FAST                'tdtemplate_oc'
         3992_3994  POP_JUMP_IF_FALSE  4056  'to 4056'

 L. 918      3996  LOAD_GLOBAL              ldap0
             3998  LOAD_ATTR                schema
             4000  LOAD_ATTR                models
             4002  LOAD_METHOD              SchemaElementOIDSet

 L. 919      4004  LOAD_DEREF               'app'
             4006  LOAD_ATTR                schema

 L. 920      4008  LOAD_GLOBAL              AttributeType

 L. 921      4010  BUILD_LIST_0          0 

 L. 918      4012  CALL_METHOD_3         3  ''
             4014  STORE_FAST               'template_attrs'

 L. 923      4016  LOAD_FAST                'tdtemplate_oc'
             4018  GET_ITER         
             4020  FOR_ITER           4042  'to 4042'
             4022  STORE_FAST               'oc'

 L. 924      4024  LOAD_FAST                'template_attrs'
             4026  LOAD_METHOD              update
             4028  LOAD_FAST                'search_tdtemplate_attrs_lower'
             4030  LOAD_FAST                'oc'
             4032  BINARY_SUBSCR    
             4034  CALL_METHOD_1         1  ''
             4036  POP_TOP          
         4038_4040  JUMP_BACK          4020  'to 4020'

 L. 925      4042  LOAD_FAST                'template_attrs'
             4044  LOAD_METHOD              intersection
             4046  LOAD_FAST                'entry'
             4048  LOAD_METHOD              keys
             4050  CALL_METHOD_0         0  ''
             4052  CALL_METHOD_1         1  ''
             4054  STORE_FAST               'tableentry_attrs'
           4056_0  COME_FROM          3992  '3992'

 L. 927      4056  LOAD_FAST                'tableentry_attrs'
         4058_4060  POP_JUMP_IF_FALSE  4136  'to 4136'

 L. 929      4062  LOAD_GLOBAL              web2ldap
             4064  LOAD_ATTR                app
             4066  LOAD_ATTR                read
             4068  LOAD_METHOD              DisplayEntry

 L. 930      4070  LOAD_DEREF               'app'

 L. 930      4072  LOAD_FAST                'r'
             4074  LOAD_ATTR                dn_s

 L. 930      4076  LOAD_DEREF               'app'
             4078  LOAD_ATTR                schema

 L. 930      4080  LOAD_FAST                'entry'

 L. 930      4082  LOAD_STR                 'searchSep'

 L. 930      4084  LOAD_CONST               False

 L. 929      4086  CALL_METHOD_6         6  ''
             4088  STORE_FAST               'tableentry'

 L. 932      4090  BUILD_LIST_0          0 
             4092  STORE_FAST               'tdlist'

 L. 933      4094  LOAD_FAST                'tdtemplate_oc'
             4096  GET_ITER         
             4098  FOR_ITER           4124  'to 4124'
             4100  STORE_FAST               'oc'

 L. 934      4102  LOAD_FAST                'tdlist'
             4104  LOAD_METHOD              append
             4106  LOAD_FAST                'search_tdtemplate'
             4108  LOAD_FAST                'oc'
             4110  BINARY_SUBSCR    
             4112  LOAD_FAST                'tableentry'
             4114  BINARY_MODULO    
             4116  CALL_METHOD_1         1  ''
             4118  POP_TOP          
         4120_4122  JUMP_BACK          4098  'to 4098'

 L. 935      4124  LOAD_STR                 '<br>\n'
             4126  LOAD_METHOD              join
             4128  LOAD_FAST                'tdlist'
             4130  CALL_METHOD_1         1  ''
             4132  STORE_FAST               'result_dd_str'
             4134  JUMP_FORWARD       4186  'to 4186'
           4136_0  COME_FROM          4058  '4058'

 L. 937      4136  LOAD_STR                 'displayName'
             4138  LOAD_FAST                'entry'
             4140  COMPARE_OP               in
         4142_4144  POP_JUMP_IF_FALSE  4176  'to 4176'

 L. 938      4146  LOAD_FAST                'utf2display'
             4148  LOAD_DEREF               'app'
             4150  LOAD_ATTR                ls
             4152  LOAD_METHOD              uc_decode
             4154  LOAD_FAST                'entry'
             4156  LOAD_STR                 'displayName'
             4158  BINARY_SUBSCR    
             4160  LOAD_CONST               0
             4162  BINARY_SUBSCR    
             4164  CALL_METHOD_1         1  ''
             4166  LOAD_CONST               0
             4168  BINARY_SUBSCR    
             4170  CALL_FUNCTION_1       1  ''
             4172  STORE_FAST               'result_dd_str'
             4174  JUMP_FORWARD       4186  'to 4186'
           4176_0  COME_FROM          4142  '4142'

 L. 942      4176  LOAD_FAST                'utf2display'
             4178  LOAD_FAST                'r'
             4180  LOAD_ATTR                dn_s
             4182  CALL_FUNCTION_1       1  ''
             4184  STORE_FAST               'result_dd_str'
           4186_0  COME_FROM          4174  '4174'
           4186_1  COME_FROM          4134  '4134'
           4186_2  COME_FROM          3930  '3930'

 L. 945      4186  BUILD_LIST_0          0 
             4188  STORE_FAST               'command_table'

 L. 948      4190  LOAD_FAST                'command_table'
             4192  LOAD_METHOD              append

 L. 949      4194  LOAD_DEREF               'app'
             4196  LOAD_METHOD              anchor

 L. 950      4198  LOAD_STR                 'read'

 L. 950      4200  LOAD_STR                 'Read'

 L. 951      4202  LOAD_STR                 'dn'
             4204  LOAD_FAST                'r'
             4206  LOAD_ATTR                dn_s
             4208  BUILD_TUPLE_2         2 
             4210  BUILD_LIST_1          1 

 L. 949      4212  CALL_METHOD_3         3  ''

 L. 948      4214  CALL_METHOD_1         1  ''
             4216  POP_TOP          

 L. 956      4218  LOAD_FAST                'entry'
             4220  LOAD_METHOD              get
             4222  LOAD_STR                 'hasSubordinates'
             4224  LOAD_CONST               b'TRUE'
             4226  BUILD_LIST_1          1 
             4228  CALL_METHOD_2         2  ''
             4230  LOAD_CONST               0
             4232  BINARY_SUBSCR    
             4234  LOAD_METHOD              upper
             4236  CALL_METHOD_0         0  ''
             4238  LOAD_CONST               b'TRUE'
             4240  COMPARE_OP               ==
             4242  STORE_FAST               'hasSubordinates'

 L. 957      4244  SETUP_FINALLY      4288  'to 4288'

 L. 958      4246  LOAD_GLOBAL              int

 L. 959      4248  LOAD_FAST                'entry'
             4250  LOAD_METHOD              get

 L. 960      4252  LOAD_STR                 'subordinateCount'

 L. 961      4254  LOAD_FAST                'entry'
             4256  LOAD_METHOD              get

 L. 962      4258  LOAD_STR                 'numAllSubordinates'

 L. 963      4260  LOAD_FAST                'entry'
             4262  LOAD_METHOD              get
             4264  LOAD_STR                 'msDS-Approx-Immed-Subordinates'
             4266  LOAD_CONST               b'1'
             4268  BUILD_LIST_1          1 
             4270  CALL_METHOD_2         2  ''

 L. 961      4272  CALL_METHOD_2         2  ''

 L. 959      4274  CALL_METHOD_2         2  ''

 L. 963      4276  LOAD_CONST               0

 L. 959      4278  BINARY_SUBSCR    

 L. 958      4280  CALL_FUNCTION_1       1  ''
             4282  STORE_FAST               'subordinateCountFlag'
             4284  POP_BLOCK        
             4286  JUMP_FORWARD       4314  'to 4314'
           4288_0  COME_FROM_FINALLY  4244  '4244'

 L. 965      4288  DUP_TOP          
             4290  LOAD_GLOBAL              ValueError
             4292  COMPARE_OP               exception-match
         4294_4296  POP_JUMP_IF_FALSE  4312  'to 4312'
             4298  POP_TOP          
             4300  POP_TOP          
             4302  POP_TOP          

 L. 966      4304  LOAD_CONST               1
             4306  STORE_FAST               'subordinateCountFlag'
             4308  POP_EXCEPT       
             4310  JUMP_FORWARD       4314  'to 4314'
           4312_0  COME_FROM          4294  '4294'
             4312  END_FINALLY      
           4314_0  COME_FROM          4310  '4310'
           4314_1  COME_FROM          4286  '4286'

 L. 969      4314  LOAD_FAST                'hasSubordinates'
         4316_4318  POP_JUMP_IF_FALSE  4558  'to 4558'
             4320  LOAD_FAST                'subordinateCountFlag'
             4322  LOAD_CONST               0
             4324  COMPARE_OP               >
         4326_4328  POP_JUMP_IF_FALSE  4558  'to 4558'

 L. 971      4330  LOAD_STR                 'List direct subordinates of %s'
             4332  LOAD_FAST                'r'
             4334  LOAD_ATTR                dn_s
             4336  BINARY_MODULO    
             4338  BUILD_LIST_1          1 
             4340  STORE_FAST               'down_title_list'

 L. 974      4342  LOAD_FAST                'entry'
             4344  LOAD_METHOD              get

 L. 975      4346  LOAD_STR                 'numSubOrdinates'

 L. 976      4348  LOAD_FAST                'entry'
             4350  LOAD_METHOD              get

 L. 977      4352  LOAD_STR                 'subordinateCount'

 L. 978      4354  LOAD_FAST                'entry'
             4356  LOAD_METHOD              get

 L. 979      4358  LOAD_STR                 'countImmSubordinates'

 L. 980      4360  LOAD_FAST                'entry'
             4362  LOAD_METHOD              get
           4364_0  COME_FROM          3678  '3678'

 L. 981      4364  LOAD_STR                 'msDS-Approx-Immed-Subordinates'

 L. 982      4366  LOAD_CONST               None
             4368  BUILD_LIST_1          1 

 L. 980      4370  CALL_METHOD_2         2  ''

 L. 978      4372  CALL_METHOD_2         2  ''

 L. 976      4374  CALL_METHOD_2         2  ''

 L. 974      4376  CALL_METHOD_2         2  ''

 L. 982      4378  LOAD_CONST               0

 L. 974      4380  BINARY_SUBSCR    
             4382  STORE_FAST               'numSubOrdinates'

 L. 983      4384  LOAD_FAST                'numSubOrdinates'
             4386  LOAD_CONST               None
             4388  COMPARE_OP               is-not
         4390_4392  POP_JUMP_IF_FALSE  4416  'to 4416'

 L. 984      4394  LOAD_GLOBAL              int
             4396  LOAD_FAST                'numSubOrdinates'
             4398  CALL_FUNCTION_1       1  ''
             4400  STORE_FAST               'numSubOrdinates'

 L. 985      4402  LOAD_FAST                'down_title_list'
             4404  LOAD_METHOD              append
             4406  LOAD_STR                 'direct: %d'
             4408  LOAD_FAST                'numSubOrdinates'
             4410  BINARY_MODULO    
             4412  CALL_METHOD_1         1  ''
             4414  POP_TOP          
           4416_0  COME_FROM          4390  '4390'

 L. 987      4416  LOAD_FAST                'entry'
             4418  LOAD_METHOD              get

 L. 988      4420  LOAD_STR                 'numAllSubOrdinates'

 L. 989      4422  LOAD_FAST                'entry'
             4424  LOAD_METHOD              get
             4426  LOAD_STR                 'countTotSubordinates'
             4428  LOAD_CONST               None
             4430  BUILD_LIST_1          1 
             4432  CALL_METHOD_2         2  ''

 L. 987      4434  CALL_METHOD_2         2  ''

 L. 990      4436  LOAD_CONST               0

 L. 987      4438  BINARY_SUBSCR    
             4440  STORE_FAST               'numAllSubOrdinates'

 L. 991      4442  LOAD_FAST                'numAllSubOrdinates'
             4444  LOAD_CONST               None
             4446  COMPARE_OP               is-not
         4448_4450  POP_JUMP_IF_FALSE  4474  'to 4474'

 L. 992      4452  LOAD_GLOBAL              int
             4454  LOAD_FAST                'numAllSubOrdinates'
             4456  CALL_FUNCTION_1       1  ''
             4458  STORE_FAST               'numAllSubOrdinates'
           4460_0  COME_FROM          3774  '3774'

 L. 993      4460  LOAD_FAST                'down_title_list'
             4462  LOAD_METHOD              append
             4464  LOAD_STR                 'total: %d'
             4466  LOAD_FAST                'numAllSubOrdinates'
             4468  BINARY_MODULO    
             4470  CALL_METHOD_1         1  ''
             4472  POP_TOP          
           4474_0  COME_FROM          4448  '4448'

 L. 995      4474  LOAD_FAST                'command_table'
             4476  LOAD_METHOD              append
             4478  LOAD_DEREF               'app'
             4480  LOAD_ATTR                anchor

 L. 996      4482  LOAD_STR                 'search'

 L. 996      4484  LOAD_STR                 'Down'

 L. 998      4486  LOAD_STR                 'dn'
             4488  LOAD_FAST                'r'
             4490  LOAD_ATTR                dn_s
             4492  BUILD_TUPLE_2         2 

 L. 999      4494  LOAD_STR                 'scope'
             4496  LOAD_GLOBAL              web2ldap
             4498  LOAD_ATTR                app
             4500  LOAD_ATTR                searchform
             4502  LOAD_ATTR                SEARCH_SCOPE_STR_ONELEVEL
             4504  BUILD_TUPLE_2         2 

 L.1000      4506  LOAD_CONST               ('searchform_mode', 'adv')

 L.1001      4508  LOAD_CONST               ('search_attr', 'objectClass')

 L.1002      4510  LOAD_STR                 'search_option'
             4512  LOAD_GLOBAL              web2ldap
             4514  LOAD_ATTR                app
             4516  LOAD_ATTR                searchform
             4518  LOAD_ATTR                SEARCH_OPT_ATTR_EXISTS
             4520  BUILD_TUPLE_2         2 

 L.1003      4522  LOAD_CONST               ('search_string', '')

 L. 997      4524  BUILD_TUPLE_6         6 

 L.1005      4526  LOAD_STR                 '\r\n'
             4528  LOAD_METHOD              join
             4530  LOAD_FAST                'down_title_list'
             4532  CALL_METHOD_1         1  ''

 L. 995      4534  LOAD_CONST               ('title',)
             4536  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
             4538  CALL_METHOD_1         1  ''
             4540  POP_TOP          
             4542  JUMP_FORWARD       4558  'to 4558'
           4544_0  COME_FROM          3882  '3882'

 L.1009      4544  LOAD_GLOBAL              ValueError
             4546  LOAD_STR                 'LDAP result of invalid type: %r'
             4548  LOAD_FAST                'r'
             4550  BUILD_TUPLE_1         1 
             4552  BINARY_MODULO    
             4554  CALL_FUNCTION_1       1  ''
             4556  RAISE_VARARGS_1       1  'exception instance'
           4558_0  COME_FROM          4542  '4542'
           4558_1  COME_FROM          4326  '4326'
           4558_2  COME_FROM          4316  '4316'
           4558_3  COME_FROM          3870  '3870'

 L.1012      4558  LOAD_DEREF               'app'
             4560  LOAD_ATTR                outf
             4562  LOAD_METHOD              write

 L.1013      4564  LOAD_STR                 '\n                    <tr>\n                      <td class="CT">\n%s\n</td>\n                      <td>\n%s\n</td>\n                    </tr>\n                    '

 L.1019      4566  LOAD_STR                 '\n'
             4568  LOAD_METHOD              join
             4570  LOAD_FAST                'command_table'
             4572  CALL_METHOD_1         1  ''

 L.1020      4574  LOAD_FAST                'result_dd_str'

 L.1018      4576  BUILD_TUPLE_2         2 

 L.1013      4578  BINARY_MODULO    

 L.1012      4580  CALL_METHOD_1         1  ''
             4582  POP_TOP          
         4584_4586  JUMP_BACK          3578  'to 3578'

 L.1024      4588  LOAD_DEREF               'app'
             4590  LOAD_ATTR                outf
             4592  LOAD_METHOD              write

 L.1025      4594  LOAD_STR                 '\n                </table>\n                <a id="params"></a>\n                %s\n                  <h3>Export to other formats</h3>\n                  <p>%s &nbsp; Include operational attributes %s</p>\n                  <p><input type="submit" value="Export"></p>\n                </form>\n                '

 L.1034      4596  LOAD_STR                 '\n'
             4598  LOAD_METHOD              join

 L.1035      4600  LOAD_DEREF               'app'
             4602  LOAD_ATTR                begin_form
             4604  LOAD_STR                 'search'
             4606  LOAD_STR                 'GET'
             4608  LOAD_STR                 'web2ldapexport'
             4610  LOAD_CONST               ('target',)
             4612  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L.1036      4614  LOAD_DEREF               'app'
             4616  LOAD_ATTR                form
             4618  LOAD_METHOD              hiddenFieldHTML
             4620  LOAD_STR                 'dn'
             4622  LOAD_DEREF               'app'
             4624  LOAD_ATTR                dn
             4626  LOAD_STR                 ''
             4628  CALL_METHOD_3         3  ''

 L.1037      4630  LOAD_DEREF               'app'
             4632  LOAD_ATTR                form
             4634  LOAD_METHOD              hiddenFieldHTML
             4636  LOAD_STR                 'search_root'
             4638  LOAD_FAST                'search_root'
             4640  LOAD_STR                 ''
             4642  CALL_METHOD_3         3  ''

 L.1038      4644  LOAD_DEREF               'app'
             4646  LOAD_ATTR                form
             4648  LOAD_METHOD              hiddenFieldHTML
             4650  LOAD_STR                 'scope'
             4652  LOAD_GLOBAL              str
             4654  LOAD_DEREF               'scope'
             4656  CALL_FUNCTION_1       1  ''
             4658  LOAD_STR                 ''
             4660  CALL_METHOD_3         3  ''

 L.1039      4662  LOAD_DEREF               'app'
             4664  LOAD_ATTR                form
             4666  LOAD_METHOD              hiddenFieldHTML
             4668  LOAD_STR                 'filterstr'
             4670  LOAD_FAST                'filterstr'
             4672  LOAD_STR                 ''
             4674  CALL_METHOD_3         3  ''

 L.1040      4676  LOAD_DEREF               'app'
             4678  LOAD_ATTR                form
             4680  LOAD_METHOD              hiddenFieldHTML
             4682  LOAD_STR                 'search_lastmod'
             4684  LOAD_GLOBAL              str
             4686  LOAD_FAST                'search_lastmod'
             4688  CALL_FUNCTION_1       1  ''
             4690  LOAD_STR                 ''
             4692  CALL_METHOD_3         3  ''

 L.1041      4694  LOAD_DEREF               'app'
             4696  LOAD_ATTR                form
             4698  LOAD_METHOD              hiddenFieldHTML
             4700  LOAD_STR                 'search_resnumber'
             4702  LOAD_STR                 '0'
             4704  LOAD_STR                 ''
             4706  CALL_METHOD_3         3  ''

 L.1042      4708  LOAD_DEREF               'app'
             4710  LOAD_ATTR                form
             4712  LOAD_METHOD              hiddenFieldHTML
             4714  LOAD_STR                 'search_attrs'
             4716  LOAD_STR                 ','
             4718  LOAD_METHOD              join
             4720  LOAD_DEREF               'search_attrs'
             4722  CALL_METHOD_1         1  ''
             4724  LOAD_STR                 ''
             4726  CALL_METHOD_3         3  ''

 L.1034      4728  BUILD_TUPLE_8         8 
             4730  CALL_METHOD_1         1  ''

 L.1044      4732  LOAD_FAST                'export_field'
             4734  LOAD_METHOD              input_html
             4736  CALL_METHOD_0         0  ''

 L.1045      4738  LOAD_GLOBAL              web2ldap
             4740  LOAD_ATTR                app
             4742  LOAD_ATTR                form
             4744  LOAD_METHOD              InclOpAttrsCheckbox
             4746  CALL_METHOD_0         0  ''
             4748  LOAD_METHOD              input_html
             4750  CALL_METHOD_0         0  ''

 L.1033      4752  BUILD_TUPLE_3         3 

 L.1025      4754  BINARY_MODULO    

 L.1024      4756  CALL_METHOD_1         1  ''
             4758  POP_TOP          

 L.1049      4760  LOAD_DEREF               'app'
             4762  LOAD_ATTR                outf
             4764  LOAD_METHOD              write

 L.1050      4766  LOAD_STR                 '\n                <h3>Search parameters used</h3>\n                %s\n                <p>\n                  Equivalent OpenLDAP command:<br>\n                  <input value="%s" size="60" readonly>\n                </p>\n                '

 L.1058      4768  LOAD_FAST                'search_param_html'

 L.1059      4770  LOAD_FAST                'utf2display'
             4772  LOAD_FAST                'ldap_search_command'
             4774  CALL_FUNCTION_1       1  ''

 L.1057      4776  BUILD_TUPLE_2         2 

 L.1050      4778  BINARY_MODULO    

 L.1049      4780  CALL_METHOD_1         1  ''
             4782  POP_TOP          

 L.1063      4784  LOAD_GLOBAL              web2ldap
             4786  LOAD_ATTR                app
             4788  LOAD_ATTR                gui
             4790  LOAD_METHOD              footer
             4792  LOAD_DEREF               'app'
             4794  CALL_METHOD_1         1  ''
             4796  POP_TOP          
             4798  JUMP_FORWARD       4852  'to 4852'
           4800_0  COME_FROM          1918  '1918'

 L.1068      4800  SETUP_FINALLY      4814  'to 4814'

 L.1069      4802  LOAD_FAST                'result_handler'
             4804  LOAD_METHOD              process_results
             4806  CALL_METHOD_0         0  ''
             4808  POP_TOP          
             4810  POP_BLOCK        
             4812  JUMP_FORWARD       4852  'to 4852'
           4814_0  COME_FROM_FINALLY  4800  '4800'

 L.1070      4814  DUP_TOP          

 L.1071      4816  LOAD_GLOBAL              ldap0
             4818  LOAD_ATTR                SIZELIMIT_EXCEEDED

 L.1072      4820  LOAD_GLOBAL              ldap0
             4822  LOAD_ATTR                ADMINLIMIT_EXCEEDED

 L.1070      4824  BUILD_TUPLE_2         2 
             4826  COMPARE_OP               exception-match
         4828_4830  POP_JUMP_IF_FALSE  4850  'to 4850'
             4832  POP_TOP          
             4834  POP_TOP          
             4836  POP_TOP          

 L.1074      4838  LOAD_FAST                'result_handler'
             4840  LOAD_METHOD              post_processing
             4842  CALL_METHOD_0         0  ''
             4844  POP_TOP          
             4846  POP_EXCEPT       
             4848  JUMP_FORWARD       4852  'to 4852'
           4850_0  COME_FROM          4828  '4828'
             4850  END_FINALLY      
           4852_0  COME_FROM          4848  '4848'
           4852_1  COME_FROM          4812  '4812'
           4852_2  COME_FROM          4798  '4798'

Parse error at or near `COME_FROM' instruction at offset 356_0