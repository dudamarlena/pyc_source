# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sch/prj/pytigon/pytigon/prj/schpolb/applib/raportylib/send_report.py
# Compiled at: 2020-03-19 14:28:10
# Size of source mod 2**32: 12289 bytes
from schreports.models import CommonGroup
from django.conf import settings
from django.db import connection
from django.core.mail import send_mail, EmailMessage, EmailMultiAlternatives
from pytigon_lib.schparser.html_parsers import SimpleTabParserBase
from pytigon_lib.schdjangoext.render import render_doc
import io, zipfile, datetime, requests, logging
logger = logging.getLogger('pytigon_task')
MAIL_CONTENT = '\nW załączeniu raport odświeżany i wysyłany automatycznie. W razie uwag proszę o kontakt z osobami:\n- Sławomir Chołaj (slawomir.cholaj@polbruk.pl) - 502 620 952\n- Robert Cmiel (robert.cmiel@polbruk.pl) - 694 485 136\n\nPolbruk S.A. Siedziba Spółki: 80-299 Gdańsk, ul. Nowy Świat 16 c, tel. 58 554 97 45, fax 58 554 59 50\nNIP: 584-025-35-91 | Sąd Rejonowy Gdańsk-Północ w Gdańsku, VII Wydz. Gospodarczy KRS, KRS: 0000062419 |Regon: 001388727 | Wysokość kapitału zakładowego: 31 766 250,00 zł\nOtrzymana przez Panią / Pana wiadomość oraz załączone do niej pliki stanowią tajemnicę Przedsiębiorstwa i są przeznaczone tylko dla wymienionych adresatów. \nJeżeli nie są Państwo zamierzonym odbiorcą, proszę poinformować o tym fakcie nadawcę oraz usunąć wiadomość ze swojego systemu. Nie powinni Państwo również nikomu ujawniać otrzymanych \ninformacji ani sporządzać / zachowywać / dystrybuować żadnej kopii otrzymanych informacji. | This message and any attachments are confidential as a business secret and are intended solely for the \nuse of the individual or entity to whom they are addressed. If you are not the intended recipient, please telephone or e-mail the sender and delete this message and any attachment from your system. \nAlso, if you are not the intended recipient you should not disclose the content or take / retain / distribute any copies. \nZanim wydrukujesz wiadomość - pomyśl o środowisku. Please consider the environment before printing out this e-mail.\n'
import os, pendulum
from pytigon_lib.schfs.vfstools import get_temp_filename
from pytigon_lib.schtools.process import py_run

def _d2s(date):
    return date.isoformat()[:10].replace('-', '').replace('.', '')


def _replace(s, date, param):
    ret = s
    date_alt = date.add(days=(-15))
    replace_tab = (
     (
      'date', _d2s(date)),
     (
      'today', _d2s(date)),
     (
      'start_of_year', _d2s(date_alt.replace(month=1, day=1))),
     (
      'end_of_year', _d2s(date_alt.replace(year=(date_alt.year + 1), month=1, day=1).add(days=(-1)))),
     (
      'start_of_current_year', _d2s(date.replace(month=1, day=1))),
     (
      'end_of_current_year', _d2s(date.replace(year=(date.year + 1), month=1, day=1).add(days=(-1)))),
     (
      'start_of_month', _d2s(date.replace(day=1))),
     (
      'end_of_month', _d2s(date.replace(day=1).add(months=1).add(days=(-1)))),
     (
      'start_of_last_month', _d2s(date.replace(day=1).add(months=(-1)))),
     (
      'end_of_last_month', _d2s(date.replace(day=1).add(days=(-1)))),
     (
      'start_of_next_month', _d2s(date.replace(day=1).add(months=1))),
     (
      'end_of_next_month', _d2s(date.add(months=2).replace(day=1).add(days=(-1)))),
     (
      'param', param))
    for pos in replace_tab:
        d1 = pos[1]
        d2 = d1[:4] + '-' + d1[4:6] + '-' + d1[6:]
        ret = ret.replace('[[' + pos[0] + '_str]]', d2)
        ret = ret.replace('{{' + pos[0] + '_str}}', d2)
        ret = ret.replace('[[' + pos[0] + ']]', d1)
        ret = ret.replace('{{' + pos[0] + '}}', d1)

    return ret


