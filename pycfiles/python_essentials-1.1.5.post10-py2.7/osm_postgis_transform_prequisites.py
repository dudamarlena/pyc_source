# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/python_essentials/osm_postgis_transform_prequisites.py
# Compiled at: 2014-12-29 19:37:18
import sys, os, subprocess as sp, logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
logger.addHandler(ch)
import python_essentials, python_essentials.lib, python_essentials.lib.pm_utils as pm_utils, python_essentials.lib.check_os as check_os, python_essentials.lib.postgis_utils as postgis_utils, python_essentials.lib.os_utils as os_utils, plac
postgis_src_dir_name = 'postgis-2.1.1'
postgis_url_default = 'http://download.osgeo.org/postgis/source/postgis-2.1.1.tar.gz'
postgis_src_archive_name = 'postgis-2.1.1.tar.gz'
postgis_src_archive_md5 = '4af86a39e2e9dbf10fe894e03c2c7027'
postgis_jdbc_name = 'postgis-jdbc-2.1.0SVN.jar'

@plac.annotations(skip_database_installation=('whether to skip installation ofpostgresql and postgis related prequisites',
                                              'flag'), skip_apt_update=('whether (possibly time consuming) invokation of apt-get update ought to be skipped (if have reason to be sure that your apt sources are quite up-to-date, e.g. if you invoked apt-get 5 minutes ago',
                                                                        'flag'), postgis_url=('The URL where the postgis tarball ought to be retrieved',
                                                                                              'option'))
def install_prequisites(skip_database_installation, skip_apt_update, postgis_url=postgis_url_default):
    if check_os.check_ubuntu() or check_os.check_debian():
        if skip_database_installation:
            pm_utils.install_packages(['osm2pgsql'], package_manager='apt-get', skip_apt_update=skip_apt_update, assume_yes=False)
        else:
            release_tuple = check_os.findout_release_ubuntu_tuple()
            install_postgresql(skip_apt_update=skip_apt_update)
    elif skip_database_installation:
        raise RuntimeError('implement simple installation of only prequisite osm2pgsql')
    else:
        install_postgresql(skip_apt_update=skip_apt_update)


def install_postgresql(skip_apt_update, pg_version=(9, 2)):
    if check_os.check_ubuntu() or check_os.check_debian() or check_os.check_linuxmint():
        if check_os.check_ubuntu() or check_os.check_debian():
            if check_os.check_ubuntu():
                release_tuple = check_os.findout_release_ubuntu_tuple()
                if release_tuple > (12, 4) and release_tuple < (13, 10):
                    release = 'precise'
                else:
                    release = check_os.findout_release_ubuntu()
            elif check_os.check_debian():
                release = check_os.findout_release_debian()
            elif check_os.check_linuxmint():
                release = check_os.findout_release_linuxmint()
                if release < 17:
                    raise RuntimeError("linuxmint releases < 17 aren't supported")
            else:
                raise RuntimeError('operating system not supported')
            apt_url = 'http://apt.postgresql.org/pub/repos/apt/'
            distribution = '%s-pgdg' % release
            component = 'main'
            if not pm_utils.check_apt_source_line_added(uri=apt_url, component=component, distribution=distribution, the_type='deb', augeas_root='/'):
                postgresql_sources_file_path = '/etc/apt/sources.list.d/postgresql.list'
                logger.info("adding postgresql apt source file '%s'" % (postgresql_sources_file_path,))
                postgresql_sources_file = open(postgresql_sources_file_path, 'w')
                postgresql_sources_file.write('deb %s %s %s' % (apt_url, distribution, component))
                postgresql_sources_file.flush()
                postgresql_sources_file.close()
                os.system('wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -')
                pm_utils.invalidate_apt()
        pg_version_string = str.join('.', [ str(x) for x in pg_version ])
        try:
            pm_utils.install_packages([
             'postgresql-%s' % pg_version_string,
             'postgresql-%s-postgis-2.1' % pg_version_string,
             'postgresql-%s-postgis-2.1-scripts' % pg_version_string,
             'postgresql-contrib-%s' % pg_version_string,
             'postgresql-client-common'], package_manager='apt-get', skip_apt_update=skip_apt_update)
        except sp.CalledProcessError as ex:
            logger.info('postgresql installation failed (which MIGHT be caused by breakage of apt package in Ubuntu 13.10')
            psql = '/opt/postgres/%s/bin/psql' % pg_version_string
            initdb = '/opt/postgres/%s/bin/initdb' % pg_version_string
            createdb = '/opt/postgres/%s/bin/createdb' % pg_version_string
            postgres = '/opt/postgres/%s/bin/postgres' % pg_version_string

        pm_utils.install_packages(['osm2pgsql'], package_manager='apt-get', skip_apt_update=skip_apt_update)
    elif check_os.check_opensuse():
        if pg_version == (9, 2):
            sp.check_call([zypper, 'install', 'postgresql', 'postgresql-contrib', 'postgresql-devel', 'postgresql-server'])
            psql = '/usr/lib/postgresql92/bin/psql'
            initdb = '/usr/lib/postgresql92/bin/initdb'
            createdb = '/usr/lib/postgresql92/bin/createdb'
            postgres = '/usr/lib/postgresql92/bin/postgres'
        else:
            raise RuntimeError('postgresql version %s not supported' % str.join('.', [ str(x) for x in pg_version ]))
    else:
        raise RuntimeError('operating system not supported!')


if __name__ == '__main__':
    plac.call(install_prequisites)