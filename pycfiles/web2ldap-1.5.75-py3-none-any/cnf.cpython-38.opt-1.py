# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/cnf.py
# Compiled at: 2020-05-04 07:52:03
# Size of source mod 2**32: 7143 bytes
"""
web2ldap.app.cnf: read configuration data

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import logging
from ldap0.ldapurl import LDAPUrl, is_ldapurl
from ldap0.dn import is_dn
from web2ldap.log import logger, LogHelper
VALID_CFG_PARAM_NAMES = {'addform_entry_templates':dict, 
 'addform_parent_attrs':tuple, 
 'binddn_mapping':str, 
 'boundas_template':dict, 
 'bulkmod_delold':bool, 
 'description':str, 
 'dit_max_levels':int, 
 'dit_search_sizelimit':int, 
 'dit_search_timelimit':int, 
 'groupadm_defs':dict, 
 'groupadm_filterstr_template':str, 
 'groupadm_optgroup_bounds':tuple, 
 'inputform_supentrytemplate':dict, 
 'input_template':dict, 
 'login_template':str, 
 'modify_constant_attrs':tuple, 
 'naming_contexts':tuple, 
 'passwd_genchars':str, 
 'passwd_genlength':int, 
 'passwd_hashtypes':tuple, 
 'passwd_modlist':tuple, 
 'passwd_template':str, 
 'print_cols':int, 
 'print_template':dict, 
 'read_tablemaxcount':dict, 
 'read_template':dict, 
 'rename_supsearchurl':dict, 
 'rename_template':str, 
 'requested_attrs':tuple, 
 '_schema':None, 
 'schema_supplement':str, 
 'schema_strictcheck':int, 
 'schema_uri':str, 
 'search_attrs':tuple, 
 'searchform_search_root_url':str, 
 'searchform_template':dict, 
 'searchoptions_template':str, 
 'search_resultsperpage':int, 
 'search_tdtemplate':dict, 
 'session_track_control':bool, 
 'starttls':int, 
 'supplement_schema':str, 
 'timeout':int, 
 'tls_options':dict, 
 'top_template':str, 
 'vcard_template':dict}

class Web2LDAPConfig(LogHelper):
    __doc__ = '\n    Base class for a web2ldap host-/backend configuration section.\n    '
    __slots__ = VALID_CFG_PARAM_NAMES.keys()

    def __init__(self, **params):
        self.update(params)

    def update(self, params):
        """
        sets params as class attributes
        """
        for param_name, param_val in params.items():
            try:
                param_type = VALID_CFG_PARAM_NAMES[param_name]
            except KeyError:
                raise ValueError('Invalid config parameter %r.' % param_name)
            else:
                if param_type is not None:
                    if not isinstance(param_val, param_type):
                        raise TypeError('Invalid type for config parameter %r. Expected %r, got %r' % (
                         param_name,
                         param_type,
                         param_val))
                setattr(self, param_name, param_val)

    def clone--- This code section failed: ---

 L. 107         0  LOAD_CLOSURE             'self'
                2  BUILD_TUPLE_1         1 
                4  LOAD_DICTCOMP            '<code_object <dictcomp>>'
                6  LOAD_STR                 'Web2LDAPConfig.clone.<locals>.<dictcomp>'
                8  MAKE_FUNCTION_8          'closure'

 L. 109        10  LOAD_GLOBAL              VALID_CFG_PARAM_NAMES

 L. 107        12  GET_ITER         
               14  CALL_FUNCTION_1       1  ''
               16  STORE_FAST               'old_params'

 L. 112        18  LOAD_GLOBAL              Web2LDAPConfig
               20  BUILD_TUPLE_0         0 
               22  LOAD_FAST                'old_params'
               24  CALL_FUNCTION_EX_KW     1  'keyword and positional arguments'
               26  STORE_FAST               'new'

 L. 113        28  LOAD_FAST                'new'
               30  LOAD_METHOD              update
               32  LOAD_FAST                'params'
               34  CALL_METHOD_1         1  ''
               36  POP_TOP          

 L. 114        38  LOAD_DEREF               'self'
               40  LOAD_METHOD              log

 L. 115        42  LOAD_GLOBAL              logging
               44  LOAD_ATTR                DEBUG

 L. 116        46  LOAD_STR                 'Cloned config %s with %d parameters to %s with %d new params %s'

 L. 117        48  LOAD_GLOBAL              id
               50  LOAD_DEREF               'self'
               52  CALL_FUNCTION_1       1  ''

 L. 118        54  LOAD_GLOBAL              len
               56  LOAD_FAST                'old_params'
               58  CALL_FUNCTION_1       1  ''

 L. 119        60  LOAD_GLOBAL              id
               62  LOAD_FAST                'new'
               64  CALL_FUNCTION_1       1  ''

 L. 120        66  LOAD_GLOBAL              len
               68  LOAD_FAST                'params'
               70  CALL_FUNCTION_1       1  ''

 L. 121        72  LOAD_FAST                'params'

 L. 114        74  CALL_METHOD_7         7  ''
               76  POP_TOP          

 L. 123        78  LOAD_FAST                'new'
               80  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `None' instruction at offset -1


import web2ldapcnf.hosts, web2ldap.app.schema

class Web2LDAPConfigDict(LogHelper):
    __doc__ = '\n    the configuration registry for site-specific parameters\n    '
    __slots__ = ('cfg_data', )

    def __init__(self, cfg_dict):
        self.cfg_data = {}
        for key, val in cfg_dict.items():
            self.set_cfg(key, val)

    @staticmethod
    def normalize_key(key):
        """
        Returns a normalized string for an LDAP URL
        """
        if key == '_':
            return '_'
            if isinstance(key, str):
                if is_ldapurl(key):
                    key = LDAPUrl(key)
        elif is_dn(key):
            key = LDAPUrl(dn=(key.lower()))
        assert isinstance(key, LDAPUrl), TypeError("Expected LDAPUrl in 'key', was %r" % key)
        key.attrs = None
        key.filterstr = None
        key.scope = None
        key.extensions = None
        try:
            host, port = key.hostport.split(':')
        except ValueError:
            pass
        else:
            if key.urlscheme == 'ldap':
                if port == '389' or key.urlscheme == 'ldaps':
                    if port == '636':
                        key.hostport = host

    def set_cfg(self, cfg_uri, cfg_data):
        """
        store config data in internal dictionary
        """
        cfg_key = self.normalize_key(cfg_uri)
        self.log(logging.DEBUG, 'Store config for %r with key %r', cfg_uri, cfg_key)
        self.cfg_data[cfg_key] = cfg_data

    def get_param(self, uri, naming_context, param, default):
        """
        retrieve a site-specific config parameter
        """
        if param not in VALID_CFG_PARAM_NAMES:
            self.log(logging.ERROR, 'Unknown config parameter %r requested', param)
            raise ValueError('Unknown config parameter %r requested' % param)
        uri = uri.lower()
        naming_context = str(naming_context).lower()
        result = default
        for cfg_key in (
         (
          uri, naming_context),
         (
          'ldap://', naming_context),
         (
          uri, ''),
         '_'):
            if cfg_key in self.cfg_data and hasattr(self.cfg_data[cfg_key], param):
                result = getattr(self.cfg_data[cfg_key], param)
                self.log(logging.DEBUG, 'get_param(%r, %r, %r, %r): Key %r -> %s', uri, naming_context, param, default, cfg_key, result)
                break
            return result


logger.debug('Initialize ldap_def')
LDAP_DEF = Web2LDAPConfigDict(web2ldapcnf.hosts.ldap_def)
web2ldap.app.schema.parse_fake_schema(LDAP_DEF)

def set_target_check_dict(ldap_uri_list):
    """
    generate a dictionary of known target servers
    with the string of the LDAP URI used as key
    """
    ldap_uri_list_check_dict = {}
    for ldap_uri in ldap_uri_list:
        try:
            ldap_uri, desc = ldap_uri
        except ValueError:
            pass
        else:
            lu_obj = LDAPUrl(ldap_uri)
            ldap_uri_list_check_dict[lu_obj.connect_uri()] = None
            logger.debug('Added target LDAP URI %s / %r', ldap_uri, desc)
    else:
        return ldap_uri_list_check_dict


LDAP_URI_LIST_CHECK_DICT = set_target_check_dict(web2ldapcnf.hosts.ldap_uri_list)