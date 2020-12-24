# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/recompute/recompute.py
# Compiled at: 2019-03-26 00:44:39
# Size of source mod 2**32: 16060 bytes
"""recompute.py

A sweet tool for Remote Execution.
This is the high-level user interface.
The user is exposed to the program through this module.
We bombard the user with a suite of features that enable comfortable execution of code in remote machines.
Each feature, named `mode` here, corresponds to a particular operation.
Scroll down for a table of available commands, options and how to use them.

"""
from recompute import utils
from recompute.instance import Instance
from recompute.config import ConfigManager
from recompute.instance import InstanceManager
from recompute.remote import Remote
from recompute.bundle import Bundle
from recompute.remote import VOID_CACHE
from getpass import getpass
import argparse, logging, os
logger = logging.getLogger(__name__)
MAN_DOCU = '\n                         _ __   ___ \n                        | \'__| / _ \\\n                        | |   |  __/\n                        |_|    \\___|\n\n+----------+-----------------------------------------------------+-----------------------+-------------------------------------+\n| Mode     | Description                                         | Options               | Example                             |\n+----------+-----------------------------------------------------+-----------------------+-------------------------------------+\n| init     | Setup current directory for remote execution        | --instance-idx        | $re init                            |\n|          |                                                     |                       | $re init --instance-idx=1           |\n+----------+-----------------------------------------------------+-----------------------+-------------------------------------+\n| rsync    | Use rsync to synchronize local files with remote    | --force               | $re rsync                           |\n+----------+-----------------------------------------------------+-----------------------+-------------------------------------+\n| sshadd   | Add a new instance to config                        | --instance            | $re sshadd --instance="usr@host"    |\n+----------+-----------------------------------------------------+-----------------------+-------------------------------------+\n| install  | Install pypi packages in requirements.txt in remote | cmd, --force          | $re install                         |\n|          |                                                     |                       | $re install "pytorch tqdm"          |\n+----------+-----------------------------------------------------+-----------------------+-------------------------------------+\n| sync     | Synchronous execution of "args.cmd" in remote       | cmd, --force, --rsync | $re sync "python3 x.py"             |\n+----------+-----------------------------------------------------+-----------------------+-------------------------------------+\n| async    | Asynchronous execution of "args.cmd" in remote      | cmd, --force, --rsync | $re async "python3 x.py"            |\n+----------+-----------------------------------------------------+-----------------------+-------------------------------------+\n| log      | Fetch log from remote machine                       | --loop, --filter      | $re log                             |\n|          |                                                     |                       | $re log --loop=2                    |\n|          |                                                     |                       | $re log --filter="pattern"          |\n+----------+-----------------------------------------------------+-----------------------+-------------------------------------+\n| list     | List out processes alive in remote machine          | --force               | $re list                            |\n+----------+-----------------------------------------------------+-----------------------+-------------------------------------+\n| kill     | Kill a process by index                             | --idx                 | $re kill                            |\n|          |                                                     |                       | $re kill --idx=1                    |\n+----------+-----------------------------------------------------+-----------------------+-------------------------------------+\n| purge    | Kill all remote process that are alive              | None                  | $re purge                           |\n+----------+-----------------------------------------------------+-----------------------+-------------------------------------+\n| ssh      | Create an ssh session in remote machine             | None                  | $re ssh                             |\n+----------+-----------------------------------------------------+-----------------------+-------------------------------------+\n| notebook | Create jupyter notebook in remote machine           | --run-async           | $re notebook                        |\n+----------+-----------------------------------------------------+-----------------------+-------------------------------------+\n| push     | Upload file to remote machine                       | cmd                   | $re push "x.py y/"                  |\n+----------+-----------------------------------------------------+-----------------------+-------------------------------------+\n| pull     | Download file from remote machine                   | cmd                   | $re pull "y/z.py ."                 |\n+----------+-----------------------------------------------------+-----------------------+-------------------------------------+\n| data     | Download data from web into data/ folder of remote  | cmd                   | $re data "url1 url2 url3"           |\n+----------+-----------------------------------------------------+-----------------------+-------------------------------------+\n| man      | Show this man page                                  | None                  | $re man                             |\n+----------+-----------------------------------------------------+-----------------------+-------------------------------------+\n'
parser = argparse.ArgumentParser(description='recompute.py -- A sweet tool for remote computation')
parser.add_argument('mode', type=str, help='(init/sync/async/rsync/install/log/list/kill/purgessh/notebook/conf/probe/data/pull/push/sshadd/man) recompute mode')
parser.add_argument('cmd', nargs='?', default='None', help='command to run in remote system')
parser.add_argument('--remote-home', nargs='?', default='projects/', help='remote projects/ directory')
parser.add_argument('--urls', nargs='?', default='', help='comma-separated list of URLs')
parser.add_argument('--instance', nargs='?', default='', help='[username@host] config.remotepass is used')
parser.add_argument('--filter', nargs='?', default='', help='keyword to filter log')
parser.add_argument('--loop', nargs='?', default='', help='number of seconds to wait to fetch log')
parser.add_argument('--idx', nargs='?', default='', help='process idx to operate on')
parser.add_argument('--name', nargs='?', default='runner', help='name of process')
parser.add_argument('--instance-idx', nargs='?', default=0, help='remote instance to use')
parser.add_argument('--force', default=False, action='store_true', help='clear cache')
parser.add_argument('--no-force', dest='force', action='store_false')
parser.add_argument('--run-async', default=False, action='store_true', help='Execute commands async')
parser.add_argument('--no-run-async', dest='run_async', action='store_false')
parser.add_argument('--rsync', default=True, action='store_true', help='Update files in remote machine')
parser.add_argument('--verbose', default=False, action='store_true', help='Print log while executing')
parser.add_argument('--no-rsync', dest='rsync', action='store_false')
args = parser.parse_args()

