# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_essentials/lib/postgis_utils.py
# Compiled at: 2014-12-28 23:07:37
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
import subprocess as sp, os, time
EXTENSION_INSTALL_EXTENSION = 1
EXTENSION_INSTALL_SQL_FILE = 2
EXTENSION_INSTALLS = [EXTENSION_INSTALL_EXTENSION, EXTENSION_INSTALL_SQL_FILE]
extension_install_default = EXTENSION_INSTALLS[0]
pwfile_path = './pwfile'
authmethod = 'md5'
postgres_server_start_timeout = 5
postgres_server_stop_timeout = postgres_server_start_timeout

def bootstrap_datadir(datadir_path, db_user, password='somepw', initdb='initdb'):
    pwfile = open(pwfile_path, 'w')
    pwfile.write(password)
    pwfile.flush()
    pwfile.close()
    sp.check_call([initdb, '-D', datadir_path, '--username=%s' % db_user, '--pwfile=%s' % pwfile_path,
     '--auth=%s' % authmethod])
    os.remove(pwfile_path)


def __pe_wrapper__(cmds, password):
    psql_proc = pe.spawn(str.join(' ', cmds))
    psql_proc.logfile = sys.stdout
    psql_proc.expect(['Password', 'Passwort', 'postgis'])
    psql_proc.sendline(password)
    psql_proc.wait()


def bootstrap_database(datadir_path, db_port, db_host, db_user, db_name, password='somepw', initdb='initdb', postgres='postgres', createdb='createdb', psql='psql', socket_dir='/tmp', extension_install=extension_install_default):
    if extension_install not in EXTENSION_INSTALLS:
        raise ValueError('extension_install has to be one of %s' % str(EXTENSION_INSTALLS))
    pg_hba_conf_file_path = os.path.join(datadir_path, 'pg_hba.conf')
    file_utils.append_file(pg_hba_conf_file_path, '\nhost all %s 0.0.0.0 0.0.0.0 %s\n' % (db_user, authmethod))
    postgres_process = sp.Popen([postgres, '-D', datadir_path, '-p', str(db_port), '-h', db_host, '-k', socket_dir])
    try:
        logger.info('sleeping %s s to ensure postgres server started' % postgres_server_start_timeout)
        time.sleep(postgres_server_start_timeout)
        __pe_wrapper__([createdb, '-p', str(db_port), '-h', db_host, '--username=%s' % db_user, db_name], password)
        __pe_wrapper__([psql, '-c', '"grant all on database %s to %s;"' % (db_name, db_user), '-p', str(db_port), '-h', db_host, '--username=%s' % db_user], password)
        if extension_install == EXTENSION_INSTALL_EXTENSION:
            __pe_wrapper__([psql, '-d', db_name, '-c', '"create extension postgis; create extension postgis_topology;"', '-p', str(db_port), '-h', db_host, '--username=%s' % db_user], password)
        elif extension_install == EXTENSION_INSTALL_SQL_FILE:
            __pe_wrapper__([psql, '-d', db_name, '-f', '/usr/share/postgresql/%s/contrib/postgis-%s/postgis.sql' % (pg_version, postgis_version_string), '-p', str(db_port), '-h', db_host, '--username=%s' % db_user, '-v', 'ON_ERROR_STOP=1'], password)
            __pe_wrapper__([psql, '-d', db_name, '-f', '/usr/share/postgresql/%s/contrib/postgis-%s/topology.sql' % (pg_version, postgis_version_string), '-p', str(db_port), '-h', db_host, '--username=%s' % db_user, '-v', 'ON_ERROR_STOP=1'], password)
            __pe_wrapper__([psql, '-d', db_name, '-f', '/usr/share/postgresql/%s/contrib/postgis-%s/spatial_ref_sys.sql' % (pg_version, postgis_version_string), '-p', str(db_port), '-h', db_host, '--username=%s' % db_user, '-v', 'ON_ERROR_STOP=1'], password)
        __pe_wrapper__([psql, '-d', db_name, '-c', '"create extension hstore;"', '-p', str(db_port), '-h', db_host, '--username=%s' % db_user, '-v', 'ON_ERROR_STOP=1'], password)
        __pe_wrapper__([psql, '-c', '"ALTER USER %s WITH PASSWORD \'%s\';"' % (db_user, password), '-p', str(db_port), '-h', db_host, '--username=%s' % db_user], password)
    finally:
        postgres_process.terminate()
        logger.info('sleeping %s s to ensure postgres server stopped' % postgres_server_stop_timeout)
        time.sleep(postgres_server_stop_timeout)