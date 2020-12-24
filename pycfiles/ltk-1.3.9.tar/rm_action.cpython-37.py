# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hectorlopez/.virtualenvs/lingotek/lib/python3.7/site-packages/ltk/actions/rm_action.py
# Compiled at: 2020-04-13 16:03:59
# Size of source mod 2**32: 9790 bytes
from ltk.actions.action import *

class RmAction(Action):

    def __init__(self, path):
        Action.__init__(self, path)
        self.use_delete = False

    def rm_action--- This code section failed: ---

 L.   9       0_2  SETUP_EXCEPT        798  'to 798'

 L.  10         4  LOAD_CONST               False
                6  STORE_FAST               'removed_folder'

 L.  11         8  SETUP_LOOP          112  'to 112'
               10  LOAD_FAST                'file_patterns'
               12  GET_ITER         
             14_0  COME_FROM            28  '28'
               14  FOR_ITER            110  'to 110'
               16  STORE_FAST               'pattern'

 L.  12        18  LOAD_GLOBAL              os
               20  LOAD_ATTR                path
               22  LOAD_METHOD              isdir
               24  LOAD_FAST                'pattern'
               26  CALL_METHOD_1         1  '1 positional argument'
               28  POP_JUMP_IF_FALSE    14  'to 14'

 L.  14        30  LOAD_FAST                'self'
               32  LOAD_ATTR                folder_manager
               34  LOAD_METHOD              folder_exists
               36  LOAD_FAST                'self'
               38  LOAD_METHOD              norm_path
               40  LOAD_FAST                'pattern'
               42  CALL_METHOD_1         1  '1 positional argument'
               44  CALL_METHOD_1         1  '1 positional argument'
               46  POP_JUMP_IF_FALSE    86  'to 86'

 L.  15        48  LOAD_FAST                'self'
               50  LOAD_ATTR                folder_manager
               52  LOAD_METHOD              remove_element
               54  LOAD_FAST                'self'
               56  LOAD_METHOD              norm_path
               58  LOAD_FAST                'pattern'
               60  CALL_METHOD_1         1  '1 positional argument'
               62  CALL_METHOD_1         1  '1 positional argument'
               64  POP_TOP          

 L.  16        66  LOAD_GLOBAL              logger
               68  LOAD_METHOD              info
               70  LOAD_STR                 'Removed folder '
               72  LOAD_FAST                'pattern'
               74  BINARY_ADD       
               76  CALL_METHOD_1         1  '1 positional argument'
               78  POP_TOP          

 L.  17        80  LOAD_CONST               True
               82  STORE_FAST               'removed_folder'
               84  JUMP_BACK            14  'to 14'
             86_0  COME_FROM            46  '46'

 L.  19        86  LOAD_GLOBAL              logger
               88  LOAD_METHOD              warning
               90  LOAD_STR                 'Folder '
               92  LOAD_GLOBAL              str
               94  LOAD_FAST                'pattern'
               96  CALL_FUNCTION_1       1  '1 positional argument'
               98  BINARY_ADD       
              100  LOAD_STR                 ' has not been added and so can not be removed'
              102  BINARY_ADD       
              104  CALL_METHOD_1         1  '1 positional argument'
              106  POP_TOP          
              108  JUMP_BACK            14  'to 14'
              110  POP_BLOCK        
            112_0  COME_FROM_LOOP        8  '8'

 L.  20       112  LOAD_STR                 'directory'
              114  LOAD_FAST                'kwargs'
              116  COMPARE_OP               in
              118  POP_JUMP_IF_FALSE   146  'to 146'
              120  LOAD_FAST                'kwargs'
              122  LOAD_STR                 'directory'
              124  BINARY_SUBSCR    
              126  POP_JUMP_IF_FALSE   146  'to 146'

 L.  21       128  LOAD_FAST                'removed_folder'
              130  POP_JUMP_IF_TRUE    142  'to 142'

 L.  22       132  LOAD_GLOBAL              logger
              134  LOAD_METHOD              info
              136  LOAD_STR                 'No folders to remove at the given path(s)'
              138  CALL_METHOD_1         1  '1 positional argument'
              140  POP_TOP          
            142_0  COME_FROM           130  '130'

 L.  23       142  LOAD_CONST               None
              144  RETURN_VALUE     
            146_0  COME_FROM           126  '126'
            146_1  COME_FROM           118  '118'

 L.  24       146  LOAD_CONST               None
              148  STORE_FAST               'matched_files'

 L.  25       150  LOAD_GLOBAL              isinstance
              152  LOAD_FAST                'file_patterns'
              154  LOAD_GLOBAL              str
              156  CALL_FUNCTION_2       2  '2 positional arguments'
              158  POP_JUMP_IF_FALSE   166  'to 166'

 L.  26       160  LOAD_FAST                'file_patterns'
              162  BUILD_LIST_1          1 
              164  STORE_FAST               'file_patterns'
            166_0  COME_FROM           158  '158'

 L.  27       166  LOAD_STR                 'force'
              168  LOAD_FAST                'kwargs'
              170  COMPARE_OP               in
              172  POP_JUMP_IF_FALSE   188  'to 188'
              174  LOAD_FAST                'kwargs'
              176  LOAD_STR                 'force'
              178  BINARY_SUBSCR    
              180  POP_JUMP_IF_FALSE   188  'to 188'

 L.  28       182  LOAD_CONST               True
              184  STORE_FAST               'force'
              186  JUMP_FORWARD        192  'to 192'
            188_0  COME_FROM           180  '180'
            188_1  COME_FROM           172  '172'

 L.  30       188  LOAD_CONST               False
              190  STORE_FAST               'force'
            192_0  COME_FROM           186  '186'

 L.  31       192  LOAD_STR                 'id'
              194  LOAD_FAST                'kwargs'
              196  COMPARE_OP               in
              198  POP_JUMP_IF_FALSE   214  'to 214'
              200  LOAD_FAST                'kwargs'
              202  LOAD_STR                 'id'
              204  BINARY_SUBSCR    
              206  POP_JUMP_IF_FALSE   214  'to 214'

 L.  32       208  LOAD_CONST               True
              210  STORE_FAST               'useID'
              212  JUMP_FORWARD        218  'to 218'
            214_0  COME_FROM           206  '206'
            214_1  COME_FROM           198  '198'

 L.  34       214  LOAD_CONST               False
              216  STORE_FAST               'useID'
            218_0  COME_FROM           212  '212'

 L.  35       218  LOAD_STR                 'remote'
              220  LOAD_FAST                'kwargs'
              222  COMPARE_OP               in
              224  POP_JUMP_IF_FALSE   242  'to 242'
              226  LOAD_FAST                'kwargs'
              228  LOAD_STR                 'remote'
              230  BINARY_SUBSCR    
              232  POP_JUMP_IF_FALSE   242  'to 242'

 L.  36       234  LOAD_CONST               True
              236  LOAD_FAST                'self'
              238  STORE_ATTR               use_delete
              240  JUMP_FORWARD        248  'to 248'
            242_0  COME_FROM           232  '232'
            242_1  COME_FROM           224  '224'

 L.  38       242  LOAD_CONST               False
              244  LOAD_FAST                'self'
              246  STORE_ATTR               use_delete
            248_0  COME_FROM           240  '240'

 L.  39       248  LOAD_STR                 'all'
              250  LOAD_FAST                'kwargs'
              252  COMPARE_OP               in
          254_256  POP_JUMP_IF_FALSE   314  'to 314'
              258  LOAD_FAST                'kwargs'
              260  LOAD_STR                 'all'
              262  BINARY_SUBSCR    
          264_266  POP_JUMP_IF_FALSE   314  'to 314'

 L.  40       268  LOAD_CONST               False
              270  STORE_FAST               'local'

 L.  41       272  LOAD_FAST                'self'
              274  LOAD_ATTR                folder_manager
              276  LOAD_METHOD              clear_all
              278  CALL_METHOD_0         0  '0 positional arguments'
              280  POP_TOP          

 L.  42       282  LOAD_CONST               True
              284  STORE_FAST               'removed_folder'

 L.  43       286  LOAD_GLOBAL              logger
              288  LOAD_METHOD              info
              290  LOAD_STR                 'Removed all folders.'
              292  CALL_METHOD_1         1  '1 positional argument'
              294  POP_TOP          

 L.  44       296  LOAD_CONST               False
              298  STORE_FAST               'useID'

 L.  45       300  LOAD_FAST                'self'
              302  LOAD_ATTR                doc_manager
              304  LOAD_METHOD              get_file_names
              306  CALL_METHOD_0         0  '0 positional arguments'
              308  STORE_FAST               'matched_files'
          310_312  JUMP_FORWARD        574  'to 574'
            314_0  COME_FROM           264  '264'
            314_1  COME_FROM           254  '254'

 L.  46       314  LOAD_STR                 'local'
              316  LOAD_FAST                'kwargs'
              318  COMPARE_OP               in
          320_322  POP_JUMP_IF_FALSE   468  'to 468'
              324  LOAD_FAST                'kwargs'
              326  LOAD_STR                 'local'
              328  BINARY_SUBSCR    
          330_332  POP_JUMP_IF_FALSE   468  'to 468'

 L.  47       334  LOAD_CONST               True
              336  STORE_FAST               'local'

 L.  48       338  LOAD_STR                 'name'
              340  LOAD_FAST                'kwargs'
              342  COMPARE_OP               in
          344_346  POP_JUMP_IF_FALSE   414  'to 414'
              348  LOAD_FAST                'kwargs'
              350  LOAD_STR                 'name'
              352  BINARY_SUBSCR    
          354_356  POP_JUMP_IF_FALSE   414  'to 414'

 L.  49       358  BUILD_LIST_0          0 
              360  STORE_FAST               'matched_files'

 L.  51       362  SETUP_LOOP          466  'to 466'
              364  LOAD_FAST                'file_patterns'
              366  GET_ITER         
            368_0  COME_FROM           388  '388'
              368  FOR_ITER            410  'to 410'
              370  STORE_FAST               'pattern'

 L.  52       372  LOAD_FAST                'self'
              374  LOAD_ATTR                doc_manager
              376  LOAD_METHOD              get_doc_by_prop
              378  LOAD_STR                 'name'
              380  LOAD_FAST                'pattern'
              382  CALL_METHOD_2         2  '2 positional arguments'
              384  STORE_FAST               'doc'

 L.  53       386  LOAD_FAST                'doc'
          388_390  POP_JUMP_IF_FALSE   368  'to 368'

 L.  54       392  LOAD_FAST                'matched_files'
              394  LOAD_METHOD              append
              396  LOAD_FAST                'doc'
              398  LOAD_STR                 'file_name'
              400  BINARY_SUBSCR    
              402  CALL_METHOD_1         1  '1 positional argument'
              404  POP_TOP          
          406_408  JUMP_BACK           368  'to 368'
              410  POP_BLOCK        
              412  JUMP_FORWARD        466  'to 466'
            414_0  COME_FROM           354  '354'
            414_1  COME_FROM           344  '344'

 L.  56       414  LOAD_GLOBAL              len
              416  LOAD_FAST                'file_patterns'
              418  CALL_FUNCTION_1       1  '1 positional argument'
              420  LOAD_CONST               0
              422  COMPARE_OP               ==
          424_426  POP_JUMP_IF_FALSE   574  'to 574'

 L.  57       428  LOAD_FAST                'self'
              430  LOAD_ATTR                folder_manager
              432  LOAD_METHOD              clear_all
              434  CALL_METHOD_0         0  '0 positional arguments'
              436  POP_TOP          

 L.  58       438  LOAD_CONST               True
              440  STORE_FAST               'removed_folder'

 L.  59       442  LOAD_GLOBAL              logger
              444  LOAD_METHOD              info
              446  LOAD_STR                 'Removed all folders.'
              448  CALL_METHOD_1         1  '1 positional argument'
              450  POP_TOP          

 L.  60       452  LOAD_CONST               False
              454  STORE_FAST               'useID'

 L.  61       456  LOAD_FAST                'self'
              458  LOAD_ATTR                doc_manager
              460  LOAD_METHOD              get_file_names
              462  CALL_METHOD_0         0  '0 positional arguments'
              464  STORE_FAST               'matched_files'
            466_0  COME_FROM           412  '412'
            466_1  COME_FROM_LOOP      362  '362'
              466  JUMP_FORWARD        574  'to 574'
            468_0  COME_FROM           330  '330'
            468_1  COME_FROM           320  '320'

 L.  63       468  LOAD_FAST                'useID'
          470_472  POP_JUMP_IF_TRUE    566  'to 566'

 L.  64       474  LOAD_CONST               False
              476  STORE_FAST               'local'

 L.  66       478  LOAD_STR                 'name'
              480  LOAD_FAST                'kwargs'
              482  COMPARE_OP               in
          484_486  POP_JUMP_IF_FALSE   554  'to 554'
              488  LOAD_FAST                'kwargs'
              490  LOAD_STR                 'name'
              492  BINARY_SUBSCR    
          494_496  POP_JUMP_IF_FALSE   554  'to 554'

 L.  67       498  BUILD_LIST_0          0 
              500  STORE_FAST               'matched_files'

 L.  69       502  SETUP_LOOP          564  'to 564'
              504  LOAD_FAST                'file_patterns'
              506  GET_ITER         
            508_0  COME_FROM           528  '528'
              508  FOR_ITER            550  'to 550'
              510  STORE_FAST               'pattern'

 L.  70       512  LOAD_FAST                'self'
              514  LOAD_ATTR                doc_manager
              516  LOAD_METHOD              get_doc_by_prop
              518  LOAD_STR                 'name'
              520  LOAD_FAST                'pattern'
              522  CALL_METHOD_2         2  '2 positional arguments'
              524  STORE_FAST               'doc'

 L.  71       526  LOAD_FAST                'doc'
          528_530  POP_JUMP_IF_FALSE   508  'to 508'

 L.  72       532  LOAD_FAST                'matched_files'
              534  LOAD_METHOD              append
              536  LOAD_FAST                'doc'
              538  LOAD_STR                 'file_name'
              540  BINARY_SUBSCR    
              542  CALL_METHOD_1         1  '1 positional argument'
              544  POP_TOP          
          546_548  JUMP_BACK           508  'to 508'
              550  POP_BLOCK        
              552  JUMP_FORWARD        564  'to 564'
            554_0  COME_FROM           494  '494'
            554_1  COME_FROM           484  '484'

 L.  74       554  LOAD_FAST                'self'
              556  LOAD_METHOD              get_doc_filenames_in_path
              558  LOAD_FAST                'file_patterns'
              560  CALL_METHOD_1         1  '1 positional argument'
              562  STORE_FAST               'matched_files'
            564_0  COME_FROM           552  '552'
            564_1  COME_FROM_LOOP      502  '502'
              564  JUMP_FORWARD        574  'to 574'
            566_0  COME_FROM           470  '470'

 L.  76       566  LOAD_CONST               False
              568  STORE_FAST               'local'

 L.  77       570  LOAD_FAST                'file_patterns'
              572  STORE_FAST               'matched_files'
            574_0  COME_FROM           564  '564'
            574_1  COME_FROM           466  '466'
            574_2  COME_FROM           424  '424'
            574_3  COME_FROM           310  '310'

 L.  78       574  LOAD_FAST                'matched_files'
          576_578  POP_JUMP_IF_FALSE   594  'to 594'
              580  LOAD_GLOBAL              len
              582  LOAD_FAST                'matched_files'
              584  CALL_FUNCTION_1       1  '1 positional argument'
              586  LOAD_CONST               0
              588  COMPARE_OP               ==
          590_592  POP_JUMP_IF_FALSE   690  'to 690'
            594_0  COME_FROM           576  '576'

 L.  79       594  LOAD_FAST                'useID'
          596_598  POP_JUMP_IF_FALSE   612  'to 612'

 L.  80       600  LOAD_GLOBAL              exceptions
              602  LOAD_METHOD              ResourceNotFound
              604  LOAD_STR                 'No documents to remove with the specified id'
              606  CALL_METHOD_1         1  '1 positional argument'
              608  RAISE_VARARGS_1       1  'exception instance'
              610  JUMP_FORWARD        690  'to 690'
            612_0  COME_FROM           596  '596'

 L.  81       612  LOAD_FAST                'removed_folder'
          614_616  POP_JUMP_IF_FALSE   630  'to 630'

 L.  82       618  LOAD_GLOBAL              logger
              620  LOAD_METHOD              info
              622  LOAD_STR                 'No documents to remove'
              624  CALL_METHOD_1         1  '1 positional argument'
              626  POP_TOP          
              628  JUMP_FORWARD        690  'to 690'
            630_0  COME_FROM           614  '614'

 L.  83       630  LOAD_FAST                'local'
          632_634  POP_JUMP_IF_FALSE   648  'to 648'

 L.  84       636  LOAD_GLOBAL              exceptions
              638  LOAD_METHOD              ResourceNotFound
              640  LOAD_STR                 'Too many agruments, to specify a document to be removed locally use -l in association with -n'
              642  CALL_METHOD_1         1  '1 positional argument'
              644  RAISE_VARARGS_1       1  'exception instance'
              646  JUMP_FORWARD        690  'to 690'
            648_0  COME_FROM           632  '632'

 L.  85       648  LOAD_STR                 'all'
              650  LOAD_FAST                'kwargs'
              652  COMPARE_OP               not-in
          654_656  POP_JUMP_IF_TRUE    668  'to 668'
              658  LOAD_FAST                'kwargs'
              660  LOAD_STR                 'all'
              662  BINARY_SUBSCR    
          664_666  POP_JUMP_IF_TRUE    680  'to 680'
            668_0  COME_FROM           654  '654'

 L.  86       668  LOAD_GLOBAL              exceptions
              670  LOAD_METHOD              ResourceNotFound
              672  LOAD_STR                 'No documents to remove with the specified file path'
              674  CALL_METHOD_1         1  '1 positional argument'
              676  RAISE_VARARGS_1       1  'exception instance'
              678  JUMP_FORWARD        690  'to 690'
            680_0  COME_FROM           664  '664'

 L.  88       680  LOAD_GLOBAL              exceptions
              682  LOAD_METHOD              ResourceNotFound
              684  LOAD_STR                 'No documents to remove'
              686  CALL_METHOD_1         1  '1 positional argument'
              688  RAISE_VARARGS_1       1  'exception instance'
            690_0  COME_FROM           678  '678'
            690_1  COME_FROM           646  '646'
            690_2  COME_FROM           628  '628'
            690_3  COME_FROM           610  '610'
            690_4  COME_FROM           590  '590'

 L.  89       690  LOAD_CONST               False
              692  STORE_FAST               'is_directory'

 L.  90       694  SETUP_LOOP          742  'to 742'
              696  LOAD_FAST                'file_patterns'
              698  GET_ITER         
            700_0  COME_FROM           728  '728'
              700  FOR_ITER            740  'to 740'
              702  STORE_FAST               'pattern'

 L.  91       704  LOAD_GLOBAL              os
              706  LOAD_ATTR                path
              708  LOAD_METHOD              basename
              710  LOAD_FAST                'pattern'
              712  CALL_METHOD_1         1  '1 positional argument'
              714  STORE_FAST               'basename'

 L.  92       716  LOAD_FAST                'basename'
          718_720  POP_JUMP_IF_FALSE   732  'to 732'
              722  LOAD_FAST                'basename'
              724  LOAD_STR                 ''
              726  COMPARE_OP               ==
          728_730  POP_JUMP_IF_FALSE   700  'to 700'
            732_0  COME_FROM           718  '718'

 L.  93       732  LOAD_CONST               True
              734  STORE_FAST               'is_directory'
          736_738  JUMP_BACK           700  'to 700'
              740  POP_BLOCK        
            742_0  COME_FROM_LOOP      694  '694'

 L.  94       742  SETUP_LOOP          794  'to 794'
              744  LOAD_FAST                'matched_files'
              746  GET_ITER         
              748  FOR_ITER            792  'to 792'
              750  STORE_FAST               'file_name'

 L.  96       752  LOAD_FAST                'self'
              754  LOAD_METHOD              _rm_document
              756  LOAD_FAST                'self'
              758  LOAD_METHOD              norm_path
              760  LOAD_FAST                'file_name'
              762  CALL_METHOD_1         1  '1 positional argument'
              764  LOAD_METHOD              replace
              766  LOAD_FAST                'self'
              768  LOAD_ATTR                path
              770  LOAD_STR                 ''
              772  CALL_METHOD_2         2  '2 positional arguments'
              774  LOAD_FAST                'useID'
              776  LOAD_FAST                'force'
          778_780  JUMP_IF_TRUE_OR_POP   784  'to 784'
              782  LOAD_FAST                'local'
            784_0  COME_FROM           778  '778'
              784  CALL_METHOD_3         3  '3 positional arguments'
              786  POP_TOP          
          788_790  JUMP_BACK           748  'to 748'
              792  POP_BLOCK        
            794_0  COME_FROM_LOOP      742  '742'
              794  POP_BLOCK        
              796  JUMP_FORWARD        890  'to 890'
            798_0  COME_FROM_EXCEPT      0  '0'

 L.  98       798  DUP_TOP          
              800  LOAD_GLOBAL              Exception
              802  COMPARE_OP               exception-match
          804_806  POP_JUMP_IF_FALSE   888  'to 888'
              808  POP_TOP          
              810  STORE_FAST               'e'
              812  POP_TOP          
              814  SETUP_FINALLY       876  'to 876'

 L. 100       816  LOAD_GLOBAL              log_error
              818  LOAD_FAST                'self'
              820  LOAD_ATTR                error_file_name
              822  LOAD_FAST                'e'
              824  CALL_FUNCTION_2       2  '2 positional arguments'
              826  POP_TOP          

 L. 102       828  LOAD_STR                 'string indices must be integers'
              830  LOAD_GLOBAL              str
              832  LOAD_FAST                'e'
              834  CALL_FUNCTION_1       1  '1 positional argument'
              836  COMPARE_OP               in
          838_840  POP_JUMP_IF_FALSE   854  'to 854'

 L. 103       842  LOAD_GLOBAL              logger
              844  LOAD_METHOD              error
              846  LOAD_STR                 "Error connecting to Lingotek's TMS"
              848  CALL_METHOD_1         1  '1 positional argument'
              850  POP_TOP          
              852  JUMP_FORWARD        872  'to 872'
            854_0  COME_FROM           838  '838'

 L. 105       854  LOAD_GLOBAL              logger
              856  LOAD_METHOD              error
              858  LOAD_STR                 'Error on remove: '
              860  LOAD_GLOBAL              str
              862  LOAD_FAST                'e'
              864  CALL_FUNCTION_1       1  '1 positional argument'
              866  BINARY_ADD       
              868  CALL_METHOD_1         1  '1 positional argument'
              870  POP_TOP          
            872_0  COME_FROM           852  '852'
              872  POP_BLOCK        
              874  LOAD_CONST               None
            876_0  COME_FROM_FINALLY   814  '814'
              876  LOAD_CONST               None
              878  STORE_FAST               'e'
              880  DELETE_FAST              'e'
              882  END_FINALLY      
              884  POP_EXCEPT       
              886  JUMP_FORWARD        890  'to 890'
            888_0  COME_FROM           804  '804'
              888  END_FINALLY      
            890_0  COME_FROM           886  '886'
            890_1  COME_FROM           796  '796'

