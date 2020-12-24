# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/procedures/misc.py
# Compiled at: 2018-01-10 00:48:14
# Size of source mod 2**32: 3292 bytes
import logging, subprocess
from mercury_agent.capabilities import capability
from mercury.common.helpers.cli import run
from mercury.common.helpers.util import download_file
log = logging.getLogger(__name__)

@capability('echo', 'Echo something to the console', num_args=1)
def echo(message):
    """
    Echo the dolphin
    :param message: message to Echo
    :return: None
    """
    log.info('Echo: %s' % message)
    print(message)
    return message


@capability('run', 'Run an arbitrary command', num_args=1)
def runner(command, _input=''):
    """
    Run a shell command
    :param command: The shell command to use
    :param _input: Optional data to pass to stdin
    :return:
    """
    log.info('Running: %s' % command)
    r = run(command, ignore_error=True, raise_exception=False, _input=_input)
    return {'stdout':r.stdout, 
     'stderr':r.stderr, 
     'returncode':r.returncode}


@capability('run_async', 'Run a command in the background', num_args=1)
def runner_async(command, shell=True):
    """
    
    :param command: 
    :param shell:
    :return: 
    """
    subprocess.Popen(('{}'.format(command)), shell=shell)


@capability('kexec', 'kexec into kernel at supplied location', kwarg_names=['kernel', 'initrd', 'options'], no_return=True,
  serial=True)
def kexec(kernel='', initrd='', options=None, kernel_type='bzImage'):
    """
    Kexec into a kernel
    """
    options = options or []
    command = 'kexec --type {kernel_type} --initrd={initrd} --append="{options}" {kernel}'.format(kernel_type=kernel_type,
      initrd=initrd,
      options=(' '.join(options)),
      kernel=kernel)
    log.info('Running Kexec: {}'.format(command))
    runner_async('sleep 5;' + command)


@capability('reload', 'kexec into current preboot kernel, re-downloading the root file system', num_args=2)
def reload(kernel_url, initrd_url):
    """
    Reload the environment
    """
    kernel_file = '/tmp/vmlinuz'
    initrd_file = '/tmp/initrd'
    log.info('Downloading: {}'.format(kernel_url))
    download_file(kernel_url, kernel_file)
    log.info('Downloading: {}'.format(initrd_url))
    download_file(initrd_url, initrd_file)
    with open('/proc/cmdline') as (fp):
        options = fp.readline().split()
    kexec(kernel=kernel_file, initrd=initrd_file, options=options)