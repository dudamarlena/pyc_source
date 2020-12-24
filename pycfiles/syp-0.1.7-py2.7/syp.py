# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/syp/syp.py
# Compiled at: 2017-01-24 22:10:38
"""We list all the packages we install on our system in a single file
(one for each package manager: one for debian packages, another for
pip, etc). Each file is under version control. We want to be able to
edit those files (add, remove packages) and "sync" our system
with the modifications.

We also want to call a program with a package as argument and that
program to add the package name to the right file.

"""
from __future__ import print_function
from __future__ import unicode_literals
import operator, os, shutil, signal, sys
from builtins import input
from functools import reduce
from io import open
from os.path import expanduser
from os.path import join
import addict, clize
from future.utils import exec_
from sigtools.modifiers import annotate
from sigtools.modifiers import kwoargs
from termcolor import colored
from settings import CONF
from settings import REQUIREMENTS_FILES
from settings import REQUIREMENTS_ROOT_DIR
from settings import SYSTEM_PACMAN

def cache_init(req_file, root_dir=b''):
    """Create the cache file for req_file. Don't copy its content yet.

    Create nested directories to mimic the dotfiles structure if needed.

    Return None for an error, [] otherwise.
    """
    fullfile = expanduser(join(root_dir, req_file))
    if not os.path.isfile(fullfile):
        print((b"The file {} does not exist, we couldn't create a cache.\nYou should check the REQUIREMENTS_ROOT_DIR variable at ~/.syp/settings.py.").format(fullfile))
        return None
    else:
        cache_apt = join(expanduser(CONF), req_file)
        split = req_file.split(b'/')[0:-1]
        for i in range(len(split)):
            maybe_dir = join(expanduser(CONF), split[i:i + 1][0])
            if not os.path.isdir(maybe_dir):
                os.makedirs(expanduser(maybe_dir))

        os.system((b'touch {}').format(cache_apt))
        return []


def get_diff(cached_list, curr_list):
    """Diff two lists, return a tuple of lists to be installed, to be
    deleted.

    """
    to_install = list(set(curr_list) - set(cached_list))
    to_delete = list(set(cached_list) - set(curr_list))
    return (to_install, to_delete)


def get_shell_cmd(pmconf, rm=False):
    """Form the shell command with the right package manager.
    It must be ready to append the packages list.

    - pmconf: tuple: name of pm, dict with conf (file, pacman, etc).

    Return: a cmd ready to run (str).
    """
    pacman = None
    un_install = b'install'
    if rm:
        un_install = b'uninstall'
    if not pmconf:
        print(b'Package manager not found. Abort.')
        return 0
    else:
        conf = pmconf[1]
        cmd = (b'{} {} {}').format(conf.get(b'sudo', b'sudo'), conf.get(b'pacman', pmconf[0]), conf.get(un_install, un_install))
        return cmd


def run_package_manager(to_install, to_delete, pmconf):
    """Construct the command, run the right package manager.

    Install and delete packages.

    return 0 when ok, 1 when there was a pb, or nothing to install nor uninstall.
    """
    if to_install or to_delete:
        go = input(b'Install and delete packages ? [Y/n]')
        ret_rm = 0
        ret_install = 0
        if go in ('y', 'yes', 'o', ''):
            if to_delete:
                print(b'Removing...')
                cmd_rm = get_shell_cmd(pmconf, rm=True)
                if not cmd_rm:
                    return 0
                cmd_rm = (b' ').join([cmd_rm] + to_delete)
                ret_rm = os.system(cmd_rm)
            if to_install:
                cmd_install = get_shell_cmd(pmconf)
                if not cmd_install:
                    return 0
                cmd_install = (b' ').join([cmd_install] + to_install)
                print(b'Installing...')
                print(cmd_install)
                ret_install = os.system(cmd_install)
            return ret_install or ret_rm
    return 1


def filter_packages(lines):
    """Get rid of comments. Return the packages list.

    warning: it removes everything after a '#'. Do some requirement
    files use it to specify the package version ?

    """
    packages = []
    for line in lines:
        if not line.startswith(b'#') and line.strip():
            if b'#' in line:
                line = line.split(b'#')[0]
            packages.append(line.strip())

    return packages


