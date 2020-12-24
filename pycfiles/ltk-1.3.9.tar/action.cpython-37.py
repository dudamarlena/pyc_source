# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hectorlopez/.virtualenvs/lingotek/lib/python3.7/site-packages/ltk/actions/action.py
# Compiled at: 2020-04-15 14:10:55
# Size of source mod 2**32: 38173 bytes
from configparser import ConfigParser, NoOptionError
import requests, ctypes, ltk.check_connection, os, shutil, fnmatch, time, getpass, itertools, copy
from ltk import exceptions
from ltk.apicalls import ApiCalls
from ltk.utils import *
from ltk.managers import DocumentManager, FolderManager
from ltk.constants import CONF_DIR, CONF_FN, SYSTEM_FILE, ERROR_FN, METADATA_FIELDS
import json
import ltk.logger as logger
from ltk.git_auto import Git_Auto
from tabulate import tabulate

class Action:

    def __init__(self, path, watch=False, timeout=60):
        self.host = ''
        self.access_token = ''
        self.project_id = ''
        self.project_name = ''
        self.path = path
        self.community_id = ''
        self.workflow_id = ''
        self.locale = ''
        self.always_check_latest_doc = 'off'
        self.clone_option = 'on'
        self.finalized_file = 'off'
        self.unzip_file = 'on'
        self.auto_format_option = ''
        self.download_option = 'clone'
        self.download_dir = None
        self.watch_locales = set()
        self.git_autocommit = None
        self.git_username = ''
        self.git_password = ''
        self.append_option = 'none'
        self.locale_folders = {}
        self.default_metadata = {}
        self.metadata_prompt = False
        self.metadata_fields = METADATA_FIELDS
        if not self._is_initialized():
            raise exceptions.UninitializedError('This project is not initialized. Please run init command.')
        self._initialize_self()
        self.watch = watch
        self.doc_manager = DocumentManager(self.path)
        self.folder_manager = FolderManager(self.path)
        self.timeout = timeout
        self.api = ApiCalls(self.host, self.access_token, self.watch, self.timeout)
        self.git_auto = Git_Auto(self.path)
        self.error_file_name = os.path.join(self.path, CONF_DIR, ERROR_FN)

    def is_hidden_file(self, file_path):
        name = os.path.abspath(file_path).replace(self.path, '')
        if self.has_hidden_attribute(file_path) or 'Thumbs.db' in file_path or 'ehthumbs.db' in file_path:
            return True
        while name != '':
            if name.startswith('.') or name.startswith('~') or name == '4913':
                return True
            name = name.split(os.sep)[1:]
            name = os.sep.join(name)

        return False

    def has_hidden_attribute(self, file_path):
        """ Detects if a file has hidden attributes """
        try:
            attrs = ctypes.windll.kernel32.GetFileAttributesW(str(file_path))
            assert attrs != -1
            result = bool(attrs & 2)
        except (AttributeError, AssertionError):
            result = False

        return result

    def append_location(self, name, path_to_file, in_directory=False):
        repo_directory = path_to_file
        path_sep = os.sep
        config_file_name, conf_parser = self.init_config_file()
        if not conf_parser.has_option('main', 'append_option'):
            self.update_config_file('append_option', 'none', conf_parser, config_file_name, 'Update: Added optional file location appending (ltk config --help)')
        else:
            append_option = conf_parser.get('main', 'append_option')
            if not in_directory:
                while repo_directory and repo_directory != '':
                    repo_directory = os.path.isdir(repo_directory + os.sep + '.ltk') or repo_directory.split(path_sep)[:-1]
                    repo_directory = path_sep.join(repo_directory)

                if repo_directory == '':
                    if append_option != 'none':
                        logger.warning('Error: File must be contained within an ltk-initialized directory')
                        return name
                path_to_file = path_to_file.replace(repo_directory, '', 1).strip(os.sep)
            elif append_option == 'none':
                return name
                if append_option == 'full':
                    return '{0} ({1})'.format(name, path_to_file.rstrip(name).rstrip(os.sep))
                if len(append_option) > 5 and append_option[:5] == 'name:':
                    folder_name = append_option[5:]
                    if folder_name in path_to_file:
                        return '{0} ({1})'.format(name, path_to_file[path_to_file.find(folder_name) + len(folder_name):].rstrip(name).strip(os.sep))
                    return '{0} ({1})'.format(name, path_to_file.rstrip(name).rstrip(os.sep))
            elif len(append_option) > 7 and append_option[:7] == 'number:':
                try:
                    folder_number = int(append_option[7:])
                except ValueError:
                    logger.warning('Error: Value after "number" must be an integer')
                    return name
                else:
                    if folder_number >= 0:
                        return '{0} ({1})'.format(name, path_sep.join(path_to_file.rstrip(name).rstrip(os.sep).split(path_sep)[-1 * folder_number if folder_number != 0 else len(path_to_file):]))
                    logger.warning('Error: Value after "number" must be a non-negative integer')
                    return name
            else:
                logger.warning('Error: Invalid value listed for append option. Please update; see ltk config --help')

    def add_document(self, file_name, title, doc_metadata={}, **kwargs):
        """ adds the document to Lingotek cloud and the db """
        if ltk.check_connection.check_for_connection() == False:
            logger.warning('Cannot connect to network. Documents added to the watch folder will be translated after you reconnect to the network.')
            while ltk.check_connection.check_for_connection() == False:
                time.sleep(15)

        else:
            if self.is_hidden_file(file_name):
                return
            try:
                if not 'locale' not in kwargs:
                    locale = kwargs['locale'] or self.locale
                else:
                    locale = kwargs['locale']
                response = (self.api.add_document)(locale, file_name, (self.project_id), (self.append_location(title, file_name)), doc_metadata, **kwargs)
                if response.status_code == 402:
                    raise_error(response.json(), '', True)
                else:
                    if response.status_code != 202:
                        raise_error(response.json(), 'Failed to add document {0}\n'.format(title), True)
                    else:
                        title = self.append_location(title, file_name)
                        logger.info('Added document {0} with ID {1}\n'.format(title, response.json()['properties']['id']))
                relative_path = self.norm_path(file_name)
                if 'download_folder' in kwargs and kwargs['download_folder']:
                    self._add_document(relative_path, title, response.json()['properties']['id'], response.json()['properties']['process_id'], kwargs['download_folder'])
                else:
                    self._add_document(relative_path, title, response.json()['properties']['id'], response.json()['properties']['process_id'])
                if 'translation_locale_code' in kwargs:
                    if kwargs['translation_locale_code']:
                        self._update_document(relative_path, None, kwargs['translation_locale_code'])
            except KeyboardInterrupt:
                raise_error('', 'Canceled adding document\n')
            except Exception as e:
                try:
                    log_error(self.error_file_name, e)
                    if 'string indices must be integers' in str(e) or 'Expecting value: line 1 column 1' in str(e):
                        logger.error("Error connecting to Lingotek's TMS\n")
                    else:
                        logger.error('Error on adding document \n' + str(file_name) + ': ' + str(e))
                finally:
                    e = None
                    del e

    def _is_initialized(self):
        actual_path = find_conf(self.path)
        if not actual_path:
            return False
        else:
            self.path = os.path.join(actual_path, '')
            return is_initialized(self.path) or False
        return True

    def _initialize_self(self):
        config_file_name = os.path.join(self.path, CONF_DIR, CONF_FN)
        conf_parser = ConfigParser()
        conf_parser.read(config_file_name)
        self.host = conf_parser.get('main', 'host')
        self.access_token = conf_parser.get('main', 'access_token')
        self.project_id = conf_parser.get('main', 'project_id')
        self.community_id = conf_parser.get('main', 'community_id')
        self.workflow_id = conf_parser.get('main', 'workflow_id')
        self.locale = conf_parser.get('main', 'default_locale')
        self.always_check_latest_doc = conf_parser.get('main', 'always_check_latest_doc')
        self.locale = self.locale.replace('_', '-')
        try:
            if conf_parser.has_option('main', 'auto_format'):
                self.auto_format_option = conf_parser.get('main', 'auto_format')
            else:
                self.update_config_file('auto_format', 'on', conf_parser, config_file_name, '')
            if conf_parser.has_option('main', 'finalized_file'):
                self.finalized_file = conf_parser.get('main', 'finalized_file')
            else:
                self.update_config_file('finalized_file', 'off', conf_parser, config_file_name, '')
            if conf_parser.has_option('main', 'unzip_file'):
                self.unzip_file = conf_parser.get('main', 'unzip_file')
            else:
                self.update_config_file('unzip_file', 'on', conf_parser, config_file_name, '')
            if conf_parser.has_option('main', 'project_name'):
                self.project_name = conf_parser.get('main', 'project_name')
            else:
                if conf_parser.has_option('main', 'download_folder'):
                    self.download_dir = conf_parser.get('main', 'download_folder')
                else:
                    self.download_dir = None
                    self.update_config_file('download_folder', json.dumps(self.download_dir), conf_parser, config_file_name, '')
                if conf_parser.has_option('main', 'watch_locales'):
                    watch_locales = conf_parser.get('main', 'watch_locales')
                    if watch_locales:
                        self.watch_locales = set(watch_locales.split(','))
                    else:
                        self.watch_locales = set()
                else:
                    self.watch_locales = set()
                    self.update_config_file('watch_locales', json.dumps(list(self.watch_locales)), conf_parser, config_file_name, '')
                if conf_parser.has_option('main', 'locale_folders'):
                    self.locale_folders = json.loads(conf_parser.get('main', 'locale_folders'))
                    locale_folders = {}
                else:
                    self.locale_folders = {}
                    self.update_config_file('locale_folders', json.dumps(self.locale_folders), conf_parser, config_file_name, '')
                if conf_parser.has_option('main', 'download_option'):
                    self.download_option = conf_parser.get('main', 'download_option')
                else:
                    self.download_option = 'clone'
                    self.update_config_file('download_option', self.download_option, conf_parser, config_file_name, '')
                if conf_parser.has_option('main', 'clone_option'):
                    self.clone_option = conf_parser.get('main', 'clone_option')
                else:
                    self.clone_option = 'on'
                    self.update_config_file('clone_option', self.clone_option, conf_parser, config_file_name, '')
                if conf_parser.has_option('main', 'always_check_latest_doc'):
                    self.always_check_latest_doc = conf_parser.get('main', 'always_check_latest_doc')
                else:
                    self.always_check_latest_doc = 'off'
                    self.update_config_file('always_check_latest_doc', self.always_check_latest_doc, conf_parser, config_file_name, '')
                if conf_parser.has_option('main', 'git_autocommit'):
                    self.git_autocommit = conf_parser.get('main', 'git_autocommit')
                else:
                    self.git_autocommit = ''
                    self.update_config_file('git_autocommit', self.git_autocommit, conf_parser, config_file_name, '')
                if conf_parser.has_option('main', 'git_username'):
                    self.git_username = conf_parser.get('main', 'git_username')
                else:
                    self.git_username = ''
                    self.update_config_file('git_username', self.git_username, conf_parser, config_file_name, '')
                if conf_parser.has_option('main', 'git_password'):
                    self.git_password = conf_parser.get('main', 'git_password')
                else:
                    self.git_password = ''
                    self.update_config_file('git_password', self.git_password, conf_parser, config_file_name, '')
                if conf_parser.has_option('main', 'append_option'):
                    self.append_option = conf_parser.get('main', 'append_option')
                else:
                    self.append_option = 'none'
                    self.update_config_file('append_option', self.append_option, conf_parser, config_file_name, '')
                if conf_parser.has_option('main', 'default_metadata'):
                    self.default_metadata = json.loads(conf_parser.get('main', 'default_metadata'))
                else:
                    self.default_metadata = {}
                    self.update_config_file('default_metadata', json.dumps(self.default_metadata), conf_parser, config_file_name, '')
                if conf_parser.has_option('main', 'metadata_prompt'):
                    self.metadata_prompt = conf_parser.get('main', 'metadata_prompt').lower() == 'on'
                else:
                    self.metadata_prompt = False
                    self.update_config_file('metadata_prompt', 'off', conf_parser, config_file_name, '')
                if conf_parser.has_option('main', 'metadata_fields'):
                    self.metadata_fields = json.loads(conf_parser.get('main', 'metadata_fields'))
                else:
                    self.metadata_fields = METADATA_FIELDS
                    self.update_config_file('metadata_fields', json.dumps(self.metadata_fields), conf_parser, config_file_name, '')
        except NoOptionError as e:
            try:
                if not self.project_name:
                    self.api = ApiCalls(self.host, self.access_token)
                    project_info = self.api.get_project_info(self.community_id)
                    self.project_name = project_info[self.project_id]
                    config_file_name, conf_parser = self.init_config_file()
                    log_info = 'Updated project name'
                    self.update_config_file('project_name', self.project_name, conf_parser, config_file_name, log_info)
            finally:
                e = None
                del e

    def _add_document(self, file_name, title, doc_id, process_id, dl_folder=''):
        """ adds a document to db """
        now = time.time()
        full_path = os.path.join(self.path, file_name)
        last_modified = os.stat(full_path).st_mtime
        if dl_folder:
            dl_folder = os.path.relpath(dl_folder, self.path)
        self.doc_manager.add_document(title, now, doc_id, last_modified, now, file_name, process_id, dl_folder)

    def _update_document(self, file_name, next_document_id=None, locales=None):
        """ updates a document in the db """
        now = time.time()
        file_path = os.path.join(self.path, file_name)
        sys_last_modified = os.stat(file_path).st_mtime
        entry = self.doc_manager.get_doc_by_prop('file_name', file_name)
        doc_id = entry['id']
        self.doc_manager.update_document('last_mod', now, doc_id)
        self.doc_manager.update_document('sys_last_mod', sys_last_modified, doc_id)
        self.doc_manager.update_document('downloaded', [], doc_id)
        if next_document_id:
            self.doc_manager.update_document('id', next_document_id, doc_id)
            doc_id = next_document_id
        if locales:
            self.doc_manager.update_document('locales', locales, doc_id)

    def locked_doc_response_manager(self, response, document_id, *args, **kwargs):
        if response.status_code == 423:
            if 'next_document_id' in response.json():
                self.doc_manager.update_document('id', response.json()['next_document_id'], document_id)
                return ((self.api.document_update)(response.json()['next_document_id'], *args, **kwargs), response.json()['next_document_id'])
        return (
         response, document_id)

    def close(self):
        self.doc_manager.close_db()

    def open(self):
        self.doc_manager.open_db()

    def init_config_file(self):
        config_file_name = os.path.join(self.path, CONF_DIR, CONF_FN)
        conf_parser = ConfigParser()
        conf_parser.read(config_file_name)
        return (config_file_name, conf_parser)

    def update_config_file(self, option, value, conf_parser, config_file_name, log_info):
        try:
            conf_parser.set('main', option, value)
            with open(config_file_name, 'w') as (new_file):
                conf_parser.write(new_file)
            self._initialize_self()
            if len(log_info):
                logger.info(log_info + '\n')
        except IOError as e:
            try:
                print(e.errno)
                print(e)
            finally:
                e = None
                del e

    def metadata_wizard--- This code section failed: ---

 L. 350         0  LOAD_CONST               0
                2  LOAD_CONST               None
                4  IMPORT_NAME              re
                6  STORE_FAST               're'

 L. 351         8  LOAD_FAST                'set_defaults'
               10  POP_JUMP_IF_FALSE    26  'to 26'

 L. 352        12  LOAD_GLOBAL              METADATA_FIELDS
               14  STORE_FAST               'fields'

 L. 353        16  BUILD_MAP_0           0 
               18  STORE_FAST               'new_metadata'

 L. 354        20  LOAD_STR                 'Default Value: '
               22  STORE_FAST               'prompt_message'
               24  JUMP_FORWARD        116  'to 116'
             26_0  COME_FROM            10  '10'

 L. 356        26  LOAD_DEREF               'self'
               28  LOAD_ATTR                metadata_fields
               30  STORE_FAST               'fields'

 L. 357        32  LOAD_GLOBAL              copy
               34  LOAD_METHOD              deepcopy
               36  LOAD_DEREF               'self'
               38  LOAD_ATTR                default_metadata
               40  CALL_METHOD_1         1  '1 positional argument'
               42  STORE_FAST               'new_metadata'

 L. 358        44  LOAD_STR                 'Value: '
               46  STORE_FAST               'prompt_message'

 L. 359        48  LOAD_GLOBAL              all
               50  LOAD_CLOSURE             'self'
               52  BUILD_TUPLE_1         1 
               54  LOAD_GENEXPR             '<code_object <genexpr>>'
               56  LOAD_STR                 'Action.metadata_wizard.<locals>.<genexpr>'
               58  MAKE_FUNCTION_8          'closure'
               60  LOAD_FAST                'fields'
               62  GET_ITER         
               64  CALL_FUNCTION_1       1  '1 positional argument'
               66  CALL_FUNCTION_1       1  '1 positional argument'
               68  POP_JUMP_IF_FALSE   116  'to 116'

 L. 360        70  LOAD_GLOBAL              print
               72  LOAD_STR                 'All fields have default metadata already set'
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  POP_TOP          

 L. 361        78  SETUP_LOOP          110  'to 110'
               80  LOAD_FAST                'fields'
               82  GET_ITER         
               84  FOR_ITER            108  'to 108'
               86  STORE_FAST               'field'

 L. 362        88  LOAD_GLOBAL              print
               90  LOAD_FAST                'field'
               92  LOAD_STR                 ': '
               94  LOAD_DEREF               'self'
               96  LOAD_ATTR                default_metadata
               98  LOAD_FAST                'field'
              100  BINARY_SUBSCR    
              102  CALL_FUNCTION_3       3  '3 positional arguments'
              104  POP_TOP          
              106  JUMP_BACK            84  'to 84'
              108  POP_BLOCK        
            110_0  COME_FROM_LOOP       78  '78'

 L. 363       110  LOAD_DEREF               'self'
              112  LOAD_ATTR                default_metadata
              114  RETURN_VALUE     
            116_0  COME_FROM            68  '68'
            116_1  COME_FROM            24  '24'

 L. 364   116_118  SETUP_LOOP          422  'to 422'
              120  LOAD_FAST                'fields'
              122  GET_ITER         
          124_126  FOR_ITER            420  'to 420'
              128  STORE_FAST               'field'

 L. 365       130  LOAD_GLOBAL              print
              132  LOAD_STR                 '\n==='
              134  LOAD_FAST                'field'
              136  LOAD_STR                 '==='
              138  CALL_FUNCTION_3       3  '3 positional arguments'
              140  POP_TOP          

 L. 366       142  LOAD_FAST                'field'
              144  LOAD_DEREF               'self'
              146  LOAD_ATTR                default_metadata
              148  COMPARE_OP               in
              150  POP_JUMP_IF_FALSE   234  'to 234'
              152  LOAD_DEREF               'self'
              154  LOAD_ATTR                default_metadata
              156  LOAD_FAST                'field'
              158  BINARY_SUBSCR    
              160  POP_JUMP_IF_FALSE   234  'to 234'

 L. 367       162  LOAD_FAST                'set_defaults'
              164  POP_JUMP_IF_FALSE   216  'to 216'

 L. 368       166  LOAD_GLOBAL              print
              168  LOAD_STR                 'Current '
              170  LOAD_FAST                'prompt_message'
              172  BINARY_ADD       
              174  LOAD_DEREF               'self'
              176  LOAD_ATTR                default_metadata
              178  LOAD_FAST                'field'
              180  BINARY_SUBSCR    
              182  CALL_FUNCTION_2       2  '2 positional arguments'
              184  POP_TOP          

 L. 369       186  LOAD_GLOBAL              yes_no_prompt
              188  LOAD_STR                 'Would you like to change the default value for this field?'
              190  LOAD_CONST               False
              192  LOAD_CONST               ('default_yes',)
              194  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              196  POP_JUMP_IF_TRUE    234  'to 234'

 L. 370       198  LOAD_DEREF               'self'
              200  LOAD_ATTR                default_metadata
              202  LOAD_FAST                'field'
              204  BINARY_SUBSCR    
              206  LOAD_FAST                'new_metadata'
              208  LOAD_FAST                'field'
              210  STORE_SUBSCR     

 L. 371       212  CONTINUE            124  'to 124'
              214  JUMP_FORWARD        234  'to 234'
            216_0  COME_FROM           164  '164'

 L. 373       216  LOAD_GLOBAL              print
              218  LOAD_FAST                'prompt_message'
              220  LOAD_DEREF               'self'
              222  LOAD_ATTR                default_metadata
              224  LOAD_FAST                'field'
              226  BINARY_SUBSCR    
              228  CALL_FUNCTION_2       2  '2 positional arguments'
              230  POP_TOP          

 L. 374       232  CONTINUE            124  'to 124'
            234_0  COME_FROM           214  '214'
            234_1  COME_FROM           196  '196'
            234_2  COME_FROM           160  '160'
            234_3  COME_FROM           150  '150'

 L. 379       234  LOAD_GLOBAL              input
              236  LOAD_FAST                'prompt_message'
              238  CALL_FUNCTION_1       1  '1 positional argument'
              240  STORE_FAST               'new_value'

 L. 381       242  LOAD_FAST                'new_value'
              244  POP_JUMP_IF_TRUE    248  'to 248'

 L. 382       246  CONTINUE            124  'to 124'
            248_0  COME_FROM           244  '244'

 L. 384       248  LOAD_FAST                'field'
              250  LOAD_STR                 'campaign_rating'
              252  COMPARE_OP               ==
          254_256  POP_JUMP_IF_FALSE   332  'to 332'

 L. 385       258  SETUP_LOOP          304  'to 304'
            260_0  COME_FROM           292  '292'
              260  LOAD_FAST                're'
              262  LOAD_METHOD              fullmatch
              264  LOAD_STR                 '-?0*[0-9]{1,7}'
              266  LOAD_FAST                'new_value'
              268  CALL_METHOD_2         2  '2 positional arguments'
          270_272  POP_JUMP_IF_TRUE    302  'to 302'

 L. 386       274  LOAD_GLOBAL              print
              276  LOAD_STR                 'Value must be an integer between -9999999 and 9999999'
              278  CALL_FUNCTION_1       1  '1 positional argument'
              280  POP_TOP          

 L. 387       282  LOAD_GLOBAL              input
              284  LOAD_FAST                'prompt_message'
              286  CALL_FUNCTION_1       1  '1 positional argument'
              288  STORE_FAST               'new_value'

 L. 389       290  LOAD_FAST                'new_value'
          292_294  POP_JUMP_IF_TRUE    260  'to 260'

 L. 390       296  BREAK_LOOP       
          298_300  JUMP_BACK           260  'to 260'
            302_0  COME_FROM           270  '270'
              302  POP_BLOCK        
            304_0  COME_FROM_LOOP      258  '258'

 L. 391       304  LOAD_FAST                'new_value'
          306_308  POP_JUMP_IF_TRUE    312  'to 312'

 L. 392       310  CONTINUE            124  'to 124'
            312_0  COME_FROM           306  '306'

 L. 394       312  LOAD_FAST                're'
              314  LOAD_METHOD              fullmatch
              316  LOAD_STR                 '-0+'
              318  LOAD_FAST                'new_value'
              320  CALL_METHOD_2         2  '2 positional arguments'
          322_324  POP_JUMP_IF_FALSE   410  'to 410'

 L. 395       326  LOAD_STR                 '0'
              328  STORE_FAST               'new_value'
              330  JUMP_FORWARD        410  'to 410'
            332_0  COME_FROM           254  '254'

 L. 397       332  LOAD_FAST                'field'
              334  LOAD_STR                 'require_review'
              336  COMPARE_OP               ==
          338_340  POP_JUMP_IF_FALSE   410  'to 410'

 L. 398       342  SETUP_LOOP          402  'to 402'
            344_0  COME_FROM           390  '390'
              344  LOAD_FAST                'new_value'
              346  LOAD_METHOD              upper
              348  CALL_METHOD_0         0  '0 positional arguments'
              350  LOAD_STR                 'TRUE'
              352  COMPARE_OP               !=
          354_356  POP_JUMP_IF_FALSE   400  'to 400'
              358  LOAD_FAST                'new_value'
              360  LOAD_METHOD              upper
              362  CALL_METHOD_0         0  '0 positional arguments'
              364  LOAD_STR                 'FALSE'
              366  COMPARE_OP               !=
          368_370  POP_JUMP_IF_FALSE   400  'to 400'

 L. 399       372  LOAD_GLOBAL              print
              374  LOAD_STR                 'Value must be either TRUE or FALSE'
              376  CALL_FUNCTION_1       1  '1 positional argument'
              378  POP_TOP          

 L. 400       380  LOAD_GLOBAL              input
              382  LOAD_FAST                'prompt_message'
              384  CALL_FUNCTION_1       1  '1 positional argument'
              386  STORE_FAST               'new_value'

 L. 402       388  LOAD_FAST                'new_value'
          390_392  POP_JUMP_IF_TRUE    344  'to 344'

 L. 403       394  BREAK_LOOP       
          396_398  JUMP_BACK           344  'to 344'
            400_0  COME_FROM           368  '368'
            400_1  COME_FROM           354  '354'
              400  POP_BLOCK        
            402_0  COME_FROM_LOOP      342  '342'

 L. 404       402  LOAD_FAST                'new_value'
          404_406  POP_JUMP_IF_TRUE    410  'to 410'

 L. 405       408  CONTINUE            124  'to 124'
            410_0  COME_FROM           404  '404'
            410_1  COME_FROM           338  '338'
            410_2  COME_FROM           330  '330'
            410_3  COME_FROM           322  '322'

 L. 406       410  LOAD_FAST                'new_value'
              412  LOAD_FAST                'new_metadata'
              414  LOAD_FAST                'field'
              416  STORE_SUBSCR     
              418  JUMP_BACK           124  'to 124'
              420  POP_BLOCK        
            422_0  COME_FROM_LOOP      116  '116'

 L. 407       422  LOAD_FAST                'new_metadata'
              424  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_BLOCK' instruction at offset 302

    def validate_metadata_fields(self, field_options):
        if field_options.lower() == 'all' or field_options == '':
            return (
             True, METADATA_FIELDS)
        converted = field_options.replace(', ', ',')
        options = converted.split(',')
        for option in options:
            if option not in METADATA_FIELDS:
                logger.warning('Error: {0} is not a valid metadata field'.format(option))
                return (False, None)

        return (
         True, options)

    def get_relative_path(self, path):
        return get_relative_path(self.path, path)

    def get_current_path(self, path):
        cwd = os.getcwd()
        if cwd in path:
            path = path.replace(cwd, '')
            return path
        cwd_relative_path = cwd.replace(self.path, '')
        return path.replace(cwd_relative_path + os.sep, '')

    def get_current_abs(self, path):
        cwd = os.getcwd()
        if cwd in path:
            path = path.replace(cwd, '')
        else:
            cwd_relative_path = cwd.replace(self.path, '')
            cwd_path = path.replace(cwd_relative_path + os.sep, '')
            path = cwd_path
        return os.path.abspath(path)

    def norm_path(self, file_location):
        if file_location:
            file_location = os.path.normpath(file_location)
            norm_path = os.path.abspath(os.path.expanduser(file_location)).replace(self.path, '')
            if file_location is not '.':
                if '..' not in file_location:
                    if os.path.exists(os.path.join(self.path, file_location)):
                        return file_location.replace(self.path, '')
            if '..' in file_location:
                if file_location != '..':
                    return norm_path.replace(self.path, '')
            if not os.path.exists(os.path.join(self.path, norm_path)):
                if os.path.exists(os.path.join(self.path, file_location)):
                    return os.path.abspath(os.path.expanduser(file_location.replace(self.path, ''))).replace(self.path, '')
            if file_location == '..':
                return os.path.abspath(os.path.expanduser(file_location.replace(self.path, ''))).replace(self.path, '')
            return norm_path
        return

    def get_docs_in_path(self, path):
        files = get_files(path)
        db_files = self.doc_manager.get_file_names()
        docs = []
        if files:
            for file in files:
                file_name = self.norm_path(file)
                if file_name in db_files:
                    docs.append(self.doc_manager.get_doc_by_prop('file_name', file_name))

        return docs

    def get_doc_filenames_in_path(self, path):
        files = get_files(path)
        db_files = self.doc_manager.get_file_names()
        docs = []
        if files:
            for file in files:
                file_name = self.norm_path(file)
                if file_name in db_files:
                    docs.append(file_name)

        return docs

    def get_doc_locales(self, doc_id, doc_name):
        locales = []
        response = self.api.document_translation_status(doc_id)
        if response.status_code != 200:
            if check_response(response):
                if response.json()['messages']:
                    if 'No translations exist' in response.json()['messages'][0]:
                        return locales
            elif doc_name:
                raise_error(response.json(), 'Failed to check target locales for document ' + doc_name, True, doc_id)
            else:
                raise_error(response.json(), 'Failed to check target locales for document ' + doc_id, True, doc_id)
        try:
            if 'entities' in response.json():
                for entry in response.json()['entities']:
                    locales.append(entry['properties']['locale_code'])

        except KeyError as e:
            try:
                print('Error listing translations')
                return
            finally:
                e = None
                del e

        return locales

    def is_locale_folder_taken(self, new_locale, path):
        for locale, folder in self.locale_folders.items():
            if path == folder:
                return locale == new_locale or locale

        return False

    def get_latest_document_version(self, document_id):
        if self.always_check_latest_doc == 'off':
            return False
        try:
            response = self.api.get_latest_document(document_id)
            if response.status_code != 200:
                print('Latest document was not found')
                return False
            latest_id = response.json()['properties']['id']
            return latest_id
        except Exception as e:
            try:
                log_error(self.error_file_name, e)
                logger.error('Error on getting latest document')
                return False
            finally:
                e = None
                del e

    def update_document_action(self, file_name, title=None, **kwargs):
        try:
            relative_path = self.norm_path(file_name)
            entry = self.doc_manager.get_doc_by_prop('file_name', relative_path)
            try:
                document_id = entry['id']
            except TypeError as e:
                try:
                    log_error(self.error_file_name, e)
                    logger.error("Document name specified for update doesn't exist: {0}".format(title))
                    return
                finally:
                    e = None
                    del e

            if title:
                response, previous_doc_id = (self.locked_doc_response_manager)((self.api.document_update)(document_id, file_name, title=title, **kwargs), document_id, file_name, title=title, **kwargs)
            else:
                response, previous_doc_id = (self.locked_doc_response_manager)((self.api.document_update(document_id, file_name)), document_id, file_name, **kwargs)
            if response.status_code == 410:
                target_locales = entry['locales']
                self.doc_manager.remove_element(previous_doc_id)
                print('Document has been archived. Reuploading...')
                self.add_document(file_name, title, (self.default_metadata), translation_locale_code=target_locales)
                return True
            if response.status_code == 402:
                raise_error(response.json(), 'Community has been disabled. Please contact support@lingotek.com to re-enable your community', True)
            else:
                if response.status_code == 202:
                    try:
                        try:
                            next_document_id = response.json()['next_document_id']
                        except Exception:
                            next_document_id = None

                    finally:
                        return

                    self._update_document(relative_path, next_document_id)
                    return True
                raise_error(response.json(), 'Failed to update document {0}'.format(file_name), True)
                return False
        except Exception as e:
            try:
                log_error(self.error_file_name, e)
                if 'string indices must be integers' in str(e) or 'Expecting value: line 1 column 1' in str(e):
                    logger.error("Error connecting to Lingotek's TMS")
                else:
                    logger.error('Error on updating document' + str(file_name) + ': ' + str(e))
                return False
            finally:
                e = None
                del e

    def _target_action_db(self, to_delete, locales, document_id):
        locale_set = set()
        for locale in locales:
            locale_set.add(locale.replace('-', '_'))

        if to_delete:
            curr_locales = self.doc_manager.get_doc_by_prop('id', document_id)['locales']
            updated_locales = set(curr_locales) - locale_set
            self.doc_manager.update_document('locales', updated_locales, document_id)
        else:
            self.doc_manager.update_document('locales', list(locales), document_id)

    def update_doc_locales(self, document_id, include_cancelled=False):
        try:
            locale_map = self.import_locale_info(document_id, include_cancelled)
            locale_info = list(iter(locale_map))
        except exceptions.RequestFailedError as e:
            try:
                log_error(self.error_file_name, e)
                locale_info = []
            finally:
                e = None
                del e

        self.doc_manager.update_document('locales', locale_info, document_id)

    def added_folder_of_file(self, file_path):
        folders = self.folder_manager.get_file_names()
        if not folders:
            return
        for folder in folders:
            folder = os.path.join(self.path, folder)
            if folder in file_path:
                return folder

    def get_new_name(self, file_name, curr_path):
        i = 1
        file_path = os.path.join(curr_path, file_name)
        name, extension = os.path.splitext(file_name)
        while os.path.isfile(file_path):
            new_name = '{name}({i}){ext}'.format(name=name, i=i, ext=extension)
            file_path = os.path.join(curr_path, new_name)
            i += 1

        return file_path

    def import_locale_info(self, document_id, poll=False, include_cancelled=False):
        locale_progress = {}
        response = self.api.document_translation_status(document_id)
        if response.status_code != 200:
            if poll or response.status_code == 404:
                return {}
            raise exceptions.RequestFailedError('Failed to get locale details of document')
        try:
            for entry in response.json()['entities']:
                curr_locale = entry['properties']['locale_code']
                curr_progress = int(entry['properties']['percent_complete'])
                curr_status = entry['properties']['status']
                curr_locale = curr_locale.replace('-', '_')
                if include_cancelled or curr_status.upper() != 'CANCELLED':
                    locale_progress[curr_locale] = curr_progress

        except KeyError:
            pass

        return locale_progress

    def delete_local(self, title, document_id, message=None):
        if not title:
            title = document_id
        message = '{0} has been deleted locally'.format(title) if not message else message
        try:
            file_name = self.doc_manager.get_doc_by_prop('id', document_id)['file_name']
        except TypeError:
            logger.info('Document to remove not found in the local database')
            return
        else:
            try:
                os.remove(os.path.join(self.path, file_name))
                logger.info(message)
            except OSError:
                logger.info('Something went wrong trying to delete the local file')

    def delete_local_translation(self, file_name):
        try:
            if not file_name:
                logger.info('Please provide a valid file name')
            logger.info('{0} (local translation) has been deleted'.format(self.get_relative_path(file_name)))
            os.remove(os.path.join(self.path, file_name))
        except OSError:
            logger.info('Something went wrong trying to download the local translation')

    def delete_local_path(self, path, message=None):
        path = self.norm_path(path)
        message = '{0} has been deleted locally.'.format(path) if not message else message
        try:
            os.remove(path)
            logger.info(message)
        except OSError:
            logger.info('Something went wrong trying to delete the local file')


