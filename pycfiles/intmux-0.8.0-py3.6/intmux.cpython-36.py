# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/scripts/intmux.py
# Compiled at: 2019-12-06 11:43:22
# Size of source mod 2**32: 4026 bytes
import argparse, logging, posix, sys
from . import tmux
logger = logging.getLogger('intmux')

def add_docker_options(subparser, include_hosts=True):
    subparser.add_argument('--docker-command',
      '-dc', default='exec -it {} bash', help="Docker command to execute (default: 'exec -it {} bash'). If '{}' is included in the command, the docker host is substituted there, the host is appended. NOTE: may invalidate any --script/--command parameters if a shell is not provided.")
    subparser.add_argument('--approximate',
      '-a', action='store_true', help='Include any docker container names that only partially match hosts.')
    if include_hosts:
        subparser.add_argument('hosts',
          nargs='*', help='List of docker containers to connect to (default: connect to all containers)')


def add_ssh_options(subparser):
    subparser.add_argument('--ssh-command',
      '-sc', default='ssh', help='SSH command (default: ssh)')
    subparser.add_argument('--ssh-options',
      '-so', default='', help='Options to pass to SSH connection.')
    subparser.add_argument('hosts', nargs='*', help='SSH hosts to connect to.')


def main():
    parser = argparse.ArgumentParser(description='Connect to several hosts in a tmux session.')
    parser.add_argument('--log',
      '-l', default='WARN', help='Log level (default: WARN)')
    parser.add_argument('--command',
      '-c', default='', help='Command to execute when connecting to a remote host')
    parser.add_argument('--input',
      '-i', type=(argparse.FileType('r')), default=None, help='Read list of hosts from input file when provided.')
    parser.add_argument('--script',
      '-s', default='', help='Execute commands in local file remotely (executes over --command option)')
    parser.add_argument('--tmux-panes',
      '-p', default=6, type=int, metavar='PANES', help='Max tmux panes per window (default: 6)')
    parser.add_argument('--tmux-no-sync',
      '-S', action='store_true', help="Do not run tmux's set-option synchronize-panes")
    parser.add_argument('--tmux-session',
      '-t', default='intmux', metavar='SESSION', help='tmux session name (default: intmux)')
    subparsers = parser.add_subparsers(help='sub-command help', dest='subcommand')
    ssh_parser = subparsers.add_parser('ssh',
      help='Connect to hosts via SSH', description='Connect to the provided hosts (or read from STDIN).')
    add_ssh_options(ssh_parser)
    docker_parser = subparsers.add_parser('docker',
      help="Connect to docker containers via 'docker exec'", description='Connect to the provided running containers (or read from STDIN).')
    add_docker_options(docker_parser)
    ssh_docker_parser = subparsers.add_parser('ssh-docker',
      help='Connect to docker containers on remote SSH hosts', description='Connect to docker containers on provided SSH hosts (or read from STDIN).')
    add_ssh_options(ssh_docker_parser)
    ssh_docker_parser.add_argument('--docker-containers',
      '-dC', help='Comma separated list of docker containers to connect to (default: connect to all containers)')
    add_docker_options(ssh_docker_parser, include_hosts=False)
    composer_parser = subparsers.add_parser('compose',
      help="Connect to docker containers associated with current docker-compose via 'docker exec'", description='Connect to containers associated with the docker-compose in the current directory.')
    add_docker_options(composer_parser)
    args = parser.parse_args()
    logging.basicConfig(level=(getattr(logging, args.log)))
    if not args.subcommand:
        print('You must supply a subcommand.')
        sys.exit(posix.EX_USAGE)
    session = tmux.TmuxSession(args)
    session.connect()