# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nori/dbms/postgresql.py
# Compiled at: 2013-12-09 14:54:12
"""
This is the PostgreSQL submodule for the nori library; see __main__.py
for license and usage information.

DOCSTRING CONTENTS:
-------------------

    1) About and Requirements
    2) API Classes

1) ABOUT AND REQUIREMENTS:
--------------------------

    This submodule provides PostgreSQL connectivity.  It requires the
    Psycopg2 package.  If the package is not available, the module will
    load, but PostgreSQL connectivity will not be available.

2) API CLASSES:
---------------

    PostgreSQL(DBMS)
        This class adapts the DBMS functionality to PostgreSQL.

        Startup and Config File Processing
        ----------------------------------

        apply_config_defaults_extra()
            Apply configuration defaults that are
            last-minute/complicated.

        DBAPI 2.0 Cursor/Connection Methods
        -----------------------------------

        nextset() is not supported.

        setoutputsize() is not supported.

        Nori Extensions
        ---------------

        change_db() is not supported.

"""
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from pprint import pprint as pp
import sys, os, copy
try:
    import psycopg2, psycopg2.extensions
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
    psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)
except ImportError:
    pass

from .. import core
from .dbms import DBMS
core.supported_features['dbms.postgresql'] = 'PostgreSQL support'
if 'psycopg2' in sys.modules:
    core.available_features.append('dbms.postgresql')