def is_initialized(project_path):
    ltk_path = os.path.join(project_path, CONF_DIR)
    if os.path.isdir(ltk_path):
        if os.path.isfile(os.path.join(ltk_path, CONF_FN)):
            if os.stat(os.path.join(ltk_path, CONF_FN)).st_size:
                return True
    return False


def choice_mapper(info):
    mapper = {}
    import operator
    sorted_info = sorted((info.items()), key=(operator.itemgetter(1)))
    index = 0
    for entry in sorted_info:
        if entry[0] and entry[1]:
            mapper[index] = {entry[0]: entry[1]}
            index += 1

    table = []
    for k, v in mapper.items():
        try:
            headers = [
             'ID', 'Name', 'UUID']
            for values in v:
                table.append([k, v[values], values])

        except UnicodeEncodeError:
            continue

    print(tabulate(table, headers=headers))
    return mapper


def find_conf(curr_path):
    """
    check if the conf folder exists in current directory's parent directories
    """
    if os.path.isdir(os.path.join(curr_path, CONF_DIR)):
        return curr_path
    if curr_path == os.path.abspath(os.sep):
        return
    return find_conf(os.path.abspath(os.path.join(curr_path, os.pardir)))


def printResponseMessages(response):
    for message in response.json()['messages']:
        logger.info(message)


