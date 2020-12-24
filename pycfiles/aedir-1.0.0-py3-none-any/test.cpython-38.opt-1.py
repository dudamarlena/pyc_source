# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /aedir/test.py
# Compiled at: 2020-02-17 13:24:16
# Size of source mod 2**32: 6893 bytes
"""
aedir.test - base classes for unit tests
"""
import json, logging, os, jinja2
from ldap0.test import SlapdObject, SlapdTestCase
from aedir import AEDirObject
__all__ = [
 'AESlapdObject',
 'AETest']

class AESlapdObject(SlapdObject):
    __doc__ = '\n    run AE-DIR test slapd process\n    '
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

    def gen_config(self):
        """
        generates a slapd.conf based on Jinja2 template
        and returns it as one string
        """
        jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader((self._j2_template_dir), encoding='utf-8'),
          trim_blocks=True,
          undefined=(jinja2.StrictUndefined),
          autoescape=None)
        for fdir, fname in (
         (
          self.testrundir, 'rootDSE.ldif'),):
            jinja_template = jinja_env.get_template(fname + '.j2')
            config_filename = os.path.join(fdir, fname)
            logging.debug('Write file %s', config_filename)
            with open(config_filename, 'wb') as (cfile):
                cfile.write(jinja_template.render(self._inventory_local).encode('utf-8'))
        else:
            jinja_template = jinja_env.get_template(self._openldap_role + '.conf.j2')
            slapd_conf = jinja_template.render(self._inventory_local)
            return slapd_conf


class AETest(SlapdTestCase):
    __doc__ = '\n    test class which initializes an AE-DIR slapd\n    '
    server_class = AESlapdObject
    ldap_object_class = AEDirObject
    inventory_path = 'tests/single-provider.json'
    j2_template_dir = os.path.join(os.environ['AEDIR_ROLE_DIR'], 'templates', 'slapd')
    init_ldif_files = ('tests/ae-dir-init.ldif', )
    ldap0_trace_level = int(os.environ.get('LDAP0_TRACE_LEVEL', '0'))
    ae_suffix = 'ou=ae-dir'
    maxDiff = 10000

    @classmethod
    def setUpClass(cls):
        logging.getLogger().setLevel(int(os.environ.get('LOGLEVEL', str(logging.WARN))))
        with open(cls.inventory_path, 'rb') as (json_file):
            cls.inventory = json.loads(json_file.read())
        cls.servers = dict()
        if cls.j2_template_dir is None:
            raise ValueError('No directory specified for Jinja2 config templates!')
        if not os.path.exists(cls.j2_template_dir):
            raise ValueError('Jinja2 templates directory %r does not exist!' % (cls.j2_template_dir,))
        for inventory_hostname in cls.inventory.keys():
            server = cls.server_class(inventory_hostname, cls.inventory, cls.j2_template_dir)
            server.start()
            cls.servers[inventory_hostname] = server
        else:
            for ldif_filename in cls.init_ldif_files:
                list(cls.servers.values())[0].ldapadd(None,
                  extra_args=[
                 '-e', 'relax',
                 '-f', ldif_filename])
            else:
                cls._rootdn_conn = {}
                for inventory_hostname, server in cls.servers.items():
                    logging.debug('Open LDAPI connection to %s', server.ldapi_uri)
                    cls._rootdn_conn[inventory_hostname] = cls.ldap_object_class((server.ldapi_uri),
                      trace_level=(cls.ldap0_trace_level))
                    logging.info('Opened LDAPI connection to %s as %s', server.ldapi_uri, cls._rootdn_conn[inventory_hostname].whoami_s())

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