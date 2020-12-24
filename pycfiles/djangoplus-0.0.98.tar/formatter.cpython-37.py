# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/breno/.virtualenvs/djangoplus/lib/python3.7/site-packages/djangoplus/utils/formatter.py
# Compiled at: 2020-02-03 13:40:07
# Size of source mod 2**32: 5340 bytes
import re, datetime, unicodedata
from decimal import Decimal
from django.conf import settings
from collections import Iterable
from django.utils.safestring import mark_safe

def normalyze(nome):
    nome = str(nome)
    if nome.isupper():
        return nome
    ponto = '\\.'
    ponto_espaco = '. '
    espaco = ' '
    regex_multiplos_espacos = '\\s+'
    regex_numero_romano = '^M{0,4}(CM|CD|D?C{0,3})(XC|XL|L?X{0,3})(IX|IV|V?I{0,3})$'
    nome = re.sub(ponto, ponto_espaco, nome)
    nome = re.sub(regex_multiplos_espacos, espaco, nome)
    nome = nome.title()
    partes_nome = nome.split(espaco)
    excecoes = [
     'de', 'di', 'do', 'da', 'dos', 'das', 'dello', 'della', 'dalla',
     'dal', 'del', 'e', 'em', 'na', 'no', 'nas', 'nos', 'van', 'von', 'y', 'para', 'pela', 'pelo', 'por']
    resultado = []
    for palavra in partes_nome:
        if palavra.lower() in excecoes:
            resultado.append(palavra.lower())
        elif re.match(regex_numero_romano, palavra.upper()):
            resultado.append(palavra.upper())
        else:
            resultado.append(palavra)

    nome = espaco.join(resultado)
    return nome


def format_bool(value):
    return value and '<span class="label label-success">Sim</span>' or '<span class="label label-danger">Não</span>'


