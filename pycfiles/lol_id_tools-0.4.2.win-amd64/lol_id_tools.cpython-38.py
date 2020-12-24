# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Users\garym\.virtualenvs\lol_id_tools-eVUSBfmh\Lib\site-packages\lol_id_tools\lol_id_tools.py
# Compiled at: 2020-05-13 06:36:29
# Size of source mod 2**32: 16592 bytes
import concurrent.futures, os, time
from concurrent.futures.thread import ThreadPoolExecutor
from pprint import pprint
import logging as log, requests, joblib
from rapidfuzz import process

class LolIdTools:

    def __init__(self, *init_locales: str):
        """
        A python class for fuzzy matching of champion, items, and rune names in League of Legends.

        :param init_locales: additional locales to load during initialisation.
                    Loads 'en_US' on first run if nothing is specified.

        Examples:
            lit = LolIdTools()
                On first run, will create English language data. On subsequent runs, will load existing data.
            lit = LolIdTools('ko_KR')
                Creates Korean language data if not present in the dump file.

        Display runtime information by showing DEBUG level logging: log.basicConfig(level=log.DEBUG)
        """
        self._save_folder = os.path.join(os.path.expanduser('~'), '.config', 'lol_id_tools')
        if not os.path.exists(self._save_folder):
            os.makedirs(self._save_folder)
        self._app_data_location = os.path.join(self._save_folder, 'id_dictionary.pkl.z')
        self._dd_url = 'https://ddragon.leagueoflegends.com/'
        self._nicknames_url = 'https://raw.githubusercontent.com/mrtolkien/lol_id_tools/master/data/nicknames.json'
        self._names_dict_name = 'from_names'
        self._ids_dict_name = 'from_ids'
        self._locales_list_name = 'loaded_locales'
        self._latest_version_name = 'latest_version'
        self.updating = False
        try:
            self._app_data = joblib.load(self._app_data_location)
            log.debug('LolIdGetter app data loaded from file. Latest version: {}.'.format(self._app_data[self._latest_version_name]))
            for locale in init_locales:
                if locale not in self._app_data[self._locales_list_name]:
                    self.add_locale(locale)

        except (FileNotFoundError, EOFError):
            if init_locales == ():
                init_locales = 'en_US'
            self.reload_app_data(init_locales)

    def get_id--- This code section failed: ---

 L.  87         0  LOAD_FAST                'input_str'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_TRUE     32  'to 32'
                8  LOAD_FAST                'input_str'
               10  LOAD_STR                 'None'
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_TRUE     32  'to 32'
               16  LOAD_FAST                'input_str'
               18  LOAD_STR                 'Loss of Ban'
               20  COMPARE_OP               ==
               22  POP_JUMP_IF_TRUE     32  'to 32'
               24  LOAD_FAST                'input_str'
               26  LOAD_STR                 ''
               28  COMPARE_OP               ==
               30  POP_JUMP_IF_FALSE    36  'to 36'
             32_0  COME_FROM            22  '22'
             32_1  COME_FROM            14  '14'
             32_2  COME_FROM             6  '6'

 L.  88        32  LOAD_CONST               None
               34  RETURN_VALUE     
             36_0  COME_FROM            30  '30'

 L.  90        36  LOAD_DEREF               'self'
               38  LOAD_ATTR                _app_data
               40  LOAD_DEREF               'self'
               42  LOAD_ATTR                _names_dict_name
               44  BINARY_SUBSCR    
               46  LOAD_METHOD              keys
               48  CALL_METHOD_0         0  ''
               50  STORE_FAST               'search_list'

 L.  91        52  LOAD_DEREF               'input_type'
               54  LOAD_CONST               None
               56  COMPARE_OP               is-not
               58  POP_JUMP_IF_FALSE    80  'to 80'

 L.  92        60  LOAD_CLOSURE             'input_type'
               62  LOAD_CLOSURE             'self'
               64  BUILD_TUPLE_2         2 
               66  LOAD_LISTCOMP            '<code_object <listcomp>>'
               68  LOAD_STR                 'LolIdTools.get_id.<locals>.<listcomp>'
               70  MAKE_FUNCTION_8          'closure'
               72  LOAD_FAST                'search_list'
               74  GET_ITER         
               76  CALL_FUNCTION_1       1  ''
               78  STORE_FAST               'search_list'
             80_0  COME_FROM            58  '58'

 L.  93        80  LOAD_DEREF               'locale'
               82  LOAD_CONST               None
               84  COMPARE_OP               is-not
               86  POP_JUMP_IF_FALSE   108  'to 108'

 L.  94        88  LOAD_CLOSURE             'locale'
               90  LOAD_CLOSURE             'self'
               92  BUILD_TUPLE_2         2 
               94  LOAD_LISTCOMP            '<code_object <listcomp>>'
               96  LOAD_STR                 'LolIdTools.get_id.<locals>.<listcomp>'
               98  MAKE_FUNCTION_8          'closure'
              100  LOAD_FAST                'search_list'
              102  GET_ITER         
              104  CALL_FUNCTION_1       1  ''
              106  STORE_FAST               'search_list'
            108_0  COME_FROM            86  '86'

 L.  97       108  LOAD_FAST                'input_str'
              110  LOAD_FAST                'search_list'
              112  COMPARE_OP               in
              114  POP_JUMP_IF_FALSE   168  'to 168'

 L.  98       116  LOAD_FAST                'return_ratio'
              118  POP_JUMP_IF_TRUE    144  'to 144'

 L.  99       120  LOAD_DEREF               'self'
              122  LOAD_ATTR                _app_data
              124  LOAD_DEREF               'self'
              126  LOAD_ATTR                _names_dict_name
              128  BINARY_SUBSCR    
              130  LOAD_FAST                'input_str'
              132  BINARY_SUBSCR    
              134  LOAD_STR                 'id'
              136  BINARY_SUBSCR    
              138  LOAD_CONST               100
              140  BUILD_TUPLE_2         2 
              142  RETURN_VALUE     
            144_0  COME_FROM           118  '118'

 L. 101       144  LOAD_DEREF               'self'
              146  LOAD_ATTR                _app_data
              148  LOAD_DEREF               'self'
              150  LOAD_ATTR                _names_dict_name
              152  BINARY_SUBSCR    
              154  LOAD_FAST                'input_str'
              156  BINARY_SUBSCR    
              158  LOAD_STR                 'id'
              160  BINARY_SUBSCR    
              162  LOAD_CONST               100
              164  BUILD_TUPLE_2         2 
              166  RETURN_VALUE     
            168_0  COME_FROM           114  '114'

 L. 103       168  LOAD_GLOBAL              process
              170  LOAD_METHOD              extractOne
              172  LOAD_FAST                'input_str'
              174  LOAD_FAST                'search_list'
              176  CALL_METHOD_2         2  ''
              178  UNPACK_SEQUENCE_2     2 
              180  STORE_FAST               'tentative_name'
              182  STORE_FAST               'ratio'

 L. 105       184  LOAD_STR                 ' matching from {} to {}.\nType: {}, Locale: {}, Precision ratio: {}'
              186  LOAD_METHOD              format

 L. 106       188  LOAD_FAST                'input_str'

 L. 107       190  LOAD_FAST                'tentative_name'

 L. 108       192  LOAD_DEREF               'self'
              194  LOAD_ATTR                _app_data
              196  LOAD_STR                 'from_names'
              198  BINARY_SUBSCR    
              200  LOAD_FAST                'tentative_name'
              202  BINARY_SUBSCR    
              204  LOAD_STR                 'id_type'
              206  BINARY_SUBSCR    

 L. 109       208  LOAD_DEREF               'self'
              210  LOAD_ATTR                _app_data
              212  LOAD_STR                 'from_names'
              214  BINARY_SUBSCR    
              216  LOAD_FAST                'tentative_name'
              218  BINARY_SUBSCR    
              220  LOAD_STR                 'locale'
              222  BINARY_SUBSCR    

 L. 110       224  LOAD_FAST                'ratio'

 L. 105       226  CALL_METHOD_5         5  ''
              228  STORE_FAST               'log_output'

 L. 113       230  LOAD_FAST                'ratio'
              232  LOAD_CONST               90
              234  COMPARE_OP               >=
          236_238  POP_JUMP_IF_FALSE   256  'to 256'

 L. 114       240  LOAD_GLOBAL              log
              242  LOAD_METHOD              debug
              244  LOAD_STR                 '\tHigh confidence'
              246  LOAD_FAST                'log_output'
              248  BINARY_ADD       
              250  CALL_METHOD_1         1  ''
              252  POP_TOP          
              254  JUMP_FORWARD        354  'to 354'
            256_0  COME_FROM           236  '236'

 L. 115       256  LOAD_CONST               75
              258  LOAD_FAST                'ratio'
              260  DUP_TOP          
              262  ROT_THREE        
              264  COMPARE_OP               <=
          266_268  POP_JUMP_IF_FALSE   280  'to 280'
              270  LOAD_CONST               90
              272  COMPARE_OP               <
          274_276  POP_JUMP_IF_FALSE   300  'to 300'
              278  JUMP_FORWARD        284  'to 284'
            280_0  COME_FROM           266  '266'
              280  POP_TOP          
              282  JUMP_FORWARD        300  'to 300'
            284_0  COME_FROM           278  '278'

 L. 116       284  LOAD_GLOBAL              log
              286  LOAD_METHOD              info
              288  LOAD_STR                 '\tLow confidence'
              290  LOAD_FAST                'log_output'
              292  BINARY_ADD       
              294  CALL_METHOD_1         1  ''
              296  POP_TOP          
              298  JUMP_FORWARD        354  'to 354'
            300_0  COME_FROM           282  '282'
            300_1  COME_FROM           274  '274'

 L. 117       300  LOAD_FAST                'ratio'
              302  LOAD_CONST               75
              304  COMPARE_OP               <=
          306_308  POP_JUMP_IF_FALSE   354  'to 354'

 L. 118       310  LOAD_FAST                'retry'
          312_314  POP_JUMP_IF_FALSE   340  'to 340'

 L. 119       316  LOAD_DEREF               'self'
              318  LOAD_METHOD              reload_app_data
              320  CALL_METHOD_0         0  ''
              322  POP_TOP          

 L. 120       324  LOAD_DEREF               'self'
              326  LOAD_METHOD              get_id
              328  LOAD_FAST                'input_str'
              330  LOAD_DEREF               'input_type'
              332  LOAD_DEREF               'locale'
              334  LOAD_CONST               False
              336  CALL_METHOD_4         4  ''
              338  RETURN_VALUE     
            340_0  COME_FROM           312  '312'

 L. 122       340  LOAD_GLOBAL              log
              342  LOAD_METHOD              warning
              344  LOAD_STR                 '\tVery low confidence'
              346  LOAD_FAST                'log_output'
              348  BINARY_ADD       
              350  CALL_METHOD_1         1  ''
              352  POP_TOP          
            354_0  COME_FROM           306  '306'
            354_1  COME_FROM           298  '298'
            354_2  COME_FROM           254  '254'

 L. 124       354  LOAD_FAST                'return_ratio'
          356_358  POP_JUMP_IF_TRUE    378  'to 378'

 L. 125       360  LOAD_DEREF               'self'
              362  LOAD_ATTR                _app_data
              364  LOAD_STR                 'from_names'
              366  BINARY_SUBSCR    
              368  LOAD_FAST                'tentative_name'
              370  BINARY_SUBSCR    
              372  LOAD_STR                 'id'
              374  BINARY_SUBSCR    
              376  RETURN_VALUE     
            378_0  COME_FROM           356  '356'

 L. 127       378  LOAD_DEREF               'self'
              380  LOAD_ATTR                _app_data
              382  LOAD_STR                 'from_names'
              384  BINARY_SUBSCR    
              386  LOAD_FAST                'tentative_name'
              388  BINARY_SUBSCR    
              390  LOAD_STR                 'id'
              392  BINARY_SUBSCR    
              394  LOAD_FAST                'ratio'
              396  BUILD_TUPLE_2         2 
              398  RETURN_VALUE     

