# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staramr/subcommand/Database.py
# Compiled at: 2019-12-17 17:26:02
# Size of source mod 2**32: 15711 bytes
"""
Classes for interacting with the (ResFinder/PointFinder/PlasmidFinder) databases used to detect AMR genes.
"""
import argparse, logging, sys
from os import path, mkdir
import staramr.SubCommand as SubCommand
from staramr.Utils import get_string_with_spacing
import staramr.blast.JobHandler as JobHandler
import staramr.databases.AMRDatabasesManager as AMRDatabasesManager
import staramr.databases.resistance.ARGDrugTable as ARGDrugTable
import staramr.exceptions.CommandParseException as CommandParseException
import staramr.exceptions.DatabaseErrorException as DatabaseErrorException
import staramr.exceptions.DatabaseNotFoundException as DatabaseNotFoundException
logger = logging.getLogger('AMRDatabaseHandler')

class Database(SubCommand):

    def __init__(self, subparser, script_name):
        super().__init__(subparser, script_name)

    def _setup_args(self, arg_parser):
        arg_parser = self._subparser.add_parser('db', help='Download ResFinder/PointFinder/PlasmidFinder databases')
        subparser = arg_parser.add_subparsers(dest='db_command', help='Subcommand for ResFinder/PointFinder/PlasmidFinder databases.')
        Build(subparser, self._script_name + ' db')
        Update(subparser, self._script_name + ' db')
        Info(subparser, self._script_name + ' db')
        RestoreDefault(subparser, self._script_name + ' db')
        return arg_parser

    def run(self, args):
        super(Database, self).run(args)
        if args.db_command is None:
            self._root_arg_parser.print_help()


class Build(Database):

    def __init__(self, subparser, script_name):
        super().__init__(subparser, script_name)

    def _setup_args(self, arg_parser):
        name = self._script_name
        self._default_dir = AMRDatabasesManager.get_default_database_directory()
        epilog = 'Example:\n\t' + name + ' build\n\t\tBuilds a new ResFinder/PointFinder/PlasmidFinder database under ' + self._default_dir + ' if it does not exist\n\n' + '\t' + name + ' build --dir databases\n' + '\t\tBuilds a new ResFinder/PointFinder/PlasmidFinder database under databases/'
        arg_parser = self._subparser.add_parser('build', epilog=epilog,
          formatter_class=(argparse.RawTextHelpFormatter),
          help='Downloads and builds databases in the given directory.')
        arg_parser.add_argument('--dir', action='store', dest='destination', type=str, help=('The directory to download the databases into [' + self._default_dir + '].'),
          default=(self._default_dir),
          required=False)
        arg_parser.add_argument('--resfinder-commit', action='store', dest='resfinder_commit', type=str, help='The specific git commit for the resfinder database [latest].',
          required=False)
        arg_parser.add_argument('--pointfinder-commit', action='store', dest='pointfinder_commit', type=str, help='The specific git commit for the pointfinder database [latest].',
          required=False)
        arg_parser.add_argument('--plasmidfinder-commit', action='store', dest='plasmidfinder_commit', type=str, help='The specific git commit for the plasmidfinder database [latest].',
          required=False)
        return arg_parser

    def run(self, args):
        super(Build, self).run(args)
        if path.exists(args.destination):
            if args.destination == self._default_dir:
                raise CommandParseException(('Error, default destination [' + args.destination + '] already exists'), (self._root_arg_parser),
                  print_help=True)
            else:
                raise CommandParseException('Error, destination [' + args.destination + '] already exists', self._root_arg_parser)
        else:
            mkdir(args.destination)
        if args.destination == AMRDatabasesManager.get_default_database_directory():
            database_repos = AMRDatabasesManager.create_default_manager().get_database_repos()
        else:
            database_repos = AMRDatabasesManager(args.destination).get_database_repos()
        database_repos.build({'resfinder':args.resfinder_commit,  'pointfinder':args.pointfinder_commit,  'plasmidfinder':args.plasmidfinder_commit})
        if not AMRDatabasesManager.is_database_repos_default_commits(database_repos):
            logger.warning('Built non-default ResFinder/PointFinder/PlasmidFinder database version. This may lead to differences in the detected AMR genes depending on how the database files are structured.')