def format_value--- This code section failed: ---

 L.  52         0  LOAD_CONST               0
                2  LOAD_CONST               ('ImageFieldFile',)
                4  IMPORT_NAME_ATTR         djangoplus.db.models.fields
                6  IMPORT_FROM              ImageFieldFile
                8  STORE_FAST               'ImageFieldFile'
               10  POP_TOP          

 L.  53        12  LOAD_CONST               0
               14  LOAD_CONST               ('FieldFile', 'ImageFieldFile')
               16  IMPORT_NAME_ATTR         django.db.models.fields.files
               18  IMPORT_FROM              FieldFile
               20  STORE_FAST               'FieldFile'
               22  IMPORT_FROM              ImageFieldFile
               24  STORE_FAST               'DjangoImageFieldFile'
               26  POP_TOP          

 L.  54        28  LOAD_STR                 'ManyRelatedManager'
               30  LOAD_GLOBAL              type
               32  LOAD_FAST                'value'
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  LOAD_ATTR                __name__
               38  COMPARE_OP               in
               40  POP_JUMP_IF_FALSE    50  'to 50'

 L.  55        42  LOAD_FAST                'value'
               44  LOAD_METHOD              all
               46  CALL_METHOD_0         0  '0 positional arguments'
               48  STORE_FAST               'value'
             50_0  COME_FROM            40  '40'

 L.  56        50  LOAD_FAST                'value'
               52  LOAD_CONST               (None, '', ())
               54  COMPARE_OP               in
               56  POP_JUMP_IF_FALSE    62  'to 62'

 L.  57        58  LOAD_STR                 '-'
               60  RETURN_VALUE     
             62_0  COME_FROM            56  '56'

 L.  58        62  LOAD_GLOBAL              isinstance
               64  LOAD_FAST                'value'
               66  LOAD_GLOBAL              str
               68  CALL_FUNCTION_2       2  '2 positional arguments'
               70  POP_JUMP_IF_TRUE     86  'to 86'
               72  LOAD_GLOBAL              type
               74  LOAD_FAST                'value'
               76  CALL_FUNCTION_1       1  '1 positional argument'
               78  LOAD_ATTR                __name__
               80  LOAD_STR                 '__proxy__'
               82  COMPARE_OP               ==
               84  POP_JUMP_IF_FALSE   114  'to 114'
             86_0  COME_FROM            70  '70'

 L.  59        86  LOAD_FAST                'html'
               88  POP_JUMP_IF_FALSE   106  'to 106'

 L.  60        90  LOAD_GLOBAL              mark_safe
               92  LOAD_FAST                'value'
               94  LOAD_METHOD              replace
               96  LOAD_STR                 '\n'
               98  LOAD_STR                 '<br>'
              100  CALL_METHOD_2         2  '2 positional arguments'
              102  CALL_FUNCTION_1       1  '1 positional argument'
              104  RETURN_VALUE     
            106_0  COME_FROM            88  '88'

 L.  62       106  LOAD_FAST                'value'
              108  RETURN_VALUE     
          110_112  JUMP_FORWARD        746  'to 746'
            114_0  COME_FROM            84  '84'

 L.  63       114  LOAD_GLOBAL              isinstance
              116  LOAD_FAST                'value'
              118  LOAD_GLOBAL              bool
              120  CALL_FUNCTION_2       2  '2 positional arguments'
              122  POP_JUMP_IF_FALSE   136  'to 136'

 L.  64       124  LOAD_FAST                'value'
              126  POP_JUMP_IF_FALSE   132  'to 132'
              128  LOAD_STR                 'Sim'
              130  JUMP_IF_TRUE_OR_POP   134  'to 134'
            132_0  COME_FROM           126  '126'
              132  LOAD_STR                 'Não'
            134_0  COME_FROM           130  '130'
              134  RETURN_VALUE     
            136_0  COME_FROM           122  '122'

 L.  65       136  LOAD_GLOBAL              isinstance
              138  LOAD_FAST                'value'
              140  LOAD_GLOBAL              datetime
              142  LOAD_ATTR                datetime
              144  CALL_FUNCTION_2       2  '2 positional arguments'
              146  POP_JUMP_IF_FALSE   158  'to 158'

 L.  66       148  LOAD_FAST                'value'
              150  LOAD_METHOD              strftime
              152  LOAD_STR                 '%d/%m/%Y %H:%M'
              154  CALL_METHOD_1         1  '1 positional argument'
              156  RETURN_VALUE     
            158_0  COME_FROM           146  '146'

 L.  67       158  LOAD_GLOBAL              isinstance
              160  LOAD_FAST                'value'
              162  LOAD_GLOBAL              datetime
              164  LOAD_ATTR                date
              166  CALL_FUNCTION_2       2  '2 positional arguments'
              168  POP_JUMP_IF_FALSE   180  'to 180'

 L.  68       170  LOAD_FAST                'value'
              172  LOAD_METHOD              strftime
              174  LOAD_STR                 '%d/%m/%Y'
              176  CALL_METHOD_1         1  '1 positional argument'
              178  RETURN_VALUE     
            180_0  COME_FROM           168  '168'

 L.  69       180  LOAD_GLOBAL              isinstance
              182  LOAD_FAST                'value'
              184  LOAD_GLOBAL              tuple
              186  CALL_FUNCTION_2       2  '2 positional arguments'
              188  POP_JUMP_IF_FALSE   210  'to 210'

 L.  70       190  LOAD_STR                 '{} {}'
              192  LOAD_METHOD              format
              194  LOAD_FAST                'value'
              196  LOAD_CONST               0
              198  BINARY_SUBSCR    
              200  LOAD_FAST                'value'
              202  LOAD_CONST               1
              204  BINARY_SUBSCR    
              206  CALL_METHOD_2         2  '2 positional arguments'
              208  RETURN_VALUE     
            210_0  COME_FROM           188  '188'

 L.  71       210  LOAD_GLOBAL              isinstance
              212  LOAD_FAST                'value'
              214  LOAD_GLOBAL              Decimal
              216  CALL_FUNCTION_2       2  '2 positional arguments'
          218_220  POP_JUMP_IF_FALSE   274  'to 274'

 L.  72       222  LOAD_GLOBAL              hasattr
              224  LOAD_FAST                'value'
              226  LOAD_STR                 'decimal3'
              228  CALL_FUNCTION_2       2  '2 positional arguments'
          230_232  POP_JUMP_IF_FALSE   242  'to 242'

 L.  73       234  LOAD_GLOBAL              format_decimal3
              236  LOAD_FAST                'value'
              238  CALL_FUNCTION_1       1  '1 positional argument'
              240  RETURN_VALUE     
            242_0  COME_FROM           230  '230'

 L.  74       242  LOAD_GLOBAL              hasattr
              244  LOAD_FAST                'value'
              246  LOAD_STR                 'decimal1'
              248  CALL_FUNCTION_2       2  '2 positional arguments'
          250_252  POP_JUMP_IF_FALSE   262  'to 262'

 L.  75       254  LOAD_GLOBAL              format_decimal1
              256  LOAD_FAST                'value'
              258  CALL_FUNCTION_1       1  '1 positional argument'
              260  RETURN_VALUE     
            262_0  COME_FROM           250  '250'

 L.  77       262  LOAD_GLOBAL              format_decimal
              264  LOAD_FAST                'value'
              266  CALL_FUNCTION_1       1  '1 positional argument'
              268  RETURN_VALUE     
          270_272  JUMP_FORWARD        746  'to 746'
            274_0  COME_FROM           218  '218'

 L.  78       274  LOAD_GLOBAL              isinstance
              276  LOAD_FAST                'value'
              278  LOAD_FAST                'ImageFieldFile'
              280  CALL_FUNCTION_2       2  '2 positional arguments'
          282_284  POP_JUMP_IF_TRUE    298  'to 298'
              286  LOAD_GLOBAL              isinstance
              288  LOAD_FAST                'value'
              290  LOAD_FAST                'DjangoImageFieldFile'
              292  CALL_FUNCTION_2       2  '2 positional arguments'
          294_296  POP_JUMP_IF_FALSE   330  'to 330'
            298_0  COME_FROM           282  '282'

 L.  79       298  LOAD_FAST                'html'
          300_302  POP_JUMP_IF_FALSE   320  'to 320'

 L.  80       304  LOAD_GLOBAL              mark_safe

 L.  81       306  LOAD_STR                 '<img width="75" class="materialboxed" src="{}"/>'
              308  LOAD_METHOD              format
              310  LOAD_FAST                'value'
              312  LOAD_ATTR                url
              314  CALL_METHOD_1         1  '1 positional argument'
              316  CALL_FUNCTION_1       1  '1 positional argument'
              318  RETURN_VALUE     
            320_0  COME_FROM           300  '300'

 L.  84       320  LOAD_FAST                'value'
              322  LOAD_ATTR                url
              324  RETURN_VALUE     
          326_328  JUMP_FORWARD        746  'to 746'
            330_0  COME_FROM           294  '294'

 L.  85       330  LOAD_GLOBAL              isinstance
              332  LOAD_FAST                'value'
              334  LOAD_FAST                'FieldFile'
              336  CALL_FUNCTION_2       2  '2 positional arguments'
          338_340  POP_JUMP_IF_FALSE   448  'to 448'

 L.  86       342  LOAD_FAST                'value'
              344  LOAD_ATTR                name
              346  LOAD_METHOD              split
              348  LOAD_STR                 '/'
              350  CALL_METHOD_1         1  '1 positional argument'
              352  LOAD_CONST               -1
              354  BINARY_SUBSCR    
              356  STORE_FAST               'file_name'

 L.  87       358  LOAD_FAST                'value'
              360  LOAD_ATTR                url
              362  LOAD_METHOD              lower
              364  CALL_METHOD_0         0  '0 positional arguments'
              366  LOAD_METHOD              endswith
              368  LOAD_STR                 '.pdf'
              370  CALL_METHOD_1         1  '1 positional argument'
          372_374  POP_JUMP_IF_FALSE   414  'to 414'

 L.  88       376  LOAD_FAST                'html'
          378_380  POP_JUMP_IF_FALSE   406  'to 406'

 L.  89       382  LOAD_GLOBAL              mark_safe

 L.  92       384  LOAD_STR                 '\n                    <a class="ajax pdf" href="{}">{}</a>{}\n                    <a href="{}"><i class="mdi-file-file-download"></i></a>\n                '
              386  LOAD_METHOD              format
              388  LOAD_FAST                'value'
              390  LOAD_ATTR                url
              392  LOAD_FAST                'file_name'
              394  LOAD_STR                 '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
              396  LOAD_FAST                'value'
              398  LOAD_ATTR                url
              400  CALL_METHOD_4         4  '4 positional arguments'
              402  CALL_FUNCTION_1       1  '1 positional argument'
              404  RETURN_VALUE     
            406_0  COME_FROM           378  '378'

 L.  94       406  LOAD_FAST                'value'
              408  LOAD_ATTR                url
              410  RETURN_VALUE     
              412  JUMP_FORWARD        746  'to 746'
            414_0  COME_FROM           372  '372'

 L.  96       414  LOAD_FAST                'html'
          416_418  POP_JUMP_IF_FALSE   438  'to 438'

 L.  97       420  LOAD_GLOBAL              mark_safe
              422  LOAD_STR                 '<a target="_blank" href="{}">{}</a>'
              424  LOAD_METHOD              format
              426  LOAD_FAST                'value'
              428  LOAD_ATTR                url
              430  LOAD_FAST                'file_name'
              432  CALL_METHOD_2         2  '2 positional arguments'
              434  CALL_FUNCTION_1       1  '1 positional argument'
              436  RETURN_VALUE     
            438_0  COME_FROM           416  '416'

 L.  99       438  LOAD_FAST                'value'
              440  LOAD_ATTR                url
              442  RETURN_VALUE     
          444_446  JUMP_FORWARD        746  'to 746'
            448_0  COME_FROM           338  '338'

 L. 100       448  LOAD_GLOBAL              isinstance
              450  LOAD_FAST                'value'
              452  LOAD_GLOBAL              dict
              454  CALL_FUNCTION_2       2  '2 positional arguments'
          456_458  POP_JUMP_IF_FALSE   612  'to 612'

 L. 101       460  LOAD_FAST                'html'
          462_464  POP_JUMP_IF_FALSE   546  'to 546'

 L. 102       466  LOAD_STR                 '<ul style="display: inline-block; padding-left:0px">'
              468  BUILD_LIST_1          1 
              470  STORE_FAST               'ul'

 L. 103       472  SETUP_LOOP          522  'to 522'
              474  LOAD_FAST                'value'
              476  LOAD_METHOD              items
              478  CALL_METHOD_0         0  '0 positional arguments'
              480  GET_ITER         
              482  FOR_ITER            520  'to 520'
              484  UNPACK_SEQUENCE_2     2 
              486  STORE_FAST               'key'
              488  STORE_FAST               'info'

 L. 104       490  LOAD_FAST                'ul'
              492  LOAD_METHOD              append
              494  LOAD_STR                 '<li style="list-style-type:none">{}: {}</li>'
              496  LOAD_METHOD              format
              498  LOAD_FAST                'key'
              500  LOAD_GLOBAL              format_value
              502  LOAD_FAST                'info'
              504  LOAD_FAST                'html'
              506  LOAD_CONST               ('html',)
              508  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              510  CALL_METHOD_2         2  '2 positional arguments'
              512  CALL_METHOD_1         1  '1 positional argument'
              514  POP_TOP          
          516_518  JUMP_BACK           482  'to 482'
              520  POP_BLOCK        
            522_0  COME_FROM_LOOP      472  '472'

 L. 105       522  LOAD_FAST                'ul'
              524  LOAD_METHOD              append
              526  LOAD_STR                 '</ul>'
              528  CALL_METHOD_1         1  '1 positional argument'
              530  POP_TOP          

 L. 106       532  LOAD_GLOBAL              mark_safe
              534  LOAD_STR                 ''
              536  LOAD_METHOD              join
              538  LOAD_FAST                'ul'
              540  CALL_METHOD_1         1  '1 positional argument'
              542  CALL_FUNCTION_1       1  '1 positional argument'
              544  RETURN_VALUE     
            546_0  COME_FROM           462  '462'

 L. 108       546  BUILD_LIST_0          0 
              548  STORE_FAST               'items'

 L. 109       550  SETUP_LOOP          600  'to 600'
              552  LOAD_FAST                'value'
              554  LOAD_METHOD              items
              556  CALL_METHOD_0         0  '0 positional arguments'
              558  GET_ITER         
              560  FOR_ITER            598  'to 598'
              562  UNPACK_SEQUENCE_2     2 
              564  STORE_FAST               'key'
              566  STORE_FAST               'info'

 L. 110       568  LOAD_FAST                'items'
              570  LOAD_METHOD              append
              572  LOAD_STR                 '{}: {}'
              574  LOAD_METHOD              format
              576  LOAD_FAST                'key'
              578  LOAD_GLOBAL              format_value
              580  LOAD_FAST                'info'
              582  LOAD_FAST                'html'
              584  LOAD_CONST               ('html',)
              586  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              588  CALL_METHOD_2         2  '2 positional arguments'
              590  CALL_METHOD_1         1  '1 positional argument'
              592  POP_TOP          
          594_596  JUMP_BACK           560  'to 560'
              598  POP_BLOCK        
            600_0  COME_FROM_LOOP      550  '550'

 L. 111       600  LOAD_STR                 ', '
              602  LOAD_METHOD              join
              604  LOAD_FAST                'items'
              606  CALL_METHOD_1         1  '1 positional argument'
              608  RETURN_VALUE     
              610  JUMP_FORWARD        746  'to 746'
            612_0  COME_FROM           456  '456'

 L. 112       612  LOAD_GLOBAL              isinstance
              614  LOAD_FAST                'value'
              616  LOAD_GLOBAL              Iterable
              618  CALL_FUNCTION_2       2  '2 positional arguments'
          620_622  POP_JUMP_IF_FALSE   738  'to 738'

 L. 113       624  LOAD_FAST                'html'
          626_628  POP_JUMP_IF_FALSE   692  'to 692'

 L. 114       630  LOAD_STR                 '<ul style="display: inline-block; padding-left:20px">'
              632  BUILD_LIST_1          1 
              634  STORE_FAST               'ul'

 L. 115       636  SETUP_LOOP          668  'to 668'
              638  LOAD_FAST                'value'
              640  GET_ITER         
              642  FOR_ITER            666  'to 666'
              644  STORE_FAST               'obj'

 L. 116       646  LOAD_FAST                'ul'
              648  LOAD_METHOD              append
              650  LOAD_STR                 '<li style="list-style-type:square">{}</li>'
              652  LOAD_METHOD              format
              654  LOAD_FAST                'obj'
              656  CALL_METHOD_1         1  '1 positional argument'
              658  CALL_METHOD_1         1  '1 positional argument'
              660  POP_TOP          
          662_664  JUMP_BACK           642  'to 642'
              666  POP_BLOCK        
            668_0  COME_FROM_LOOP      636  '636'

 L. 117       668  LOAD_FAST                'ul'
              670  LOAD_METHOD              append
              672  LOAD_STR                 '</ul>'
              674  CALL_METHOD_1         1  '1 positional argument'
              676  POP_TOP          

 L. 118       678  LOAD_GLOBAL              mark_safe
              680  LOAD_STR                 ''
              682  LOAD_METHOD              join
              684  LOAD_FAST                'ul'
              686  CALL_METHOD_1         1  '1 positional argument'
              688  CALL_FUNCTION_1       1  '1 positional argument'
              690  RETURN_VALUE     
            692_0  COME_FROM           626  '626'

 L. 120       692  BUILD_LIST_0          0 
              694  STORE_FAST               'items'

 L. 121       696  SETUP_LOOP          726  'to 726'
              698  LOAD_FAST                'value'
              700  GET_ITER         
              702  FOR_ITER            724  'to 724'
              704  STORE_FAST               'obj'

 L. 122       706  LOAD_FAST                'items'
              708  LOAD_METHOD              append
              710  LOAD_GLOBAL              str
            712_0  COME_FROM           412  '412'
              712  LOAD_FAST                'obj'
              714  CALL_FUNCTION_1       1  '1 positional argument'
              716  CALL_METHOD_1         1  '1 positional argument'
              718  POP_TOP          
          720_722  JUMP_BACK           702  'to 702'
              724  POP_BLOCK        
            726_0  COME_FROM_LOOP      696  '696'

 L. 123       726  LOAD_STR                 ', '
              728  LOAD_METHOD              join
              730  LOAD_FAST                'items'
              732  CALL_METHOD_1         1  '1 positional argument'
              734  RETURN_VALUE     
              736  JUMP_FORWARD        746  'to 746'
            738_0  COME_FROM           620  '620'

 L. 125       738  LOAD_GLOBAL              str
              740  LOAD_FAST                'value'
              742  CALL_FUNCTION_1       1  '1 positional argument'
              744  RETURN_VALUE     
            746_0  COME_FROM           736  '736'
            746_1  COME_FROM           610  '610'
            746_2  COME_FROM           444  '444'
            746_3  COME_FROM           326  '326'
            746_4  COME_FROM           270  '270'
            746_5  COME_FROM           110  '110'

Parse error at or near `COME_FROM' instruction at offset 712_0


def format_decimal(value, decimal_places=2):
    str_format = '{{:.{}f}}'.format(decimal_places)
    if value is not None:
        value = str_format.format(Decimal(value))
        if settings.LANGUAGE_CODE == 'pt-br':
            value = value.replace('.', ',')
    return value


def format_decimal3(value):
    if value is None:
        return ''
    return format_decimalvalue3


def format_decimal1(value):
    if value is None:
        return ''
    return format_decimalvalue1


def to_ascii(txt, codif='utf-8'):
    if not isinstancetxtstr:
        txt = str(txt)
    if isinstancetxtstr:
        txt = txt.encode('utf-8')
    return unicodedata.normalize('NFKD', txt.decode(codif)).encode('ASCII', 'ignore').decode('utf-8')