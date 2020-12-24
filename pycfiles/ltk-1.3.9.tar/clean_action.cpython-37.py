# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hectorlopez/.virtualenvs/lingotek/lib/python3.7/site-packages/ltk/actions/clean_action.py
# Compiled at: 2020-04-13 16:03:13
# Size of source mod 2**32: 4744 bytes
from ltk.actions.action import *

class CleanAction(Action):

    def __init__(self, path):
        Action.__init__(self, path)

    def clean_action(self, force, dis_all, path):
        try:
            if dis_all:
                self._clean_all()
                return
                if path:
                    locals_to_delete = self._clean_by_path(path)
                else:
                    locals_to_delete = self._check_docs_to_clean()
                if locals_to_delete:
                    for curr_id in locals_to_delete:
                        removed_title = self._clean_local(curr_id, force)
                        logger.info('Removing association for document {0}'.format(removed_title))

            else:
                logger.info('Local documents already up-to-date with Lingotek Cloud')
                return
            logger.info('Cleaned up associations between local documents and Lingotek Cloud')
        except Exception as e:
            try:
                log_error(self.error_file_name, e)
                if 'string indices must be integers' in str(e) or 'Expecting value: line 1 column 1' in str(e):
                    logger.error("Error connecting to Lingotek's TMS")
                else:
                    logger.error('Error on clean: ' + str(e))
            finally:
                e = None
                del e

    def _clean_local(self, doc_id, force):
        removed_doc = self.doc_manager.get_doc_by_prop('id', doc_id)
        if not removed_doc:
            return
        removed_title = removed_doc['name']
        if force:
            self.delete_local(removed_title, doc_id)
        self.doc_manager.remove_element(doc_id)
        return removed_title

    def _clean_by_path--- This code section failed: ---

 L.  46         0  BUILD_LIST_0          0 
                2  STORE_FAST               'locals_to_delete'

 L.  47         4  LOAD_GLOBAL              get_files
                6  LOAD_FAST                'path'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  STORE_FAST               'files'

 L.  48        12  LOAD_FAST                'self'
               14  LOAD_ATTR                doc_manager
               16  LOAD_METHOD              get_file_names
               18  CALL_METHOD_0         0  '0 positional arguments'
               20  STORE_FAST               'docs'

 L.  50        22  LOAD_FAST                'files'
               24  LOAD_CONST               None
               26  COMPARE_OP               !=
               28  POP_JUMP_IF_FALSE   136  'to 136'
               30  LOAD_GLOBAL              len
               32  LOAD_FAST                'files'
               34  CALL_FUNCTION_1       1  '1 positional argument'
               36  LOAD_GLOBAL              len
               38  LOAD_FAST                'docs'
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  COMPARE_OP               >
               44  POP_JUMP_IF_FALSE   136  'to 136'

 L.  51        46  SETUP_LOOP          210  'to 210'
               48  LOAD_FAST                'docs'
               50  GET_ITER         
               52  FOR_ITER            132  'to 132'
               54  STORE_FAST               'file_name'

 L.  52        56  SETUP_LOOP          130  'to 130'
               58  LOAD_FAST                'files'
               60  GET_ITER         
             62_0  COME_FROM            96  '96'
             62_1  COME_FROM            72  '72'
               62  FOR_ITER            128  'to 128'
               64  STORE_FAST               'name'

 L.  53        66  LOAD_FAST                'file_name'
               68  LOAD_FAST                'name'
               70  COMPARE_OP               in
               72  POP_JUMP_IF_FALSE    62  'to 62'

 L.  54        74  LOAD_FAST                'self'
               76  LOAD_ATTR                doc_manager
               78  LOAD_METHOD              get_doc_by_prop
               80  LOAD_STR                 'file_name'
               82  LOAD_FAST                'self'
               84  LOAD_METHOD              norm_path
               86  LOAD_FAST                'file_name'
               88  CALL_METHOD_1         1  '1 positional argument'
               90  CALL_METHOD_2         2  '2 positional arguments'
               92  STORE_FAST               'entry'

 L.  55        94  LOAD_FAST                'entry'
               96  POP_JUMP_IF_FALSE    62  'to 62'

 L.  56        98  LOAD_FAST                'locals_to_delete'
              100  LOAD_METHOD              append
              102  LOAD_FAST                'entry'
              104  LOAD_STR                 'id'
              106  BINARY_SUBSCR    
              108  CALL_METHOD_1         1  '1 positional argument'
              110  POP_TOP          

 L.  57       112  LOAD_FAST                'self'
              114  LOAD_METHOD              _cancel_document
              116  LOAD_FAST                'entry'
              118  LOAD_STR                 'id'
              120  BINARY_SUBSCR    
              122  CALL_METHOD_1         1  '1 positional argument'
              124  POP_TOP          
              126  JUMP_BACK            62  'to 62'
              128  POP_BLOCK        
            130_0  COME_FROM_LOOP       56  '56'
              130  JUMP_BACK            52  'to 52'
              132  POP_BLOCK        
              134  JUMP_FORWARD        210  'to 210'
            136_0  COME_FROM            44  '44'
            136_1  COME_FROM            28  '28'

 L.  58       136  LOAD_FAST                'files'
              138  LOAD_CONST               None
              140  COMPARE_OP               !=
              142  POP_JUMP_IF_FALSE   210  'to 210'

 L.  59       144  SETUP_LOOP          210  'to 210'
              146  LOAD_FAST                'files'
              148  GET_ITER         
            150_0  COME_FROM           176  '176'
              150  FOR_ITER            208  'to 208'
              152  STORE_FAST               'file_name'

 L.  60       154  LOAD_FAST                'self'
              156  LOAD_ATTR                doc_manager
              158  LOAD_METHOD              get_doc_by_prop
              160  LOAD_STR                 'file_name'
              162  LOAD_FAST                'self'
              164  LOAD_METHOD              norm_path
              166  LOAD_FAST                'file_name'
              168  CALL_METHOD_1         1  '1 positional argument'
              170  CALL_METHOD_2         2  '2 positional arguments'
              172  STORE_FAST               'entry'

 L.  61       174  LOAD_FAST                'entry'
              176  POP_JUMP_IF_FALSE   150  'to 150'

 L.  62       178  LOAD_FAST                'locals_to_delete'
              180  LOAD_METHOD              append
              182  LOAD_FAST                'entry'
              184  LOAD_STR                 'id'
              186  BINARY_SUBSCR    
              188  CALL_METHOD_1         1  '1 positional argument'
              190  POP_TOP          

 L.  63       192  LOAD_FAST                'self'
              194  LOAD_METHOD              _cancel_document
              196  LOAD_FAST                'entry'
              198  LOAD_STR                 'id'
              200  BINARY_SUBSCR    
              202  CALL_METHOD_1         1  '1 positional argument'
              204  POP_TOP          
              206  JUMP_BACK           150  'to 150'
              208  POP_BLOCK        
            210_0  COME_FROM_LOOP      144  '144'
            210_1  COME_FROM           142  '142'
            210_2  COME_FROM           134  '134'
            210_3  COME_FROM_LOOP       46  '46'

 L.  65       210  LOAD_FAST                'locals_to_delete'
              212  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 210

    def _check_docs_to_clean(self):
        locals_to_delete = []
        local_ids = self.doc_manager.get_doc_ids()
        for check_id in local_ids:
            response = self.api.document_status(check_id)
            if response.status_code == 200:
                if response.json()['properties']['status'].upper() == 'CANCELLED':
                    locals_to_delete.append(check_id)
                else:
                    if response.status_code == 404:
                        locals_to_delete.append(check_id)
            else:
                raise_error(response.json(), 'Error trying to list documents in TMS for cleaning')

        db_entries = self.doc_manager.get_all_entries()
        for entry in db_entries:
            if not os.path.isfile(os.path.join(self.path, entry['file_name'])):
                locals_to_delete.append(entry['id'])
                self._cancel_document(entry['id'])

        return locals_to_delete

    def _clean_all(self):
        local_ids = self.doc_manager.get_doc_ids()
        for doc_id in local_ids:
            self._cancel_document(doc_id)

        self.doc_manager.clear_all()
        logger.info('Removed all associations between local and remote documents.')

    def _cancel_document(self, cancel_id):
        response = self.api.document_cancel(cancel_id)
        if response.status_code == 404 or response.status_code == 204:
            return
        if response.status_code == 400:
            for message in response.json()['messages']:
                if 'already in a completed state' in message:
                    return

        logger.warning('Error cleaning up association in TMS for document id {0}'.format(doc_id))