# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bugnofree/DevSpace/sshmgr/src/ssh.py
# Compiled at: 2019-07-24 00:46:07
# Size of source mod 2**32: 15171 bytes
import os, sys, random, time, json, paramiko
from . import docker_general

class SSH:
    __doc__ = 'Manage the user with ssh key'

    def __init__(self, hostid, dockerprog='docker', **kwargs):
        """
        :docker -> str: The command to fireup docker program.
            For example, to start the normal docker command, you run `docker`,
            to start nvida-docker2, you run `nvidid-docker`.
        """
        self.hostid = hostid
        self.hostip = ''
        self.dockerdb = '/root/dockerdb/userdb.json'
        self.sshconf = os.path.expanduser('~/.ssh/config')
        self.docker = dockerprog
        if not os.path.exists(self.sshconf):
            print(f"[x] No config file found in {self.sshconf}!")
            sys.exit(1)
        try:
            self.conn = self._SSH__connect()
        except Exception as e:
            strerr = str(e)
            if 'invalid key' in strerr.lower():
                raise Exception('Invalid key! Make sure your private key is in PEM format!')
            else:
                raise Exception(f"Cannot connect to the server! Error => {strerr}")

    def connect(self):
        conn = self._SSH__connect()
        return conn

    def __connect(self):
        config = paramiko.SSHConfig()
        with open(self.sshconf, 'r') as (_):
            config.parse(_)
        hostopt = config.lookup(self.hostid)
        cfg = dict()
        if 'include' in hostopt:
            with open(os.path.expanduser(hostopt['include']), 'r') as (_):
                config.parse(_)
                hostopt = config.lookup(self.hostid)
        else:
            cfg['hostname'] = hostopt['hostname']
            cfg['username'] = hostopt['user']
            if 'port' in hostopt.keys():
                cfg['port'] = hostopt['port']
            else:
                cfg['port'] = 22
        cfg['key_filename'] = hostopt['identityfile']
        cfg['timeout'] = 10
        if 'proxycommand' in hostopt:
            cfg['sock'] = paramiko.ProxyCommand(hostopt['proxycommand'])
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        (ssh.connect)(**cfg)
        self.hostip = hostopt['hostname']
        return ssh

    def getport(self):
        busy, free = set(), set(range(65536))
        conn = self._SSH__connect()
        stdin, stdout, stderr = conn.exec_command('netstat -lnptu')
        ipports = [l.split()[3] for l in stdout.readlines()[2:]]
        for ipport in ipports:
            busy.add(int(ipport.split(':')[(-1)]))

        free -= busy
        conn.close()
        return (busy, free)

    def rndport(self, num, specport=None, start=1, end=65536):
        """Random select port number

        :param num (int): The number of random ports.
        :param specport (list of ints): (optional) The must having ports in radmom generated ports.
        :return ports (list), status (bool):
        """
        if specport is None:
            specport = list()
        if len(specport) > num:
            print('[x] The specified ports number should less or equal to the total number of ports.')
            return (None, False)
        else:
            for p in specport:
                if p < start or p >= end:
                    print('[x] The specified port is not in range!')
                    return (None, False)

            busy, free = self.getport()
            takenports = busy & set(specport)
            if len(takenports) > 0:
                msg = ','.join([str(takenport) for takenport in takenports])
                print('[!] The following ports have been taken {:s}.'.format(msg))
                return (None, False)
            satport = [i for i in free if i >= start if i < end]
            for p in specport:
                if p in satport:
                    satport.remove(p)

            ports = list()
            for i in range(num - len(specport)):
                port = random.choice(satport)
                satport.remove(port)
                ports.append(port)

            ports.extend(specport)
            return (ports, True)

    def newuser(self, user, shell='/bin/false'):
        flag = True
        conn = self._SSH__connect()
        cmd = 'useradd -d /home/{user:s} -m -s {shell:s} {user}'.format(user=user, shell=shell)
        stdin, stdout, stderr = conn.exec_command(cmd)
        conn.close()
        return flag

    def is_user_exist(self, user):
        conn = self._SSH__connect()
        cmd = 'cat /etc/passwd | grep {user:s}: | wc -l'.format(user=(user.strip()))
        stdin, stdout, stderr = conn.exec_command(cmd)
        lines = stdout.readlines()
        cnt = int(lines[0])
        conn.close()
        if cnt == 0:
            return False
        else:
            return True

    def hasimage(self, user):
        conn = self._SSH__connect()
        cmd = f"{self.docker} image ls {self.hostid}:{user} | wc -l"
        i, o, e = conn.exec_command(cmd)
        lines = o.readlines()
        cnt = int(lines[0])
        conn.close()
        if cnt >= 2:
            return True
        else:
            return False

    def get_dckrjar_list(self, user):
        conn = self._SSH__connect()
        cmd = f"{self.docker} ps -a | grep {self.hostid}:{user}"
        i, o, e = conn.exec_command(cmd)
        lines = [l.strip('\n') for l in o.readlines()]
        jar = list()
        for line in lines:
            jar.append(line.split()[(-1)])

        conn.close()
        return jar

    def deldckr(self, user):
        conn = self._SSH__connect()
        if self.is_user_exist(user):
            if self.hasimage(user):
                for jar in self.get_dckrjar_list(user):
                    i, o, e = conn.exec_command(f"{self.docker} stop {jar} && {self.docker} rm {jar}")
                    o.channel.recv_exit_status()

                i, o, e = conn.exec_command(f"{self.docker} rmi {self.hostid}:{user}")
                o.channel.recv_exit_status()
        if self.is_file_exist(self.dockerdb):
            sftp = conn.open_sftp()
            fuserdb = sftp.file(self.dockerdb, 'r')
            userdb = json.load(fuserdb)
            fuserdb.close()
            if user in userdb.keys():
                del userdb[user]
            fuserdb = sftp.file(self.dockerdb, 'w')
            json.dump(userdb, fuserdb)
            fuserdb.close()
            sftp.close()
        i, o, e = conn.exec_command(f"yes | {self.docker} image prune")
        o.channel.recv_exit_status()
        i, o, e = conn.exec_command(f"yes | {self.docker} contanier prune")
        o.channel.recv_exit_status()
        conn.close()
        return True

    def newdckr(self, user, apt, himsg, dockerfile, portnum=0, specport=None):
        """Create a docker for user

        :param user (string): The user name.
        :param apt (string): The apt source type.
        :param himsg (string): The hello message showed afer login in.
        :dockerfile -> str: The path to docker file.
        :param portnum (int): The number of exposed ports.
        :param specport (list of ints): The specified ports in random generated ports.

        return dckrinfo (dict), status (bool):
            dckrinfo:
                - user (string): The user name
                - sshport (int): The ssh connection port.
                - xport (list): The extra exposed ports.
                - ip (string): The connection ip address.
                - psd (string): The user password.
        """
        conn = self._SSH__connect()
        conn.exec_command(f"mkdir -p {os.path.dirname(self.dockerdb)}")
        i, o, e = conn.exec_command(f"hash {self.docker} 2>/dev/null && echo 1")
        output = o.readlines()
        lines = [l.strip('\n') for l in output]
        if len(lines) == 0:
            print(f"[x] Please install {self.docker} first!")
            conn.close()
            return (None, False)
        if specport is None:
            specport = list()
        dckrinfo = dict()
        dckrinfo['user'] = user
        dckrinfo['xport'] = list()
        portnum += 1
        dckrinfo['ip'] = self.hostip
        if self.hasimage(user):
            print('[!] Docker for the user is existed!')
            return (self.get_userinfo(user), True)
        rndports, status = self.rndport(portnum, specport)
        if status is False:
            print('[x] Cannot listenning ports!')
            conn.close()
            return (None, False)
        dckrinfo['sshport'] = rndports[0]
        exposed_ports = ' --publish {port:d}:22 '.format(port=(rndports[0]))
        for p in rndports[1:]:
            dckrinfo['xport'].append(p)
            exposed_ports += ' --publish {port:d}:{port} '.format(port=p)

        if not self.is_user_exist(user):
            self.newuser(user)
        user_dockerfile_content = ''
        if dockerfile:
            with open(dockerfile, 'r') as (_):
                firstline = _.readline().strip()
                if firstline.startswith('FROM ubuntu:16.04'):
                    user_dockerfile_content = _.read()
                else:
                    print('[x] The docker file is not supported!')
                    return (None, False)
        finish_build = docker_general.build(conn, dockerprog=(self.docker), user=user,
          hostid=(self.hostid),
          content=user_dockerfile_content,
          apt=apt,
          himsg=himsg)
        if finish_build == False:
            return (None, False)
        conn.exec_command(f"mkdir -p /home/{user}/share")
        dckrun = '{docker:s} run --hostname={hostid:s} --name {user:s} --volume /home/{user}/share:/home/{user}/share'.format(docker=(self.docker),
          hostid=(self.hostid),
          user=user)
        dckrun += exposed_ports
        dckrun += ' -d {hostid:s}:{user:s} '.format(hostid=(self.hostid), user=user)
        print('[+] {}'.format(dckrun))
        stdin, stdout, stderr = conn.exec_command(dckrun)
        err = stdout.channel.recv_exit_status()
        if err:
            print('[x] docker run failed!')
            conn.close()
            return (None, False)
        dckrperm = f"{self.docker} exec -i {user} chown -R {user}:{user} /home/{user}/share"
        print('[+] {}'.format(dckrperm))
        stdin, stdout, stderr = conn.exec_command(dckrperm)
        err = stdout.channel.recv_exit_status()
        if err:
            print('[x] Cannot change share folder permission!')
            conn.close()
            return (None, False)
        else:
            i, o, e = conn.exec_command(f"{self.docker} exec -i {user} cat /home/{user}/.defpsd")
            if o.channel.recv_exit_status():
                print('[x] Cannot retrieve default password!')
                print(f"[ERROR] {e.readlines()}")
                conn.close()
                return (None, False)
            lines = o.readlines()
            dckrinfo['psd'] = lines[0].strip('\n')
            self.set_userinfo(user, dckrinfo)
            conn.close()
            return (dckrinfo, True)

    def set_userinfo(self, user, userinfo):
        conn = self._SSH__connect()
        sftp = conn.open_sftp()
        userdb = dict()
        if self.is_file_exist(self.dockerdb):
            fuserdb = sftp.file(self.dockerdb, 'r')
            userdb.update(json.load(fuserdb))
            fuserdb.close()
        userdb[user] = userinfo
        fuserdb = sftp.file(self.dockerdb, 'w')
        json.dump(userdb, fuserdb)
        fuserdb.close()
        sftp.close()
        conn.close()

    def is_file_exist(self, path):
        conn = self._SSH__connect()
        sftp = conn.open_sftp()
        status = True
        try:
            sftp.stat(path)
        except IOError:
            status = False

        sftp.close()
        conn.close()
        return status

    def get_userinfo(self, user=None):
        """Get one or all user hosted in the host"""
        conn = self._SSH__connect()
        sftp = conn.open_sftp()
        if not self.is_file_exist(self.dockerdb):
            return
        fuserdb = sftp.file(self.dockerdb, 'r')
        userdb = json.load(fuserdb)
        sftp.close()
        conn.close()
        if user is None:
            return userdb
        else:
            if user in userdb.keys():
                return userdb[user]
            return

    @staticmethod
    def getoutput(conn, cmd):
        i, o, e = conn.exec_command(cmd)
        err = o.channel.recv_exit_status()
        if err:
            return (None, False)
        else:
            output = o.readlines()
            lines = [l.strip('\n') for l in output]
            return (lines, True)

    def gethome(self):
        conn = self._SSH__connect()
        homes, ok = self.getoutput(conn, 'readlink -f ~')
        home = None
        if ok:
            home = homes[0]
        conn.close()
        return home

    def change_passwd(self, newpasswd):
        pass

    def change_sshkey(self, key):
        """Change user ssh

        :key (str): The path to load or save ssh key.
        """
        conn = self._SSH__connect()
        sftp = conn.open_sftp()
        home = self.gethome()
        haserr = False
        if home is not None:
            key = os.path.expanduser(key)
            if not os.path.exists(key):
                print('[x] Cannot find key in the given path!')
                haserr = True
        elif not key.endswith('.pub'):
            print('[x] Not a public ssh key!')
            haserr = True
        else:
            if not haserr:
                with open(key, 'r') as (fkey):
                    with sftp.file(f"{home}/.ssh/authorized_keys", 'w') as (_):
                        _.write(fkey.read())
            else:
                print('[x] Cannot get home path!')
                haserr = True
        sftp.close()
        conn.close()
        if haserr:
            return False
        else:
            return True


def add_sshkey_by_passwd(ip, user, passwd):
    pass