def read_packages(conf_file, root_dir=b''):
    """Read file root_dir/conf_file and return a list of packages (str).
    """
    conf_file = expanduser(os.path.join(root_dir, conf_file))
    lines = []
    if os.path.isfile(conf_file):
        with open(conf_file, b'r') as (f):
            lines = f.readlines()
            lines = filter_packages(lines)
    return lines


def write_packages(packages, conf_file=None, message=None, root_dir=b''):
    """Add the packages to the given conf file. Don't write duplicates.
    """
    conf_file = expanduser(os.path.join(root_dir, conf_file))
    existing = read_packages(conf_file, root_dir=root_dir)
    existing = set(existing)
    packages = set(list(packages))
    to_install = packages - existing
    already_present = packages - to_install
    to_install = list(to_install)
    for pack in already_present:
        print((b"'{}' is already present").format(pack))

    if to_install:
        if os.path.isfile(conf_file):
            lines = []
            for pack in to_install:
                if message:
                    try:
                        lines.append((b'{} \t# {}\n').format(pack, message))
                    except UnicodeDecodeError:
                        message = message.decode(b'utf8')
                        lines.append((b'{} \t# {}\n').format(pack, message))

                    message = None
                else:
                    lines.append((b'{}\n').format(pack))

            with open(conf_file, b'a') as (f):
                f.writelines(lines)
                print((b"Added '{}' to {} package list...").format((b' ').join(to_install), conf_file))
                return 0
        else:
            print((b"mmh... the config file doesn't exist: {}").format(conf_file))
            exit(1)
    return


def erase_packages(packages, conf_file=None, message=None, root_dir=b''):
    conf_file = expanduser(os.path.join(root_dir, conf_file))
    if os.path.isfile(conf_file):
        with open(conf_file, b'r') as (f):
            lines = f.readlines()
            erased = []
            for pack in packages:
                lines = [ line for line in lines if not line.startswith(pack) ]

        with open(conf_file, b'w') as (f):
            f.writelines(lines)
            print((b'Removed {} from {} package list.').format((b', ').join(packages), conf_file))


def check_file_and_get_package_list(afile, create_cache=False, root_dir=b''):
    """From a given file, read its package list.
    Create the cache file if appropriate.
    """
    packages = []
    fullfile = expanduser(join(CONF, afile))
    if os.path.isfile(fullfile):
        with open(fullfile, b'rt') as (f):
            lines = f.readlines()
        packages = filter_packages(lines)
    else:
        if create_cache:
            pkgname = colored((b'{}').format(join(root_dir, afile)), b'blue')
            print((b"No cache found for {}. Let's create one.").format(pkgname))
            return cache_init(afile, root_dir=root_dir)
        else:
            print((b"We don't find the package list at {}.\n").format(join(root_dir, afile)))
            return

    return packages


def copy_file(curr_f, cached_f):
    shutil.copyfile(curr_f, cached_f)


def sync_packages(pmconf, root_dir=b''):
    """Install or delete packages.

    - pmconf: tuple of a package manager config: pmconf[0] is the pm,
      pmconf[1] a dict with 'file', 'install', 'pacman' etc.

    return: a return code (int).

    """
    ret = 0
    conf = addict.Dict(pmconf[1])
    cached_f = expanduser(join(CONF, conf.file))
    cached_f_list = check_file_and_get_package_list(conf.file, create_cache=True, root_dir=root_dir)
    curr_list = []
    curr_f = expanduser(join(root_dir, conf.file))
    curr_list = check_file_and_get_package_list(curr_f)
    if curr_list is None:
        return 1
    else:
        to_install, to_delete = get_diff(cached_f_list, curr_list)
        print(b'In ' + colored((b'{}:').format(conf.file), b'blue'))
        if not len(to_install) and not len(to_delete):
            print(colored(b'\t✔ nothing to do', b'green'))
        else:
            if len(to_install):
                txt = (b'\tFound {} packages to install: {}').format(len(to_install), (b', ').join(to_install))
                txt = colored(txt, b'green')
            else:
                txt = b'\tNothing to install'
            print(txt)
            if len(to_delete):
                txt = (b'\tFound {} packages to delete: {}').format(len(to_delete), to_delete)
                txt = colored(txt, b'red')
            else:
                txt = b'\tNothing to delete'
            print(txt)
            ret = run_package_manager(to_install, to_delete, pmconf)
            if ret == 0:
                print(b'copying cache of %s' % curr_list)
                copy_file(curr_f, cached_f)
        return ret