def gen_report--- This code section failed: ---

 L.  89         0  LOAD_GLOBAL              CommonGroup
                2  LOAD_ATTR                objects
                4  LOAD_ATTR                filter
                6  LOAD_STR                 'SimpleReport'
                8  LOAD_FAST                'report_name'
               10  LOAD_CONST               ('group_def_name', 'title')
               12  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               14  STORE_FAST               'reports'

 L.  90        16  LOAD_GLOBAL              len
               18  LOAD_FAST                'reports'
               20  CALL_FUNCTION_1       1  '1 positional argument'
               22  LOAD_CONST               1
               24  COMPARE_OP               !=
               26  POP_JUMP_IF_FALSE    32  'to 32'

 L.  91        28  LOAD_CONST               None
               30  RETURN_VALUE     
             32_0  COME_FROM            26  '26'

 L.  92        32  LOAD_FAST                'reports'
               34  LOAD_CONST               0
               36  BINARY_SUBSCR    
               38  STORE_FAST               'report'

 L.  94        40  LOAD_GLOBAL              logger
               42  LOAD_METHOD              info
               44  LOAD_STR                 'Start report: '
               46  LOAD_FAST                'report_name'
               48  FORMAT_VALUE          0  ''
               50  BUILD_STRING_2        2 
               52  CALL_METHOD_1         1  '1 positional argument'
               54  POP_TOP          

 L.  96        56  LOAD_FAST                'report'
               58  LOAD_ATTR                json_code
               60  POP_JUMP_IF_FALSE    72  'to 72'

 L.  97        62  LOAD_GLOBAL              exec
               64  LOAD_FAST                'report'
               66  LOAD_ATTR                json_code
               68  CALL_FUNCTION_1       1  '1 positional argument'
               70  POP_TOP          
             72_0  COME_FROM            60  '60'

 L.  99        72  LOAD_GLOBAL              locals
               74  CALL_FUNCTION_0       0  '0 positional arguments'
               76  LOAD_METHOD              get
               78  LOAD_STR                 'init'
               80  LOAD_CONST               None
               82  CALL_METHOD_2         2  '2 positional arguments'
               84  STORE_FAST               'fun'

 L. 100        86  LOAD_FAST                'fun'
               88  POP_JUMP_IF_FALSE   112  'to 112'

 L. 101        90  LOAD_FAST                'fun'
               92  CALL_FUNCTION_0       0  '0 positional arguments'
               94  STORE_FAST               'x'

 L. 102        96  LOAD_STR                 'date_gen'
               98  LOAD_FAST                'x'
              100  COMPARE_OP               in
              102  POP_JUMP_IF_FALSE   112  'to 112'

 L. 103       104  LOAD_FAST                'x'
              106  LOAD_STR                 'date_gen'
              108  BINARY_SUBSCR    
              110  STORE_FAST               'date_gen'
            112_0  COME_FROM           102  '102'
            112_1  COME_FROM            88  '88'

 L. 105       112  BUILD_LIST_0          0 
              114  STORE_FAST               'ret_files'

 L. 107       116  LOAD_FAST                'date_gen'
              118  LOAD_CONST               None
              120  COMPARE_OP               ==
              122  POP_JUMP_IF_FALSE   132  'to 132'

 L. 108       124  LOAD_GLOBAL              pendulum
              126  LOAD_METHOD              now
              128  CALL_METHOD_0         0  '0 positional arguments'
              130  STORE_FAST               'date_gen'
            132_0  COME_FROM           122  '122'

 L. 109       132  LOAD_FAST                'date'
              134  LOAD_CONST               None
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   144  'to 144'

 L. 110       140  LOAD_FAST                'date_gen'
              142  STORE_FAST               'date'
            144_0  COME_FROM           138  '138'

 L. 114       144  LOAD_FAST                'date_gen'
              146  LOAD_METHOD              isoformat
              148  CALL_METHOD_0         0  '0 positional arguments'
              150  LOAD_CONST               None
              152  LOAD_CONST               10
              154  BUILD_SLICE_2         2 
              156  BINARY_SUBSCR    
              158  STORE_FAST               'date_gen_str'

 L. 115       160  LOAD_FAST                'date_gen'
              162  LOAD_METHOD              isoformat
              164  CALL_METHOD_0         0  '0 positional arguments'
              166  LOAD_CONST               None
              168  LOAD_CONST               16
              170  BUILD_SLICE_2         2 
              172  BINARY_SUBSCR    
              174  LOAD_METHOD              replace
              176  LOAD_STR                 'T'
              178  LOAD_STR                 ' '
              180  CALL_METHOD_2         2  '2 positional arguments'
              182  STORE_FAST               'datetime_gen_str'

 L. 117       184  LOAD_FAST                'date_gen_str'
              186  LOAD_CONST               None
              188  LOAD_CONST               4
              190  BUILD_SLICE_2         2 
              192  BINARY_SUBSCR    
              194  STORE_FAST               'date_gen_year'

 L. 118       196  LOAD_FAST                'date_gen_str'
              198  LOAD_CONST               5
              200  LOAD_CONST               7
              202  BUILD_SLICE_2         2 
              204  BINARY_SUBSCR    
              206  STORE_FAST               'date_gen_month'

 L. 119       208  LOAD_FAST                'date_gen_str'
              210  LOAD_CONST               None
              212  LOAD_CONST               10
              214  BUILD_SLICE_2         2 
              216  BINARY_SUBSCR    
              218  LOAD_METHOD              replace
              220  LOAD_STR                 '-'
              222  LOAD_STR                 ''
              224  CALL_METHOD_2         2  '2 positional arguments'
              226  LOAD_METHOD              replace
              228  LOAD_STR                 '.'
              230  LOAD_STR                 ''
              232  CALL_METHOD_2         2  '2 positional arguments'
              234  STORE_FAST               'date_gen_id'

 L. 121       236  LOAD_STR                 ''
              238  STORE_FAST               'param'

 L. 123       240  LOAD_FAST                'report_type'
          242_244  POP_JUMP_IF_TRUE    266  'to 266'

 L. 124       246  LOAD_FAST                'report'
              248  LOAD_ATTR                json_rep_type
              250  LOAD_METHOD              split
              252  LOAD_STR                 '.'
              254  CALL_METHOD_1         1  '1 positional argument'
              256  LOAD_CONST               -1
              258  BINARY_SUBSCR    
              260  LOAD_METHOD              strip
              262  CALL_METHOD_0         0  '0 positional arguments'
              264  STORE_FAST               'report_type'
            266_0  COME_FROM           242  '242'

 L. 126       266  LOAD_FAST                'destination'
          268_270  POP_JUMP_IF_TRUE    292  'to 292'

 L. 127       272  LOAD_FAST                'report'
              274  LOAD_ATTR                json_dest
              276  LOAD_METHOD              split
              278  LOAD_STR                 '.'
              280  CALL_METHOD_1         1  '1 positional argument'
              282  LOAD_CONST               0
              284  BINARY_SUBSCR    
              286  LOAD_METHOD              strip
              288  CALL_METHOD_0         0  '0 positional arguments'
              290  STORE_FAST               'destination'
            292_0  COME_FROM           268  '268'

 L. 129       292  LOAD_FAST                'report'
              294  LOAD_ATTR                json_columns
              296  LOAD_METHOD              split
              298  LOAD_STR                 ';'
              300  CALL_METHOD_1         1  '1 positional argument'
              302  STORE_FAST               'columns'

 L. 130       304  LOAD_CONST               0
              306  STORE_FAST               'width_sum'

 L. 131       308  BUILD_LIST_0          0 
              310  STORE_FAST               'columns2'

 L. 132       312  BUILD_LIST_0          0 
              314  STORE_FAST               'width'

 L. 133       316  SETUP_LOOP          428  'to 428'
              318  LOAD_FAST                'columns'
              320  GET_ITER         
              322  FOR_ITER            426  'to 426'
              324  STORE_FAST               'pos'

 L. 134       326  LOAD_FAST                'pos'
              328  LOAD_METHOD              split
              330  LOAD_STR                 ':'
              332  CALL_METHOD_1         1  '1 positional argument'
              334  STORE_FAST               'c'

 L. 135       336  LOAD_FAST                'columns2'
              338  LOAD_METHOD              append
              340  LOAD_FAST                'c'
              342  LOAD_CONST               0
              344  BINARY_SUBSCR    
              346  CALL_METHOD_1         1  '1 positional argument'
              348  POP_TOP          

 L. 136       350  LOAD_GLOBAL              len
              352  LOAD_FAST                'c'
              354  CALL_FUNCTION_1       1  '1 positional argument'
              356  LOAD_CONST               1
              358  COMPARE_OP               >
          360_362  POP_JUMP_IF_FALSE   400  'to 400'

 L. 137       364  SETUP_EXCEPT        382  'to 382'

 L. 138       366  LOAD_GLOBAL              int
              368  LOAD_FAST                'c'
              370  LOAD_CONST               1
              372  BINARY_SUBSCR    
              374  CALL_FUNCTION_1       1  '1 positional argument'
              376  STORE_FAST               'w'
              378  POP_BLOCK        
              380  JUMP_FORWARD        398  'to 398'
            382_0  COME_FROM_EXCEPT    364  '364'

 L. 139       382  POP_TOP          
              384  POP_TOP          
              386  POP_TOP          

 L. 140       388  LOAD_CONST               0
              390  STORE_FAST               'w'
              392  POP_EXCEPT       
              394  JUMP_FORWARD        398  'to 398'
              396  END_FINALLY      
            398_0  COME_FROM           394  '394'
            398_1  COME_FROM           380  '380'
              398  JUMP_FORWARD        404  'to 404'
            400_0  COME_FROM           360  '360'

 L. 142       400  LOAD_CONST               0
              402  STORE_FAST               'w'
            404_0  COME_FROM           398  '398'

 L. 143       404  LOAD_FAST                'width'
              406  LOAD_METHOD              append
              408  LOAD_FAST                'w'
              410  CALL_METHOD_1         1  '1 positional argument'
              412  POP_TOP          

 L. 144       414  LOAD_FAST                'width_sum'
              416  LOAD_FAST                'w'
              418  INPLACE_ADD      
              420  STORE_FAST               'width_sum'
          422_424  JUMP_BACK           322  'to 322'
              426  POP_BLOCK        
            428_0  COME_FROM_LOOP      316  '316'

 L. 146       428  LOAD_FAST                'width_sum'
              430  LOAD_CONST               100
              432  COMPARE_OP               <
          434_436  POP_JUMP_IF_FALSE   558  'to 558'

 L. 147       438  LOAD_CONST               0
              440  STORE_FAST               'c'

 L. 148       442  SETUP_LOOP          476  'to 476'
              444  LOAD_FAST                'width'
              446  GET_ITER         
            448_0  COME_FROM           458  '458'
              448  FOR_ITER            474  'to 474'
              450  STORE_FAST               'pos'

 L. 149       452  LOAD_FAST                'pos'
              454  LOAD_CONST               0
              456  COMPARE_OP               ==
          458_460  POP_JUMP_IF_FALSE   448  'to 448'

 L. 150       462  LOAD_FAST                'c'
              464  LOAD_CONST               1
              466  INPLACE_ADD      
              468  STORE_FAST               'c'
          470_472  JUMP_BACK           448  'to 448'
              474  POP_BLOCK        
            476_0  COME_FROM_LOOP      442  '442'

 L. 151       476  LOAD_FAST                'c'
              478  LOAD_CONST               0
              480  COMPARE_OP               >
          482_484  POP_JUMP_IF_FALSE   558  'to 558'

 L. 152       486  LOAD_GLOBAL              int
              488  LOAD_CONST               100
              490  LOAD_FAST                'width_sum'
              492  BINARY_SUBTRACT  
              494  LOAD_FAST                'c'
              496  BINARY_TRUE_DIVIDE
              498  CALL_FUNCTION_1       1  '1 positional argument'
              500  STORE_FAST               'dx'

 L. 153       502  BUILD_LIST_0          0 
              504  STORE_FAST               'width2'

 L. 154       506  SETUP_LOOP          554  'to 554'
              508  LOAD_FAST                'width'
              510  GET_ITER         
              512  FOR_ITER            552  'to 552'
              514  STORE_FAST               'pos'

 L. 155       516  LOAD_FAST                'pos'
              518  LOAD_CONST               0
              520  COMPARE_OP               ==
          522_524  POP_JUMP_IF_FALSE   538  'to 538'

 L. 156       526  LOAD_FAST                'width2'
              528  LOAD_METHOD              append
              530  LOAD_FAST                'dx'
              532  CALL_METHOD_1         1  '1 positional argument'
              534  POP_TOP          
              536  JUMP_BACK           512  'to 512'
            538_0  COME_FROM           522  '522'

 L. 158       538  LOAD_FAST                'width2'
              540  LOAD_METHOD              append
              542  LOAD_FAST                'pos'
              544  CALL_METHOD_1         1  '1 positional argument'
              546  POP_TOP          
          548_550  JUMP_BACK           512  'to 512'
              552  POP_BLOCK        
            554_0  COME_FROM_LOOP      506  '506'

 L. 159       554  LOAD_FAST                'width2'
              556  STORE_FAST               'width'
            558_0  COME_FROM           482  '482'
            558_1  COME_FROM           434  '434'

 L. 161       558  BUILD_LIST_0          0 
              560  STORE_FAST               'columns'

 L. 162       562  SETUP_LOOP          608  'to 608'
              564  LOAD_GLOBAL              range
              566  LOAD_GLOBAL              len
              568  LOAD_FAST                'columns2'
              570  CALL_FUNCTION_1       1  '1 positional argument'
              572  CALL_FUNCTION_1       1  '1 positional argument'
              574  GET_ITER         
              576  FOR_ITER            606  'to 606'
              578  STORE_FAST               'i'

 L. 163       580  LOAD_FAST                'columns'
              582  LOAD_METHOD              append
              584  LOAD_FAST                'columns2'
              586  LOAD_FAST                'i'
              588  BINARY_SUBSCR    
              590  LOAD_FAST                'width'
              592  LOAD_FAST                'i'
              594  BINARY_SUBSCR    
              596  BUILD_TUPLE_2         2 
              598  CALL_METHOD_1         1  '1 positional argument'
              600  POP_TOP          
          602_604  JUMP_BACK           576  'to 576'
              606  POP_BLOCK        
            608_0  COME_FROM_LOOP      562  '562'

 L. 165       608  LOAD_STR                 'select'
              610  LOAD_FAST                'report'
              612  LOAD_ATTR                json_mail
              614  LOAD_METHOD              lower
              616  CALL_METHOD_0         0  '0 positional arguments'
              618  COMPARE_OP               in
          620_622  POP_JUMP_IF_FALSE   786  'to 786'

 L. 166       624  LOAD_GLOBAL              _replace
              626  LOAD_FAST                'report'
              628  LOAD_ATTR                json_mail
              630  LOAD_FAST                'date'
              632  LOAD_STR                 ''
              634  CALL_FUNCTION_3       3  '3 positional arguments'
              636  STORE_FAST               'sel'

 L. 167       638  LOAD_STR                 'mysql'
              640  LOAD_FAST                'sel'
              642  COMPARE_OP               in
          644_646  POP_JUMP_IF_FALSE   676  'to 676'

 L. 168       648  LOAD_GLOBAL              connection
              650  LOAD_METHOD              cursor
              652  CALL_METHOD_0         0  '0 positional arguments'
              654  STORE_FAST               'cursor'

 L. 169       656  LOAD_FAST                'cursor'
              658  LOAD_METHOD              execute
              660  LOAD_FAST                'sel'
              662  CALL_METHOD_1         1  '1 positional argument'
              664  POP_TOP          

 L. 170       666  LOAD_FAST                'cursor'
              668  LOAD_METHOD              fetchall
              670  CALL_METHOD_0         0  '0 positional arguments'
              672  STORE_FAST               'parameters'
              674  JUMP_FORWARD        784  'to 784'
            676_0  COME_FROM           644  '644'

 L. 171       676  LOAD_STR                 'http'
              678  LOAD_FAST                'sel'
              680  COMPARE_OP               in
          682_684  POP_JUMP_IF_FALSE   748  'to 748'
              686  LOAD_STR                 '://'
              688  LOAD_FAST                'sel'
              690  COMPARE_OP               in
          692_694  POP_JUMP_IF_FALSE   748  'to 748'

 L. 172       696  LOAD_GLOBAL              requests
              698  LOAD_METHOD              get
              700  LOAD_FAST                'sel'
              702  CALL_METHOD_1         1  '1 positional argument'
              704  STORE_FAST               'r'

 L. 173       706  LOAD_FAST                'r'
              708  LOAD_ATTR                text
              710  STORE_FAST               'p'

 L. 174       712  LOAD_GLOBAL              SimpleTabParserBase
              714  CALL_FUNCTION_0       0  '0 positional arguments'
              716  STORE_FAST               'parser'

 L. 175       718  LOAD_FAST                'parser'
              720  LOAD_METHOD              feed
              722  LOAD_FAST                'p'
              724  CALL_METHOD_1         1  '1 positional argument'
              726  POP_TOP          

 L. 176       728  LOAD_FAST                'parser'
              730  LOAD_ATTR                tables
              732  LOAD_CONST               0
              734  BINARY_SUBSCR    
              736  LOAD_CONST               1
              738  LOAD_CONST               None
              740  BUILD_SLICE_2         2 
              742  BINARY_SUBSCR    
              744  STORE_FAST               'parameters'
              746  JUMP_FORWARD        784  'to 784'
            748_0  COME_FROM           692  '692'
            748_1  COME_FROM           682  '682'

 L. 178       748  LOAD_GLOBAL              settings
              750  LOAD_ATTR                DB
              752  SETUP_WITH          778  'to 778'
              754  STORE_FAST               'db'

 L. 179       756  LOAD_FAST                'db'
              758  LOAD_METHOD              execute
              760  LOAD_FAST                'sel'
              762  CALL_METHOD_1         1  '1 positional argument'
              764  POP_TOP          

 L. 180       766  LOAD_FAST                'db'
              768  LOAD_METHOD              fetchall
              770  CALL_METHOD_0         0  '0 positional arguments'
              772  STORE_FAST               'parameters'
              774  POP_BLOCK        
              776  LOAD_CONST               None
            778_0  COME_FROM_WITH      752  '752'
              778  WITH_CLEANUP_START
              780  WITH_CLEANUP_FINISH
              782  END_FINALLY      
            784_0  COME_FROM           746  '746'
            784_1  COME_FROM           674  '674'
              784  JUMP_FORWARD        798  'to 798'
            786_0  COME_FROM           620  '620'

 L. 182       786  LOAD_STR                 ''
              788  LOAD_FAST                'report'
              790  LOAD_ATTR                json_mail
              792  BUILD_TUPLE_2         2 
              794  BUILD_TUPLE_1         1 
              796  STORE_FAST               'parameters'
            798_0  COME_FROM           784  '784'

 L. 184       798  LOAD_CONST               0
              800  STORE_FAST               'count'

 L. 185   802_804  SETUP_LOOP         1948  'to 1948'
              806  LOAD_FAST                'parameters'
              808  GET_ITER         
            810_0  COME_FROM          1884  '1884'
          810_812  FOR_ITER           1946  'to 1946'
              814  UNPACK_SEQUENCE_2     2 
              816  STORE_FAST               'param'
              818  STORE_FAST               'mail'

 L. 186       820  LOAD_LISTCOMP            '<code_object <listcomp>>'
              822  LOAD_STR                 'gen_report.<locals>.<listcomp>'
              824  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              826  LOAD_FAST                'mail'
              828  LOAD_METHOD              split
              830  LOAD_STR                 ';'
              832  CALL_METHOD_1         1  '1 positional argument'
              834  GET_ITER         
              836  CALL_FUNCTION_1       1  '1 positional argument'
              838  STORE_FAST               'mail_to'

 L. 187       840  LOAD_GLOBAL              _replace
              842  LOAD_FAST                'report'
              844  LOAD_ATTR                json_select
              846  LOAD_FAST                'date'
              848  LOAD_FAST                'param'
              850  CALL_FUNCTION_3       3  '3 positional arguments'
              852  STORE_FAST               'sel'

 L. 188       854  LOAD_GLOBAL              _replace
              856  LOAD_FAST                'report'
              858  LOAD_ATTR                json_desc
              860  LOAD_FAST                'date'
              862  LOAD_FAST                'param'
              864  CALL_FUNCTION_3       3  '3 positional arguments'
              866  STORE_FAST               'desc'

 L. 189       868  LOAD_FAST                'desc'
              870  LOAD_METHOD              split
              872  LOAD_STR                 '<'
              874  CALL_METHOD_1         1  '1 positional argument'
              876  LOAD_CONST               0
              878  BINARY_SUBSCR    
              880  STORE_FAST               'desc2'

 L. 191       882  LOAD_CONST               None
              884  STORE_FAST               'attachment_name'

 L. 193       886  LOAD_STR                 'to_print'
              888  LOAD_FAST                'sel'
              890  COMPARE_OP               in
          892_894  POP_JUMP_IF_FALSE  1114  'to 1114'

 L. 194       896  LOAD_FAST                'param'
          898_900  POP_JUMP_IF_FALSE   916  'to 916'

 L. 195       902  LOAD_FAST                'sel'
              904  LOAD_STR                 '&param='
              906  BINARY_ADD       
              908  LOAD_FAST                'param'
              910  BINARY_ADD       
              912  STORE_FAST               'address'
              914  JUMP_FORWARD        920  'to 920'
            916_0  COME_FROM           898  '898'

 L. 197       916  LOAD_FAST                'sel'
              918  STORE_FAST               'address'
            920_0  COME_FROM           914  '914'

 L. 198       920  LOAD_FAST                'report_type'
              922  LOAD_STR                 'pdf'
              924  COMPARE_OP               ==
          926_928  POP_JUMP_IF_FALSE  1684  'to 1684'
              930  LOAD_FAST                'destination'
              932  LOAD_STR                 '2'
              934  COMPARE_OP               !=
          936_938  POP_JUMP_IF_FALSE  1684  'to 1684'

 L. 199       940  LOAD_GLOBAL              get_temp_filename
              942  CALL_FUNCTION_0       0  '0 positional arguments'
              944  STORE_FAST               'temp_file_name'

 L. 200       946  LOAD_GLOBAL              os
              948  LOAD_ATTR                path
              950  LOAD_METHOD              dirname
              952  LOAD_GLOBAL              os
              954  LOAD_ATTR                path
              956  LOAD_METHOD              abspath
              958  LOAD_GLOBAL              __file__
              960  CALL_METHOD_1         1  '1 positional argument'
              962  CALL_METHOD_1         1  '1 positional argument'
              964  STORE_FAST               'base_path'

 L. 201       966  LOAD_GLOBAL              os
              968  LOAD_ATTR                path
              970  LOAD_METHOD              join
              972  LOAD_FAST                'base_path'
              974  LOAD_STR                 'gen_pdf.py'
              976  CALL_METHOD_2         2  '2 positional arguments'
              978  STORE_FAST               'pypath'

 L. 202       980  LOAD_GLOBAL              py_run
              982  LOAD_FAST                'pypath'
              984  LOAD_FAST                'address'
              986  LOAD_FAST                'temp_file_name'
              988  BUILD_LIST_3          3 
              990  CALL_FUNCTION_1       1  '1 positional argument'
              992  UNPACK_SEQUENCE_3     3 
              994  STORE_FAST               'ret_code'
              996  STORE_FAST               'info_tab'
              998  STORE_FAST               'err_tab'

 L. 203      1000  LOAD_FAST                'info_tab'
         1002_1004  POP_JUMP_IF_FALSE  1032  'to 1032'

 L. 204      1006  SETUP_LOOP         1032  'to 1032'
             1008  LOAD_FAST                'info_tab'
             1010  GET_ITER         
             1012  FOR_ITER           1030  'to 1030'
             1014  STORE_FAST               'pos'

 L. 205      1016  LOAD_GLOBAL              print
             1018  LOAD_STR                 'INFO: '
             1020  LOAD_FAST                'pos'
             1022  CALL_FUNCTION_2       2  '2 positional arguments'
             1024  POP_TOP          
         1026_1028  JUMP_BACK          1012  'to 1012'
             1030  POP_BLOCK        
           1032_0  COME_FROM_LOOP     1006  '1006'
           1032_1  COME_FROM          1002  '1002'

 L. 206      1032  LOAD_FAST                'err_tab'
         1034_1036  POP_JUMP_IF_FALSE  1064  'to 1064'

 L. 207      1038  SETUP_LOOP         1064  'to 1064'
             1040  LOAD_FAST                'err_tab'
             1042  GET_ITER         
             1044  FOR_ITER           1062  'to 1062'
             1046  STORE_FAST               'pos'

 L. 208      1048  LOAD_GLOBAL              print
             1050  LOAD_STR                 'ERR: '
             1052  LOAD_FAST                'pos'
             1054  CALL_FUNCTION_2       2  '2 positional arguments'
             1056  POP_TOP          
         1058_1060  JUMP_BACK          1044  'to 1044'
             1062  POP_BLOCK        
           1064_0  COME_FROM_LOOP     1038  '1038'
           1064_1  COME_FROM          1034  '1034'

 L. 209      1064  LOAD_GLOBAL              open
             1066  LOAD_FAST                'temp_file_name'
             1068  LOAD_STR                 'rb'
             1070  CALL_FUNCTION_2       2  '2 positional arguments'
             1072  SETUP_WITH         1088  'to 1088'
             1074  STORE_FAST               'f'

 L. 210      1076  LOAD_FAST                'f'
             1078  LOAD_METHOD              read
             1080  CALL_METHOD_0         0  '0 positional arguments'
             1082  STORE_FAST               'content'
             1084  POP_BLOCK        
             1086  LOAD_CONST               None
           1088_0  COME_FROM_WITH     1072  '1072'
             1088  WITH_CLEANUP_START
             1090  WITH_CLEANUP_FINISH
             1092  END_FINALLY      

 L. 211      1094  LOAD_STR                 'pdf'
             1096  STORE_FAST               'doc_type'

 L. 212      1098  LOAD_STR                 'application/pdf'
             1100  LOAD_STR                 ''
             1102  LOAD_CONST               ('Content-Type', 'Content-Disposition')
             1104  BUILD_CONST_KEY_MAP_2     2 
             1106  STORE_FAST               'attrs'
             1108  JUMP_FORWARD       1684  'to 1684'

 L. 214  1110_1112  JUMP_FORWARD       1684  'to 1684'
           1114_0  COME_FROM           892  '892'

 L. 217      1114  LOAD_STR                 'mysql'
             1116  LOAD_FAST                'sel'
             1118  COMPARE_OP               in
         1120_1122  POP_JUMP_IF_FALSE  1152  'to 1152'

 L. 218      1124  LOAD_GLOBAL              connection
             1126  LOAD_METHOD              cursor
             1128  CALL_METHOD_0         0  '0 positional arguments'
             1130  STORE_FAST               'cursor'

 L. 219      1132  LOAD_FAST                'cursor'
             1134  LOAD_METHOD              execute
             1136  LOAD_FAST                'sel'
             1138  CALL_METHOD_1         1  '1 positional argument'
             1140  POP_TOP          

 L. 220      1142  LOAD_FAST                'cursor'
             1144  LOAD_METHOD              fetchall
             1146  CALL_METHOD_0         0  '0 positional arguments'
             1148  STORE_FAST               'object_list'
             1150  JUMP_FORWARD       1356  'to 1356'
           1152_0  COME_FROM          1120  '1120'

 L. 221      1152  LOAD_STR                 'http'
             1154  LOAD_FAST                'sel'
             1156  COMPARE_OP               in
         1158_1160  POP_JUMP_IF_FALSE  1224  'to 1224'
             1162  LOAD_STR                 '://'
             1164  LOAD_FAST                'sel'
             1166  COMPARE_OP               in
         1168_1170  POP_JUMP_IF_FALSE  1224  'to 1224'

 L. 222      1172  LOAD_GLOBAL              requests
             1174  LOAD_METHOD              get
             1176  LOAD_FAST                'sel'
             1178  CALL_METHOD_1         1  '1 positional argument'
             1180  STORE_FAST               'r'

 L. 223      1182  LOAD_FAST                'r'
             1184  LOAD_ATTR                text
             1186  STORE_FAST               'p'

 L. 224      1188  LOAD_GLOBAL              SimpleTabParserBase
             1190  CALL_FUNCTION_0       0  '0 positional arguments'
             1192  STORE_FAST               'parser'

 L. 225      1194  LOAD_FAST                'parser'
             1196  LOAD_METHOD              feed
             1198  LOAD_FAST                'p'
             1200  CALL_METHOD_1         1  '1 positional argument'
             1202  POP_TOP          

 L. 226      1204  LOAD_FAST                'parser'
             1206  LOAD_ATTR                tables
             1208  LOAD_CONST               0
             1210  BINARY_SUBSCR    
             1212  LOAD_CONST               1
             1214  LOAD_CONST               None
             1216  BUILD_SLICE_2         2 
             1218  BINARY_SUBSCR    
             1220  STORE_FAST               'object_list'
             1222  JUMP_FORWARD       1356  'to 1356'
           1224_0  COME_FROM          1168  '1168'
           1224_1  COME_FROM          1158  '1158'

 L. 228      1224  LOAD_GLOBAL              settings
             1226  LOAD_ATTR                DB
             1228  SETUP_WITH         1350  'to 1350'
             1230  STORE_FAST               'db'

 L. 229      1232  LOAD_STR                 '$$$'
             1234  LOAD_FAST                'sel'
             1236  COMPARE_OP               in
         1238_1240  POP_JUMP_IF_FALSE  1328  'to 1328'

 L. 230      1242  LOAD_FAST                'sel'
             1244  LOAD_METHOD              split
             1246  LOAD_STR                 '$$$'
             1248  CALL_METHOD_1         1  '1 positional argument'
             1250  STORE_FAST               'sel_list'

 L. 231      1252  BUILD_LIST_0          0 
             1254  STORE_FAST               'object_list'

 L. 232      1256  SETUP_LOOP         1346  'to 1346'
             1258  LOAD_FAST                'sel_list'
             1260  GET_ITER         
           1262_0  COME_FROM          1272  '1272'
             1262  FOR_ITER           1324  'to 1324'
             1264  STORE_FAST               'sel2'

 L. 233      1266  LOAD_FAST                'sel'
             1268  LOAD_METHOD              strip
             1270  CALL_METHOD_0         0  '0 positional arguments'
         1272_1274  POP_JUMP_IF_FALSE  1262  'to 1262'

 L. 234      1276  LOAD_FAST                'db'
             1278  LOAD_METHOD              execute
             1280  LOAD_FAST                'sel2'
             1282  CALL_METHOD_1         1  '1 positional argument'
             1284  POP_TOP          

 L. 235      1286  LOAD_FAST                'db'
             1288  LOAD_METHOD              fetchall
             1290  CALL_METHOD_0         0  '0 positional arguments'
             1292  STORE_FAST               'ret'

 L. 236      1294  SETUP_LOOP         1320  'to 1320'
             1296  LOAD_FAST                'ret'
             1298  GET_ITER         
             1300  FOR_ITER           1318  'to 1318'
             1302  STORE_FAST               'pos'

 L. 237      1304  LOAD_FAST                'object_list'
             1306  LOAD_METHOD              append
             1308  LOAD_FAST                'pos'
             1310  CALL_METHOD_1         1  '1 positional argument'
             1312  POP_TOP          
         1314_1316  JUMP_BACK          1300  'to 1300'
             1318  POP_BLOCK        
           1320_0  COME_FROM_LOOP     1294  '1294'
         1320_1322  JUMP_BACK          1262  'to 1262'
             1324  POP_BLOCK        
             1326  JUMP_FORWARD       1346  'to 1346'
           1328_0  COME_FROM          1238  '1238'

 L. 239      1328  LOAD_FAST                'db'
             1330  LOAD_METHOD              execute
             1332  LOAD_FAST                'sel'
             1334  CALL_METHOD_1         1  '1 positional argument'
             1336  POP_TOP          

 L. 240      1338  LOAD_FAST                'db'
             1340  LOAD_METHOD              fetchall
             1342  CALL_METHOD_0         0  '0 positional arguments'
             1344  STORE_FAST               'object_list'
           1346_0  COME_FROM          1326  '1326'
           1346_1  COME_FROM_LOOP     1256  '1256'
             1346  POP_BLOCK        
             1348  LOAD_CONST               None
           1350_0  COME_FROM_WITH     1228  '1228'
             1350  WITH_CLEANUP_START
             1352  WITH_CLEANUP_FINISH
             1354  END_FINALLY      
           1356_0  COME_FROM          1222  '1222'
           1356_1  COME_FROM          1150  '1150'

 L. 242      1356  LOAD_GLOBAL              locals
             1358  CALL_FUNCTION_0       0  '0 positional arguments'
             1360  LOAD_METHOD              get
             1362  LOAD_STR                 'transform_object_list'
             1364  LOAD_CONST               None
             1366  CALL_METHOD_2         2  '2 positional arguments'
             1368  STORE_FAST               'fun'

 L. 243      1370  LOAD_FAST                'fun'
         1372_1374  POP_JUMP_IF_FALSE  1388  'to 1388'

 L. 244      1376  LOAD_FAST                'fun'
             1378  LOAD_FAST                'object_list'
             1380  LOAD_FAST                'param'
             1382  LOAD_FAST                'mail'
             1384  CALL_FUNCTION_3       3  '3 positional arguments'
             1386  STORE_FAST               'object_list'
           1388_0  COME_FROM          1372  '1372'

 L. 246      1388  LOAD_GLOBAL              len
             1390  LOAD_FAST                'object_list'
             1392  CALL_FUNCTION_1       1  '1 positional argument'
             1394  LOAD_CONST               0
             1396  COMPARE_OP               <=
         1398_1400  POP_JUMP_IF_FALSE  1414  'to 1414'
             1402  LOAD_FAST                'report'
             1404  LOAD_ATTR                json_send_always
         1406_1408  POP_JUMP_IF_TRUE   1414  'to 1414'

 L. 247  1410_1412  CONTINUE            810  'to 810'
           1414_0  COME_FROM          1406  '1406'
           1414_1  COME_FROM          1398  '1398'

 L. 249      1414  LOAD_STR                 'html'
             1416  STORE_FAST               'doc_type'

 L. 250      1418  LOAD_STR                 'raporty/formsimplereport_'
             1420  LOAD_FAST                'report_name'
             1422  BINARY_ADD       
             1424  LOAD_STR                 'raporty/formsimplereport'
             1426  BUILD_LIST_2          2 
             1428  STORE_FAST               'template_names'

 L. 251      1430  LOAD_FAST                'report_type'
             1432  LOAD_STR                 'pdf'
             1434  COMPARE_OP               ==
         1436_1438  POP_JUMP_IF_FALSE  1456  'to 1456'
             1440  LOAD_FAST                'destination'
             1442  LOAD_STR                 '2'
             1444  COMPARE_OP               !=
         1446_1448  POP_JUMP_IF_FALSE  1456  'to 1456'

 L. 252      1450  LOAD_STR                 'pdf'
             1452  STORE_FAST               'doc_type'
             1454  JUMP_FORWARD       1522  'to 1522'
           1456_0  COME_FROM          1446  '1446'
           1456_1  COME_FROM          1436  '1436'

 L. 253      1456  LOAD_FAST                'report_type'
             1458  LOAD_STR                 'odf'
             1460  COMPARE_OP               ==
         1462_1464  POP_JUMP_IF_FALSE  1482  'to 1482'
             1466  LOAD_FAST                'destination'
             1468  LOAD_STR                 '2'
             1470  COMPARE_OP               !=
         1472_1474  POP_JUMP_IF_FALSE  1482  'to 1482'

 L. 254      1476  LOAD_STR                 'ods'
             1478  STORE_FAST               'doc_type'
             1480  JUMP_FORWARD       1522  'to 1522'
           1482_0  COME_FROM          1472  '1472'
           1482_1  COME_FROM          1462  '1462'

 L. 255      1482  LOAD_FAST                'report_type'
             1484  LOAD_STR                 'xlsx'
             1486  COMPARE_OP               ==
         1488_1490  POP_JUMP_IF_FALSE  1508  'to 1508'
             1492  LOAD_FAST                'destination'
             1494  LOAD_STR                 '2'
             1496  COMPARE_OP               !=
         1498_1500  POP_JUMP_IF_FALSE  1508  'to 1508'

 L. 256      1502  LOAD_STR                 'xlsx'
             1504  STORE_FAST               'doc_type'
             1506  JUMP_FORWARD       1522  'to 1522'
           1508_0  COME_FROM          1498  '1498'
           1508_1  COME_FROM          1488  '1488'

 L. 257      1508  LOAD_FAST                'report_type'
             1510  LOAD_STR                 'txt'
             1512  COMPARE_OP               ==
         1514_1516  POP_JUMP_IF_FALSE  1522  'to 1522'

 L. 258      1518  LOAD_STR                 'txt'
             1520  STORE_FAST               'doc_type'
           1522_0  COME_FROM          1514  '1514'
           1522_1  COME_FROM          1506  '1506'
           1522_2  COME_FROM          1480  '1480'
           1522_3  COME_FROM          1454  '1454'

 L. 260      1522  LOAD_GLOBAL              len
             1524  LOAD_FAST                'object_list'
             1526  CALL_FUNCTION_1       1  '1 positional argument'
             1528  LOAD_CONST               0
             1530  COMPARE_OP               >
         1532_1534  POP_JUMP_IF_FALSE  1580  'to 1580'
             1536  LOAD_GLOBAL              len
             1538  LOAD_FAST                'object_list'
             1540  LOAD_CONST               0
             1542  BINARY_SUBSCR    
             1544  CALL_FUNCTION_1       1  '1 positional argument'
             1546  LOAD_GLOBAL              len
             1548  LOAD_FAST                'columns'
             1550  CALL_FUNCTION_1       1  '1 positional argument'
             1552  COMPARE_OP               >
         1554_1556  POP_JUMP_IF_FALSE  1580  'to 1580'

 L. 261      1558  LOAD_CONST               True
             1560  STORE_FAST               'colors'

 L. 262      1562  LOAD_STR                 '0:'
             1564  LOAD_GLOBAL              str
             1566  LOAD_GLOBAL              len
             1568  LOAD_FAST                'columns'
             1570  CALL_FUNCTION_1       1  '1 positional argument'
             1572  CALL_FUNCTION_1       1  '1 positional argument'
             1574  BINARY_ADD       
             1576  STORE_FAST               'sli'
             1578  JUMP_FORWARD       1588  'to 1588'
           1580_0  COME_FROM          1554  '1554'
           1580_1  COME_FROM          1532  '1532'

 L. 264      1580  LOAD_STR                 ':'
             1582  STORE_FAST               'sli'

 L. 265      1584  LOAD_CONST               False
             1586  STORE_FAST               'colors'
           1588_0  COME_FROM          1578  '1578'

 L. 268      1588  LOAD_FAST                'object_list'
             1590  LOAD_FAST                'doc_type'
             1592  LOAD_FAST                'report_type'
             1594  LOAD_FAST                'date'

 L. 269      1596  LOAD_FAST                'columns'
             1598  LOAD_FAST                'datetime_gen_str'
             1600  LOAD_FAST                'report'
             1602  LOAD_FAST                'date_gen_year'
             1604  LOAD_FAST                'date_gen_month'

 L. 270      1606  LOAD_FAST                'colors'
             1608  LOAD_FAST                'sli'
             1610  LOAD_FAST                'param'
             1612  LOAD_FAST                'template_names'
             1614  LOAD_FAST                'desc'
             1616  LOAD_CONST               ('object_list', 'doc_type', 'report_type', 'date', 'columns', 'time_str', 'report', 'year', 'month', 'colors', 'sli', 'param', 'template_names', 'description')
             1618  BUILD_CONST_KEY_MAP_14    14 
             1620  STORE_FAST               'rep_dict'

 L. 273      1622  LOAD_GLOBAL              locals
             1624  CALL_FUNCTION_0       0  '0 positional arguments'
             1626  LOAD_METHOD              get
             1628  LOAD_STR                 'transform_context'
             1630  LOAD_CONST               None
             1632  CALL_METHOD_2         2  '2 positional arguments'
             1634  STORE_FAST               'fun'

 L. 274      1636  LOAD_FAST                'fun'
         1638_1640  POP_JUMP_IF_FALSE  1654  'to 1654'

 L. 275      1642  LOAD_FAST                'fun'
             1644  LOAD_FAST                'rep_dict'
             1646  LOAD_FAST                'param'
             1648  LOAD_FAST                'mail'
             1650  CALL_FUNCTION_3       3  '3 positional arguments'
             1652  POP_TOP          
           1654_0  COME_FROM          1638  '1638'

 L. 277      1654  LOAD_GLOBAL              render_doc
             1656  LOAD_FAST                'rep_dict'
             1658  CALL_FUNCTION_1       1  '1 positional argument'
             1660  UNPACK_SEQUENCE_2     2 
             1662  STORE_FAST               'attrs'
             1664  STORE_FAST               'content'

 L. 279      1666  LOAD_STR                 'attachment_name'
             1668  LOAD_FAST                'rep_dict'
             1670  COMPARE_OP               in
         1672_1674  POP_JUMP_IF_FALSE  1684  'to 1684'

 L. 280      1676  LOAD_FAST                'rep_dict'
             1678  LOAD_STR                 'attachment_name'
           1680_0  COME_FROM          1108  '1108'
             1680  BINARY_SUBSCR    
             1682  STORE_FAST               'attachment_name'
           1684_0  COME_FROM          1672  '1672'
           1684_1  COME_FROM          1110  '1110'
           1684_2  COME_FROM           936  '936'
           1684_3  COME_FROM           926  '926'

 L. 282      1684  LOAD_GLOBAL              len
             1686  LOAD_FAST                'mail_to'
             1688  CALL_FUNCTION_1       1  '1 positional argument'
             1690  LOAD_CONST               0
             1692  COMPARE_OP               >
         1694_1696  POP_JUMP_IF_FALSE  1876  'to 1876'

 L. 284      1698  LOAD_FAST                'destination'
             1700  LOAD_STR                 '1'
             1702  COMPARE_OP               ==
         1704_1706  POP_JUMP_IF_FALSE  1776  'to 1776'

 L. 285      1708  LOAD_GLOBAL              EmailMessage
             1710  LOAD_FAST                'desc2'
             1712  LOAD_GLOBAL              MAIL_CONTENT
             1714  LOAD_FAST                'mail_to'
             1716  LOAD_CONST               ('to',)
             1718  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1720  STORE_FAST               'mail'

 L. 286      1722  LOAD_FAST                'mail'
             1724  LOAD_METHOD              attach
             1726  LOAD_FAST                'attachment_name'
         1728_1730  POP_JUMP_IF_FALSE  1736  'to 1736'
             1732  LOAD_FAST                'attachment_name'
             1734  JUMP_FORWARD       1754  'to 1754'
           1736_0  COME_FROM          1728  '1728'
             1736  LOAD_FAST                'report_name'
             1738  FORMAT_VALUE          0  ''
             1740  LOAD_STR                 '_'
             1742  LOAD_FAST                'date_gen_id'
             1744  FORMAT_VALUE          0  ''
             1746  LOAD_STR                 '.'
             1748  LOAD_FAST                'doc_type'
             1750  FORMAT_VALUE          0  ''
             1752  BUILD_STRING_5        5 
           1754_0  COME_FROM          1734  '1734'
             1754  LOAD_FAST                'content'
             1756  LOAD_FAST                'attrs'
             1758  LOAD_STR                 'Content-Type'
             1760  BINARY_SUBSCR    
             1762  CALL_METHOD_3         3  '3 positional arguments'
             1764  POP_TOP          

 L. 287      1766  LOAD_FAST                'mail'
             1768  LOAD_METHOD              send
             1770  CALL_METHOD_0         0  '0 positional arguments'
             1772  POP_TOP          
             1774  JUMP_FORWARD       1868  'to 1868'
           1776_0  COME_FROM          1704  '1704'

 L. 288      1776  LOAD_FAST                'destination'
             1778  LOAD_STR                 '2'
             1780  COMPARE_OP               ==
         1782_1784  POP_JUMP_IF_FALSE  1846  'to 1846'

 L. 289      1786  LOAD_GLOBAL              EmailMultiAlternatives
             1788  LOAD_FAST                'desc2'
             1790  LOAD_GLOBAL              MAIL_CONTENT
             1792  LOAD_FAST                'mail_to'
             1794  LOAD_CONST               ('to',)
             1796  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
             1798  STORE_FAST               'mail'

 L. 290      1800  LOAD_GLOBAL              type
             1802  LOAD_FAST                'content'
             1804  CALL_FUNCTION_1       1  '1 positional argument'
             1806  LOAD_GLOBAL              bytes
             1808  COMPARE_OP               ==
         1810_1812  POP_JUMP_IF_FALSE  1824  'to 1824'

 L. 291      1814  LOAD_FAST                'content'
             1816  LOAD_METHOD              decode
             1818  LOAD_STR                 'utf-8'
             1820  CALL_METHOD_1         1  '1 positional argument'
             1822  STORE_FAST               'content'
           1824_0  COME_FROM          1810  '1810'

 L. 292      1824  LOAD_FAST                'mail'
             1826  LOAD_METHOD              attach_alternative
             1828  LOAD_FAST                'content'
             1830  LOAD_STR                 'text/html'
             1832  CALL_METHOD_2         2  '2 positional arguments'
             1834  POP_TOP          

 L. 293      1836  LOAD_FAST                'mail'
             1838  LOAD_METHOD              send
             1840  CALL_METHOD_0         0  '0 positional arguments'
             1842  POP_TOP          
             1844  JUMP_FORWARD       1868  'to 1868'
           1846_0  COME_FROM          1782  '1782'

 L. 294      1846  LOAD_FAST                'destination'
             1848  LOAD_STR                 '3'
             1850  COMPARE_OP               ==
         1852_1854  POP_JUMP_IF_FALSE  1858  'to 1858'

 L. 295      1856  JUMP_FORWARD       1868  'to 1868'
           1858_0  COME_FROM          1852  '1852'

 L. 296      1858  LOAD_FAST                'destination'
             1860  LOAD_STR                 '4'
             1862  COMPARE_OP               ==
         1864_1866  POP_JUMP_IF_FALSE  1868  'to 1868'
           1868_0  COME_FROM          1864  '1864'
           1868_1  COME_FROM          1856  '1856'
           1868_2  COME_FROM          1844  '1844'
           1868_3  COME_FROM          1774  '1774'

 L. 298      1868  LOAD_FAST                'count'
             1870  LOAD_CONST               1
             1872  INPLACE_ADD      
             1874  STORE_FAST               'count'
           1876_0  COME_FROM          1694  '1694'

 L. 300      1876  LOAD_FAST                'destination'
             1878  LOAD_METHOD              startswith
             1880  LOAD_STR                 '5'
             1882  CALL_METHOD_1         1  '1 positional argument'
         1884_1886  POP_JUMP_IF_FALSE   810  'to 810'

 L. 301      1888  LOAD_FAST                'mail_to'
         1890_1892  POP_JUMP_IF_FALSE  1906  'to 1906'

 L. 302      1894  LOAD_STR                 ';'
             1896  LOAD_METHOD              join
             1898  LOAD_FAST                'mail_to'
             1900  CALL_METHOD_1         1  '1 positional argument'
             1902  STORE_FAST               'x'
             1904  JUMP_FORWARD       1910  'to 1910'
           1906_0  COME_FROM          1890  '1890'

 L. 304      1906  LOAD_FAST                'date_gen_id'
             1908  STORE_FAST               'x'
           1910_0  COME_FROM          1904  '1904'

 L. 305      1910  LOAD_FAST                'ret_files'
             1912  LOAD_METHOD              append
             1914  LOAD_FAST                'report_name'
             1916  FORMAT_VALUE          0  ''
             1918  LOAD_STR                 '_'
             1920  LOAD_FAST                'x'
             1922  FORMAT_VALUE          0  ''
             1924  LOAD_STR                 '.'
             1926  LOAD_FAST                'doc_type'
             1928  FORMAT_VALUE          0  ''
             1930  BUILD_STRING_5        5 
             1932  LOAD_FAST                'content'
             1934  LOAD_FAST                'attrs'
             1936  BUILD_TUPLE_3         3 
             1938  CALL_METHOD_1         1  '1 positional argument'
             1940  POP_TOP          
         1942_1944  JUMP_BACK           810  'to 810'
             1946  POP_BLOCK        
           1948_0  COME_FROM_LOOP      802  '802'

 L. 307      1948  LOAD_FAST                'ret_files'
         1950_1952  POP_JUMP_IF_FALSE  2114  'to 2114'

 L. 308      1954  LOAD_GLOBAL              len
             1956  LOAD_FAST                'ret_files'
             1958  CALL_FUNCTION_1       1  '1 positional argument'
             1960  LOAD_CONST               1
             1962  COMPARE_OP               ==
         1964_1966  POP_JUMP_IF_FALSE  1994  'to 1994'

 L. 309      1968  LOAD_GLOBAL              logger
             1970  LOAD_METHOD              info
             1972  LOAD_STR                 'End report: '
             1974  LOAD_FAST                'report_name'
             1976  FORMAT_VALUE          0  ''
             1978  LOAD_STR                 ', ret_files[0]'
             1980  BUILD_STRING_3        3 
             1982  CALL_METHOD_1         1  '1 positional argument'
             1984  POP_TOP          

 L. 310      1986  LOAD_FAST                'ret_files'
             1988  LOAD_CONST               0
             1990  BINARY_SUBSCR    
             1992  RETURN_VALUE     
           1994_0  COME_FROM          1964  '1964'

 L. 312      1994  LOAD_GLOBAL              io
             1996  LOAD_METHOD              BytesIO
             1998  CALL_METHOD_0         0  '0 positional arguments'
             2000  STORE_FAST               'file_like_object'

 L. 313      2002  LOAD_GLOBAL              zipfile
             2004  LOAD_ATTR                ZipFile
             2006  LOAD_FAST                'file_like_object'
             2008  LOAD_STR                 'w'
             2010  LOAD_CONST               ('mode',)
             2012  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             2014  STORE_FAST               'zipfileobj'

 L. 314      2016  SETUP_LOOP         2052  'to 2052'
             2018  LOAD_FAST                'ret_files'
             2020  GET_ITER         
             2022  FOR_ITER           2050  'to 2050'
             2024  STORE_FAST               'f'

 L. 315      2026  LOAD_FAST                'zipfileobj'
             2028  LOAD_METHOD              writestr
             2030  LOAD_FAST                'f'
             2032  LOAD_CONST               0
             2034  BINARY_SUBSCR    
             2036  LOAD_FAST                'f'
             2038  LOAD_CONST               1
             2040  BINARY_SUBSCR    
             2042  CALL_METHOD_2         2  '2 positional arguments'
             2044  POP_TOP          
         2046_2048  JUMP_BACK          2022  'to 2022'
             2050  POP_BLOCK        
           2052_0  COME_FROM_LOOP     2016  '2016'

 L. 316      2052  LOAD_FAST                'zipfileobj'
             2054  LOAD_METHOD              close
             2056  CALL_METHOD_0         0  '0 positional arguments'
             2058  POP_TOP          

 L. 317      2060  LOAD_FAST                'file_like_object'
             2062  LOAD_METHOD              seek
             2064  LOAD_CONST               0
             2066  CALL_METHOD_1         1  '1 positional argument'
             2068  POP_TOP          

 L. 318      2070  LOAD_FAST                'file_like_object'
             2072  LOAD_METHOD              read
             2074  CALL_METHOD_0         0  '0 positional arguments'
             2076  STORE_FAST               'data'

 L. 319      2078  LOAD_GLOBAL              logger
             2080  LOAD_METHOD              info
             2082  LOAD_STR                 'End report: '
             2084  LOAD_FAST                'report_name'
             2086  FORMAT_VALUE          0  ''
             2088  LOAD_STR                 ', ret: data.zip'
             2090  BUILD_STRING_3        3 
             2092  CALL_METHOD_1         1  '1 positional argument'
             2094  POP_TOP          

 L. 320      2096  LOAD_STR                 'data.zip'
             2098  LOAD_FAST                'data'
             2100  LOAD_STR                 'application/zip'
             2102  LOAD_STR                 'attachment; filename=data.zip;'
             2104  LOAD_CONST               ('Content-Type', 'Content-Disposition')
             2106  BUILD_CONST_KEY_MAP_2     2 
             2108  BUILD_TUPLE_3         3 
             2110  RETURN_VALUE     
             2112  JUMP_FORWARD       2136  'to 2136'
           2114_0  COME_FROM          1950  '1950'

 L. 322      2114  LOAD_GLOBAL              logger
             2116  LOAD_METHOD              info
             2118  LOAD_STR                 'End report: '
             2120  LOAD_FAST                'report_name'
             2122  FORMAT_VALUE          0  ''
             2124  LOAD_STR                 ', ret: count'
             2126  BUILD_STRING_3        3 
             2128  CALL_METHOD_1         1  '1 positional argument'
             2130  POP_TOP          

 L. 323      2132  LOAD_FAST                'count'
             2134  RETURN_VALUE     
           2136_0  COME_FROM          2112  '2112'

Parse error at or near `COME_FROM' instruction at offset 1680_0