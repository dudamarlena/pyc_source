# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autoxtrabackup.py
# Compiled at: 2020-03-24 02:41:06
# Size of source mod 2**32: 13499 bytes
import click, humanfriendly, logging, logging.handlers, os, pid, re, time, sys
from logging.handlers import RotatingFileHandler
from sys import platform as _platform
from sys import exit
from backup_prepare.prepare import Prepare
from general_conf.generalops import GeneralClass
from general_conf import path_config
from master_backup_script.backuper import Backup
from partial_recovery.partial import PartialRecovery
from prepare_env_test_mode.runner_test_mode import RunnerTestMode
from process_runner.process_runner import ProcessRunner
logger = logging.getLogger('')
destinations_hash = {'linux':'/dev/log',  'linux2':'/dev/log',  'darwin':'/var/run/syslog'}

def address_matcher(plt):
    return destinations_hash.get(plt, ('localhost', 514))


handler = logging.handlers.SysLogHandler(address=(address_matcher(_platform)))
logger.addHandler(handler)

def print_help(ctx, param, value):
    if value is False:
        return
    click.echo(ctx.get_help())
    ctx.exit()


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo('Developed by Shahriyar Rzayev from Azerbaijan MUG(http://mysql.az)')
    click.echo('Link : https://github.com/ShahriyarR/MySQL-AutoXtraBackup')
    click.echo('Email: rzayev.shahriyar@yandex.com')
    click.echo('Based on Percona XtraBackup: https://github.com/percona/percona-xtrabackup/')
    click.echo('MySQL-AutoXtraBackup Version: 1.5.5')
    ctx.exit()


def check_file_content(file):
    """Check if all mandatory headers and keys exist in file"""
    with open(file, 'r') as (config_file):
        file_content = config_file.read()
    config_headers = ['MySQL', 'Backup', 'Encrypt', 'Compress', 'Commands']
    config_keys = [
     'mysql',
     'mycnf',
     'mysqladmin',
     'mysql_user',
     'mysql_password',
     'mysql_host',
     'datadir',
     'tmp_dir',
     'backup_dir',
     'backup_tool',
     'xtra_prepare',
     'start_mysql_command',
     'stop_mysql_command',
     'chown_command']
    for header in config_headers:
        if header not in file_content:
            raise KeyError("Mandatory header [%s] doesn't exist in %s" % (
             header, file))

    for key in config_keys:
        if key not in file_content:
            raise KeyError("Mandatory key '%s' doesn't exists in %s." % (
             key, file))

    return True


def validate_file--- This code section failed: ---

 L. 100         0  LOAD_GLOBAL              os
                2  LOAD_ATTR                path
                4  LOAD_ATTR                isfile
                6  LOAD_FAST                'file'
                8  CALL_FUNCTION_1       1  '1 positional argument'
               10  POP_JUMP_IF_FALSE    56  'to 56'

 L. 102        12  LOAD_GLOBAL              re
               14  LOAD_ATTR                compile
               16  LOAD_STR                 '.*\\.cnf'
               18  CALL_FUNCTION_1       1  '1 positional argument'
               20  STORE_FAST               'pattern'

 L. 104        22  LOAD_FAST                'pattern'
               24  LOAD_ATTR                match
               26  LOAD_FAST                'file'
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  POP_JUMP_IF_FALSE    46  'to 46'

 L. 106        32  LOAD_GLOBAL              check_file_content
               34  LOAD_FAST                'file'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  POP_JUMP_IF_FALSE    54  'to 54'

 L. 107        40  LOAD_CONST               None
               42  RETURN_VALUE     
             44_0  COME_FROM            38  '38'
               44  JUMP_ABSOLUTE        64  'to 64'
               46  ELSE                     '54'

 L. 109        46  LOAD_GLOBAL              ValueError
               48  LOAD_STR                 'Invalid file extension. Expecting .cnf'
               50  CALL_FUNCTION_1       1  '1 positional argument'
               52  RAISE_VARARGS_1       1  'exception'
               54  JUMP_FORWARD         64  'to 64'
               56  ELSE                     '64'

 L. 111        56  LOAD_GLOBAL              FileNotFoundError
               58  LOAD_STR                 'Specified file does not exist.'
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  RAISE_VARARGS_1       1  'exception'
             64_0  COME_FROM            54  '54'

