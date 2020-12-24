# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/recompute/cmd.py
# Compiled at: 2019-03-23 11:20:41
# Size of source mod 2**32: 4686 bytes
"""cmd.py

Unorganized messy blob of commands.

TODO
----
This definitely requires better organization.
Commands in string format should be replaced with functions with arguments for formatting the command.

"""
PIP_REQS = 'pipreqs . --force'
GPU_FREE_MEMORY = 'nvidia-smi     --query-gpu=memory.free     --format=csv,nounits,noheader'
DISK_FREE_MEMORY = 'free -m'
JUPYTER_SERVER = 'jupyter-notebook --no-browser --port={port_num}    --NotebookApp.token="" .'
SSH_HEADER = 'sshpass -p {password}'
JUPYTER_CLIENT = SSH_HEADER + ' ' + 'ssh -N -L     {client_port_num}:localhost:{server_port_num}     {username}@{host}'
PROCESS_LIST_LINUX = 'ps axf | grep re.runner | grep -v grep'
PROCESS_LIST_OSX = 'ps aux | grep re.runner | grep -v grep'
PROCESS_PID_LINUX = 'ps -aux | grep {pid}'
KILL_PROCESS = 'kill -9 {}'
SCP_FROM_REMOTE = 'scp -r {username}@{host}:{remotepath} {localpath}'
SCP_TO_REMOTE = 'scp -r {localpath} {username}@{host}:{remotepath}'
RSYNC = 'rsync -a --files-from={deps_file} .         {username}@{host}:{remote_dir}'
SSH_EXEC = "ssh {username}@{host} '{cmd}'"
SSH_EXEC_PSEUDO_TERMINAL = "ssh -t {username}@{host} '{cmd}'"
SSH_EXEC_ASYNC = "ssh {username}@{host} 'nohup {cmd} > {logfile}     2>{logfile} & echo $!'"
__SSH_INTO_REMOTE_DIR = 'ssh -t {username}@{host}             "cd {remote_dir}; exec \\$SHELL --login"'
SSH_INTO_REMOTE_DIR = SSH_HEADER + ' ' + __SSH_INTO_REMOTE_DIR
SSH_MAKE_DIR = 'ssh {username}@{host} mkdir -p {remote_dir}'
SSH_TEST = "ssh {username}@{host} 'exit'"
CMD_LOG_FOOTER_ASYNC = ' > {logfile} 2>{logfile} &'
CMD_LOG_FOOTER = ' > {logfile} 2>{logfile}'
LAST_MODIFIED = 'date -r {filename}'
CD = 'cd {path}'
TRAP = 'trap "kill 0" SIGINT'
REDIRECT_STDOUT = '{command} > {logfile} 2>&1'
REDIRECT_STDOUT_NULL = '{command} > /dev/null 2>&1'
WAIT = 'wait'
EXEC_RUNNER = 'bash {runner}'
TRAP_INT_TERM = 'trap "exit" INT TERM'
TRAP_EXIT = 'trap "kill 0" EXIT'

def make_wget(urls):
    """Download multiple URLs with `wget`

  Parameters
  ----------
  urls : list
    A list of URLs to download from
  """
    return 'wget -c {}'.format(' '.join(urls))


def make_traps():
    """Return a list of traps.

  We place these traps, one in a line, in the `runner` script.
  """
    return [
     TRAP_INT_TERM, TRAP_EXIT]


def kill_procs(pids):
    """ Kill a list of processes using their PIDs

  Parameters
  ----------
  pids : list
    A list of process id's (processes that ought to be killed)
  """
    return ' '.join(['kill -9'] + [str(pid) for pid in pids])