# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hanzz/releases/odcs/server/odcs/server/mock_runroot.py
# Compiled at: 2019-05-07 00:57:40
from __future__ import print_function
import platform, sys, koji, os, uuid, tempfile
from odcs.server import conf
from odcs.server.backend import create_koji_session
from odcs.server.utils import makedirs, execute_cmd

def do_mounts(rootdir, mounts):
    """
    Mounts the host `mounts` in the Mock chroot `rootdir`.

    :param str rootdir: Full path to root directory for Mock chroot.
    :param list mounts: Full paths to mount directories which will be mounted
        in the `rootdir`.
    """
    for mount in mounts:
        mpoint = '%s%s' % (rootdir, mount)
        makedirs(mpoint)
        cmd = ['mount', '-o', 'bind', mount, mpoint]
        execute_cmd(cmd)


def undo_mounts(rootdir, mounts):
    """
    Umounts the host `mounts` from the Mock chroot `rootdir`.

    :param str rootdir: Full path to root directory for Mock chroot.
    :param list mounts: Full paths to mount directories which will be umounted
        from the `rootdir`.
    """
    for mount in mounts:
        mpoint = '%s%s' % (rootdir, mount)
        cmd = ['umount', '-l', mpoint]
        execute_cmd(cmd)


def runroot_tmp_path(runroot_key):
    """
    Creates and returns the temporary path to store the configuration files
    or logs for the runroot task.

    :param str runroot_key: The Runroot key.
    :return str: Full-path to temporary directory.
    """
    path = os.path.join(tempfile.gettempdir(), 'odcs-runroot-%s' % runroot_key)
    makedirs(path)
    return path


def execute_mock(runroot_key, args, log_output=True):
    """
    Executes the Mock command with `args` for given `runroot_key` Mock chroot.

    :param str runroot_key: Runroot key.
    :param list args: The "mock" command arguments.
    :param bool log_output: When True, stdout and stderr of Mock command are
        redirected to logs.
    """
    runroot_path = runroot_tmp_path(runroot_key)
    mock_cfg_path = os.path.join(runroot_path, 'mock.cfg')
    cmd = ['mock', '-r', mock_cfg_path] + args
    if log_output:
        stdout_log_path = os.path.join(runroot_path, 'mock-stdout.log')
        stderr_log_path = os.path.join(runroot_path, 'mock-stderr.log')
        with open(stdout_log_path, 'a') as (stdout_log):
            with open(stderr_log_path, 'a') as (stderr_log):
                execute_cmd(cmd, stdout=stdout_log, stderr=stderr_log)
    else:
        execute_cmd(cmd)


def mock_runroot_init(tag_name):
    """
    Creates and initializes new Mock chroot for runroot task.
    Prints the unique ID of chroot ("runroot_key") to stdout.

    :param str tag_name: Koji tag name from which the default packages for
        the Mock chroot are taken.
    """
    runroot_key = str(uuid.uuid1())
    koji_module = koji.get_profile_module(conf.koji_profile)
    koji_session = create_koji_session()
    repo = koji_session.getRepo(tag_name)
    if not repo:
        raise ValueError('Repository for tag %s does not exist.' % tag_name)
    opts = {}
    opts['topdir'] = koji_module.pathinfo.topdir
    opts['topurl'] = koji_module.config.topurl
    opts['use_host_resolv'] = True
    opts['package_manager'] = 'dnf'
    arch = koji.canonArch(platform.machine())
    output = koji_module.genMockConfig(runroot_key, arch, repoid=repo['id'], tag_name=tag_name, **opts)
    mock_cfg_path = os.path.join(runroot_tmp_path(runroot_key), 'mock.cfg')
    with open(mock_cfg_path, 'w') as (mock_cfg):
        mock_cfg.write(output)
    print(runroot_key)
    execute_mock(runroot_key, ['--init'])


def raise_if_runroot_key_invalid(runroot_key):
    """
    Raise an ValueError exception in case the `runroot_key` contains forbidden
    characters.
    """
    for c in runroot_key:
        if c != '-' and not c.isalnum():
            raise ValueError('Unexpected character \'%s\' in the runroot key "%s".' % (
             c, runroot_key))


def mock_runroot_install(runroot_key, packages):
    """
    Installs the `packages` in the Mock chroot defined by `runroot_key`.

    :param str runroot_key: Runroot key.
    :param list packages: List of packages to install.
    """
    raise_if_runroot_key_invalid(runroot_key)
    execute_mock(runroot_key, ['--install'] + packages)


def mock_runroot_run(runroot_key, cmd):
    """
    Executes the `cmd` in the Mock chroot defined by `runroot_key`.

    :param str runroot_key: Runroot key.
    :param list cmd: Command to execute.
    """
    raise_if_runroot_key_invalid(runroot_key)
    rootdir = '/var/lib/mock/%s/root' % runroot_key
    try:
        do_mounts(rootdir, [conf.target_dir])
        sh_wrapper = [
         '/bin/sh', '-c', '{ %s; }' % (' ').join(cmd)]
        args = [
         '--old-chroot', '--chroot', '--'] + sh_wrapper
        execute_mock(runroot_key, args, False)
    finally:
        undo_mounts(rootdir, [conf.target_dir])


def mock_runroot_main(argv=None):
    """
    Main method handling the subcommands.

    :param list argv: List of arguments. If None, sys.argv is used.
    """
    argv = argv or sys.argv
    if argv[1] == 'init':
        mock_runroot_init(argv[2])
    elif argv[1] == 'install':
        mock_runroot_install(argv[2], argv[3:])
    elif argv[1] == 'run':
        mock_runroot_run(argv[2], argv[3:])