# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/eggbasket/commands.py
# Compiled at: 2008-07-13 16:55:56
"""This module contains functions called from console script entry points."""
import logging, optparse, sys
from os import getcwd
from os.path import dirname, exists, join
import pkg_resources
pkg_resources.require('TurboGears >= 1.0.4.4')
pkg_resources.require('SQLAlchemy >= 0.4')
pkg_resources.require('Genshi >= 0.4')
pkg_resources.require('docutils >= 0.4')
import cherrypy, turbogears
from turbogears.util import load_project_config, get_model
cherrypy.lowercase_api = True
log = logging.getLogger('eggbasket')

class ConfigurationError(Exception):
    pass


def find_config(args):
    """Return for environment-specific configuration in several places.

    First look on the command line for a desired config file,
    if it's not on the command line, then look for 'setup.py'
    in the current directory. If there, load configuration
    from a file called 'dev.cfg'. If it's not there, the project
    is probably installed and we'll look first for a file called
    'prod.cfg' in the current directory and then for a default
    config file called 'default.cfg' packaged in the egg.

    If all fails, raise ConfigurationError.
    """
    setupdir = dirname(dirname(__file__))
    curdir = getcwd()
    if args:
        configfile = args[0]
    elif exists(join(setupdir, 'setup.py')):
        configfile = join(setupdir, 'dev.cfg')
    elif exists(join(curdir, 'prod.cfg')):
        configfile = join(curdir, 'prod.cfg')
    else:
        try:
            configfile = pkg_resources.resource_filename(pkg_resources.Requirement.parse('EggBasket'), 'config/default.cfg')
        except pkg_resources.DistributionNotFound:
            raise ConfigurationError('Could not find default configuration.')

    log.info('Using configuration file %s', configfile)
    return configfile


def init_database(args):
    """Create bootstrap data in the database specified by the given config file.

    This will create a user with user_name/password "admin", who belongs
    to the group "maintainers", which has the "upload" permission.

    This function can safely be run several times for the same database. If a
    a user with user_name == 'admin' already exists, it does nothing.

    """
    configfile = find_config(args)
    turbogears.update_config(configfile=configfile, modulename='eggbasket.config')
    from turbogears import database
    model = get_model()
    session = database.session
    database.bind_meta_data()
    database.metadata.create_all(database.get_engine())
    try:
        model.User.query().filter_by(user_name='admin').one()
    except model.InvalidRequestError:
        adminuser = model.User(display_name='Administrator', user_name='admin', password='admin', email_address='admin@localhost.localdomain')
        anongroup = model.Group(display_name='Anonymous users', group_name='anonymous')
        authgroup = model.Group(display_name='Authenticated users', group_name='authenticated')
        maintgroup = model.Group(display_name='Package maintainers', group_name='maintainer')
        admingroup = model.Group(display_name='Administrators', group_name='admin')
        adminuser.groups.append(maintgroup)
        adminuser.groups.append(admingroup)
        uploadperm = model.Permission(permission_name='upload', description='Can upload package files')
        overwriteperm = model.Permission(permission_name='overwrite', description='Can overwrite existing files in the package repository')
        deleteperm = model.Permission(permission_name='delete', description='Can delete package files from the repository')
        dloadperm = model.Permission(permission_name='download', description='Can download package files')
        viewpkgsperm = model.Permission(permission_name='viewpkgs', description='Can view package list')
        viewfilesperm = model.Permission(permission_name='viewfiles', description='Can view package file list')
        viewinfoperm = model.Permission(permission_name='viewinfo', description='Can view package meta data')
        uploadperm.groups.append(maintgroup)
        overwriteperm.groups.append(maintgroup)
        deleteperm.groups.append(maintgroup)
        dloadperm.groups.extend([anongroup, authgroup])
        viewfilesperm.groups.extend([anongroup, authgroup])
        viewpkgsperm.groups.extend([anongroup, authgroup])
        viewinfoperm.groups.extend([anongroup, authgroup])
        session.flush()
        print 'Database initialized successfully'
    else:
        print "There already is an 'admin' user in the database."


def start_server(args):
    """Start the CherryPy application server."""
    configfile = find_config(args)
    turbogears.update_config(configfile=configfile, modulename='eggbasket.config')
    from eggbasket.controllers import Root
    turbogears.start_server(Root())


def main():
    from eggbasket import __version__
    parser = optparse.OptionParser(prog='eggbasket-server', version=__version__)
    parser.add_option('-i', '--init', action='store_true', help="Init database only, don't start server.", dest='init', default=False)
    (options, args) = parser.parse_args()
    if options.init:
        init_database(args)
    else:
        start_server(args)


if __name__ == '__main__':
    main()