Parse error at or near `BUILD_TUPLE_2' instruction at offset 396

    def get_name--- This code section failed: ---

 L. 146         0  LOAD_FAST                'locale'
                2  LOAD_FAST                'self'
                4  LOAD_ATTR                _app_data
                6  LOAD_FAST                'self'
                8  LOAD_ATTR                _locales_list_name
               10  BINARY_SUBSCR    
               12  COMPARE_OP               not-in
               14  POP_JUMP_IF_FALSE    26  'to 26'

 L. 147        16  LOAD_FAST                'self'
               18  LOAD_METHOD              add_locale
               20  LOAD_FAST                'locale'
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          
             26_0  COME_FROM            14  '14'

 L. 149        26  SETUP_FINALLY        54  'to 54'

 L. 150        28  LOAD_FAST                'self'
               30  LOAD_ATTR                _app_data
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _ids_dict_name
               36  BINARY_SUBSCR    
               38  LOAD_FAST                'input_id'
               40  LOAD_FAST                'locale'
               42  BUILD_TUPLE_2         2 
               44  BINARY_SUBSCR    
               46  LOAD_STR                 'name'
               48  BINARY_SUBSCR    
               50  POP_BLOCK        
               52  RETURN_VALUE     
             54_0  COME_FROM_FINALLY    26  '26'

 L. 151        54  DUP_TOP          
               56  LOAD_GLOBAL              KeyError
               58  COMPARE_OP               exception-match
               60  POP_JUMP_IF_FALSE   106  'to 106'
               62  POP_TOP          
               64  POP_TOP          
               66  POP_TOP          

 L. 152        68  LOAD_FAST                'retry'
               70  POP_JUMP_IF_FALSE    96  'to 96'

 L. 153        72  LOAD_FAST                'self'
               74  LOAD_METHOD              reload_app_data
               76  CALL_METHOD_0         0  ''
               78  POP_TOP          

 L. 154        80  LOAD_FAST                'self'
               82  LOAD_METHOD              get_name
               84  LOAD_FAST                'input_id'
               86  LOAD_FAST                'locale'
               88  LOAD_CONST               False
               90  CALL_METHOD_3         3  ''
               92  POP_TOP          
               94  JUMP_FORWARD        102  'to 102'
             96_0  COME_FROM            70  '70'

 L. 157        96  POP_EXCEPT       
               98  LOAD_CONST               None
              100  RETURN_VALUE     
            102_0  COME_FROM            94  '94'
              102  POP_EXCEPT       
              104  JUMP_FORWARD        108  'to 108'
            106_0  COME_FROM            60  '60'
              106  END_FINALLY      
            108_0  COME_FROM           104  '104'

Parse error at or near `POP_TOP' instruction at offset 64

    def get_translation(self, input_str: str, output_locale: str='en_US', input_type: str=None, input_locale: str=None, retry: bool=False, return_ratio=False):
        """
        Tries to get the translation of a given Riot object name matching with the loaded locals.

        :param input_str: name of the object.
        :param output_locale: the output locale. Default is 'en_US'.
        :param input_type: accepts 'champion', 'item', 'rune'. Default is None.
        :param input_locale: accepts any locale and will load it if needed. Default is None.
        :param retry: will try once to reload all the data if it is not finding a good match. Default is True.
        :return: the best translation result through fuzzy matching.
        :param return_ratio: ask for ratio as well as translation

        Examples:
            lit.get_translation('미스 포츈')
            lit.get_translation('Miss Fortune', 'ko_KR')
            lit.get_translation('MF')   # Returns the "clean name" that was fuzzy matched, can be useful too!
        """
        if input_locale is not None:
            if input_locale not in self._app_data[self._locales_list_name]:
                self.add_locale(input_locale)
        else:
            return return_ratio or self.get_name(self.get_idinput_strinput_typeinput_localeretry, output_locale)
        returned_id, ratio = self.get_idinput_strinput_typeinput_localeretryreturn_ratio
        return (self.get_name(returned_id, output_locale), ratio)

    def show_available_locales(self):
        """
        Displays available locales from Riot.
        """
        pprint(self._get_json('{}cdn/languages.json'.format(self._dd_url)))

    def show_loaded_locales(self):
        """
        Displays loaded locales.
        """
        pprint(self._app_data[self._locales_list_name])

    def add_locale(self, locale: str):
        """
        Adds a new locale to the package.
        To delete locales, regenerate the data with reload_app_data().

        :param locale: locale to add
        """
        while self.updating:
            time.sleep(0.1)

        self.updating = True
        if locale in self._app_data[self._locales_list_name]:
            log.warning('Trying to add an existing locale in {}. Exiting.'.format(locale))
            self.updating = False
            return
        log.info('Adding locale {}'.format(locale))
        executor = ThreadPoolExecutor(max_workers=1)
        future_nicknames_json = executor.submit(self._get_nicknames_json)
        try:
            latest_version = self._app_data[self._latest_version_name]
        except (KeyError, AttributeError):
            latest_version = self._get_json('https://ddragon.leagueoflegends.com/api/versions.json')[0]
        else:
            self._load_locale_from_server(locale, latest_version)
            self._add_nicknames(future_nicknames_json.result)
            joblib.dump(self._app_data, self._app_data_location)
            self.updating = False

    def reload_app_data(self, *locales: str):
        """
        Reloads all the data from scratch and dumps it for future use of the package.

        :param locales: If empty, refreshes the locales already existing. If not, loads only the given locales.

        Examples:
            reload_app_data()
                Refreshes existing locales
            reload_app_data('en_US', 'fr_FR', 'ko_KR')
                Destroys existing locales and loads English, French, and Korean language info.
        """
        while self.updating:
            time.sleep(0.1)

        self.updating = True
        if locales == ():
            locales = self._app_data[self._locales_list_name]
        executor = ThreadPoolExecutor(max_workers=5)
        future_nicknames_json = executor.submit(self._get_nicknames_json)
        self._app_data = {self._names_dict_name: {}, self._ids_dict_name: {}, 
         self._locales_list_name: [], 
         self._latest_version_name: self._get_json('https://ddragon.leagueoflegends.com/api/versions.json')[0]}
        for locale in locales:
            executor.submit(self._load_locale_from_server(locale, self._app_data[self._latest_version_name]))
        else:
            executor.shutdown
            self._add_nicknames(future_nicknames_json.result)
            joblib.dump(self._app_data, self._app_data_location)
            self.updating = False

    def _load_locale_from_server--- This code section failed: ---

 L. 278         0  BUILD_MAP_0           0 
                2  STORE_FAST               'data'

 L. 280         4  LOAD_GLOBAL              concurrent
                6  LOAD_ATTR                futures
                8  LOAD_ATTR                ThreadPoolExecutor
               10  LOAD_CONST               3
               12  LOAD_CONST               ('max_workers',)
               14  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
               16  SETUP_WITH           86  'to 86'
               18  STORE_DEREF              'executor'

 L. 282        20  LOAD_CLOSURE             'executor'
               22  LOAD_CLOSURE             'latest_version'
               24  LOAD_CLOSURE             'locale'
               26  LOAD_CLOSURE             'self'
               28  BUILD_TUPLE_4         4 
               30  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               32  LOAD_STR                 'LolIdTools._load_locale_from_server.<locals>.<dictcomp>'
               34  MAKE_FUNCTION_8          'closure'

 L. 286        36  LOAD_CONST               ('item', 'runesReforged', 'champion')

 L. 282        38  GET_ITER         
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'future_to_get'

 L. 288        44  LOAD_GLOBAL              concurrent
               46  LOAD_ATTR                futures
               48  LOAD_METHOD              as_completed
               50  LOAD_FAST                'future_to_get'
               52  CALL_METHOD_1         1  ''
               54  GET_ITER         
               56  FOR_ITER             82  'to 82'
               58  STORE_FAST               'future'

 L. 289        60  LOAD_FAST                'future_to_get'
               62  LOAD_FAST                'future'
               64  BINARY_SUBSCR    
               66  STORE_FAST               'request_type'

 L. 290        68  LOAD_FAST                'future'
               70  LOAD_METHOD              result
               72  CALL_METHOD_0         0  ''
               74  LOAD_FAST                'data'
               76  LOAD_FAST                'request_type'
               78  STORE_SUBSCR     
               80  JUMP_BACK            56  'to 56'
               82  POP_BLOCK        
               84  BEGIN_FINALLY    
             86_0  COME_FROM_WITH       16  '16'
               86  WITH_CLEANUP_START
               88  WITH_CLEANUP_FINISH
               90  END_FINALLY      

 L. 292        92  LOAD_FAST                'data'
               94  POP_JUMP_IF_TRUE    116  'to 116'

 L. 293        96  LOAD_GLOBAL              log
               98  LOAD_METHOD              error
              100  LOAD_STR                 '\tLocale "{}" not found on Riot’s server.\nUse lit.show_available_locales() for a list of available options.'
              102  LOAD_METHOD              format

 L. 294       104  LOAD_DEREF               'locale'

 L. 293       106  CALL_METHOD_1         1  ''
              108  CALL_METHOD_1         1  ''
              110  POP_TOP          

 L. 295       112  LOAD_GLOBAL              KeyError
              114  RAISE_VARARGS_1       1  'exception instance'
            116_0  COME_FROM            94  '94'

 L. 297       116  LOAD_FAST                'data'
              118  LOAD_STR                 'champion'
              120  BINARY_SUBSCR    
              122  LOAD_STR                 'data'
              124  BINARY_SUBSCR    
              126  LOAD_METHOD              items
              128  CALL_METHOD_0         0  ''
              130  GET_ITER         
              132  FOR_ITER            178  'to 178'
              134  UNPACK_SEQUENCE_2     2 
              136  STORE_FAST               'champion_tag'
              138  STORE_FAST               'champion_dict'

 L. 299       140  LOAD_GLOBAL              int
              142  LOAD_FAST                'champion_dict'
              144  LOAD_STR                 'key'
              146  BINARY_SUBSCR    
              148  CALL_FUNCTION_1       1  ''

 L. 300       150  LOAD_DEREF               'locale'

 L. 301       152  LOAD_STR                 'champion'

 L. 302       154  LOAD_FAST                'champion_dict'
              156  LOAD_STR                 'name'
              158  BINARY_SUBSCR    

 L. 298       160  LOAD_CONST               ('id', 'locale', 'id_type', 'name')
              162  BUILD_CONST_KEY_MAP_4     4 
              164  STORE_FAST               'id_information'

 L. 304       166  LOAD_DEREF               'self'
              168  LOAD_METHOD              _update_app_data
              170  LOAD_FAST                'id_information'
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          
              176  JUMP_BACK           132  'to 132'

 L. 306       178  LOAD_FAST                'data'
              180  LOAD_STR                 'item'
              182  BINARY_SUBSCR    
              184  LOAD_STR                 'data'
              186  BINARY_SUBSCR    
              188  LOAD_METHOD              items
              190  CALL_METHOD_0         0  ''
              192  GET_ITER         
              194  FOR_ITER            236  'to 236'
              196  UNPACK_SEQUENCE_2     2 
              198  STORE_FAST               'item_id'
              200  STORE_FAST               'item_dict'

 L. 308       202  LOAD_GLOBAL              int
              204  LOAD_FAST                'item_id'
              206  CALL_FUNCTION_1       1  ''

 L. 309       208  LOAD_DEREF               'locale'

 L. 310       210  LOAD_STR                 'item'

 L. 311       212  LOAD_FAST                'item_dict'
              214  LOAD_STR                 'name'
              216  BINARY_SUBSCR    

 L. 307       218  LOAD_CONST               ('id', 'locale', 'id_type', 'name')
              220  BUILD_CONST_KEY_MAP_4     4 
              222  STORE_FAST               'id_information'

 L. 313       224  LOAD_DEREF               'self'
              226  LOAD_METHOD              _update_app_data
              228  LOAD_FAST                'id_information'
              230  CALL_METHOD_1         1  ''
              232  POP_TOP          
              234  JUMP_BACK           194  'to 194'

 L. 315       236  LOAD_FAST                'data'
              238  LOAD_STR                 'runesReforged'
              240  BINARY_SUBSCR    
              242  GET_ITER         
              244  FOR_ITER            314  'to 314'
              246  STORE_FAST               'rune_tree'

 L. 316       248  LOAD_FAST                'rune_tree'
              250  LOAD_STR                 'slots'
              252  BINARY_SUBSCR    
              254  GET_ITER         
              256  FOR_ITER            312  'to 312'
              258  STORE_FAST               'slot'

 L. 317       260  LOAD_FAST                'slot'
              262  LOAD_STR                 'runes'
              264  BINARY_SUBSCR    
              266  GET_ITER         
              268  FOR_ITER            308  'to 308'
              270  STORE_FAST               'rune'

 L. 319       272  LOAD_FAST                'rune'
              274  LOAD_STR                 'id'
              276  BINARY_SUBSCR    

 L. 320       278  LOAD_DEREF               'locale'

 L. 321       280  LOAD_STR                 'rune'

 L. 322       282  LOAD_FAST                'rune'
              284  LOAD_STR                 'name'
              286  BINARY_SUBSCR    

 L. 318       288  LOAD_CONST               ('id', 'locale', 'id_type', 'name')
              290  BUILD_CONST_KEY_MAP_4     4 
              292  STORE_FAST               'id_information'

 L. 324       294  LOAD_DEREF               'self'
              296  LOAD_METHOD              _update_app_data
              298  LOAD_FAST                'id_information'
              300  CALL_METHOD_1         1  ''
              302  POP_TOP          
          304_306  JUMP_BACK           268  'to 268'
          308_310  JUMP_BACK           256  'to 256'
              312  JUMP_BACK           244  'to 244'

 L. 326       314  LOAD_DEREF               'self'
              316  LOAD_ATTR                _app_data
              318  LOAD_DEREF               'self'
              320  LOAD_ATTR                _locales_list_name
              322  BINARY_SUBSCR    
              324  LOAD_METHOD              append
              326  LOAD_DEREF               'locale'
              328  CALL_METHOD_1         1  ''
              330  POP_TOP          