class PostgreSQL(DBMS):
    """This class adapts the DBMS functionality to PostgreSQL."""
    DBMS_NAME = 'PostgreSQL'
    REQUIRES = DBMS.REQUIRES + ['dbms.postgresql']
    MODULE = psycopg2
    DEFAULT_LOCAL_PORT = 6432
    DEFAULT_REMOTE_PORT = 5432
    SOCKET_SEARCH_PATH = [
     '/tmp', '/var/run/postgresql', '/var/run']
    _SUPPORTED = copy.copy(DBMS._SUPPORTED)

    def create_settings(self, heading='', extra_text='', ignore=None, extra_requires=[], tunnel=True if 'ssh' in core.available_features else False):
        """
        Add a block of DBMS config settings to the script.

        Parameters:
            see DBMS.create_settings()

        Dependencies:
            class vars: DBMS_NAME, DEFAULT_REMOTE_PORT
            instance vars: _prefix, _delim
            methods: settings_extra_text(),
                     apply_config_defaults_extra()
            config settings: [_prefix+_delim+:] use_ssh_tunnel,
                             protocol, host, port, socket_file,
                             connect_db
            modules: os, core, dbms.DBMS

        """
        DBMS.create_settings(self, heading, extra_text, ignore, extra_requires, tunnel)
        pd = self._prefix + self._delim
        if tunnel:
            core.config_settings[(pd + 'use_ssh_tunnel')]['descr'] = ("\nUse an SSH tunnel for the {0} connection (True/False)?\n\nIf True, specify the host in {1}ssh_host and the port in\n{1}remote_port instead of {1}host and\n{1}port.\n\nNote: to use {0}'s SSL support, you will need to add the\nnecessary options to {1}connect_options:\n    sslmode\n    sslcompression\n    sslcert\n    sslkey\n    sslrootcert\n    sslcrl\nSee the {0} documentation for more information.\n").format(self.DBMS_NAME, pd)
        del core.config_settings[pd + 'protocol']
        core.config_settings[(pd + 'host')]['descr'] = (("\nHostname or socket directory for the {0} connection.\n\nIf this doesn't start with '/', it will be treated as a remote hostname\nto connect to via TCP.\n\nIf it does start with '/', it will be treated as the directory containing\nthe Unix socket file.  The file used will be 'HOST/.s.PGSQL.PORT', where\nHOST and PORT are the given settings.\n\nNote: there is apparently no way, with {0}, to specify a\nrelative directory or the full name of the socket file, or to use\nanything other than a port number as the suffix.\n").format(self.DBMS_NAME, pd) if os.name == 'posix' else ('\nHostname for the {0} connection.\n').format(self.DBMS_NAME, pd)) + (('\nIgnored if {0}use_ssh_tunnel is True.').format(pd) if tunnel else '')
        core.config_settings[(pd + 'port')]['descr'] = ('\nPort number for the {0} connection.\n\nUsed for both TCP and socket connections; see {1}host.\n').format(self.DBMS_NAME, pd) + (('\nIgnored if {0}use_ssh_tunnel is True.').format(pd) if tunnel else '')
        core.config_settings[(pd + 'port')]['default'] = self.DEFAULT_REMOTE_PORT
        del core.config_settings[pd + 'socket_file']
        core.config_settings[(pd + 'connect_db')]['descr'] = ("\nInitial database for the {0} connection.\n\n{0} requires a database to connect to even for commands that\ndon't use any (such as getting the list of databases).\n").format(self.DBMS_NAME)
        core.config_settings[(pd + 'connect_db')]['default'] = 'postgres'
        if extra_text:
            setting_list = [
             'host', 'port', 'connect_db']
            if tunnel:
                setting_list += ['use_ssh_tunnel']
            self.settings_extra_text(setting_list, extra_text)
        core.apply_config_defaults_hooks.append(self.apply_config_defaults_extra)

    def apply_config_defaults_extra(self):
        """
        Apply configuration defaults that are last-minute/complicated.

        Dependencies:
            class vars: SOCKET_SEARCH_PATH
            instance vars: _prefix, _delim
            config settings: [_prefix+_delim+:] host, port, remote_port
            modules: os, core

        """
        pd = self._prefix + self._delim
        found_socket = False
        if os.name == 'posix':
            for d in self.SOCKET_SEARCH_PATH:
                f = d + '/.s.PGSQL.' + str(core.cfg[(pd + 'port')])
                if core.check_file_type(f, 'PostgreSQL socket', type_char='s', follow_links=True, must_exist=True, use_logger=None, warn_only=True) and core.check_file_access(f, 'PostgreSQL socket', file_rwx='rw', use_logger=None, warn_only=True):
                    core.config_settings[(pd + 'host')]['default'] = f
                    found_socket = True
                    break

        if not found_socket:
            core.config_settings[(pd + 'host')]['default'] = '127.0.0.1'
        for s_name in [pd + 'port', pd + 'remote_port']:
            if s_name in core.config_settings and core.config_settings[s_name]['default'] == 5432:
                core.config_settings[s_name]['default_descr'] = '5432 (the standard port)'

        return

    def validate_config(self):
        """
        Validate DBMS config settings.
        Only does checks that aren't done in DBMS.validate_config().
        Dependencies:
            instance vars: _ignore, _prefix, _delim, _tunnel_config
            config settings: [_prefix+_delim+:] use_ssh_tunnel, host,
                             port, connect_db
            modules: core, dbms.DBMS
            Python: 2.0/3.2, for callable()
        """
        if callable(self._ignore) and self._ignore():
            return
        pd = self._prefix + self._delim
        if not self._tunnel_config or not core.cfg[(pd + 'use_ssh_tunnel')]:
            core.setting_check_not_blank(pd + 'host')
            if core.cfg[(pd + 'host')][0] == '/':
                core.setting_check_dir_search(pd + 'host')
            core.setting_check_is_set(pd + 'port')
        core.setting_check_is_set(pd + 'connect_db')
        DBMS.validate_config(self)

    _SUPPORTED.remove('nextset')
    _SUPPORTED.remove('setoutputsize')

    def _autocommit(self, what=None):
        """
        Get or set the built-in autocommit status of a DBMS connection.
        If what is True or False, returns True on success, False on
        error.  If what is None, returns True/False, or None on error.
        This internal method handles (only) the DBMS's autocommit
        functionality.
        Parameters:
            what: if True, turn autocommit on; if False, turn it off;
                  if None, return the current status
        Dependencies:
            instance vars: conn
            modules: (conn's module)
        """
        if what is None:
            return self.conn.autocommit
        else:
            self.conn.autocommit = what
            return True

    def get_db_list(self, cur):
        """
        Get the list of databases from a DBMS.
        Returns a tuple: (success?, fetched_rows)
        Parameters:
            cur: the cursor to use; if None, the main cursor is used
        Dependencies:
            methods: execute(), fetchall()
        """
        if not self.execute(cur, 'SELECT datname FROM pg_catalog.pg_database;', has_results=True):
            return (False, None)
        else:
            return self.fetchall(cur)

    _SUPPORTED.remove('change_db')

    def get_table_list(self, cur):
        """
        Get the list of tables in the current database.
        Returns a tuple: (success?, fetched_rows)
        Parameters:
            cur: the cursor to use; if None, the main cursor is used
        Dependencies:
            methods: execute(), fetchall()
        """
        if not self.execute(cur, "\nSELECT table_name\nFROM information_schema.tables\nWHERE table_schema='public'\nAND table_type='BASE TABLE';\n", has_results=True):
            return (False, None)
        else:
            return self.fetchall(cur)

    def get_last_id(self, cur):
        """
        Get the last auto-increment ID inserted into the database.
        Returns a tuple: (success?, last_id)
        Parameters:
            cur: the cursor to use; if None, the main cursor is used
        Dependencies:
            methods: execute(), fetchall()
        """
        if not self.execute(cur, 'SELECT lastval();', has_results=True):
            return (False, None)
        else:
            ret = self.fetchall(cur)
            return (ret[0], ret[1][0][0] if ret[0] else None)