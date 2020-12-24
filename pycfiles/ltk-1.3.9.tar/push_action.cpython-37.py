# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hectorlopez/.virtualenvs/lingotek/lib/python3.7/site-packages/ltk/actions/push_action.py
# Compiled at: 2020-01-30 14:00:13
# Size of source mod 2**32: 5469 bytes
from ltk.actions.action import *

class PushAction(Action):

    def __init__(self, path, test, title):
        Action.__init__(self, path)
        self.title = title
        self.test = test

    def push_action(self, files=None, set_metadata=False, metadata_only=False, **kwargs):
        self.metadata_only = metadata_only
        self.metadata = copy.deepcopy(self.default_metadata)
        if set_metadata:
            self.metadata = self.metadata_wizard()
        else:
            if self.metadata_prompt:
                if yes_no_prompt('Would you like to launch the metadata wizard?', default_yes=True):
                    self.metadata = self.metadata_wizard()
            else:
                try:
                    if files:
                        added, updated, failed = (self._push_specific_files)(files, **kwargs)
                    else:
                        added = (self._add_new_docs)(**kwargs)
                        updated, failed = (self._update_current_docs)(**kwargs)
                    total = added + updated + failed
                    if total is 0:
                        report = 'All documents up-to-date with Lingotek Cloud. '
                    else:
                        report = 'Added {0}, Updated {1}, Failed {2} (Total {3})'.format(added, updated, failed, total)
                    if self.test:
                        logger.info('TEST RUN: ' + report)
                    else:
                        logger.info(report)
                except Exception as e:
                    try:
                        log_error(self.error_file_name, e)
                        if 'string indices must be integers' in str(e) or 'Expecting value: line 1 column 1' in str(e):
                            logger.error("Error connecting to Lingotek's TMS")
                        else:
                            logger.error('Error on push: ' + str(e))
                    finally:
                        e = None
                        del e

    def _add_new_docs(self, **kwargs):
        folders = self.folder_manager.get_file_names()
        added = 0
        if len(folders):
            if not self.metadata_only:
                for folder in folders:
                    matched_files = get_files(folder)
                    if matched_files:
                        for file_name in matched_files:
                            try:
                                relative_path = self.norm_path(file_name)
                                title = os.path.basename(relative_path)
                                if self.doc_manager.is_doc_new(relative_path):
                                    if not self.doc_manager.is_translation(relative_path, title, matched_files, self):
                                        display_name = title if self.title else relative_path
                                        if self.test:
                                            print('Add {0}'.format(display_name))
                                        else:
                                            (self.add_document)(file_name, title, doc_metadata=self.metadata, **kwargs)
                                        added += 1
                            except json.decoder.JSONDecodeError as e:
                                try:
                                    log_error(self.error_file_name, e)
                                    logger.error('JSON error on adding document.')
                                finally:
                                    e = None
                                    del e

        return added

    def _update_current_docs--- This code section failed: ---

 L.  64         0  LOAD_CONST               0
                2  STORE_FAST               'updated'

 L.  65         4  LOAD_CONST               0
                6  STORE_FAST               'failed'

 L.  66         8  LOAD_FAST                'self'
               10  LOAD_ATTR                doc_manager
               12  LOAD_METHOD              get_all_entries
               14  CALL_METHOD_0         0  '0 positional arguments'
               16  STORE_FAST               'entries'

 L.  67        18  SETUP_LOOP          134  'to 134'
               20  LOAD_FAST                'entries'
               22  GET_ITER         
             24_0  COME_FROM            82  '82'
             24_1  COME_FROM            76  '76'
               24  FOR_ITER            132  'to 132'
               26  STORE_FAST               'entry'

 L.  68        28  LOAD_GLOBAL              len
               30  LOAD_FAST                'self'
               32  LOAD_ATTR                metadata
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  LOAD_CONST               0
               38  COMPARE_OP               >
               40  POP_JUMP_IF_TRUE     84  'to 84'
               42  LOAD_FAST                'kwargs'
               44  LOAD_STR                 'due_date'
               46  BINARY_SUBSCR    
               48  POP_JUMP_IF_TRUE     84  'to 84'
               50  LOAD_FAST                'kwargs'
               52  LOAD_STR                 'due_reason'
               54  BINARY_SUBSCR    
               56  POP_JUMP_IF_TRUE     84  'to 84'
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                doc_manager
               62  LOAD_METHOD              is_doc_modified
               64  LOAD_FAST                'entry'
               66  LOAD_STR                 'file_name'
               68  BINARY_SUBSCR    
               70  LOAD_FAST                'self'
               72  LOAD_ATTR                path
               74  CALL_METHOD_2         2  '2 positional arguments'
               76  POP_JUMP_IF_FALSE    24  'to 24'
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                metadata_only
               82  POP_JUMP_IF_TRUE     24  'to 24'
             84_0  COME_FROM            56  '56'
             84_1  COME_FROM            48  '48'
             84_2  COME_FROM            40  '40'

 L.  69        84  LOAD_FAST                'self'
               86  LOAD_ATTR                title
               88  POP_JUMP_IF_FALSE    98  'to 98'
               90  LOAD_FAST                'entry'
               92  LOAD_STR                 'name'
               94  BINARY_SUBSCR    
               96  JUMP_FORWARD        104  'to 104'
             98_0  COME_FROM            88  '88'
               98  LOAD_FAST                'entry'
              100  LOAD_STR                 'file_name'
              102  BINARY_SUBSCR    
            104_0  COME_FROM            96  '96'
              104  STORE_FAST               'display_name'

 L.  70       106  LOAD_FAST                'self'
              108  LOAD_ATTR                _handle_update
              110  LOAD_FAST                'updated'
              112  LOAD_FAST                'failed'
              114  LOAD_FAST                'display_name'
              116  LOAD_FAST                'entry'
              118  BUILD_TUPLE_4         4 
              120  LOAD_FAST                'kwargs'
              122  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              124  UNPACK_SEQUENCE_2     2 
              126  STORE_FAST               'updated'
              128  STORE_FAST               'failed'
              130  JUMP_BACK            24  'to 24'
              132  POP_BLOCK        
            134_0  COME_FROM_LOOP       18  '18'

 L.  71       134  LOAD_FAST                'updated'
              136  LOAD_FAST                'failed'
              138  BUILD_TUPLE_2         2 
              140  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 132

    def _push_specific_files--- This code section failed: ---

 L.  74         0  LOAD_GLOBAL              set
                2  CALL_FUNCTION_0       0  '0 positional arguments'
                4  STORE_FAST               'files'

 L.  75         6  LOAD_CONST               0
                8  STORE_FAST               'added'

 L.  76        10  LOAD_CONST               0
               12  STORE_FAST               'updated'

 L.  77        14  LOAD_CONST               0
               16  STORE_FAST               'failed'

 L.  78        18  SETUP_LOOP          104  'to 104'
               20  LOAD_FAST                'patterns'
               22  GET_ITER         
               24  FOR_ITER            102  'to 102'
               26  STORE_FAST               'pattern'

 L.  79        28  LOAD_GLOBAL              os
               30  LOAD_ATTR                path
               32  LOAD_METHOD              isdir
               34  LOAD_FAST                'pattern'
               36  CALL_METHOD_1         1  '1 positional argument'
               38  POP_JUMP_IF_FALSE    80  'to 80'

 L.  80        40  SETUP_LOOP          100  'to 100'
               42  LOAD_GLOBAL              get_files
               44  LOAD_FAST                'pattern'
               46  CALL_FUNCTION_1       1  '1 positional argument'
               48  GET_ITER         
               50  FOR_ITER             76  'to 76'
               52  STORE_FAST               'file'

 L.  81        54  LOAD_FAST                'self'
               56  LOAD_METHOD              norm_path
               58  LOAD_FAST                'file'
               60  CALL_METHOD_1         1  '1 positional argument'
               62  STORE_FAST               'relative_path'

 L.  82        64  LOAD_FAST                'files'
               66  LOAD_METHOD              add
               68  LOAD_FAST                'relative_path'
               70  CALL_METHOD_1         1  '1 positional argument'
               72  POP_TOP          
               74  JUMP_BACK            50  'to 50'
               76  POP_BLOCK        
               78  JUMP_BACK            24  'to 24'
             80_0  COME_FROM            38  '38'

 L.  84        80  LOAD_FAST                'self'
               82  LOAD_METHOD              norm_path
               84  LOAD_FAST                'pattern'
               86  CALL_METHOD_1         1  '1 positional argument'
               88  STORE_FAST               'relative_path'

 L.  85        90  LOAD_FAST                'files'
               92  LOAD_METHOD              add
               94  LOAD_FAST                'relative_path'
               96  CALL_METHOD_1         1  '1 positional argument'
               98  POP_TOP          
            100_0  COME_FROM_LOOP       40  '40'
              100  JUMP_BACK            24  'to 24'
              102  POP_BLOCK        
            104_0  COME_FROM_LOOP       18  '18'

 L.  86   104_106  SETUP_LOOP          364  'to 364'
              108  LOAD_FAST                'files'
              110  GET_ITER         
            112_0  COME_FROM           310  '310'
            112_1  COME_FROM           292  '292'
            112_2  COME_FROM           286  '286'
              112  FOR_ITER            362  'to 362'
              114  STORE_FAST               'file'

 L.  87       116  LOAD_GLOBAL              os
              118  LOAD_ATTR                path
              120  LOAD_METHOD              basename
              122  LOAD_FAST                'file'
              124  CALL_METHOD_1         1  '1 positional argument'
              126  STORE_FAST               'title'

 L.  88       128  LOAD_FAST                'self'
              130  LOAD_ATTR                metadata_only
              132  POP_JUMP_IF_TRUE    236  'to 236'
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                doc_manager
              138  LOAD_METHOD              is_doc_new
              140  LOAD_FAST                'file'
              142  CALL_METHOD_1         1  '1 positional argument'
              144  POP_JUMP_IF_FALSE   236  'to 236'
              146  LOAD_FAST                'self'
              148  LOAD_ATTR                doc_manager
              150  LOAD_METHOD              is_translation
              152  LOAD_FAST                'file'
              154  LOAD_FAST                'title'
              156  LOAD_FAST                'files'
              158  LOAD_FAST                'self'
              160  CALL_METHOD_4         4  '4 positional arguments'
              162  POP_JUMP_IF_TRUE    236  'to 236'

 L.  89       164  LOAD_FAST                'self'
              166  LOAD_ATTR                title
              168  POP_JUMP_IF_FALSE   174  'to 174'
              170  LOAD_FAST                'title'
              172  JUMP_FORWARD        176  'to 176'
            174_0  COME_FROM           168  '168'
              174  LOAD_FAST                'file'
            176_0  COME_FROM           172  '172'
              176  STORE_FAST               'display_name'

 L.  90       178  LOAD_FAST                'self'
              180  LOAD_ATTR                test
              182  POP_JUMP_IF_FALSE   200  'to 200'

 L.  91       184  LOAD_GLOBAL              print
              186  LOAD_STR                 'Add {0}'
              188  LOAD_METHOD              format
              190  LOAD_FAST                'display_name'
              192  CALL_METHOD_1         1  '1 positional argument'
              194  CALL_FUNCTION_1       1  '1 positional argument'
              196  POP_TOP          
              198  JUMP_FORWARD        226  'to 226'
            200_0  COME_FROM           182  '182'

 L.  93       200  LOAD_FAST                'self'
              202  LOAD_ATTR                add_document
              204  LOAD_FAST                'file'
              206  LOAD_FAST                'title'
              208  BUILD_TUPLE_2         2 
              210  LOAD_STR                 'doc_metadata'
              212  LOAD_FAST                'self'
              214  LOAD_ATTR                metadata
              216  BUILD_MAP_1           1 
              218  LOAD_FAST                'kwargs'
              220  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              222  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              224  POP_TOP          
            226_0  COME_FROM           198  '198'

 L.  94       226  LOAD_FAST                'added'
              228  LOAD_CONST               1
              230  INPLACE_ADD      
              232  STORE_FAST               'added'
              234  JUMP_BACK           112  'to 112'
            236_0  COME_FROM           162  '162'
            236_1  COME_FROM           144  '144'
            236_2  COME_FROM           132  '132'

 L.  95       236  LOAD_GLOBAL              len
              238  LOAD_FAST                'self'
              240  LOAD_ATTR                metadata
              242  CALL_FUNCTION_1       1  '1 positional argument'
              244  LOAD_CONST               0
              246  COMPARE_OP               >
          248_250  POP_JUMP_IF_TRUE    294  'to 294'
              252  LOAD_FAST                'kwargs'
              254  LOAD_STR                 'due_date'
              256  BINARY_SUBSCR    
          258_260  POP_JUMP_IF_TRUE    294  'to 294'
              262  LOAD_FAST                'kwargs'
              264  LOAD_STR                 'due_reason'
              266  BINARY_SUBSCR    
          268_270  POP_JUMP_IF_TRUE    294  'to 294'
              272  LOAD_FAST                'self'
              274  LOAD_ATTR                doc_manager
              276  LOAD_METHOD              is_doc_modified
              278  LOAD_FAST                'file'
              280  LOAD_FAST                'self'
              282  LOAD_ATTR                path
              284  CALL_METHOD_2         2  '2 positional arguments'
              286  POP_JUMP_IF_FALSE   112  'to 112'
              288  LOAD_FAST                'self'
              290  LOAD_ATTR                metadata_only
              292  POP_JUMP_IF_TRUE    112  'to 112'
            294_0  COME_FROM           268  '268'
            294_1  COME_FROM           258  '258'
            294_2  COME_FROM           248  '248'

 L.  96       294  LOAD_FAST                'self'
              296  LOAD_ATTR                doc_manager
              298  LOAD_METHOD              get_doc_by_prop
              300  LOAD_STR                 'file_name'
              302  LOAD_FAST                'file'
              304  CALL_METHOD_2         2  '2 positional arguments'
              306  STORE_FAST               'entry'

 L.  97       308  LOAD_FAST                'entry'
              310  POP_JUMP_IF_FALSE   112  'to 112'

 L.  98       312  LOAD_FAST                'self'
              314  LOAD_ATTR                title
          316_318  POP_JUMP_IF_FALSE   328  'to 328'
              320  LOAD_FAST                'entry'
              322  LOAD_STR                 'name'
              324  BINARY_SUBSCR    
              326  JUMP_FORWARD        334  'to 334'
            328_0  COME_FROM           316  '316'
              328  LOAD_FAST                'entry'
              330  LOAD_STR                 'file_name'
              332  BINARY_SUBSCR    
            334_0  COME_FROM           326  '326'
              334  STORE_FAST               'display_name'

 L.  99       336  LOAD_FAST                'self'
              338  LOAD_ATTR                _handle_update
              340  LOAD_FAST                'updated'
              342  LOAD_FAST                'failed'
              344  LOAD_FAST                'display_name'
              346  LOAD_FAST                'entry'
              348  BUILD_TUPLE_4         4 
              350  LOAD_FAST                'kwargs'
              352  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
              354  UNPACK_SEQUENCE_2     2 
              356  STORE_FAST               'updated'
              358  STORE_FAST               'failed'
              360  JUMP_BACK           112  'to 112'
              362  POP_BLOCK        
            364_0  COME_FROM_LOOP      104  '104'

 L. 100       364  LOAD_FAST                'added'
              366  LOAD_FAST                'updated'
              368  LOAD_FAST                'failed'
              370  BUILD_TUPLE_3         3 
              372  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 364_0

    def _handle_update(self, updated, failed, display_name, entry, **kwargs):
        if self.test:
            updated += 1
            print('Update {0}'.format(display_name))
            return (updated, failed)
        elif (self.update_document_action)(entry['file_name'], display_name, doc_metadata=self.metadata, **kwargs):
            updated += 1
            logger.info('Updated {0}'.format(display_name))
        else:
            failed += 1
        return (
         updated, failed)