Parse error at or near `LOAD_DICTCOMP' instruction at offset 30

    def _update_app_data(self, id_info):
        self._app_data[self._names_dict_name][id_info['name']] = id_info
        if (
         id_info['id'], id_info['locale']) in self._app_data[self._ids_dict_name]:
            log.warning('Multiple objects with ID {}'.format(id_info['id']))
            log.warning('\tExisting object: {}'.format(self._app_data[self._ids_dict_name][(id_info['id'], id_info['locale'])]['name'], self._app_data[self._ids_dict_name][(id_info['id'], id_info['locale'])]['id_type']))
            log.warning('\tNew object: {}/{}'.format(id_info['name'], id_info['id_type']))
        self._app_data[self._ids_dict_name][(id_info['id'], id_info['locale'])] = id_info

    def _get_nicknames_json(self):
        return self._get_json(self._nicknames_url)

    def _add_nicknames(self, json):
        for locale in json:
            if locale not in self._app_data[self._locales_list_name]:
                pass
            else:
                for nickname, real_name in json[locale].items:
                    try:
                        self._app_data[self._names_dict_name][nickname] = self._app_data[self._names_dict_name][real_name]
                    except KeyError:
                        log.info('Unable to add {}/{} as a nickname because it doesn’t match a Riot name.'.format(nickname, real_name))

    @staticmethod
    def _get_json(url):
        log.debug('Making call: {}'.format(url))
        return requests.get(url=url).json