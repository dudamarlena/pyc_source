# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/checkpoint/command.py
# Compiled at: 2009-01-07 23:58:31
__doc__ = 'Checkpoint command-line utility (CLI)'
import os, sys, logging
from textwrap import dedent
from optparse import OptionParser
from checkpoint.manager import MirrorManager, RepositoryManager
from checkpoint.release import DESCRIPTION, VERSION, URL
from checkpoint.error import CheckpointError
__all__ = [
 'mirror', 'repository']
log = logging.getLogger('checkpoint')
SUCCESS = 0
ERROR = 1
crash_recovery_confirmation = dedent('\n    --------------------------------------------------------------\n    !!! Confirm Crash Recovery! !!!\n\n    You have selected crash recovery.  This process will move all\n    files to a new crash recovery directory and then one-by-one \n    restore your files from the good copies in the repository.\n\n    If this process is interrupted for any reason, you can try \n    recovery again to attempt to restore your files.  If recovery\n    still does not finish successfully, or if it finishes successfully\n    but you still appear to be missing files, you may have to try \n    manual crash-recovery.  See the documentation for more details.\n    --------------------------------------------------------------\n\n')

def configure_loggers():
    log_level = logging.INFO
    try:
        if int(os.environ['CHECKPOINT_DEBUG']) == 1:
            log_level = logging.DEBUG
    except KeyError:
        pass

    log.setLevel(log_level)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter('%(message)s'))
    log.addHandler(handler)


def mirror(argv=sys.argv):
    usage = '\n        usage:  %(prog)s <command> [args]\n        Checkpoint Mirror command-line utility, version %(version)s\n\n        Most commands accept a directory argument.  If this argument is not\n        specified, the current directory will be used by default.\n        \n        Mirror Commands:\n            mirror <source-dir> <dest-dir>  Mirror a checkpoint directory\n            refresh [<dir>]                 Bring a mirror up to date\n            forget [<dir>]                  Delete mirror configuration\n            recover [<dir>]                 Recover after a crash or failure\n    \n        %(description)s\n        For additional information, see %(url)s\n    ' % dict(prog=os.path.basename(argv[0]), description=DESCRIPTION, version=VERSION, url=URL)
    usage = dedent(usage)
    configure_loggers()
    try:
        command = argv[1]
        if command not in MirrorManager.COMMANDS:
            raise ValueError
    except (IndexError, ValueError):
        print usage
        return ERROR

    source_directory = None
    destination_directory = None
    if command == 'mirror':
        if len(argv) == 3:
            source_directory = argv[2]
            destination_directory = os.getcwd()
        elif len(argv) == 4:
            source_directory = argv[2]
            destination_directory = argv[3]
        else:
            print usage
            return ERROR
    elif command in ('refresh', 'forget', 'recover'):
        if len(argv) == 3:
            destination_directory = argv[2]
        else:
            destination_directory = os.getcwd()
    else:
        print usage
        return ERROR
    if command == 'recover':
        print crash_recovery_confirmation
        choice = raw_input('Proceed with crash recovery [yes/no]: ')
        if choice.lower() != 'yes':
            print 'Crash recovery was cancelled.'
            return SUCCESS
    try:
        manager = MirrorManager(destination_directory=destination_directory)
        if command == 'mirror':
            kw = dict(source_directory=source_directory)
        else:
            kw = dict()
        return manager.dispatch(command, **kw)
    except CheckpointError, e:
        print >> sys.stderr, '%s\n' % e.message
        return ERROR

    return


def repository(argv=sys.argv):
    usage = '\n        usage:  %(prog)s <command> [options] [args]\n        Checkpoint command-line utility, version %(version)s\n\n        Most commands accept a directory argument.  If this argument is not\n        specified, the current directory will be used by default.\n\n        Repository Commands:\n            watch [<dir>]                   Watch directory for changes\n            status [<dir>]                  List all changes since last commit\n            commit [<dir>]                  Save all changes since last commit\n            revert -c changeset [<dir>]     Revert to a previous changeset\n            forget [<dir>]                  Delete saved history of changes\n            recover [<dir>]                 Recover after a crash or failure\n    \n        %(description)s\n        For additional information, see %(url)s\n    ' % dict(prog=os.path.basename(argv[0]), description=DESCRIPTION, version=VERSION, url=URL)
    usage = dedent(usage)
    configure_loggers()
    try:
        command = argv[1]
        if command not in RepositoryManager.COMMANDS:
            raise ValueError
    except (IndexError, ValueError):
        print usage
        return ERROR

    parser = OptionParser()
    parser.add_option('-c', dest='changeset', default=None, type='int')
    try:
        (options, extra_args) = parser.parse_args(argv[2:])
    except:
        print usage
        return ERROR

    if len(extra_args) == 1:
        directory = extra_args[0]
    else:
        directory = os.getcwd()
    if command == 'recover':
        print crash_recovery_confirmation
        choice = raw_input('Proceed with crash recovery [yes/no]: ')
        if choice.lower() != 'yes':
            print 'Crash recovery was cancelled.'
            return SUCCESS
    try:
        manager = RepositoryManager(directory)
        if command == 'revert':
            kw = dict(desired_changeset=options.changeset)
        else:
            kw = dict()
        return manager.dispatch(command, **kw)
    except CheckpointError, e:
        print >> sys.stderr, '%s\n' % e.message
        return ERROR

    return