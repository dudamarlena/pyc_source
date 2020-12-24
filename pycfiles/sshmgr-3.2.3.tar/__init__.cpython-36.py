# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bugnofree/DevSpace/sshmgr/src/__init__.py
# Compiled at: 2019-04-25 01:16:07
# Size of source mod 2**32: 5777 bytes
from .ssh import SSH
import argparse, os, sys

def get_version():
    ROOT = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(ROOT, '__VERSION__'), 'r') as (_):
        return _.readline().strip()


def parse_docker_cmd(args):
    if not args.hosts:
        print('Require hosts parameters!')
        return
    hosts = list()
    for h in args.hosts:
        if h.startswith('@'):
            h = os.path.expanduser(h[1:])
            if os.path.exists(h):
                with open(h, 'r') as (_):
                    lines = _.readlines()
                    hosts += [l.strip('\n') for l in lines]
        else:
            if len(h.split('..')) == 2:
                beg, end = h.split('..')[0], h.split('..')[1]
                for i in range(int(beg), int(end) + 1, 1):
                    hosts.append(f"{str(i):>0{len(beg)}}")

            else:
                hosts.append(h)

    for curhost in hosts:
        haserr = False
        ssh = None
        try:
            if args.enable_nvidia:
                ssh = SSH(curhost, docker='nvidia-docker')
            else:
                ssh = SSH(curhost, docker='docker')
        except Exception as e:
            print(str(e))
            print(f"{curhost} Connection Error! Skipped!")
            haserr = True

        if haserr:
            continue
        if args.new:
            dckrinfo, ok = ssh.newdckr((args.new), portnum=3, dockerfile=(args.fdocker))
            if ok:
                dckrinfo or print('[*] Cannot get the user inforamtion !')
            else:
                infomsg = "Now you can use 'ssh {user:s}@{ip:s} -p {sshport:d}' and password '{psd:s}' to login.".format(user=(dckrinfo['user']),
                  ip=(dckrinfo['ip']),
                  sshport=(dckrinfo['sshport']),
                  psd=(dckrinfo['psd']))
                print(infomsg)
                if len(dckrinfo['xport']) > 0:
                    portstr = ','.join([str(i) for i in dckrinfo['xport']])
                    print('Your extra available ports are: {xport:s}'.format(xport=portstr))
                else:
                    ssh.deldckr(args.new)
                    print('Cannot make docker for the user!')
        else:
            if args.delete:
                print(f"[+] Removing docker of {args.delete} ... ", end='')
                try:
                    if ssh.deldckr(args.delete):
                        print('[OK]')
                    else:
                        print('[X]')
                except Exception as e:
                    print('[x]')
                    print(f"ERROR: {str(e)}")

            if args.query:
                userinfo = ssh.get_userinfo(args.query)
                if userinfo is not None:
                    print(f"User             name: {userinfo['user']}")
                    print(f"User           xports: {userinfo['xport']}")
                    print(f"User         SSH port: {userinfo['sshport']}")
                    print(f"User default password: {userinfo['psd']}")
                else:
                    print(f"User {args.query} does not exist!")
            else:
                if args.list:
                    users = ssh.get_userinfo()
                    if users is not None:
                        for user in users.keys():
                            print(users[user])

                    else:
                        print('[!] No user found!')


def main():
    parser = argparse.ArgumentParser(prog='sshmgr', description='A powerful linux server manager')
    parser.add_argument('-v', '--version', action='version', version=(get_version()), help='Show the version of sshmgr')
    parser.add_argument('--hosts', metavar='hosts', type=str, help='The host(s) to be operated on')
    parser.add_argument('--sshkey', type=str, metavar='path_of_the_new_ssh_key', help='Update ssh key for administrator')
    subparsers = parser.add_subparsers(dest='has_docker_cmd')
    docker_cmd_parser = subparsers.add_parser('docker')
    docker_args_group = docker_cmd_parser.add_mutually_exclusive_group(required=True)
    docker_args_group.add_argument('--new', type=str, metavar='username',
      action='store',
      help='The user to add')
    docker_args_group.add_argument('--delete', type=str, metavar='username',
      action='store',
      help='The user to delete')
    docker_args_group.add_argument('--query', type=str, metavar='username',
      action='store',
      help='Query the information of username')
    docker_args_group.add_argument('--list', action='store_true', help='List all users in the host.')
    docker_cmd_parser.add_argument('--fdocker', metavar='dockerfile', type=str,
      action='store',
      default='',
      help='The file path to dockerfile, the first line of the file must be `FROM ubuntu:16.04`')
    docker_cmd_parser.add_argument('--nvidia', action='store_true',
      dest='enable_nvidia',
      help='Enable gpu based nvidia docker')
    docker_cmd_parser.add_argument('--himsg', metavar='hello_message', type=str,
      help='Messages showed after your guest logined into the server')
    args = parser.parse_args()
    if args.has_docker_cmd:
        parse_docker_cmd(args)
    else:
        if args.sshkey:
            ok = ssh.change_sshkey(args.sshkey)
            if ok:
                print(f"[OK] Change ssh key for {curhost} successfully!")
            else:
                print(f"[x] Some error happend when changed ssh key for {curhost}!")
        else:
            parser.print_usage()


if __name__ == '__main__':
    main()