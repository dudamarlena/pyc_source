# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_essentials/osm_postgis_transform.py
# Compiled at: 2014-12-29 20:55:33
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
import subprocess as sp, os, time, argparse, sys, shutil, python_essentials, python_essentials.lib, python_essentials.lib.pm_utils as pm_utils, python_essentials.lib.check_os as check_os, python_essentials.lib.postgis_utils as postgis_utils, python_essentials.lib.os_utils as os_utils
try:
    import pexpect, plac
except ImportError as ex:
    logger.error('import of one of the modules %s failed. Did you run the osm_postgis_transform_prequisites.py scripts?' % ['pexpect', 'plac'])

pg_version = (9, 2)
pg_version_string = str.join('.', [ str(i) for i in pg_version ])
postgis_version = (2, 0)
postgis_version_string = str.join('.', [ str(i) for i in postgis_version ])
initdb = '/usr/lib/postgresql/%s/bin/initdb' % pg_version_string
postgres = '/usr/lib/postgresql/%s/bin/postgres' % pg_version_string
psql = '/usr/lib/postgresql/%s/bin/psql' % pg_version_string
createdb = '/usr/lib/postgresql/%s/bin/createdb' % pg_version_string
osm2pgsql_number_processes = int(sp.check_output(['grep', '-c', '^processor', '/proc/cpuinfo']).strip())
db_socket_dir = '/tmp'
start_db_default = False
db_host_default = 'localhost'
db_port_default = 5204
db_user_default = 'postgis'
db_password_default = 'postgis'
db_name_default = 'postgis'
osm2pgsql_default = 'osm2pgsql'
data_dir_default = os.path.join(os.environ['HOME'], 'osm_postgis_db-9.2')
cache_size_default = 1000
postgres_server_start_timeout = 5

def a_list(arg):
    return arg.split(',')


@plac.annotations(osm_files=(
 'a comma (`,`) separated list of OSM files to be passed to osm2pgsql (gunzipped files are accepted if osm2pgsql accepts them (the version installed by osm_postgis_transform_prequisites does))', 'positional', None, a_list), skip_start_db=('Specify this flag in order to feed the data to an already running postgres process which the script will attempt to connect to with the parameters specified by `db-host`, `db-port`, `db-user`, `db-password` and `db-name` arguments.',
                                                                                                                                                                                                                                               'flag'), data_dir=("The directory which contains or will contain the data of the PostGIS database (see documentation of `-D` option in `man initdb` for further details). The directory will be created if it doesn't exist. If a file is passed as argument, the script will fail argument validation. The script will fail if the directory is an invalid PostGIS data directory (e.g. one which allows partial start of a `postgres` process but contains invalid permissions or misses files). As soon as a non-empty directory is passed as argument, it is expected to be a valid PostGIS data directory! If the script fails due to an unexpected error, YOU have to take care of cleaning that directory from anything besides the stuff inside before the script has been invoked!",
                                                                                                                                                                                                                                                                  'option'), db_host=("The host where the nested database process should run (has to be specified if default value isn't reachable) or the host where to reach the already running postgres process (see --start-db for details)",
                                                                                                                                                                                                                                                                                      'option'), db_port=('The port where the nested database process will be listening (has to be specified if the port denoted by the default value is occupied) or the port where to reach the already running postgres process (see --start-db for details)',
                                                                                                                                                                                                                                                                                                          'option'), db_user=("name of user to use for authentication at the database (will be created if database doesn't exist) (see --start-db for details)",
                                                                                                                                                                                                                                                                                                                              'option'), db_password=("password for the user specified with `--db-user` argument to use for authentication at the database (will be set up if database doesn't exist) (see --start-db for details)",
                                                                                                                                                                                                                                                                                                                                                      'option'), db_name=('name of the database to connect to or to be created (see --start-db for details)',
                                                                                                                                                                                                                                                                                                                                                                          'option'), cache_size=('size of osm2pgsql cache (see `--cache` option of `man osm2pgsql`)',
                                                                                                                                                                                                                                                                                                                                                                                                 'option'), osm2pgsql=('optional path to a osm2pgsql binary',
                                                                                                                                                                                                                                                                                                                                                                                                                       'option'))
