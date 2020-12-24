# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.7.1/lib/python3.7/site-packages/onepassword_tools/lib/OnePasswordUtils.py
# Compiled at: 2019-05-24 16:38:50
# Size of source mod 2**32: 7524 bytes
import onepassword_tools.lib.ClickUtils as ClickUtils
import onepassword_tools.lib.ConfigFile as ConfigFile
import onepassword_tools.lib.Log as Log
from onepassword_tools.lib.MiscUtils import is_uuid
import json, os, secrets, string, subprocess, sys
if os.environ.get('USE_LOCAL'):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/../../../onepassword-local-search')
import onepassword_local_search.models.Item as Item
import onepassword_local_search.OnePassword as OnePassword
import onepassword_local_search.exceptions.ManagedException as ManagedException
import re

class OnePasswordUtils:
    onePassword: OnePassword
    suggestions = []
    suggestions: []

    def __init__(self):
        self.onePassword = OnePassword()
        self.config = ConfigFile()

    @staticmethod
    def _communicate(subproc, inputstr=None):
        """
        Encode the input given to the subprocess if any
        :param subproc:
        :param inputstr:
        :return: A tuple of (stdout, stderr)
        """
        if inputstr is None:
            return subproc.communicate()
        if not inputstr:
            inputstr = ''
        return subproc.communicate(inputstr.encode())

    def _authenticate(self, shorthand=''):
        """
        Authenticate over 1Password and register the session key in the environment variable
        :return: Nothing
        """
        try:
            sessionKey = subprocess.check_output(['op', 'signin', shorthand, '--output=raw']).decode('utf-8').replace('\n', '')
            os.environ['OP_SESSION_' + shorthand] = sessionKey
        except subprocess.CalledProcessError:
            ClickUtils.error('Failed to authenticate. You may have written the wrong password ?')
            sys.exit(1)

    def authenticate--- This code section failed: ---

 L.  57         0  LOAD_FAST                'account'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    78  'to 78'

 L.  58         8  LOAD_FAST                'self'
               10  LOAD_ATTR                config
               12  LOAD_METHOD              get_section
               14  LOAD_STR                 'accounts'
               16  CALL_METHOD_1         1  '1 positional argument'
               18  STORE_FAST               'accounts'

 L.  59        20  LOAD_GLOBAL              len
               22  LOAD_FAST                'accounts'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  LOAD_CONST               0
               28  COMPARE_OP               >
               30  POP_JUMP_IF_FALSE    58  'to 58'

 L.  60        32  SETUP_LOOP           76  'to 76'
               34  LOAD_FAST                'accounts'
               36  GET_ITER         
               38  FOR_ITER             54  'to 54'
               40  STORE_FAST               'account'

 L.  61        42  LOAD_FAST                'self'
               44  LOAD_METHOD              _authenticate
               46  LOAD_FAST                'account'
               48  CALL_METHOD_1         1  '1 positional argument'
               50  POP_TOP          
               52  JUMP_BACK            38  'to 38'
               54  POP_BLOCK        
               56  JUMP_ABSOLUTE        88  'to 88'
             58_0  COME_FROM            30  '30'

 L.  63        58  LOAD_FAST                'self'
               60  LOAD_METHOD              _authenticate
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                onePassword
               66  LOAD_ATTR                configFileService
               68  LOAD_METHOD              get_latest_signin
               70  CALL_METHOD_0         0  '0 positional arguments'
               72  CALL_METHOD_1         1  '1 positional argument'
               74  POP_TOP          
             76_0  COME_FROM_LOOP       32  '32'
               76  JUMP_FORWARD         88  'to 88'
             78_0  COME_FROM             6  '6'

 L.  65        78  LOAD_FAST                'self'
               80  LOAD_METHOD              _authenticate
               82  LOAD_FAST                'account'
               84  CALL_METHOD_1         1  '1 positional argument'
               86  POP_TOP          
             88_0  COME_FROM            76  '76'