Parse error at or near `COME_FROM_LOOP' instruction at offset 466_1

    def _rm_clone(self, file_name):
        trans_files = []
        entry = self.doc_manager.get_doc_by_prop('file_name', file_name)
        if entry:
            if 'locales' in entry:
                if entry['locales']:
                    locales = entry['locales']
                    for locale_code in locales:
                        if locale_code in self.locale_folders:
                            download_root = self.locale_folders[locale_code]
                        else:
                            if self.download_dir and len(self.download_dir):
                                download_root = os.path.join(self.download_dir if (self.download_dir and self.download_dir != 'null') else '', locale_code)
                            else:
                                download_root = locale_code
                        download_root = os.path.join(self.path, download_root)
                        source_file_name = entry['file_name']
                        source_path = os.path.join(self.path, os.path.dirnamesource_file_name)
                        trans_files.extendget_translation_files(file_name, download_root, self.download_option, self.doc_manager)

        return trans_files

    def _rm_document(self, file_name, useID, force):
        try:
            doc = None
            if not useID:
                relative_path = self.norm_pathfile_name
                doc = self.doc_manager.get_doc_by_prop('file_name', relative_path)
                title = os.path.basenameself.norm_pathfile_name
                try:
                    document_id = doc['id']
                except TypeError:
                    logger.warning"Document name specified for remove isn't in the local database: {0}".formatrelative_path
                    return

            else:
                document_id = file_name
                doc = self.doc_manager.get_doc_by_prop('id', document_id)
                if doc:
                    file_name = doc['file_name']
                elif self.use_delete:
                    response = self.api.document_deletedocument_id
                else:
                    response = self.api.document_canceldocument_id
                if response.status_code != 204 and response.status_code != 202:
                    logger.error'Failed to {0} {1} remotely'.format('delete' if self.use_delete else 'cancel', file_name)
                else:
                    logger.info'{0} has been {1} remotely'.format(file_name, 'deleted' if self.use_delete else 'cancelled')
                if force:
                    trans_files = []
                    if 'clone' in self.download_option:
                        trans_files = self._rm_clonefile_name
                    else:
                        if 'folder' in self.download_option:
                            trans_files = self._rm_folderfile_name
                        else:
                            if 'same' in self.download_option:
                                download_path = self.path
                                trans_files = get_translation_files(file_name, download_path, self.download_option, self.doc_manager)
                            self.delete_local(file_name, document_id)
                self.doc_manager.remove_elementdocument_id
        except json.decoder.JSONDecodeError:
            logger.error'JSON error on removing document'
        except KeyboardInterrupt:
            raise_error'''Canceled removing document'
            return
        except Exception as e:
            try:
                log_errorself.error_file_namee
                logger.error('Error on removing document ' + str(file_name) + ': ' + str(e))
            finally:
                e = None
                del e

    def _rm_folder(self, file_name):
        trans_files = []
        entry = self.doc_manager.get_doc_by_prop('file_name', file_name)
        if entry:
            if 'locales' in entry:
                if entry['locales']:
                    locales = entry['locales']
                    for locale_code in locales:
                        if locale_code in self.locale_folders:
                            if self.locale_folders[locale_code] == 'null':
                                logger.warning('Download failed: folder not specified for ' + locale_code)
                            else:
                                download_path = self.locale_folders[locale_code]
                        else:
                            download_path = self.download_dir
                        download_path = os.path.join(self.path, download_path)
                        trans_files.extendget_translation_files(file_name, download_path, self.download_option, self.doc_manager)

        return trans_files