Parse error at or near `RAISE_VARARGS_1' instruction at offset 62


@click.command()
@click.option('--dry-run', is_flag=True, help='Enable the dry run.')
@click.option('--prepare', is_flag=True, help='Prepare/recover backups.')
@click.option('--backup', is_flag=True,
  help='Take full and incremental backups.')
@click.option('--partial', is_flag=True,
  help='Recover specified table (partial recovery).')
@click.option('--version', is_flag=True,
  callback=print_version,
  expose_value=False,
  is_eager=True,
  help='Version information.')
@click.option('--defaults-file', default=(path_config.config_path_file),
  show_default=True,
  help='Read options from the given file')
@click.option('--tag', help='Pass the tag string for each backup')
@click.option('--show-tags', is_flag=True,
  help='Show backup tags and exit')
@click.option('-v', '--verbose', is_flag=True, help='Be verbose (print to console)')
@click.option('-lf', '--log-file',
  default=(path_config.log_file_path),
  show_default=True,
  help='Set log file')
@click.option('-l', '--log',
  '--log-level',
  default='INFO',
  show_default=True,
  type=(click.Choice(['DEBUG',
 'INFO',
 'WARNING',
 'ERROR',
 'CRITICAL'])),
  help='Set log level')
@click.option('--log-file-max-bytes', default=1073741824,
  show_default=True,
  nargs=1,
  type=int,
  help='Set log file max size in bytes')
@click.option('--log-file-backup-count', default=7,
  show_default=True,
  nargs=1,
  type=int,
  help='Set log file backup count')
@click.option('--keyring-vault', default=0,
  show_default=True,
  nargs=1,
  type=int,
  help='Enable this when you pass keyring_vault options in default mysqld options in config[Only for using with --test-mode]')
@click.option('--test-mode', is_flag=True,
  help='Enable test mode. Must be used with --defaults-file and only for TESTs for XtraBackup')
@click.option('--help', is_flag=True,
  callback=print_help,
  expose_value=False,
  is_eager=False,
  help='Print help message and exit.')
@click.pass_context
def all_procedure(ctx, prepare, backup, partial, tag, show_tags, verbose, log_file, log, defaults_file, dry_run, test_mode, log_file_max_bytes, log_file_backup_count, keyring_vault):
    config = GeneralClass(defaults_file)
    formatter = logging.Formatter(fmt='%(asctime)s %(levelname)s [%(module)s:%(lineno)d] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    if verbose:
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        ch.setFormatter(formatter)
        logger.addHandler(ch)
    elif log_file:
        try:
            if config.log_file_max_bytes:
                if config.log_file_backup_count:
                    file_handler = RotatingFileHandler(log_file, mode='a', maxBytes=(int(config.log_file_max_bytes)),
                      backupCount=(int(config.log_file_backup_count)))
            else:
                file_handler = RotatingFileHandler(log_file, mode='a', maxBytes=log_file_max_bytes,
                  backupCount=log_file_backup_count)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except PermissionError as err:
            exit('{} Please consider to run as root or sudo'.format(err))

    else:
        if log is not None:
            logger.setLevel(log)
        else:
            if 'log_level' in config.__dict__:
                logger.setLevel(config.log_level)
            else:
                logger.setLevel('INFO')
    validate_file(defaults_file)
    pid_file = pid.PidFile(piddir=(config.pid_dir))
    try:
        with pid_file:
            if prepare is False:
                if backup is False:
                    if partial is False and verbose is False and dry_run is False and test_mode is False and show_tags is False:
                        print_help(ctx, None, value=True)
                    else:
                        if show_tags and defaults_file:
                            b = Backup(config=defaults_file)
                            b.show_tags(backup_dir=(b.backupdir))
                else:
                    if test_mode and defaults_file:
                        logger.warning('Enabled Test Mode!!!')
                        logger.info('Starting Test Mode')
                        test_obj = RunnerTestMode(config=defaults_file)
                        for basedir in test_obj.basedirs:
                            if '5.7' in basedir:
                                if '2_4_ps_5_7' in defaults_file:
                                    if keyring_vault == 1:
                                        test_obj.wipe_backup_prepare_copyback(basedir=basedir, keyring_vault=1)
                                    else:
                                        test_obj.wipe_backup_prepare_copyback(basedir=basedir)
                            elif '8.0' in basedir:
                                if '8_0_ps_8_0' in defaults_file:
                                    if keyring_vault == 1:
                                        test_obj.wipe_backup_prepare_copyback(basedir=basedir, keyring_vault=1)
                                    else:
                                        test_obj.wipe_backup_prepare_copyback(basedir=basedir)
                            elif '5.6' in basedir:
                                if '2_4_ps_5_6' in defaults_file:
                                    test_obj.wipe_backup_prepare_copyback(basedir=basedir)
                            elif '5.6' in basedir:
                                if '2_3_ps_5_6' in defaults_file:
                                    test_obj.wipe_backup_prepare_copyback(basedir=basedir)
                            elif '5.5' in basedir:
                                if '2_3_ps_5_5' in defaults_file:
                                    test_obj.wipe_backup_prepare_copyback(basedir=basedir)
                            elif '5.5' in basedir:
                                if '2_4_ps_5_5' in defaults_file:
                                    test_obj.wipe_backup_prepare_copyback(basedir=basedir)
                            else:
                                logger.error('Please pass proper already generated config file!')
                                logger.error('Please check also if you have run prepare_env.bats file')

                if prepare:
                    if not test_mode:
                        if dry_run or tag:
                            a = Prepare(config=defaults_file, tag=tag)
                            a.prepare_backup_and_copy_back()
                        else:
                            a = Prepare(config=defaults_file)
                            a.prepare_backup_and_copy_back()
                    else:
                        logger.warning('Dry run enabled!')
                        logger.warning('Do not recover/copy-back in this mode!')
                        if tag:
                            a = Prepare(config=defaults_file, dry_run=1, tag=tag)
                            a.prepare_backup_and_copy_back()
                        else:
                            a = Prepare(config=defaults_file, dry_run=1)
                            a.prepare_backup_and_copy_back()
                elif backup:
                    if not test_mode:
                        if dry_run or tag:
                            b = Backup(config=defaults_file, tag=tag)
                            b.all_backup()
                        else:
                            b = Backup(config=defaults_file)
                            b.all_backup()
                    else:
                        logger.warning('Dry run enabled!')
                        if tag:
                            b = Backup(config=defaults_file, dry_run=1, tag=tag)
                            b.all_backup()
                        else:
                            b = Backup(config=defaults_file, dry_run=1)
                            b.all_backup()
                elif partial:
                    c = dry_run or PartialRecovery(config=defaults_file)
                    c.final_actions()
            else:
                logger.critical('Dry run is not implemented for partial recovery!')
    except pid.PidFileAlreadyLockedError as error:
        if hasattr(config, 'pid_runtime_warning'):
            if time.time() - os.stat(pid_file.filename).st_ctime > config.pid_runtime_warning:
                pid.fh.seek(0)
                pid_str = pid.fh.read(16).split('\n', 1)[0].strip()
                logger.critical('Backup (pid: ' + pid_str + ') has been running for logger than: ' + str(humanfriendly.format_timespan(config.pid_runtime_warning)))
    except pid.PidFileAlreadyRunningError as error:
        if hasattr(config, 'pid_runtime_warning'):
            if time.time() - os.stat(pid_file.filename).st_ctime > config.pid_runtime_warning:
                pid.fh.seek(0)
                pid_str = pid.fh.read(16).split('\n', 1)[0].strip()
                logger.critical('Backup (pid: ' + pid_str + ') has been running for logger than: ' + str(humanfriendly.format_timespan(config.pid_runtime_warning)))
    except pid.PidFileUnreadableError as error:
        logger.warning('Pid file can not be read: ' + str(error))
    except pid.PidFileError as error:
        logger.warning('Generic error with pid file: ' + str(error))

    logger.info('Xtrabackup command history:')
    for i in ProcessRunner.xtrabackup_history_log:
        logger.info(str(i))

    logger.info('Autoxtrabackup completed successfully!')
    return True


if __name__ == '__main__':
    all_procedure()