def osm_postgis_transform(osm_files, skip_start_db, data_dir=data_dir_default, db_host=db_host_default, db_port=db_port_default, db_user=db_user_default, db_password=db_password_default, db_name=db_name_default, cache_size=cache_size_default, osm2pgsql=osm2pgsql_default):
    """
    This script sets up PostGIS database with data from an OSM (.osm) file. It 
    is essentially a wrapper around `osm2pgsql`. By default it will either spawn a database process based on the data directory speified with the `--data-dir` argument (if the data directory is non-empty) or create a database data directory and spawn a database process based on that newly created data directory and feed data to it. If the nested database process can't be connected to with the default value for database connection parameters, they have to be overwritten, otherwise the script will fail with the error message of the `postgres` process.
    
    The start of a nested database process can be skipped if `--skip-start-db` command line flag is set. In this case the database connection parameters will be used to connect to an external already running `postgres` process where data will be fed to.
    
    WARNING: The script has not yet been tested completely to hide database credentials (including the password) from output and/or other logging backends (files, syslog, etc.). It is currently recommended to specify a separate database and local host for the script only and to not care about it at all (as OSM data is as far from a secret as it could be).
    """
    if osm_files is None:
        raise ValueError("osm_files mustn't be None")
    if str(type(osm_files)) != "<type 'list'>":
        raise ValueError('osm_files has to be a list')
    if len(osm_files) == 0:
        raise ValueError("osm_files mustn't be empty")
    if pg_version == (9, 2):
        if postgis_version > (2, 0):
            raise ValueError('postgis > %s is not compatible with postgresql %s' % (postgis_version_string, pg_version_string))
    if data_dir is None:
        raise ValueError("data_dir mustn't be None")
    if os.path.exists(data_dir) and not os.path.isdir(data_dir):
        raise ValueError("data_dir '%s' exists, but isn't a directory" % (data_dir,))
    if os_utils.which(osm2pgsql) is None:
        raise RuntimeError('osm2pgsql not found, make sure you have invoked osm_postgis_transform_prequisites.py')
    postgres_proc = None
    try:
        try:
            if not skip_start_db:
                if not os.path.exists(data_dir) or len(os.listdir(data_dir)) == 0:
                    logger.info("creating PostGIS data directory in data_dir '%s'" % (data_dir,))
                    if not os.path.exists(data_dir):
                        logger.info("creating inexisting data_dir '%s'" % (data_dir,))
                        os.makedirs(data_dir)
                    postgis_utils.bootstrap_datadir(data_dir, db_user, password=db_password, initdb=initdb)
                    postgis_utils.bootstrap_database(data_dir, db_port, db_host, db_user, db_name, password=db_password, initdb=initdb, postgres=postgres, createdb=createdb, psql=psql, socket_dir=db_socket_dir)
                if postgres_proc is None:
                    logger.info("spawning database process based on existing data directory '%s'" % (data_dir,))
                    postgres_proc = pexpect.spawn(str.join(' ', [postgres, '-D', data_dir, '-p', str(db_port), '-h', db_host, '-k', db_socket_dir]))
                    postgres_proc.logfile = sys.stdout
                    logger.info('sleeping %s s to ensure postgres server started' % postgres_server_start_timeout)
                    time.sleep(postgres_server_start_timeout)
            logger.debug('using osm2pgsql binary %s' % osm2pgsql)
            osm2pgsql_proc = pexpect.spawn(str.join(' ', [osm2pgsql, '--create', '--database', db_name, '--cache', str(cache_size), '--number-processes', str(osm2pgsql_number_processes), '--slim', '--port', str(db_port), '--host', db_host, '--username', db_user, '--latlong', '--password', '--keep-coastlines', '--extra-attributes', '--hstore-all'] + osm_files))
            osm2pgsql_proc.logfile = sys.stdout
            osm2pgsql_proc.expect(['Password:', 'Passwort:'])
            osm2pgsql_proc.sendline(db_password)
            osm2pgsql_proc.timeout = 100000000
            osm2pgsql_proc.expect(pexpect.EOF)
        except Exception as ex:
            logger.error(ex)

    finally:
        if postgres_proc is not None:
            postgres_proc.terminate()

    return


if __name__ == '__main__':
    plac.call(osm_postgis_transform)