Parse error at or near `COME_FROM_LOOP' instruction at offset 76_0

    def create_item(self, request_object, template, title, tags=None, url='', vault='', account=''):
        if tags is None:
            tags = []
        try:
            Log.debug(request_object, 'request data')
            rc, output, error = self.op_cli('encode', json.dumps(request_object))
            if output is not None and len(output) > 1:
                encrypted_data = output[:-1]
            else:
                raise Exception('Error while encoding json')
            command = 'create item "%s" %s' % (template, encrypted_data)
            if title:
                if title != '':
                    command += ' --title="%s"' % title
            if type(tags).__name__ != 'list':
                tags = [
                 tags]
            if tags:
                if len(tags) > 0:
                    command += ' --tags="%s"' % ','.join(tags)
            if url:
                if url != '':
                    if template == 'Login':
                        command += ' --url="%s"' % url
            if vault:
                if vault != '':
                    command += ' --vault="%s"' % vault
            if account:
                if account != '':
                    command += ' --account=%s' % account
            Log.debug(command, 'op command executed')
            rc, output, error = self.op_cli(command)
            if output is not None:
                if len(output) > 1:
                    created_item = json.loads(output.replace('\n', ''))
                    created_item.get('uuid') or Log.error(error)
                    raise Exception('Error while creating onepassword entry')
                else:
                    created_item['request_object'] = request_object
                    return created_item
            else:
                Log.error(error)
                raise Exception('Error while creating onepassword entry')
        except Exception:
            raise Exception('Entry while creating onepassword entry')

    def is_authenticated--- This code section failed: ---

 L. 116         0  LOAD_FAST                'check_mode'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_TRUE     16  'to 16'
                8  LOAD_FAST                'check_mode'
               10  LOAD_STR                 'local'
               12  COMPARE_OP               ==
               14  POP_JUMP_IF_FALSE    30  'to 30'
             16_0  COME_FROM             6  '6'

 L. 117        16  LOAD_FAST                'self'
               18  LOAD_ATTR                onePassword
               20  LOAD_METHOD              is_authenticated
               22  CALL_METHOD_0         0  '0 positional arguments'
               24  POP_JUMP_IF_TRUE     30  'to 30'

 L. 118        26  LOAD_CONST               False
               28  RETURN_VALUE     
             30_0  COME_FROM            24  '24'
             30_1  COME_FROM            14  '14'

 L. 120        30  LOAD_FAST                'check_mode'
               32  LOAD_CONST               None
               34  COMPARE_OP               is
               36  POP_JUMP_IF_TRUE     46  'to 46'
               38  LOAD_FAST                'check_mode'
               40  LOAD_STR                 'remote'
               42  COMPARE_OP               ==
               44  POP_JUMP_IF_FALSE   170  'to 170'
             46_0  COME_FROM            36  '36'

 L. 121        46  LOAD_FAST                'account'
               48  LOAD_CONST               None
               50  COMPARE_OP               is
               52  POP_JUMP_IF_FALSE   144  'to 144'

 L. 122        54  LOAD_FAST                'self'
               56  LOAD_ATTR                config
               58  LOAD_METHOD              get_section
               60  LOAD_STR                 'accounts'
               62  CALL_METHOD_1         1  '1 positional argument'
               64  STORE_FAST               'accounts'

 L. 123        66  LOAD_GLOBAL              len
               68  LOAD_FAST                'accounts'
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  LOAD_CONST               0
               74  COMPARE_OP               >
               76  POP_JUMP_IF_FALSE   120  'to 120'

 L. 124        78  SETUP_LOOP          142  'to 142'
               80  LOAD_FAST                'accounts'
               82  GET_ITER         
             84_0  COME_FROM           108  '108'
               84  FOR_ITER            116  'to 116'
               86  STORE_FAST               'account_'

 L. 125        88  LOAD_FAST                'self'
               90  LOAD_METHOD              op_cli
               92  LOAD_STR                 'get account --account="%s"'
               94  LOAD_FAST                'account_'
               96  BINARY_MODULO    
               98  CALL_METHOD_1         1  '1 positional argument'
              100  LOAD_CONST               0
              102  BINARY_SUBSCR    
              104  LOAD_CONST               0
              106  COMPARE_OP               ==
              108  POP_JUMP_IF_TRUE     84  'to 84'

 L. 126       110  LOAD_CONST               False
              112  RETURN_VALUE     
              114  JUMP_BACK            84  'to 84'
              116  POP_BLOCK        
              118  JUMP_ABSOLUTE       170  'to 170'
            120_0  COME_FROM            76  '76'

 L. 128       120  LOAD_FAST                'self'
              122  LOAD_METHOD              op_cli
              124  LOAD_STR                 'get account'
              126  CALL_METHOD_1         1  '1 positional argument'
              128  LOAD_CONST               0
              130  BINARY_SUBSCR    
              132  LOAD_CONST               0
              134  COMPARE_OP               ==
              136  POP_JUMP_IF_TRUE    170  'to 170'

 L. 129       138  LOAD_CONST               False
              140  RETURN_VALUE     
            142_0  COME_FROM_LOOP       78  '78'
              142  JUMP_FORWARD        170  'to 170'
            144_0  COME_FROM            52  '52'

 L. 131       144  LOAD_FAST                'self'
              146  LOAD_METHOD              op_cli
              148  LOAD_STR                 'get account --account="%s"'
              150  LOAD_FAST                'account'
              152  BINARY_MODULO    
              154  CALL_METHOD_1         1  '1 positional argument'
              156  LOAD_CONST               0
              158  BINARY_SUBSCR    
              160  LOAD_CONST               0
              162  COMPARE_OP               ==
              164  POP_JUMP_IF_TRUE    170  'to 170'

 L. 132       166  LOAD_CONST               False
              168  RETURN_VALUE     
            170_0  COME_FROM           164  '164'
            170_1  COME_FROM           142  '142'
            170_2  COME_FROM           136  '136'
            170_3  COME_FROM            44  '44'

 L. 133       170  LOAD_CONST               True
              172  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 142_0

    def generate_op_field_uuid(self):
        return self.generate_op_uuid(26)

    def generate_op_section_uuid(self):
        return self.generate_op_uuid(29)

    @staticmethod
    def generate_op_uuid(length=26):
        return ''.join((secrets.choice(string.ascii_lowercase) for _ in range(length)))

    def get_alias(self, search):
        """
        Search if the input string is aliases to an uuid in the config file
        :param search:
        :return:
        """
        if self.config.config_key_exists('aliases', search):
            return self.config.config['aliases'][search]
        return search

    def op_cli(self, cmd, inputstr=None):
        """
        Call the 1Password cli (op)
        :param cmd: the op arguments and options
        :param inputstr: the input given to the command
        :return: A tuple of (returncode, stdout, stderr)
        """
        e = os.environ.copy()
        p = subprocess.Popen(('op ' + cmd), bufsize=0,
          close_fds=True,
          env=e,
          shell=True,
          stdin=(subprocess.PIPE),
          stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        try:
            out, err = self._communicate(p, inputstr=inputstr)
        except subprocess.CalledProcessError:
            out = ''
            err = ''

        rc = p.returncode
        return (rc, out.decode('utf-8'), err.decode('utf-8'))

    def search_item_uuid_by_title(self, search):
        """
        Search an item by title
        :param search:
        :return: Item if only one match, None either
        """
        items = self.onePassword.get_items(search)
        if len(items) == 1:
            return self.onePassword.get((items[0].uuid), output=False)
        return items

    def try_to_grab_item(self, search) -> Item:
        """
        First try to grab by using 1Password or custom UUID, then fallback to
        search item by title.
        :param search:
        :return: Item or None
        """
        search = self.get_alias(search)
        try:
            item = self.onePassword.get(search, output=False)
        except ManagedException:
            item = self.search_item_uuid_by_title(search)

        return item