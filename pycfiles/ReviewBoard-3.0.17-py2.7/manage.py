# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/reviewboard/manage.py
# Compiled at: 2020-02-11 04:03:56
from __future__ import print_function, unicode_literals
import os, shutil, subprocess, sys
from datetime import datetime
from os.path import abspath, dirname
from wsgiref import simple_server
from django.core.management import execute_from_command_line

def check_dependencies(settings):
    from djblets.util.filesystem import is_exe_in_path
    from reviewboard.admin.import_utils import has_module
    from reviewboard.dependencies import dependency_error, dependency_warning, fail_if_missing_dependencies
    if sys.version_info[0] != 2 or sys.version_info[1] != 7:
        dependency_error(b'Python 2.7 is required.')
    if not is_exe_in_path(b'node'):
        dependency_error(b'node (from NodeJS) was not found. It must be installed from your package manager or from https://nodejs.org/')
    if not os.path.exists(b'node_modules'):
        dependency_error(b'The node_modules directory is missing. Please re-run `./setup.py develop` to install all NodeJS dependencies.')
    for key in ('UGLIFYJS_BINARY', 'LESS_BINARY', 'BABEL_BINARY'):
        path = settings.PIPELINE[key]
        if not os.path.exists(path):
            dependency_error(b'%s is missing. Please re-run `./setup.py develop` to install all NodeJS dependencies.' % os.path.abspath(path))

    if not has_module(b'pysvn') and not has_module(b'subvertpy'):
        dependency_warning(b'Neither the subvertpy nor pysvn Python modules were found. Subversion integration will not work. For pysvn, see your package manager for the module or download from http://pysvn.tigris.org/project_downloads.html. For subvertpy, run `pip install subvertpy`. We recommend pysvn for better compatibility.')
    if has_module(b'P4'):
        try:
            subprocess.call([b'p4', b'-h'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        except OSError:
            dependency_warning(b'The p4 command not found. Perforce integration will not work. To enable support, download p4 from http://cdist2.perforce.com/perforce/ and place it in your PATH.')

    else:
        dependency_warning(b'The p4python module was not found. Perforce integration will not work. To enable support, run `pip install p4python`')
    if not is_exe_in_path(b'hg'):
        dependency_warning(b'The hg command was not found. Mercurial integration will not work. To enable support, run `pip install mercurial`')
    if not is_exe_in_path(b'bzr'):
        dependency_warning(b'The bzr command was not found. Bazaar integration will not work. To enable support, run `pip install bzr`')
    if not is_exe_in_path(b'cvs'):
        dependency_warning(b'The cvs command was not found. CVS integration will not work. To enable support, install cvs from your package manager or from http://www.nongnu.org/cvs/')
    if not is_exe_in_path(b'git'):
        dependency_warning(b'The git command not found. Git integration will not work. To enable support, install git from your package manager or from https://git-scm.com/downloads')
    fail_if_missing_dependencies()


def include_enabled_extensions(settings):
    """
    This adds enabled extensions to the INSTALLED_APPS cache
    so that operations like syncdb and evolve will take extensions
    into consideration.
    """
    from django.db.models.loading import load_app
    from django.db import DatabaseError
    from reviewboard.extensions.base import get_extension_manager
    try:
        manager = get_extension_manager()
    except DatabaseError:
        return

    for extension in manager.get_enabled_extensions():
        load_app(extension.info.app_name)


def upgrade_database():
    """Perform an upgrade of the database.

    This will prompt the user for confirmation, with instructions on what
    will happen. If the database is using SQLite3, it will be backed up
    automatically, making a copy that contains the current timestamp.
    Otherwise, the user will be prompted to back it up instead.

    Returns:
        bool:
        ``True`` if the user has confirmed the upgrade. ``False`` if they
        have not.
    """
    from django.conf import settings
    from django.utils.six.moves import input
    database = settings.DATABASES[b'default']
    db_name = database[b'NAME']
    backup_db_name = None
    if b'--no-backup' not in sys.argv and database[b'ENGINE'] == b'django.db.backends.sqlite3' and os.path.exists(db_name):
        backup_db_name = b'%s.%s' % (
         db_name,
         datetime.now().strftime(b'%Y%m%d.%H%M%S'))
        try:
            shutil.copy(db_name, backup_db_name)
        except Exception as e:
            sys.stderr.write(b'Unable to make a backup of your database at %s: %s\n\n' % (
             db_name, e))
            backup_db_name = None

    if b'--noinput' in sys.argv:
        if backup_db_name:
            print(b'Your existing database has been backed up to\n%s\n' % backup_db_name)
        perform_upgrade = True
    else:
        message = b'You are about to upgrade your database, which cannot be undone.\n\n'
        if backup_db_name:
            message += b'Your existing database has been backed up to\n%s' % backup_db_name
        else:
            message += b'PLEASE MAKE A BACKUP BEFORE YOU CONTINUE!'
        message += b'\n\nType "yes" to continue or "no" to cancel: '
        perform_upgrade = input(message).lower() in ('yes', 'y')
        print(b'\n')
    if perform_upgrade:
        print(b'===========================================================\nPerforming the database upgrade. Any "unapplied evolutions"\nwill be handled automatically.\n===========================================================\n')
        commands = [
         [
          b'syncdb', b'--noinput'],
         [
          b'evolve', b'--noinput']]
        for command in commands:
            execute_from_command_line([sys.argv[0]] + command)

    else:
        print(b'The upgrade has been cancelled.\n')
        sys.exit(1)
    return


def main(settings, in_subprocess):
    if dirname(settings.__file__) == os.getcwd():
        sys.stderr.write(b"manage.py should not be run from within the 'reviewboard' Python package directory.\n")
        sys.stderr.write(b'Make sure to run this from the top of the Review Board source tree.\n')
        sys.exit(1)
    try:
        command_name = sys.argv[1]
    except IndexError:
        command_name = None

    if command_name in ('runserver', 'test'):
        if settings.DEBUG and not in_subprocess:
            sys.stderr.write(b'Running dependency checks (set DEBUG=False to turn this off)...\n')
            check_dependencies(settings)
        if command_name == b'runserver':
            simple_server.ServerHandler.http_version = b'1.1'
    elif command_name not in ('syncdb', 'migrate'):
        from reviewboard import initialize
        initialize()
        if command_name == b'upgrade':
            upgrade_database()
            return
        include_enabled_extensions(settings)
    execute_from_command_line(sys.argv)
    return


def run():
    sys.path.insert(0, dirname(dirname(abspath(__file__))))
    try:
        sys.path.remove(dirname(abspath(__file__)))
    except ValueError:
        pass

    if b'DJANGO_SETTINGS_MODULE' not in os.environ:
        in_subprocess = False
        os.environ.setdefault(b'DJANGO_SETTINGS_MODULE', b'reviewboard.settings')
    else:
        in_subprocess = True
    if len(sys.argv) > 1 and sys.argv[1] == b'test':
        os.environ[b'RB_RUNNING_TESTS'] = b'1'
    try:
        from reviewboard import settings
    except ImportError as e:
        sys.stderr.write(b"Error: Can't find the file 'settings.py' in the directory containing %r. It appears you've customized things.\nYou'll have to run django-admin.py, passing it your settings module.\n(If the file settings.py does indeed exist, it's causing an ImportError somehow.)\n" % __file__)
        sys.stderr.write(b'The error we got was: %s\n' % e)
        sys.exit(1)

    main(settings, in_subprocess)


if __name__ == b'__main__':
    run()