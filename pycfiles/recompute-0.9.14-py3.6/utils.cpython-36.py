# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/recompute/utils.py
# Compiled at: 2019-03-23 12:45:40
# Size of source mod 2**32: 3781 bytes
"""utils.py : A suite of helper functions"""
from prettytable import PrettyTable
import os, logging, random
LOCAL_CONFIG_DIR = '.recompute'
if not os.path.exists(LOCAL_CONFIG_DIR):
    os.makedirs(LOCAL_CONFIG_DIR)
LOG = '.recompute/log'
LOG_OVERFLOW = 2000

def get_logger(name, level=logging.INFO):
    """Configure logging mechanism and return logger instance

  Parameters
  ----------
  name : str
    module name (__name__)
  level : int, optional
    Level of logging (default logging.INFO)

  Returns
  -------
  logging.Logger
    A logger instance
  """
    if not os.path.exists(LOG) or len(open(LOG).readlines()) > LOG_OVERFLOW:
        open(LOG, 'w').close()
    logging.basicConfig(filename=LOG, filemode='a', level=level)
    return logging.getLogger(name)


logger = get_logger(__name__)

def parse_log(log):
    """Parse log

  Parameters
  ----------
  log : str
    Contents of log file

  Returns
  -------
  str
    Parsed log file
  """
    return log


def tabulate_processes(processes):
    """Convert list of processes into a Pretty Table

  Parameters
  ----------
  processes : list
    List of processes (name, pid)

  Returns
  -------
  PrettyTable
    A table of processes
  """
    table = PrettyTable()
    table.field_names = ['Index', 'Name', 'PID']
    table.add_row((0, 'all', '*'))
    for idx, (name, pid) in enumerate(processes):
        table.add_row((idx + 1, name, pid))

    return table


def tabulate_instances(instances):
    """Convert a dictionary of instances into a Pretty Table

  Parameters
  ----------
  instances : dict
    Dictionary of instances

  Returns
  -------
  PrettyTable
    A table of instances
  """
    table = PrettyTable()
    table.field_names = [
     'Machine', 'Status', 'GPU (MB)', 'Disk (MB)']
    for instance, values in instances.items():
        table.add_row(values)

    return table


def resolve_relative_path(filename, path):
    """Convert relative path to absolute"""
    return os.path.join(path, filename)


def resolve_absolute_path(filename):
    """Fetch filename from absolute path"""
    return filename.split('/')[(-1)]


def chain_commands(commands):
    """Chain commands together using `&&` "and" operator

  Parameters
  ----------
  commands : list
    A list of commands to be chained together

  Returns
  -------
  str
    Chained command
  """
    if isinstance(commands, type('42')):
        commands = commands.split('&&')
    root = commands[0]
    subseq = ['exec {}'.format(command) for command in commands[1:]]
    return root + ' ' + ' && '.join(subseq)


def parse_ps_results(stdout):
    """Parse result of `ps` command

  Parameters
  ----------
  stdout : str
    Output of running `ps` command

  Returns
  -------
  list
    A List of process id's
  """
    if not stdout.replace('\n', '').strip():
        return []
    else:
        return [int(line.split()[0]) for line in stdout.split('\n') if line.replace('\n', '').strip()]


def parse_free_results(stdout):
    """Parse results of `free` command

  Parameters
  ----------
  stdout : str
    Output of running `free` command

  Returns
  -------
  int
    Free Disk space
  """
    line = stdout.split('\n')[1]
    assert 'Mem:' in line
    return int(line.split()[3])


def rand_server_port(a=8824, b=8850):
    """Get a random integer between `a` and `b`"""
    return random.randint(a, b)


def rand_client_port(a=8850, b=8890):
    """Get a random integer between `a` and `b`"""
    return random.randint(a, b)