def check_conf_dir(conf=CONF, create_venv_conf=False):
    """If config directory doesn't exist, create it.
    """
    if not os.path.exists(expanduser(conf)):
        os.makedirs(expanduser(conf))
        print((b'Config directory created at {}').format(conf))


def get_conf_file(pacman):
    """Return the configuration file of the given package manager.
    """
    conf = REQUIREMENTS_FILES.get(pacman.lower())
    if not conf:
        print((b'The {} package manager is unknown. Choice is one of: {}').format(pacman.lower(), (b', ').join(REQUIREMENTS_FILES.keys())))
        exit(1)
    conf = conf.get(b'file')
    if not conf:
        print(b'There is no configuration file for this package manager. Abort.')
        return None
    else:
        return conf


def run_editor(root_dir, conf_file):
    conf = expanduser(os.path.join(root_dir, conf_file))
    cmd = (b' ').join([os.environ.get(b'EDITOR'), conf])
    ret = os.system(cmd)
    return ret


@annotate(pm=b'p', message=b'm', dest=b'd', editor=b'e')
@kwoargs(b'pm', b'message', b'dest', b'rm', b'editor')
def main(pm=b'', message=b'', dest=b'', rm=False, editor=False, *packages):
    """syp will check what's new in your config files, take the
    arguments into account, and it will install and remove packages
    accordingly. It uses a cache in ~/.syp/.

    pm: set the package manager, according to your settings. If not specified, it will work on all of them.

    message: comment to be written in the configuration file.

    dest: <not implemented>

    rm: remove the given packages. If no package is specified, call $EDITOR on the configuration file.

    editor: call your shell's $EDITOR to edit the configuration file associated to the given package manager, before the rest.

    XXX: give a list of available pacman.

    Tweak your settings in ~/syp/settings.py.
    """
    CFG_FILE = b'~/.syp/settings.py'
    cfg_file = expanduser(CFG_FILE)

    def signal_handler(signal, frame):
        print(b'')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)
    if os.path.isfile(cfg_file):
        with open(cfg_file, b'rb') as (fd):
            user_config = fd.read()
        exec_(user_config, globals(), locals())
    root_dir = locals().get(b'REQUIREMENTS_ROOT_DIR') or REQUIREMENTS_ROOT_DIR
    requirements = locals().get(b'REQUIREMENTS_FILES') or REQUIREMENTS_FILES
    req_files = requirements.items()
    if pm:
        req_files = [ tup for tup in req_files if tup[0] == pm ]
        print((b"Let's use {} to install packages {} !").format(pm, (b' ').join(packages)))
        conf_file = get_conf_file(pm)
        if not conf_file:
            exit(1)
        if editor:
            run_editor(root_dir, conf_file)
        if not rm:
            write_packages(packages, message=message, conf_file=conf_file, root_dir=root_dir)
        else:
            if not packages:
                conf = expanduser(os.path.join(root_dir, conf_file))
                cmd = (b' ').join([os.environ.get(b'EDITOR'), conf])
                ret = os.system(cmd)
            erase_packages(packages, message=message, conf_file=conf_file, root_dir=root_dir)
        print((b'Syncing {} packages...').format(pm.lower()))
    if dest:
        print(b'destination to write: ', dest)
        exit
    check_conf_dir()
    ret_codes = []
    for req_file in req_files:
        ret_codes.append(sync_packages(req_file, root_dir=root_dir))

    exit(reduce(operator.or_, ret_codes, 0))


def run():
    exit(clize.run(main))


if __name__ == b'__main__':
    exit(clize.run(main))