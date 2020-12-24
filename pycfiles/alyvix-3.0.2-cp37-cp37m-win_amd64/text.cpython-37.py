# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\python\envs\alyvix\alyvix_py37\lib\site-packages\alyvix\core\engine\text.py
# Compiled at: 2020-01-28 05:51:43
# Size of source mod 2**32: 35519 bytes
import os, time, cv2, numpy as np, re, difflib, datetime
import alyvix.core.tesserocr as tesserocr
from PIL import Image
from alyvix.tools.screen import ScreenManager
from alyvix.core.contouring import ContouringManager

class Result:

    def __init__(self):
        self.x = None
        self.y = None
        self.w = None
        self.h = None
        self.type = 'T'
        self.scraped_text = None
        self.group = 0
        self.is_main = False
        self.index_in_tree = 0
        self.index_in_group = 0
        self.mouse = {}
        self.keyboard = {}
        self.roi = None
        self.extract_text = None
        self.check = False


class TextManager:

    def __init__(self):
        self._color_screen = None
        self._gray_screen = None
        self._scaling_factor = None
        self._scale_for_tesseract = 2
        self._regexp = ''
        self._arguments = None
        self._tessdata_path = os.path.dirname(__file__) + os.sep + 'tessdata'
        self._map = None
        self._dict_month = {'ja(m|n|nn)uar(y|v)':'1', 
         '(7|f|t)ebruar(y|v)':'2', 
         '(m|n|nn)arch':'3', 
         'apr(l|1|i)(l|1|i)':'4', 
         '(m|n|nn)a(y|v)':'5', 
         'ju(m|n|nn)e':'6', 
         'ju(l|1|i)(y|v)':'7', 
         'au(g|q)u(5|s)(7|f|t)':'8', 
         '(5|s)ep(7|f|t)e(m|n|nn)ber':'9', 
         '(o|0)c(7|f|t)(o|0)ber':'10', 
         '(m|n|nn)(o|0)(y|v)e(m|n|nn)ber':'11', 
         'dece(m|n|nn)ber':'12', 
         'ja(m|n|nn).':'1', 
         '(7|f|t)eb.':'2', 
         '(m|n|nn)ar.':'3', 
         'apr.':'4', 
         '(m|n|nn)a(y|v).':'5', 
         'ju(m|n|nn).':'6', 
         'ju(l|1|i).':'7', 
         'au(g|q).':'8', 
         '(5|s)ep.':'9', 
         '(o|0)c(7|f|t).':'10', 
         '(m|n|nn)(o|0)(v|y).':'11', 
         'dec.':'12', 
         '(g|q)e((m|n|nn)(m|n|nn)|m|nn)a(l|1|i)(o|0)':'1', 
         '(7|f|t)ebbra(l|1|i)(o|0)':'2', 
         '(m|n|nn)arz(o|0)':'3', 
         'apr(l|1|i)(l|1|i)e':'4', 
         '(m|n|nn)a(g|q)(g|q)(l|1|i)(o|0)':'5', 
         '(g|q)(l|1|i)u(g|q)n(o|0)':'6', 
         'lu(g|q)(l|1|i)(l|1|i)(o|0)':'7', 
         'a(g|q)(o|0)(5|s)(7|f|t)(o|0)':'8', 
         '(5|s)e(7|f|t)(7|f|t)e(m|n|nn)bre':'9', 
         '(o|0)(7|f|t)(7|f|t)(o|0)bre':'10', 
         '(m|n|nn)(o|0)ve(m|n|nn)bre':'11', 
         'd(l|1|i)ce(m|n|nn)bre':'12', 
         '(g|q)e(m|n|nn).':'1', 
         '(7|f|t)eb.':'2', 
         '(m|n|nn)ar.':'3', 
         'apr.':'4', 
         '(m|n|nn)a(g|q).':'5', 
         '(g|q)(l|1|i)u.':'6', 
         '(l|1|i)u(g|q).':'7', 
         'a(g|q)(o|0).':'8', 
         '(5|s)e(7|f|t).':'9', 
         '(o|0)(7|f|t)(7|f|t).':'10', 
         '(m|n|nn)(o|0)(y|v).':'11', 
         'd(l|1|i)c.':'12'}

    def set_color_screen(self, screen):
        self._color_screen = screen

    def set_gray_screen(self, screen):
        self._gray_screen = screen

    def set_scaling_factor(self, scaling_factor):
        self._scaling_factor = scaling_factor

    def set_regexp(self, regexp, args=None, maps={}, executed_objects=[]):
        self._regexp = regexp
        args_in_string = re.findall('\\{[1-9]\\d*\\}', self._regexp, re.IGNORECASE)
        for arg_pattern in args_in_string:
            try:
                i = int(arg_pattern.lower().replace('{', '').replace('}', ''))
                self._regexp = self._regexp.replace(arg_pattern, args[(i - 1)])
            except:
                pass

        extract_args = re.findall('\\{.*\\.extract\\}', self._regexp, re.IGNORECASE)
        for arg_pattern in extract_args:
            try:
                obj_name = arg_pattern.lower().replace('{', '').replace('}', '')
                obj_name = obj_name.split('.')[0]
                extract_value = None
                for executed_obj in executed_objects:
                    if executed_obj.object_name == obj_name:
                        extract_value = executed_obj.records['extract']

                if extract_value is not None:
                    self._regexp = self._regexp.replace(arg_pattern, extract_value)
            except:
                pass

        text_args = re.findall('\\{.*\\.text\\}', self._regexp, re.IGNORECASE)
        for arg_pattern in text_args:
            try:
                obj_name = arg_pattern.lower().replace('{', '').replace('}', '')
                obj_name = obj_name.split('.')[0]
                text_value = None
                for executed_obj in executed_objects:
                    if executed_obj.object_name == obj_name:
                        text_value = executed_obj.records['text']

                if text_value is not None:
                    self._regexp = self._regexp.replace(arg_pattern, text_value)
            except:
                pass

        check_args = re.findall('\\{.*\\.check\\}', self._regexp, re.IGNORECASE)
        for arg_pattern in check_args:
            try:
                obj_name = arg_pattern.lower().replace('{', '').replace('}', '')
                obj_name = obj_name.split('.')[0]
                check_value = None
                for executed_obj in executed_objects:
                    if executed_obj.object_name == obj_name:
                        check_value = executed_obj.records['check']

                if check_value is not None:
                    self._regexp = self._regexp.replace(arg_pattern, str(check_value))
            except:
                pass

        maps_args = re.findall('\\{.*\\..*\\}', self._regexp, re.IGNORECASE)
        for arg_pattern in maps_args:
            try:
                map_arg = arg_pattern.lower().replace('{', '').replace('}', '')
                map_name = map_arg.split('.')[0]
                map_key = map_arg.split('.')[1]
                map_value = maps[map_name][map_key]
                if isinstance(map_value, list):
                    str_value = ''
                    for obj in map_value:
                        str_value += str(obj) + ' '

                    str_value = str_value[:-1]
                else:
                    str_value = str(map_value)
                self._regexp = self._regexp.replace(arg_pattern, str_value)
            except:
                pass

    def _build_regexp(self, string):
        regexp = ''
        for char in string:
            if char in ('a', '4'):
                regexp += '[a4]'
            elif char in ('b', 'h', '6', 'g', '8'):
                regexp += '[bh6g8]'
            elif char in ('d', 'o', '0'):
                regexp += '[do0]'
            elif char in ('e', '3'):
                regexp += '[e3]'
            elif char in ('f', 't', '7'):
                regexp += '[ft7]'
            elif char in ('i', 'l', '1', '|'):
                regexp += '[il1|]'
            elif char in ('s', '5'):
                regexp += '[s5]'
            elif char in ('z', '2', 'k'):
                regexp += '[z2l1k]'
            else:
                regexp += char

        return regexp

    def _build_month_regexp(self):
        regexp = '('
        for month in self._dict_month:
            regexp += month.replace('.', '\\.') + '|'

        regexp = regexp[:-1]
        regexp += ')'
        return regexp

    def _char_to_number(self, string):
        return string.replace('z', '2').replace('s', '5').replace('o', '0').replace('i', '1').replace('l', '1').replace('f', '7').replace('t', '7')

    def _get_char_as_number(self):
        return '([0-9]|b|[li]|z|o|e|t|s)'

    def _get_hour_str(self, hour_str):
        reg_number = self._get_char_as_number()
        hour = re.search('(' + reg_number + '{2}:' + reg_number + '{2}:' + reg_number + '{2}.*(pm|am))', hour_str, re.IGNORECASE)
        if hour is not None:
            hour = hour.group(0).replace(' ', '')
            hour = self._char_to_number(hour)
            return (
             hour, '%I:%M:%S%p')
        hour = re.search('(' + reg_number + '{2}:' + reg_number + '{2}\\.' + reg_number + '{2}.*(pm|am))', hour_str, re.IGNORECASE)
        if hour is not None:
            hour = hour.group(0).replace(' ', '')
            hour = self._char_to_number(hour)
            return (
             hour, '%I:%M:%S%p')
        hour = re.search('(' + reg_number + '{2}:' + reg_number + '{2}:' + reg_number + '{2})', hour_str)
        if hour is not None:
            hour = hour.group(0)
            hour = self._char_to_number(hour)
            return (
             hour, '%H:%M:%S')
        hour = re.search('(' + reg_number + '{2}:' + reg_number + '{2})', hour_str)
        if hour is not None:
            hour = hour.group(0)
            hour = self._char_to_number(hour)
            return (
             hour, '%H:%M')
        hour = re.search('(' + reg_number + '{2}:' + reg_number + '{2}.' + reg_number + '{2})', hour_str)
        if hour is not None:
            hour = hour.group(0)
            hour = self._char_to_number(hour)
            return (
             hour, '%H:%M:%S')
        hour = re.search('(' + reg_number + '{6})', hour_str)
        if hour is not None:
            hour = hour.group(0)
            hour = self._char_to_number(hour)
            return (
             hour, '%H%M%S')
        return ('', '')

    def _get_date_str(self, date_str):
        reg_number = self._get_char_as_number()
        date = re.search('(' + reg_number + '{2}/' + reg_number + '{2}/' + reg_number + '{4})', date_str)
        if date is not None:
            date = date.group(0)
            date = self._char_to_number(date)
            return (
             date, '%d/%m/%Y')
        month_reg = self._build_month_regexp()
        date = re.search('(' + reg_number + '{1,2} ' + month_reg + ' ' + reg_number + '{4})', date_str)
        if date is not None:
            date = date.group(0)
            arr = date.split(' ')
            day = arr[0]
            month = arr[1]
            year = arr[2]
            day = self._char_to_number(day)
            year = self._char_to_number(year)
            for month_reg in self._dict_month:
                res = re.search(month_reg, month)
                if res is not None:
                    number_of_month = self._dict_month[month_reg]
                    break

            return (
             day + ' ' + number_of_month + ' ' + year, '%d %m %Y')
        date = re.search('(' + month_reg + ' ' + reg_number + '{1,2}, ' + reg_number + '{4})', date_str)
        if date is not None:
            date = date.group(0)
            arr = date.split(' ')
            day = arr[1].replace(',', '')
            month = arr[0]
            year = arr[2]
            day = self._char_to_number(day)
            year = self._char_to_number(year)
            for month_reg in self._dict_month:
                res = re.search(month_reg, month)
                if res is not None:
                    number_of_month = self._dict_month[month_reg]
                    break

            return (
             number_of_month + ' ' + day + ', ' + year, '%m %d, %Y')
        date = re.search('(' + reg_number + '{4}/' + reg_number + '{2}/' + reg_number + '{2})', date_str)
        if date is not None:
            date = date.group(0)
            date = self._char_to_number(date)
            return (
             date, '%Y/%m/%d')
        date = re.search('(' + reg_number + '{8})', date_str)
        if date is not None:
            date = date.group(0)
            date = self._char_to_number(date)
            return (date, '%Y%m%d')
        return ('', '')

    def scrape--- This code section failed: ---

 L. 425         0  LOAD_FAST                'map_dict'
                2  LOAD_CONST               None
                4  COMPARE_OP               is-not
              6_8  POP_JUMP_IF_FALSE   398  'to 398'

 L. 426        10  BUILD_LIST_0          0 
               12  STORE_FAST               'result_list'

 L. 427        14  LOAD_FAST                'self'
               16  LOAD_ATTR                _find_sub
               18  LOAD_FAST                'roi'
               20  LOAD_CONST               True
               22  LOAD_CONST               ('scrape',)
               24  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               26  STORE_FAST               'scraped_text'

 L. 429     28_30  SETUP_LOOP         1194  'to 1194'
               32  LOAD_FAST                'scraped_text'
               34  GET_ITER         
             36_0  COME_FROM           364  '364'
             36_1  COME_FROM            50  '50'
            36_38  FOR_ITER            392  'to 392'
               40  STORE_FAST               's_text'

 L. 431        42  LOAD_FAST                's_text'
               44  LOAD_ATTR                scraped_text
               46  LOAD_STR                 ''
               48  COMPARE_OP               !=
               50  POP_JUMP_IF_FALSE    36  'to 36'

 L. 433        52  SETUP_LOOP          210  'to 210'
               54  LOAD_FAST                'map_dict'
               56  GET_ITER         
             58_0  COME_FROM           188  '188'
               58  FOR_ITER            208  'to 208'
               60  STORE_FAST               'key'

 L. 435        62  LOAD_GLOBAL              len
               64  LOAD_FAST                's_text'
               66  LOAD_ATTR                scraped_text
               68  CALL_FUNCTION_1       1  '1 positional argument'
               70  LOAD_GLOBAL              len
               72  LOAD_FAST                'key'
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  COMPARE_OP               >=
               78  POP_JUMP_IF_FALSE   132  'to 132'

 L. 437        80  LOAD_FAST                'self'
               82  LOAD_METHOD              _build_regexp
               84  LOAD_FAST                'key'
               86  CALL_METHOD_1         1  '1 positional argument'
               88  STORE_FAST               'regexp'

 L. 440        90  LOAD_GLOBAL              re
               92  LOAD_METHOD              match
               94  LOAD_STR                 '.*'
               96  LOAD_FAST                'regexp'
               98  BINARY_ADD       
              100  LOAD_STR                 '.*'
              102  BINARY_ADD       
              104  LOAD_FAST                's_text'
              106  LOAD_ATTR                scraped_text
              108  LOAD_METHOD              replace
              110  LOAD_STR                 ' '
              112  LOAD_STR                 '.*'
              114  CALL_METHOD_2         2  '2 positional arguments'
              116  LOAD_GLOBAL              re
              118  LOAD_ATTR                DOTALL
              120  LOAD_GLOBAL              re
              122  LOAD_ATTR                IGNORECASE
              124  BINARY_OR        
              126  CALL_METHOD_3         3  '3 positional arguments'
              128  STORE_FAST               'result'
              130  JUMP_FORWARD        182  'to 182'
            132_0  COME_FROM            78  '78'

 L. 443       132  LOAD_FAST                'self'
              134  LOAD_METHOD              _build_regexp
              136  LOAD_FAST                's_text'
              138  LOAD_ATTR                scraped_text
              140  LOAD_METHOD              replace
              142  LOAD_STR                 ' '
              144  LOAD_STR                 '.*'
              146  CALL_METHOD_2         2  '2 positional arguments'
              148  CALL_METHOD_1         1  '1 positional argument'
              150  STORE_FAST               'regexp'

 L. 445       152  LOAD_GLOBAL              re
              154  LOAD_METHOD              match
              156  LOAD_STR                 '.*'
              158  LOAD_FAST                'regexp'
              160  BINARY_ADD       
              162  LOAD_STR                 '.*'
              164  BINARY_ADD       
              166  LOAD_FAST                'key'
              168  LOAD_GLOBAL              re
              170  LOAD_ATTR                DOTALL
              172  LOAD_GLOBAL              re
              174  LOAD_ATTR                IGNORECASE
              176  BINARY_OR        
              178  CALL_METHOD_3         3  '3 positional arguments'
              180  STORE_FAST               'result'
            182_0  COME_FROM           130  '130'

 L. 447       182  LOAD_FAST                'result'
              184  LOAD_CONST               None
              186  COMPARE_OP               is-not
              188  POP_JUMP_IF_FALSE    58  'to 58'

 L. 448       190  LOAD_FAST                'result_list'
              192  LOAD_METHOD              append
              194  LOAD_FAST                'key'
              196  LOAD_CONST               0.2
              198  LOAD_CONST               ('key', 'score')
              200  BUILD_CONST_KEY_MAP_2     2 
              202  CALL_METHOD_1         1  '1 positional argument'
              204  POP_TOP          
              206  JUMP_BACK            58  'to 58'
              208  POP_BLOCK        
            210_0  COME_FROM_LOOP       52  '52'

 L. 453       210  SETUP_LOOP          336  'to 336'
              212  LOAD_FAST                'result_list'
              214  GET_ITER         
              216  FOR_ITER            334  'to 334'
              218  STORE_FAST               'result'

 L. 455       220  LOAD_FAST                'result'
              222  LOAD_STR                 'score'
              224  BINARY_SUBSCR    
              226  STORE_FAST               'score'

 L. 456       228  LOAD_GLOBAL              difflib
              230  LOAD_METHOD              get_close_matches
              232  LOAD_FAST                's_text'
              234  LOAD_ATTR                scraped_text
              236  LOAD_FAST                'result'
              238  LOAD_STR                 'key'
              240  BINARY_SUBSCR    
              242  BUILD_LIST_1          1 
              244  LOAD_CONST               1
              246  LOAD_CONST               0.2
              248  CALL_METHOD_4         4  '4 positional arguments'
              250  STORE_FAST               'best_match'

 L. 457       252  LOAD_GLOBAL              len
              254  LOAD_FAST                'best_match'
              256  CALL_FUNCTION_1       1  '1 positional argument'
              258  LOAD_CONST               0
              260  COMPARE_OP               >
          262_264  POP_JUMP_IF_FALSE   290  'to 290'

 L. 458       266  LOAD_GLOBAL              difflib
              268  LOAD_METHOD              SequenceMatcher
              270  LOAD_CONST               None
              272  LOAD_FAST                's_text'
              274  LOAD_ATTR                scraped_text
              276  LOAD_FAST                'best_match'
              278  LOAD_CONST               0
              280  BINARY_SUBSCR    
              282  CALL_METHOD_3         3  '3 positional arguments'
              284  LOAD_METHOD              ratio
              286  CALL_METHOD_0         0  '0 positional arguments'
              288  STORE_FAST               'score'
            290_0  COME_FROM           262  '262'

 L. 466       290  LOAD_GLOBAL              abs
              292  LOAD_GLOBAL              len
              294  LOAD_FAST                's_text'
              296  LOAD_ATTR                scraped_text
              298  CALL_FUNCTION_1       1  '1 positional argument'
              300  LOAD_GLOBAL              len
              302  LOAD_FAST                'result'
              304  LOAD_STR                 'key'
              306  BINARY_SUBSCR    
              308  CALL_FUNCTION_1       1  '1 positional argument'
              310  BINARY_SUBTRACT  
              312  CALL_FUNCTION_1       1  '1 positional argument'
              314  STORE_FAST               'diff_len'

 L. 468       316  LOAD_FAST                'score'
              318  LOAD_FAST                'diff_len'
              320  LOAD_CONST               1000000000000
              322  BINARY_TRUE_DIVIDE
              324  BINARY_SUBTRACT  
              326  LOAD_FAST                'result'
              328  LOAD_STR                 'score'
              330  STORE_SUBSCR     
              332  JUMP_BACK           216  'to 216'
              334  POP_BLOCK        
            336_0  COME_FROM_LOOP      210  '210'

 L. 472       336  LOAD_GLOBAL              sorted
              338  LOAD_FAST                'result_list'
              340  LOAD_LAMBDA              '<code_object <lambda>>'
              342  LOAD_STR                 'TextManager.scrape.<locals>.<lambda>'
              344  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              346  LOAD_CONST               True
              348  LOAD_CONST               ('key', 'reverse')
              350  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              352  STORE_FAST               'result_list'

 L. 475       354  LOAD_GLOBAL              len
              356  LOAD_FAST                'result_list'
              358  CALL_FUNCTION_1       1  '1 positional argument'
              360  LOAD_CONST               0
              362  COMPARE_OP               >
              364  POP_JUMP_IF_FALSE    36  'to 36'

 L. 476       366  LOAD_FAST                'map_dict'
              368  LOAD_FAST                'result_list'
              370  LOAD_CONST               0
              372  BINARY_SUBSCR    
              374  LOAD_STR                 'key'
              376  BINARY_SUBSCR    
              378  BINARY_SUBSCR    
              380  LOAD_FAST                's_text'
              382  STORE_ATTR               extract_text

 L. 477       384  LOAD_CONST               True
              386  LOAD_FAST                's_text'
              388  STORE_ATTR               check
              390  JUMP_BACK            36  'to 36'
              392  POP_BLOCK        
          394_396  JUMP_FORWARD       1194  'to 1194'
            398_0  COME_FROM             6  '6'

 L. 479       398  LOAD_FAST                'logic'
              400  LOAD_CONST               None
              402  COMPARE_OP               is-not
          404_406  POP_JUMP_IF_FALSE  1158  'to 1158'

 L. 480       408  LOAD_STR                 'date'
              410  LOAD_FAST                'logic'
              412  COMPARE_OP               in
          414_416  POP_JUMP_IF_FALSE  1022  'to 1022'

 L. 481       418  LOAD_FAST                'self'
              420  LOAD_ATTR                _find_sub
              422  LOAD_FAST                'roi'
              424  LOAD_CONST               True
              426  LOAD_CONST               ('scrape',)
              428  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              430  STORE_FAST               'scraped_text'

 L. 483   432_434  SETUP_LOOP         1156  'to 1156'
              436  LOAD_FAST                'scraped_text'
              438  GET_ITER         
            440_0  COME_FROM           998  '998'
            440_1  COME_FROM           976  '976'
            440_2  COME_FROM           756  '756'
            440_3  COME_FROM           454  '454'
          440_442  FOR_ITER           1018  'to 1018'
              444  STORE_FAST               's_text'

 L. 485       446  LOAD_FAST                's_text'
              448  LOAD_ATTR                scraped_text
              450  LOAD_STR                 ''
              452  COMPARE_OP               !=
          454_456  POP_JUMP_IF_FALSE   440  'to 440'

 L. 487       458  LOAD_GLOBAL              re
              460  LOAD_METHOD              sub
              462  LOAD_STR                 '\\s+'
              464  LOAD_STR                 ' '
              466  LOAD_FAST                's_text'
              468  LOAD_ATTR                scraped_text
              470  LOAD_METHOD              lower
              472  CALL_METHOD_0         0  '0 positional arguments'
              474  CALL_METHOD_3         3  '3 positional arguments'
              476  LOAD_METHOD              strip
              478  CALL_METHOD_0         0  '0 positional arguments'
              480  STORE_FAST               'scraped_text_one_space'

 L. 489       482  LOAD_FAST                'self'
              484  LOAD_METHOD              _get_date_str
              486  LOAD_FAST                'scraped_text_one_space'
              488  CALL_METHOD_1         1  '1 positional argument'
              490  STORE_FAST               'date'

 L. 491       492  LOAD_FAST                'self'
              494  LOAD_METHOD              _get_hour_str
              496  LOAD_FAST                'scraped_text_one_space'
              498  CALL_METHOD_1         1  '1 positional argument'
              500  STORE_FAST               'hour'

 L. 493       502  LOAD_STR                 ''
              504  STORE_FAST               'extract_text'

 L. 494       506  LOAD_FAST                'date'
              508  LOAD_CONST               0
              510  BINARY_SUBSCR    
              512  LOAD_STR                 ''
              514  COMPARE_OP               !=
          516_518  POP_JUMP_IF_FALSE   592  'to 592'
              520  LOAD_FAST                'hour'
              522  LOAD_CONST               0
              524  BINARY_SUBSCR    
              526  LOAD_STR                 ''
              528  COMPARE_OP               !=
          530_532  POP_JUMP_IF_FALSE   592  'to 592'

 L. 495       534  LOAD_GLOBAL              datetime
              536  LOAD_ATTR                datetime
              538  LOAD_METHOD              strptime
              540  LOAD_FAST                'date'
              542  LOAD_CONST               0
              544  BINARY_SUBSCR    
              546  LOAD_STR                 ' '
              548  BINARY_ADD       
              550  LOAD_FAST                'hour'
              552  LOAD_CONST               0
              554  BINARY_SUBSCR    
              556  BINARY_ADD       
              558  LOAD_FAST                'date'
              560  LOAD_CONST               1
              562  BINARY_SUBSCR    
              564  LOAD_STR                 ' '
              566  BINARY_ADD       
              568  LOAD_FAST                'hour'
              570  LOAD_CONST               1
              572  BINARY_SUBSCR    
              574  BINARY_ADD       
              576  CALL_METHOD_2         2  '2 positional arguments'
              578  STORE_FAST               'date_time'

 L. 496       580  LOAD_FAST                'date_time'
              582  LOAD_METHOD              strftime
              584  LOAD_STR                 '%Y%m%d%H%M%S'
              586  CALL_METHOD_1         1  '1 positional argument'
              588  STORE_FAST               'extract_text'
              590  JUMP_FORWARD        750  'to 750'
            592_0  COME_FROM           530  '530'
            592_1  COME_FROM           516  '516'

 L. 498       592  LOAD_FAST                'date'
              594  LOAD_CONST               0
              596  BINARY_SUBSCR    
              598  LOAD_STR                 ''
              600  COMPARE_OP               !=
          602_604  POP_JUMP_IF_FALSE   654  'to 654'
              606  LOAD_FAST                'hour'
              608  LOAD_CONST               0
              610  BINARY_SUBSCR    
              612  LOAD_STR                 ''
              614  COMPARE_OP               ==
          616_618  POP_JUMP_IF_FALSE   654  'to 654'

 L. 499       620  LOAD_GLOBAL              datetime
              622  LOAD_ATTR                datetime
              624  LOAD_METHOD              strptime
              626  LOAD_FAST                'date'
              628  LOAD_CONST               0
              630  BINARY_SUBSCR    
              632  LOAD_FAST                'date'
              634  LOAD_CONST               1
              636  BINARY_SUBSCR    
              638  CALL_METHOD_2         2  '2 positional arguments'
              640  STORE_FAST               'date_time'

 L. 500       642  LOAD_FAST                'date_time'
              644  LOAD_METHOD              strftime
              646  LOAD_STR                 '%Y%m%d%H%M%S'
              648  CALL_METHOD_1         1  '1 positional argument'
              650  STORE_FAST               'extract_text'
              652  JUMP_FORWARD        750  'to 750'
            654_0  COME_FROM           616  '616'
            654_1  COME_FROM           602  '602'

 L. 502       654  LOAD_FAST                'date'
              656  LOAD_CONST               0
              658  BINARY_SUBSCR    
              660  LOAD_STR                 ''
              662  COMPARE_OP               ==
          664_666  POP_JUMP_IF_FALSE   750  'to 750'
              668  LOAD_FAST                'hour'
              670  LOAD_CONST               0
              672  BINARY_SUBSCR    
              674  LOAD_STR                 ''
              676  COMPARE_OP               !=
          678_680  POP_JUMP_IF_FALSE   750  'to 750'

 L. 503       682  LOAD_GLOBAL              datetime
              684  LOAD_ATTR                datetime
              686  LOAD_METHOD              strptime
              688  LOAD_FAST                'hour'
              690  LOAD_CONST               0
              692  BINARY_SUBSCR    
              694  LOAD_FAST                'hour'
              696  LOAD_CONST               1
              698  BINARY_SUBSCR    
              700  CALL_METHOD_2         2  '2 positional arguments'
              702  STORE_FAST               'date_time'

 L. 504       704  LOAD_GLOBAL              datetime
              706  LOAD_ATTR                datetime
              708  LOAD_METHOD              now
              710  CALL_METHOD_0         0  '0 positional arguments'
              712  STORE_FAST               'date_now'

 L. 505       714  LOAD_FAST                'date_now'
              716  LOAD_ATTR                replace
              718  LOAD_FAST                'date_time'
              720  LOAD_ATTR                hour
              722  LOAD_FAST                'date_time'
              724  LOAD_ATTR                minute
              726  LOAD_FAST                'date_time'
              728  LOAD_ATTR                second
              730  LOAD_CONST               ('hour', 'minute', 'second')
              732  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              734  STORE_FAST               'date_now'

 L. 506       736  LOAD_FAST                'date_now'
              738  STORE_FAST               'date_time'

 L. 507       740  LOAD_FAST                'date_time'
              742  LOAD_METHOD              strftime
              744  LOAD_STR                 '%Y%m%d%H%M%S'
              746  CALL_METHOD_1         1  '1 positional argument'
              748  STORE_FAST               'extract_text'
            750_0  COME_FROM           678  '678'
            750_1  COME_FROM           664  '664'
            750_2  COME_FROM           652  '652'
            750_3  COME_FROM           590  '590'

 L. 509       750  LOAD_FAST                'extract_text'
              752  LOAD_STR                 ''
              754  COMPARE_OP               !=
          756_758  POP_JUMP_IF_FALSE   440  'to 440'

 L. 511       760  LOAD_GLOBAL              datetime
              762  LOAD_ATTR                datetime
              764  LOAD_METHOD              now
              766  CALL_METHOD_0         0  '0 positional arguments'
              768  STORE_FAST               'date_now'

 L. 512       770  LOAD_FAST                'date_time'
              772  LOAD_ATTR                hour
              774  LOAD_CONST               0
              776  COMPARE_OP               ==
          778_780  POP_JUMP_IF_FALSE   832  'to 832'
              782  LOAD_FAST                'date_time'
              784  LOAD_ATTR                minute
              786  LOAD_CONST               0
              788  COMPARE_OP               ==
          790_792  POP_JUMP_IF_FALSE   832  'to 832'
              794  LOAD_FAST                'date_time'
              796  LOAD_ATTR                second
              798  LOAD_CONST               0
              800  COMPARE_OP               ==
          802_804  POP_JUMP_IF_FALSE   832  'to 832'

 L. 513       806  LOAD_FAST                'date_time'
              808  LOAD_ATTR                replace
              810  LOAD_FAST                'date_now'
              812  LOAD_ATTR                hour
              814  LOAD_FAST                'date_now'
              816  LOAD_ATTR                minute

 L. 514       818  LOAD_FAST                'date_now'
              820  LOAD_ATTR                second

 L. 515       822  LOAD_FAST                'date_now'
              824  LOAD_ATTR                microsecond
              826  LOAD_CONST               ('hour', 'minute', 'second', 'microsecond')
              828  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
              830  STORE_FAST               'date_time'
            832_0  COME_FROM           802  '802'
            832_1  COME_FROM           790  '790'
            832_2  COME_FROM           778  '778'

 L. 517       832  LOAD_FAST                'logic'
              834  LOAD_STR                 'date_last_hour'
              836  COMPARE_OP               ==
          838_840  POP_JUMP_IF_FALSE   878  'to 878'

 L. 518       842  LOAD_FAST                'date_time'
              844  LOAD_FAST                'date_now'
              846  LOAD_GLOBAL              datetime
              848  LOAD_ATTR                timedelta
              850  LOAD_CONST               1
              852  LOAD_CONST               ('hours',)
              854  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              856  BINARY_SUBTRACT  
              858  COMPARE_OP               >=
          860_862  POP_JUMP_IF_FALSE  1014  'to 1014'

 L. 519       864  LOAD_CONST               True
              866  LOAD_FAST                's_text'
              868  STORE_ATTR               check

 L. 520       870  LOAD_FAST                'extract_text'
              872  LOAD_FAST                's_text'
              874  STORE_ATTR               extract_text
              876  JUMP_BACK           440  'to 440'
            878_0  COME_FROM           838  '838'

 L. 521       878  LOAD_FAST                'logic'
              880  LOAD_STR                 'date_last_day'
              882  COMPARE_OP               ==
          884_886  POP_JUMP_IF_FALSE   924  'to 924'

 L. 522       888  LOAD_FAST                'date_time'
              890  LOAD_FAST                'date_now'
              892  LOAD_GLOBAL              datetime
              894  LOAD_ATTR                timedelta
              896  LOAD_CONST               1
              898  LOAD_CONST               ('days',)
              900  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              902  BINARY_SUBTRACT  
              904  COMPARE_OP               >=
          906_908  POP_JUMP_IF_FALSE  1014  'to 1014'

 L. 523       910  LOAD_CONST               True
              912  LOAD_FAST                's_text'
              914  STORE_ATTR               check

 L. 524       916  LOAD_FAST                'extract_text'
              918  LOAD_FAST                's_text'
              920  STORE_ATTR               extract_text
              922  JUMP_BACK           440  'to 440'
            924_0  COME_FROM           884  '884'

 L. 525       924  LOAD_FAST                'logic'
              926  LOAD_STR                 'date_last_week'
              928  COMPARE_OP               ==
          930_932  POP_JUMP_IF_FALSE   970  'to 970'

 L. 526       934  LOAD_FAST                'date_time'
              936  LOAD_FAST                'date_now'
              938  LOAD_GLOBAL              datetime
              940  LOAD_ATTR                timedelta
              942  LOAD_CONST               7
              944  LOAD_CONST               ('days',)
              946  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              948  BINARY_SUBTRACT  
              950  COMPARE_OP               >=
          952_954  POP_JUMP_IF_FALSE  1014  'to 1014'

 L. 527       956  LOAD_CONST               True
              958  LOAD_FAST                's_text'
              960  STORE_ATTR               check

 L. 528       962  LOAD_FAST                'extract_text'
              964  LOAD_FAST                's_text'
              966  STORE_ATTR               extract_text
              968  JUMP_BACK           440  'to 440'
            970_0  COME_FROM           930  '930'

 L. 529       970  LOAD_FAST                'logic'
              972  LOAD_STR                 'date_last_month'
              974  COMPARE_OP               ==
          976_978  POP_JUMP_IF_FALSE   440  'to 440'

 L. 530       980  LOAD_FAST                'date_time'
              982  LOAD_FAST                'date_now'
              984  LOAD_GLOBAL              datetime
              986  LOAD_ATTR                timedelta
              988  LOAD_CONST               31
              990  LOAD_CONST               ('days',)
              992  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              994  BINARY_SUBTRACT  
              996  COMPARE_OP               >=
         998_1000  POP_JUMP_IF_FALSE   440  'to 440'

 L. 531      1002  LOAD_CONST               True
             1004  LOAD_FAST                's_text'
             1006  STORE_ATTR               check

 L. 532      1008  LOAD_FAST                'extract_text'
             1010  LOAD_FAST                's_text'
             1012  STORE_ATTR               extract_text
           1014_0  COME_FROM           952  '952'
           1014_1  COME_FROM           906  '906'
           1014_2  COME_FROM           860  '860'
         1014_1016  JUMP_BACK           440  'to 440'
             1018  POP_BLOCK        
             1020  JUMP_FORWARD       1156  'to 1156'
           1022_0  COME_FROM           414  '414'

 L. 534      1022  LOAD_STR                 'number'
             1024  LOAD_FAST                'logic'
             1026  COMPARE_OP               in
         1028_1030  POP_JUMP_IF_FALSE  1194  'to 1194'

 L. 535      1032  LOAD_FAST                'self'
             1034  LOAD_ATTR                _find_sub
             1036  LOAD_FAST                'roi'
             1038  LOAD_CONST               True
             1040  LOAD_CONST               ('scrape',)
             1042  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1044  STORE_FAST               'scraped_text'

 L. 537      1046  SETUP_LOOP         1194  'to 1194'
             1048  LOAD_FAST                'scraped_text'
             1050  GET_ITER         
           1052_0  COME_FROM          1134  '1134'
           1052_1  COME_FROM          1124  '1124'
           1052_2  COME_FROM          1088  '1088'
           1052_3  COME_FROM          1064  '1064'
             1052  FOR_ITER           1154  'to 1154'
             1054  STORE_FAST               's_text'

 L. 539      1056  LOAD_FAST                's_text'
             1058  LOAD_ATTR                scraped_text
             1060  LOAD_STR                 ''
             1062  COMPARE_OP               !=
         1064_1066  POP_JUMP_IF_FALSE  1052  'to 1052'

 L. 546      1068  LOAD_GLOBAL              re
             1070  LOAD_METHOD              search
             1072  LOAD_STR                 '(-[ ]{0,}\\d+|\\d+)'
             1074  LOAD_FAST                's_text'
             1076  LOAD_ATTR                scraped_text
             1078  CALL_METHOD_2         2  '2 positional arguments'
             1080  STORE_FAST               'result'

 L. 548      1082  LOAD_FAST                'result'
             1084  LOAD_CONST               None
             1086  COMPARE_OP               is-not
         1088_1090  POP_JUMP_IF_FALSE  1052  'to 1052'

 L. 550      1092  LOAD_FAST                'result'
             1094  LOAD_METHOD              group
             1096  LOAD_CONST               0
             1098  CALL_METHOD_1         1  '1 positional argument'
             1100  STORE_FAST               'result'

 L. 552      1102  LOAD_GLOBAL              int
             1104  LOAD_FAST                'result'
             1106  LOAD_METHOD              replace
             1108  LOAD_STR                 ' '
             1110  LOAD_STR                 ''
             1112  CALL_METHOD_2         2  '2 positional arguments'
             1114  CALL_FUNCTION_1       1  '1 positional argument'
             1116  STORE_FAST               'int_result'

 L. 554      1118  LOAD_FAST                'logic'
             1120  LOAD_STR                 'number_more_than_zero'
             1122  COMPARE_OP               ==
         1124_1126  POP_JUMP_IF_FALSE  1052  'to 1052'

 L. 555      1128  LOAD_FAST                'int_result'
             1130  LOAD_CONST               0
             1132  COMPARE_OP               >
         1134_1136  POP_JUMP_IF_FALSE  1052  'to 1052'

 L. 556      1138  LOAD_CONST               True
             1140  LOAD_FAST                's_text'
             1142  STORE_ATTR               check

 L. 557      1144  LOAD_FAST                'result'
             1146  LOAD_FAST                's_text'
             1148  STORE_ATTR               extract_text
         1150_1152  JUMP_BACK          1052  'to 1052'
             1154  POP_BLOCK        
           1156_0  COME_FROM_LOOP     1046  '1046'
           1156_1  COME_FROM          1020  '1020'
           1156_2  COME_FROM_LOOP      432  '432'
             1156  JUMP_FORWARD       1194  'to 1194'
           1158_0  COME_FROM           404  '404'

 L. 561      1158  LOAD_FAST                'self'
             1160  LOAD_ATTR                _find_sub
             1162  LOAD_FAST                'roi'
             1164  LOAD_CONST               True
             1166  LOAD_CONST               ('scrape',)
             1168  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
             1170  STORE_FAST               'scraped_text'

 L. 563      1172  SETUP_LOOP         1194  'to 1194'
             1174  LOAD_FAST                'scraped_text'
             1176  GET_ITER         
             1178  FOR_ITER           1192  'to 1192'
             1180  STORE_FAST               's_text'

 L. 564      1182  LOAD_CONST               True
             1184  LOAD_FAST                's_text'
             1186  STORE_ATTR               check
         1188_1190  JUMP_BACK          1178  'to 1178'
             1192  POP_BLOCK        
           1194_0  COME_FROM_LOOP     1172  '1172'
           1194_1  COME_FROM          1156  '1156'
           1194_2  COME_FROM          1028  '1028'
           1194_3  COME_FROM           394  '394'
           1194_4  COME_FROM_LOOP       28  '28'

 L. 566      1194  LOAD_FAST                'scraped_text'
             1196  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_FORWARD' instruction at offset 1156

    def set_scaling_factor(self, scaling_factor):
        self._scaling_factor = scaling_factor

    def find(self, detection, roi=None):
        ret_value = []
        if roi is None:
            ret_value = self._find_main()
        else:
            ret_value = self._find_sub(roi)
        return ret_value

    def _find_main(self):
        source_image = self._color_screen
        objects_found = []
        new_width = int(source_image.shape[1] * self._scale_for_tesseract)
        new_height = int(source_image.shape[0] * self._scale_for_tesseract)
        dim = (new_width, new_height)
        bigger_image = cv2.resize(source_image, dim, interpolation=(cv2.INTER_CUBIC))
        bw_matrix = np.zeros((source_image.shape[0], source_image.shape[1], 1), np.uint8)
        bigger_bw_matrix = np.zeros((int(source_image.shape[0] * self._scale_for_tesseract),
         int(source_image.shape[1] * self._scale_for_tesseract), 1), np.uint8)
        contouring_manager = ContouringManager(canny_threshold1=50.0,
          canny_threshold2=75.0,
          canny_apertureSize=3,
          hough_threshold=10,
          hough_minLineLength=30,
          hough_maxLineGap=1,
          line_angle_tolerance=0,
          ellipse_width=2,
          ellipse_height=2,
          text_roi_emptiness=0.45,
          text_roi_proportion=1.3,
          image_roi_emptiness=0.1,
          vline_hw_proportion=2,
          vline_w_maxsize=10,
          hline_wh_proportion=2,
          hline_h_maxsize=10,
          rect_w_minsize=5,
          rect_h_minsize=5,
          rect_w_maxsize_01=800,
          rect_h_maxsize_01=100,
          rect_w_maxsize_02=100,
          rect_h_maxsize_02=800,
          rect_hw_proportion=2,
          rect_hw_w_maxsize=10,
          rect_wh_proportion=2,
          rect_wh_h_maxsize=10,
          hrect_proximity=10,
          vrect_proximity=10,
          vrect_others_proximity=40,
          hrect_others_proximity=80)
        contouring_manager.auto_contouring(source_image)
        boxes = contouring_manager.getTextBoxes()
        for x, y, w, h in boxes:
            endX = x + w
            endY = y + h
            cv2.rectangle(bw_matrix, (x + 2, y + 2), (endX - 4, endY - 4), (255, 255,
                                                                            255), -1)

        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (55, 3))
        dilation = cv2.dilate(bw_matrix, rect_kernel, iterations=1)
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        boundingBoxes = [cv2.boundingRect(c) for c in contours]
        contours, boundingBoxes = zip(*sorted((zip(contours, boundingBoxes)), key=(lambda b: b[1][1]),
          reverse=False))
        cnt = 0
        t0 = time.time()
        image_pil = Image.fromarray(cv2.cvtColor(bigger_image, cv2.COLOR_BGR2RGB).astype('uint8'))
        H, W = source_image.shape[:2]
        with tesserocr.PyTessBaseAPI(path=(self._tessdata_path), lang='eng') as (api):
            api.SetImage(image_pil)
            api.SetPageSegMode(tesserocr.PSM.AUTO)
            cnt = 0
            text_list = []
            results = []
            text = ''
            for box in boundingBoxes:
                x, y, w, h = box
                x = x * self._scale_for_tesseract
                y = y * self._scale_for_tesseract
                w = w * self._scale_for_tesseract
                h = h * self._scale_for_tesseract
                x = x - 2 * self._scale_for_tesseract
                w = w + 7 * self._scale_for_tesseract
                y = y - 2 * self._scale_for_tesseract
                h = h + 7 * self._scale_for_tesseract
                if h > H * self._scale_for_tesseract:
                    h = H * self._scale_for_tesseract
                if w > W * self._scale_for_tesseract:
                    w = W * self._scale_for_tesseract
                if x < 0:
                    x = 0
                if y < 0:
                    y = 0
                api.SetRectanglexywh
                api.Recognize()
                ri = api.GetIterator()
                level = tesserocr.RIL.WORD
                i = 0
                for r in tesserocr.iterate_level(ri, level):
                    try:
                        symbol = r.GetUTF8Text(level)
                    except:
                        continue

                    conf = r.Confidence(level)
                    if conf > 45:
                        pass
                    else:
                        continue
                    bbox = r.BoundingBoxInternal(level)
                    bbox = (
                     int((bbox[0] + x) / self._scale_for_tesseract),
                     int((bbox[1] + y) / self._scale_for_tesseract),
                     int(bbox[2] / self._scale_for_tesseract),
                     int(bbox[3] / self._scale_for_tesseract))
                    text_list.append((bbox, symbol, conf))
                    text += ' ' + symbol
                    result = re.match('.*' + self._regexp + '.*', text, re.DOTALL | re.IGNORECASE)
                    if result is not None:
                        text_for_result = ''
                        boxes_for_result = []
                        for box in reversed(text_list):
                            text_for_result = box[1] + ' ' + text_for_result
                            boxes_for_result.append(box)
                            result2 = re.match('.*' + self._regexp + '.*', text_for_result, re.DOTALL | re.IGNORECASE)
                            if result2 is not None:
                                boxes_for_result = boxes_for_result[::-1]
                                text_list = []
                                text = ''
                                first_word = boxes_for_result[0]
                                bounding_box = first_word[0]
                                return_value = Result()
                                return_value.x = bounding_box[0]
                                return_value.y = bounding_box[1]
                                return_value.w = bounding_box[2]
                                return_value.h = bounding_box[3]
                                objects_found.append(return_value)
                                break

                        a = 'bb'
                    i += 1

                cnt += 1

        end_T = time.time() - t0
        return objects_found

    def _find_sub(self, roi, scrape=False):
        offset_x = 0
        offset_y = 0
        objects_found = []
        scraped_words = []
        source_img_h, source_img_w = self._gray_screen.shape
        y1 = roi.y
        y2 = y1 + roi.h
        x1 = roi.x
        x2 = x1 + roi.w
        if roi.unlimited_up is True:
            y1 = 0
            y2 = roi.y + roi.h
        if roi.unlimited_down is True:
            y2 = source_img_h
        if roi.unlimited_left is True:
            x1 = 0
            x2 = roi.x + roi.w
        if roi.unlimited_right is True:
            x2 = source_img_w
        if y1 < 0:
            y1 = 0
        else:
            if y1 > source_img_h:
                y1 = source_img_h
            elif y2 < 0:
                y2 = 0
            else:
                if y2 > source_img_h:
                    y2 = source_img_h
                elif x1 < 0:
                    x1 = 0
                else:
                    if x1 > source_img_w:
                        x1 = source_img_w
                if x2 < 0:
                    x2 = 0
                else:
                    if x2 > source_img_w:
                        x2 = source_img_w
            offset_x = x1
            offset_y = y1
            source_image = self._color_screen[y1:y2, x1:x2]
            new_width = int(source_image.shape[1] * self._scale_for_tesseract)
            new_height = int(source_image.shape[0] * self._scale_for_tesseract)
            dim = (new_width, new_height)
            try:
                bigger_image = cv2.resize(source_image, dim, interpolation=(cv2.INTER_CUBIC))
            except:
                return_value = Result()
                return_value.x = 0
                return_value.y = 0
                return_value.w = 0
                return_value.h = 0
                return_value.scraped_text = ''
                objects_found.append(return_value)
                return objects_found
                t0 = time.time()
                image_pil = Image.fromarray(cv2.cvtColor(bigger_image, cv2.COLOR_BGR2RGB).astype('uint8'))
                text = ''
                text_for_finder = ''
                obj_found = True
                with tesserocr.PyTessBaseAPI(path=(self._tessdata_path), lang='eng') as (api):
                    api.SetImage(image_pil)
                    api.SetPageSegMode(tesserocr.PSM.AUTO)
                    cnt = 0
                    text_list = []
                    results = []
                    api.Recognize()
                    ri = api.GetIterator()
                    level = tesserocr.RIL.WORD
                    i = 0
                    for r in tesserocr.iterate_level(ri, level):
                        try:
                            symbol = r.GetUTF8Text(level)
                        except:
                            continue

                        conf = r.Confidence(level)
                        bbox = r.BoundingBoxInternal(level)
                        bbox = (
                         int(bbox[0] / self._scale_for_tesseract),
                         int(bbox[1] / self._scale_for_tesseract),
                         int(bbox[2] / self._scale_for_tesseract),
                         int(bbox[3] / self._scale_for_tesseract))
                        symbol = symbol.replace('—', '-')
                        text_list.append((bbox, symbol, conf))
                        text += ' ' + symbol
                        text_for_finder += ' ' + symbol
                        if scrape is False:
                            result = re.search(self._regexp, text_for_finder, re.DOTALL | re.IGNORECASE)
                            if result is not None:
                                text_for_result = ''
                                boxes_for_result = []
                                for box in reversed(text_list):
                                    text_for_result = box[1] + ' ' + text_for_result
                                    boxes_for_result.append(box)
                                    result2 = re.match('.*' + self._regexp, text_for_result + '.*', re.DOTALL | re.IGNORECASE)
                                    if result2 is not None:
                                        boxes_for_result = boxes_for_result[::-1]
                                        text_list = []
                                        text_for_finder = ''
                                        first_word = boxes_for_result[0]
                                        bounding_box = first_word[0]
                                        return_value = Result()
                                        return_value.x = offset_x + bounding_box[0]
                                        return_value.y = offset_y + bounding_box[1]
                                        return_value.w = bounding_box[2] - bounding_box[0]
                                        return_value.h = bounding_box[3] - bounding_box[1]
                                        return_value.extract_text = result.group(0)
                                        objects_found.append(return_value)
                                        break

                                a = 'bb'
                        else:
                            scraped_words.append(bbox)
                        i += 1

                    cnt += 1
                end_T = time.time() - t0
                if scrape is True:
                    x1 = 999999999
                    y1 = 999999999
                    x2 = 0
                    y2 = 0
                    if len(scraped_words) == 0:
                        return_value = Result()
                        return_value.x = 0
                        return_value.y = 0
                        return_value.w = 0
                        return_value.h = 0
                        return_value.scraped_text = text.lstrip().rstrip()
                        objects_found.append(return_value)
                    else:
                        for word in scraped_words:
                            if word[2] + 5 > roi.w and word[3] + 5 > roi.h and word[0] - 5 < roi.x:
                                if word[1] - 5 < roi.y:
                                    continue
                                if word[0] < x1:
                                    x1 = word[0]
                                if word[1] < y1:
                                    y1 = word[1]
                                if word[2] > x2:
                                    x2 = word[2]
                                if word[3] > y2:
                                    y2 = word[3]

                        return_value = Result()
                        return_value.x = offset_x + x1
                        return_value.y = offset_y + y1
                        return_value.w = x2 - x1
                        return_value.h = y2 - y1
                        return_value.scraped_text = text.lstrip().rstrip()
                        objects_found.append(return_value)
                    return objects_found
                    if len(objects_found) > 0:
                        for obj_found in objects_found:
                            obj_found.scraped_text = text.lstrip().rstrip()

                else:
                    return_value = Result()
                    return_value.x = 0
                    return_value.y = 0
                    return_value.w = 0
                    return_value.h = 0
                    return_value.scraped_text = text.lstrip().rstrip()
                    objects_found.append(return_value)
                return objects_found