def get_files(patterns):
    """ gets all files matching pattern from root
        pattern supports any unix shell-style wildcards (not same as RE) """
    cwd = os.getcwd()
    if isinstance(patterns, str):
        patterns = [
         patterns]
    allPatterns = []
    if isinstance(patterns, list) or isinstance(patterns, tuple):
        for pattern in patterns:
            basename = os.path.basename(pattern)
            if basename and basename != '':
                allPatterns.extend(getRegexFiles(pattern, cwd))
            else:
                allPatterns.append(pattern)

    else:
        basename = os.path.basename(patterns)
        if basename and basename != '':
            allPatterns.extend(getRegexFiles(patterns, cwd))
        else:
            allPatterns.append(patterns)
    matched_files = []
    for pattern in allPatterns:
        path = os.path.abspath(pattern)
        if os.path.exists(path):
            if os.path.isdir(path):
                for root, subdirs, files in os.walk(path):
                    for file in files:
                        if not 'desktop.ini' in file:
                            'Thumbs.db' in file or 'ehthumbs.db' in file or matched_files.append(os.path.join(root, file))

            else:
                matched_files.append(path)

    if len(matched_files) == 0:
        return
    return matched_files


def getRegexFiles(pattern, path):
    dir_name = os.path.dirname(pattern)
    if dir_name:
        path = os.path.join(path, dir_name)
    pattern_name = os.path.basename(pattern)
    matched_files = []
    if pattern_name:
        if '*' not in pattern:
            return [
             pattern]
    for path, subdirs, files in os.walk(path):
        for fn in fnmatch.filter(files, pattern):
            matched_files.append(os.path.join(path, fn))

    return matched_files