def init():
    """Setup current directory for remote execution

  * Setup remote instance for execution
  * Create local configuration files
  * Bundle up local repository
  * Sync files
  * Install Dependencies

  Returns
  -------
  remote.Remote
    An instance of Remote class
  """
    confman = ConfigManager()
    instanceman = InstanceManager(confman)
    instance_idx = int(args.instance_idx) if args.instance_idx else None
    instance = instanceman.get(instance_idx)
    bundle = Bundle()
    remote = Remote(instance, bundle, remote_home=(args.remote_home))
    remote.rsync()
    remote.install_deps()
    return remote


def cache_exists():
    """Does cache exist?"""
    return os.path.exists(VOID_CACHE)


def get_remote():
    """Get an instance of Remote from cache or create anew"""
    if cache_exists():
        logger.info('Cache exists')
        return Remote()
    else:
        logger.info("Cache doesn't exist")
        return init()


def main():
    """ Boilerplate """
    confman = ConfigManager()
    instanceman = InstanceManager(confman)
    if args.mode == 'man':
        print(MAN_DOCU)
        exit()
    else:
        if args.mode == 'conf':
            config = confman.generate(force=(args.force))
            if not config:
                logger.info('config exists; use --force to overwrite it')
                print('config exists; use --force to overwrite it')
        else:
            if args.mode == 'sshadd':
                try:
                    assert args.instance
                    password = getpass('Password:')
                    instance = Instance(password=password).resolve_str(args.instance)
                    instanceman.add_instance(instance)
                except AssertionError:
                    logger.error('Invalid/Empty instance')

    if args.mode == 'probe':
        print(instanceman.probe(force=(args.force)))
    else:
        if args.mode == 'data':
            try:
                assert args.urls
                get_remote().download((args.urls.split(' ')), run_async=(args.run_async))
            except AssertionError:
                logger.error('Input a list of URLs to download')

        else:
            if args.mode == 'init':
                init()
            else:
                if args.mode == 'sync':
                    assert args.cmd
                    remote = get_remote()
                    if 'python' in args.cmd:
                        if args.rsync:
                            remote.rsync(update=(args.force))
                    remote.execute([args.cmd], log=True, name=(args.name))
                else:
                    assert args.mode == 'async' and args.cmd
                    remote = get_remote()
    if 'python' in args.cmd:
        if args.rsync:
            remote.rsync(update=(args.force))
        remote.async_execute([args.cmd], name=(args.name))
    else:
        if args.mode == 'rsync':
            get_remote().rsync(update=(args.force))
        else:
            if args.mode == 'install':
                if not args.cmd:
                    get_remote().install_deps(update=(args.force))
                else:
                    get_remote().install(args.cmd.split(' '))
            else:
                if args.mode == 'log':
                    remote = get_remote()
                    if os.path.exists(remote.local_logfile):
                        os.remove(remote.local_logfile)
                    if args.loop:
                        remote.loop_get_remote_log(int(args.loop), args.filter)
                    else:
                        log = remote.get_remote_log(args.filter)
                        print(utils.parse_log(log))
                else:
                    if args.mode == 'list':
                        print(utils.tabulate_processes(get_remote().list_processes(force=True)))
                    else:
                        if args.mode == 'kill':
                            remote = get_remote()
                            print(utils.tabulate_processes(remote.list_processes(force=True)))
                            idx = int(args.idx) if args.idx else None
                            if not args.idx:
                                try:
                                    idx = int(input('Process to kill (index) : '))
                                except KeyboardInterrupt:
                                    exit()

                            remote.kill(idx)
                        else:
                            if args.mode == 'purge':
                                get_remote().kill(0)
                            else:
                                if args.mode == 'ssh':
                                    get_remote().get_session()
                                else:
                                    if args.mode == 'notebook':
                                        get_remote().start_notebook(args.run_async)
                                    else:
                                        if args.mode == 'pull':
                                            assert args.cmd
                                            remote = get_remote()
                                            filepaths = args.cmd.split(' ')
                                            try:
                                                assert len(filepaths) <= 2
                                            except AssertionError:
                                                logger.error('Copy one file/directory at a time')
                                                exit()

                                            remotefile = os.path.join(remote.remote_dir, filepaths[0])
                                            localpath = None if len(filepaths) == 1 else os.path.join(remote.bundle.path, filepaths[1])
                                            remote.get_file_from_remote(remotefile, localpath)
                                        else:
                                            if args.mode == 'push':
                                                assert args.cmd
                                                remote = get_remote()
                                                filepaths = args.cmd.split(' ')
                                                try:
                                                    assert len(filepaths) <= 2
                                                except AssertionError:
                                                    logger.error('Copy one file/directory at a time')
                                                    exit()

                                                localfile = os.path.join(remote.bundle.path, filepaths[0])
                                                remotepath = None if len(filepaths) == 1 else os.path.join(remote.remote_dir, filepaths[1])
                                                remote.copy_file_to_remote(localfile, remotepath)
                                            else:
                                                logger.error('Something went wrong! Check command-line arguments')