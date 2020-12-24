# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /aedir/test.py
# Compiled at: 2020-02-17 13:24:16
# Size of source mod 2**32: 6893 bytes
__doc__ = '\naedir.test - base classes for unit tests\n'
import json, logging, os, jinja2
from ldap0.test import SlapdObject, SlapdTestCase
from aedir import AEDirObject
__all__ = [
 'AESlapdObject',
 'AETest']

class AESlapdObject(SlapdObject):
    """AESlapdObject"""
    testrunsubdirs = ('schema', 'um', 'accesslog', 'session')
    openldap_schema_files = ('core.schema', 'cosine.schema', 'inetorgperson.schema',
                             'dyngroup.schema', 'openldap.schema', 'ppolicy.schema',
                             'nis.schema', 'duaconf.schema')

    def __init__(self, inventory_hostname, inventory, j2_template_dir):
        self._inventory = inventory
        self._inventory_local = self._inventory[inventory_hostname]
        self._openldap_role = self._inventory_local['openldap_role']
        self._j2_template_dir = j2_template_dir
        SlapdObject.__init__(self)
        self._schema_prefix = os.path.join(self.testrundir, 'schema')
        self._oath_ldap_socket_path = os.path.join(self.testrundir, 'bind-listener')
        self._inventory_local.update({'oath_ldap_socket_path':self._oath_ldap_socket_path, 
         'aedir_etc_openldap':self.testrundir, 
         'openldap_slapd_conf':self._slapd_conf, 
         'openldap_data':self.testrundir, 
         'openldap_rundir':self.testrundir, 
         'aedir_schema_prefix':self._schema_prefix, 
         'openldap_server_id':self.server_id, 
         'hostvars':self._inventory, 
         'aedir_rootdn_uid_number':os.getuid(), 
         'aedir_rootdn_gid_number':os.getgid(), 
         'openldap_path':{'conf_prefix': self.testrundir}})

    def setup_rundir(self):
        """
        creates rundir structure
        """
        SlapdObject.setup_rundir(self)
        self._ln_schema_files(self._inventory_local['openldap_schema_files'], os.path.join(os.environ['AEDIR_ROLE_DIR'], 'files', 'schema'))

    def gen_config--- This code section failed: ---

 L.  92         0  LOAD_GLOBAL              jinja2
                2  LOAD_ATTR                Environment

 L.  93         4  LOAD_GLOBAL              jinja2
                6  LOAD_ATTR                FileSystemLoader
                8  LOAD_FAST                'self'
               10  LOAD_ATTR                _j2_template_dir
               12  LOAD_STR                 'utf-8'
               14  LOAD_CONST               ('encoding',)
               16  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'

 L.  94        18  LOAD_CONST               True

 L.  95        20  LOAD_GLOBAL              jinja2
               22  LOAD_ATTR                StrictUndefined

 L.  96        24  LOAD_CONST               None

 L.  92        26  LOAD_CONST               ('loader', 'trim_blocks', 'undefined', 'autoescape')
               28  CALL_FUNCTION_KW_4     4  '4 total positional and keyword args'
               30  STORE_FAST               'jinja_env'

 L. 100        32  LOAD_FAST                'self'
               34  LOAD_ATTR                testrundir
               36  LOAD_STR                 'rootDSE.ldif'
               38  BUILD_TUPLE_2         2 

 L.  99        40  BUILD_TUPLE_1         1 
               42  GET_ITER         
               44  FOR_ITER            140  'to 140'
               46  UNPACK_SEQUENCE_2     2 
               48  STORE_FAST               'fdir'
               50  STORE_FAST               'fname'

 L. 102        52  LOAD_FAST                'jinja_env'
               54  LOAD_METHOD              get_template
               56  LOAD_FAST                'fname'
               58  LOAD_STR                 '.j2'
               60  BINARY_ADD       
               62  CALL_METHOD_1         1  ''
               64  STORE_FAST               'jinja_template'

 L. 103        66  LOAD_GLOBAL              os
               68  LOAD_ATTR                path
               70  LOAD_METHOD              join
               72  LOAD_FAST                'fdir'
               74  LOAD_FAST                'fname'
               76  CALL_METHOD_2         2  ''
               78  STORE_FAST               'config_filename'

 L. 104        80  LOAD_GLOBAL              logging
               82  LOAD_METHOD              debug
               84  LOAD_STR                 'Write file %s'
               86  LOAD_FAST                'config_filename'
               88  CALL_METHOD_2         2  ''
               90  POP_TOP          

 L. 105        92  LOAD_GLOBAL              open
               94  LOAD_FAST                'config_filename'
               96  LOAD_STR                 'wb'
               98  CALL_FUNCTION_2       2  ''
              100  SETUP_WITH          132  'to 132'
              102  STORE_FAST               'cfile'

 L. 106       104  LOAD_FAST                'cfile'
              106  LOAD_METHOD              write
              108  LOAD_FAST                'jinja_template'
              110  LOAD_METHOD              render
              112  LOAD_FAST                'self'
              114  LOAD_ATTR                _inventory_local
              116  CALL_METHOD_1         1  ''
              118  LOAD_METHOD              encode
              120  LOAD_STR                 'utf-8'
              122  CALL_METHOD_1         1  ''
              124  CALL_METHOD_1         1  ''
              126  POP_TOP          
              128  POP_BLOCK        
              130  BEGIN_FINALLY    
            132_0  COME_FROM_WITH      100  '100'
              132  WITH_CLEANUP_START
              134  WITH_CLEANUP_FINISH
              136  END_FINALLY      
              138  JUMP_BACK            44  'to 44'

 L. 108       140  LOAD_FAST                'jinja_env'
              142  LOAD_METHOD              get_template
              144  LOAD_FAST                'self'
              146  LOAD_ATTR                _openldap_role
              148  LOAD_STR                 '.conf.j2'
              150  BINARY_ADD       
              152  CALL_METHOD_1         1  ''
              154  STORE_FAST               'jinja_template'

 L. 109       156  LOAD_FAST                'jinja_template'
              158  LOAD_METHOD              render
              160  LOAD_FAST                'self'
              162  LOAD_ATTR                _inventory_local
              164  CALL_METHOD_1         1  ''
              166  STORE_FAST               'slapd_conf'

 L. 110       168  LOAD_FAST                'slapd_conf'
              170  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `BEGIN_FINALLY' instruction at offset 130


class AETest(SlapdTestCase):
    """AETest"""
    server_class = AESlapdObject
    ldap_object_class = AEDirObject
    inventory_path = 'tests/single-provider.json'
    j2_template_dir = os.path.join(os.environ['AEDIR_ROLE_DIR'], 'templates', 'slapd')
    init_ldif_files = ('tests/ae-dir-init.ldif', )
    ldap0_trace_level = int(os.environ.get('LDAP0_TRACE_LEVEL', '0'))
    ae_suffix = 'ou=ae-dir'
    maxDiff = 10000

    @classmethod
    def setUpClass--- This code section failed: ---

 L. 133         0  LOAD_GLOBAL              logging
                2  LOAD_METHOD              getLogger
                4  CALL_METHOD_0         0  ''
                6  LOAD_METHOD              setLevel
                8  LOAD_GLOBAL              int
               10  LOAD_GLOBAL              os
               12  LOAD_ATTR                environ
               14  LOAD_METHOD              get
               16  LOAD_STR                 'LOGLEVEL'
               18  LOAD_GLOBAL              str
               20  LOAD_GLOBAL              logging
               22  LOAD_ATTR                WARN
               24  CALL_FUNCTION_1       1  ''
               26  CALL_METHOD_2         2  ''
               28  CALL_FUNCTION_1       1  ''
               30  CALL_METHOD_1         1  ''
               32  POP_TOP          

 L. 135        34  LOAD_GLOBAL              open
               36  LOAD_FAST                'cls'
               38  LOAD_ATTR                inventory_path
               40  LOAD_STR                 'rb'
               42  CALL_FUNCTION_2       2  ''
               44  SETUP_WITH           68  'to 68'
               46  STORE_FAST               'json_file'

 L. 136        48  LOAD_GLOBAL              json
               50  LOAD_METHOD              loads
               52  LOAD_FAST                'json_file'
               54  LOAD_METHOD              read
               56  CALL_METHOD_0         0  ''
               58  CALL_METHOD_1         1  ''
               60  LOAD_FAST                'cls'
               62  STORE_ATTR               inventory
               64  POP_BLOCK        
               66  BEGIN_FINALLY    
             68_0  COME_FROM_WITH       44  '44'
               68  WITH_CLEANUP_START
               70  WITH_CLEANUP_FINISH
               72  END_FINALLY      

 L. 138        74  LOAD_GLOBAL              dict
               76  CALL_FUNCTION_0       0  ''
               78  LOAD_FAST                'cls'
               80  STORE_ATTR               servers

 L. 139        82  LOAD_FAST                'cls'
               84  LOAD_ATTR                j2_template_dir
               86  LOAD_CONST               None
               88  COMPARE_OP               is
               90  POP_JUMP_IF_FALSE   100  'to 100'

 L. 140        92  LOAD_GLOBAL              ValueError
               94  LOAD_STR                 'No directory specified for Jinja2 config templates!'
               96  CALL_FUNCTION_1       1  ''
               98  RAISE_VARARGS_1       1  ''
            100_0  COME_FROM            90  '90'

 L. 141       100  LOAD_GLOBAL              os
              102  LOAD_ATTR                path
              104  LOAD_METHOD              exists
              106  LOAD_FAST                'cls'
              108  LOAD_ATTR                j2_template_dir
              110  CALL_METHOD_1         1  ''
              112  POP_JUMP_IF_TRUE    130  'to 130'

 L. 142       114  LOAD_GLOBAL              ValueError

 L. 143       116  LOAD_STR                 'Jinja2 templates directory %r does not exist!'
              118  LOAD_FAST                'cls'
              120  LOAD_ATTR                j2_template_dir
              122  BUILD_TUPLE_1         1 
              124  BINARY_MODULO    

 L. 142       126  CALL_FUNCTION_1       1  ''
              128  RAISE_VARARGS_1       1  ''
            130_0  COME_FROM           112  '112'

 L. 144       130  LOAD_FAST                'cls'
              132  LOAD_ATTR                inventory
              134  LOAD_METHOD              keys
              136  CALL_METHOD_0         0  ''
              138  GET_ITER         
              140  FOR_ITER            182  'to 182'
              142  STORE_FAST               'inventory_hostname'

 L. 145       144  LOAD_FAST                'cls'
              146  LOAD_METHOD              server_class

 L. 146       148  LOAD_FAST                'inventory_hostname'

 L. 147       150  LOAD_FAST                'cls'
              152  LOAD_ATTR                inventory

 L. 148       154  LOAD_FAST                'cls'
              156  LOAD_ATTR                j2_template_dir

 L. 145       158  CALL_METHOD_3         3  ''
              160  STORE_FAST               'server'

 L. 150       162  LOAD_FAST                'server'
              164  LOAD_METHOD              start
              166  CALL_METHOD_0         0  ''
              168  POP_TOP          

 L. 152       170  LOAD_FAST                'server'
              172  LOAD_FAST                'cls'
              174  LOAD_ATTR                servers
              176  LOAD_FAST                'inventory_hostname'
              178  STORE_SUBSCR     
              180  JUMP_BACK           140  'to 140'

 L. 154       182  LOAD_FAST                'cls'
              184  LOAD_ATTR                init_ldif_files
              186  GET_ITER         
              188  FOR_ITER            230  'to 230'
              190  STORE_FAST               'ldif_filename'

 L. 155       192  LOAD_GLOBAL              list
              194  LOAD_FAST                'cls'
              196  LOAD_ATTR                servers
              198  LOAD_METHOD              values
              200  CALL_METHOD_0         0  ''
              202  CALL_FUNCTION_1       1  ''
              204  LOAD_CONST               0
              206  BINARY_SUBSCR    
              208  LOAD_ATTR                ldapadd

 L. 156       210  LOAD_CONST               None

 L. 158       212  LOAD_STR                 '-e'

 L. 158       214  LOAD_STR                 'relax'

 L. 159       216  LOAD_STR                 '-f'

 L. 159       218  LOAD_FAST                'ldif_filename'

 L. 157       220  BUILD_LIST_4          4 

 L. 155       222  LOAD_CONST               ('extra_args',)
              224  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              226  POP_TOP          
              228  JUMP_BACK           188  'to 188'

 L. 162       230  BUILD_MAP_0           0 
              232  LOAD_FAST                'cls'
              234  STORE_ATTR               _rootdn_conn

 L. 165       236  LOAD_FAST                'cls'
              238  LOAD_ATTR                servers
              240  LOAD_METHOD              items
              242  CALL_METHOD_0         0  ''
              244  GET_ITER         
              246  FOR_ITER            320  'to 320'
              248  UNPACK_SEQUENCE_2     2 
              250  STORE_FAST               'inventory_hostname'
              252  STORE_FAST               'server'

 L. 166       254  LOAD_GLOBAL              logging
              256  LOAD_METHOD              debug
              258  LOAD_STR                 'Open LDAPI connection to %s'
              260  LOAD_FAST                'server'
              262  LOAD_ATTR                ldapi_uri
              264  CALL_METHOD_2         2  ''
              266  POP_TOP          

 L. 167       268  LOAD_FAST                'cls'
              270  LOAD_ATTR                ldap_object_class

 L. 168       272  LOAD_FAST                'server'
              274  LOAD_ATTR                ldapi_uri

 L. 169       276  LOAD_FAST                'cls'
              278  LOAD_ATTR                ldap0_trace_level

 L. 167       280  LOAD_CONST               ('trace_level',)
              282  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              284  LOAD_FAST                'cls'
              286  LOAD_ATTR                _rootdn_conn
              288  LOAD_FAST                'inventory_hostname'
              290  STORE_SUBSCR     

 L. 171       292  LOAD_GLOBAL              logging
              294  LOAD_METHOD              info

 L. 172       296  LOAD_STR                 'Opened LDAPI connection to %s as %s'

 L. 173       298  LOAD_FAST                'server'
              300  LOAD_ATTR                ldapi_uri

 L. 174       302  LOAD_FAST                'cls'
              304  LOAD_ATTR                _rootdn_conn
              306  LOAD_FAST                'inventory_hostname'
              308  BINARY_SUBSCR    
              310  LOAD_METHOD              whoami_s
              312  CALL_METHOD_0         0  ''

 L. 171       314  CALL_METHOD_3         3  ''
              316  POP_TOP          
              318  JUMP_BACK           246  'to 246'

Parse error at or near `BEGIN_FINALLY' instruction at offset 66

    def setUp(self):
        pass

    def _get_conn(self, inventory_hostname=None, who=None, cred=None, cacert_filename=None, client_cert_filename=None, client_key_filename=None, cache_ttl=0.0, sasl_authz_id=''):
        if inventory_hostname:
            server = self.servers[inventory_hostname]
        else:
            server = list(self.servers.values())[0]
        aedir_conn = self.ldap_object_class((server.ldapi_uri),
          trace_level=(self.ldap0_trace_level),
          who=who,
          cred=cred,
          cacert_filename=cacert_filename,
          client_cert_filename=client_cert_filename,
          client_key_filename=client_key_filename,
          cache_ttl=cache_ttl,
          sasl_authz_id=sasl_authz_id)
        return aedir_conn

    @classmethod
    def tearDownClass(cls):
        for server in cls.servers.values():
            server.stop()