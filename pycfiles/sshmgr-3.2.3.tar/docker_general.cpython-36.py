# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bugnofree/DevSpace/sshmgr/src/docker_general.py
# Compiled at: 2019-04-25 05:14:11
# Size of source mod 2**32: 4144 bytes
import time, os, paramiko
from . import util
dckrtpl = 'FROM ubuntu:16.04\nCOPY {sourcelist:s} {init:s} {motd:s} {sprvsr:s} /tmp/\nRUN bash /tmp/{init} {user:s} /tmp/{sourcelist} /tmp/{motd} /tmp/{sprvsr} {psdlen:d}\n{content:s}\nSHELL ["/bin/bash", "-c"]\nENTRYPOINT "/usr/bin/supervisord"\n'
init = '#! /bin/bash\nuser=$1\nsourcelist=$2\nmotd=$3\nsprvsr=$4\npsdlen=$5\n\napt update && apt install -y wget ca-certificates apt-transport-https\ncat $sourcelist > /etc/apt/sources.list && apt update\nmkdir -p /$user/.ssh/ && mkdir -p /var/run/sshd && mkdir -p /var/log/supervisor\napt install -y openssh-server vim supervisor sudo locales pwgen\n\nuseradd -d /home/$user -m -s /bin/bash $user\nusermod -aG sudo $user\n\necho "LC_ALL=en_US.UTF-8" >> /etc/environment\necho "en_US.UTF-8 UTF-8" >> /etc/locale.gen\necho "LANG=en_US.UTF-8" > /etc/locale.conf\nlocale-gen en_US.UTF-8\n\nrm -rf /etc/update-motd.d/*\ncat $motd > /etc/update-motd.d/00-sshmgr-sayhello\nchmod +x /etc/update-motd.d/00-sshmgr-sayhello\n\ncat $sprvsr > /etc/supervisor/conf.d/supervisord.conf\n\npsd=$(pwgen -N 1 $psdlen) && echo "$user:$psd" | chpasswd\necho $psd > /home/$user/.defpsd\n'
motdfmt = '#! /bin/bash\necho --------------------------------------------------------------------\necho\necho "         _                          ";\necho "        | |                         ";\necho " ___ ___| |__  _ __ ___   __ _ _ __ ";\necho "/ __/ __| \'_ \\| \'_ \\` _ \\ / _\\` | \'__|";\necho "\\__ \\__ \\ | | | | | | | | (_| | |   ";\necho "|___/___/_| |_|_| |_| |_|\\__, |_|   ";\necho "                          __/ |     ";\necho "                         |___/      ";\necho\necho [Powered by sshmger, see https://github.com/ikey4u/sshmgr for more infomation]\necho\necho --------------------------------------------------------------------\necho {himsg}\necho ID: {hostid:s}:{user}\necho --------------------------------------------------------------------\n'
sprvsrfile = '[supervisord]\nnodaemon=true\n[program:sshd]\ncommand=/usr/sbin/sshd -D\n'

def build(conn: paramiko.SSHClient, **extra) -> bool:
    """Build a general docker

    :conn: An established paramiko connection.
    :extra: Extra information.
        {
            'dockerprog': The docker program.
            'user': The user name.
            'hostid': The host where the docker is built in.
            'content': The customized docker file content.
            'himsg': The hello message from the administrator.
            'apg': The apt souce type.
        }

    :return: if build successfully, return true, or else false.
    """
    tm = str(time.time())
    sftp = conn.open_sftp()
    with sftp.file(f"/tmp/{tm}.sourcelist", 'w') as (srcfile):
        with open(os.path.join(util.get_data_root(), 'ubuntu', extra['apt']), 'r') as (_):
            srcfile.write(_.read())
    with sftp.file(f"/tmp/{tm}.motd", 'w') as (_):
        _.write(motdfmt.format(himsg=(extra['himsg']), user=(extra['user']), hostid=(extra['hostid'])))
    with sftp.file(f"/tmp/{tm}.supervisord", 'w') as (_):
        _.write(sprvsrfile)
    with sftp.file(f"/tmp/{tm}.init", 'w') as (_):
        _.write(init)
    with sftp.file(f"/tmp/{tm}.dockerfile", 'w') as (_):
        dockerfile = dckrtpl.format(content=(extra['content']), sourcelist=f"{tm}.sourcelist",
          init=f"{tm}.init",
          motd=f"{tm}.motd",
          sprvsr=f"{tm}.supervisord",
          user=(f"{extra['user']}"),
          psdlen=15)
        _.write(dockerfile)
    sftp.close()
    docker_build_cmd = f"{extra['dockerprog']} build --tag {extra['hostid']}:{extra['user']} --file /tmp/{tm}.dockerfile /tmp"
    print(f"[+] {docker_build_cmd}")
    stdin, stdout, stderr = conn.exec_command(docker_build_cmd)
    err = stdout.channel.recv_exit_status()
    conn.exec_command(f"rm -rf /tmp/{tm}.*")
    if err:
        print('[x] Cannot run docker build!')
        for line in stderr.readlines():
            print(line.strip('\n'))

        conn.close()
        return False
    else:
        return True