class Update(Database):

    def __init__(self, subparser, script_name):
        super().__init__(subparser, script_name)

    def _setup_args(self, arg_parser):
        self._default_dir = AMRDatabasesManager.get_default_database_directory()
        name = self._script_name
        epilog = 'Example:\n\t' + name + ' update databases/\n\t\tUpdates the ResFinder/PointFinder/PlasmidFinder database under databases/\n\n' + '\t' + name + ' update -d\n' + '\t\tUpdates the default ResFinder/PointFinder/PlasmidFinder database under ' + self._default_dir
        arg_parser = self._subparser.add_parser('update', epilog=epilog,
          formatter_class=(argparse.RawTextHelpFormatter),
          help='Updates databases in the given directories.')
        arg_parser.add_argument('-d', '--update-default', action='store_true', dest='update_default', help=('Updates default database directory (' + self._default_dir + ').'),
          required=False)
        arg_parser.add_argument('--resfinder-commit', action='store', dest='resfinder_commit', type=str, help='The specific git commit for the resfinder database [latest].',
          required=False)
        arg_parser.add_argument('--pointfinder-commit', action='store', dest='pointfinder_commit', type=str, help='The specific git commit for the pointfinder database [latest].',
          required=False)
        arg_parser.add_argument('--plasmidfinder-commit', action='store', dest='plasmidfinder_commit', type=str, help='The specific git commit for the plasmidfinder database [latest].',
          required=False)
        arg_parser.add_argument('directories', nargs='*')
        return arg_parser

    def run(self, args):
        super(Update, self).run(args)
        if len(args.directories) == 0:
            if not args.update_default:
                raise CommandParseException("Must pass at least one directory to update, or use '--update-default'", (self._root_arg_parser),
                  print_help=True)
            else:
                try:
                    database_repos = AMRDatabasesManager.create_default_manager().get_database_repos(force_use_git=True)
                    database_repos.update({'resfinder':args.resfinder_commit, 
                     'pointfinder':args.pointfinder_commit,  'plasmidfinder':args.plasmidfinder_commit})
                    if not AMRDatabasesManager.is_database_repos_default_commits(database_repos):
                        logger.warning('Updated to non-default ResFinder/PointFinder/PlasmidFinder database version. This may lead to differences in the detected AMR genes depending on how the database files are structured.')
                except DatabaseErrorException as e:
                    try:
                        logger.error("Could not update default database. Please try restoring with 'staramr db restore-default'")
                        raise e
                    finally:
                        e = None
                        del e

        else:
            for directory in args.directories:
                database_repos = AMRDatabasesManager(directory).get_database_repos()
                database_repos.update({'resfinder':args.resfinder_commit,  'pointfinder':args.pointfinder_commit,  'plasmidfinder':args.plasmidfinder_commit})
                if not AMRDatabasesManager.is_database_repos_default_commits(database_repos):
                    logger.warning('Updated to non-default ResFinder/PointFinder/PlasmidFinder database version [%s]. This may lead to differences in the detected AMR genes depending on how the database files are structured.', directory)


class RestoreDefault(Database):

    def __init__(self, subparser, script_name):
        super().__init__(subparser, script_name)

    def _setup_args(self, arg_parser):
        name = self._script_name
        epilog = 'Example:\n\t' + name + ' restore-default\n\t\tRestores the default ResFinder/PointFinder/PlasmidFinder database\n\n'
        arg_parser = self._subparser.add_parser('restore-default', epilog=epilog,
          formatter_class=(argparse.RawTextHelpFormatter),
          help='Restores the default ResFinder/PointFinder/PlasmidFinder databases.')
        arg_parser.add_argument('-f', '--force', action='store_true', dest='force', help='Force restore without asking for confirmation.',
          required=False)
        return arg_parser

    def _confirm_restore(self):
        """
        Confirms with the user whether or not to restore the database directory.
        :return: True if should restore, False otherwise.
        """
        confirmed = False
        while not confirmed:
            response = str(input('Restore the default ResFinder/PointFinder/PlasmidFinder databases (Y/N)? ').lower().strip())
            if not response == 'y':
                if response == 'yes':
                    return True
                if response == 'n' or response == 'no':
                    return False

    def run(self, args):
        super(RestoreDefault, self).run(args)
        database_manager = AMRDatabasesManager.create_default_manager()
        if not args.force:
            response = self._confirm_restore()
        else:
            response = True
        if response:
            database_manager.restore_default()


class Info(Database):

    def __init__(self, subparser, script_name):
        super().__init__(subparser, script_name)

    def _setup_args(self, arg_parser):
        name = self._script_name
        default_dir = AMRDatabasesManager.get_default_database_directory()
        epilog = 'Example:\n\t' + name + ' info\n\t\tPrints information about the default database in ' + default_dir + '\n\n' + '\t' + name + ' info databases\n' + '\t\tPrints information on the database stored in databases/'
        arg_parser = self._subparser.add_parser('info', epilog=epilog,
          formatter_class=(argparse.RawTextHelpFormatter),
          help='Prints information on databases in the given directories.')
        arg_parser.add_argument('directories', nargs='*')
        return arg_parser

    def run(self, args):
        super(Info, self).run(args)
        arg_drug_table = ARGDrugTable()
        if len(args.directories) == 0:
            database_repos = AMRDatabasesManager.create_default_manager().get_database_repos()
            if not AMRDatabasesManager.is_database_repos_default_commits(database_repos):
                logger.warning('Using non-default ResFinder/PointFinder/PlasmidFinder database versions. This may lead to differences in the detected AMR genes depending on how the database files are structured.')
            try:
                database_info = database_repos.info()
                database_info['mlst_version'] = JobHandler.get_mlst_version(JobHandler)
                database_info.update(arg_drug_table.get_resistance_table_info())
                sys.stdout.write(get_string_with_spacing(database_info))
            except DatabaseNotFoundException as e:
                try:
                    logger.error("No database found. Perhaps try restoring the default with 'staramr db restore-default'")
                finally:
                    e = None
                    del e

        else:
            for directory in args.directories:
                try:
                    database_repos = AMRDatabasesManager(directory).get_database_repos()
                    if not AMRDatabasesManager.is_database_repos_default_commits(database_repos):
                        logger.warning('Using non-default ResFinder/PointFinder/PlasmidFinder database version [%s]. This may lead to differences in the detected AMR genes depending on how the database files are structured.', directory)
                    database_info = database_repos.info()
                    database_info.update(arg_drug_table.get_resistance_table_info())
                    sys.stdout.write(get_string_with_spacing(database_info))
                except DatabaseNotFoundException as e:
                    try:
                        logger.error("Database not found in [%s]. Perhaps try building with 'staramr db build --dir %s'", directory, directory)
                    finally:
                        e = None
                        del e