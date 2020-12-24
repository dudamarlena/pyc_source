# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dr/Documents/code/Python/Projects/ControllProxy/seed/mrclients/controll.py
# Compiled at: 2018-05-07 01:14:09
# Size of source mod 2**32: 19989 bytes
import os, sys, argparse, getpass, zipfile
from fabric.api import execute, put, get, run, parallel
from fabric.api import env
from fabric.api import prompt
from fabric.contrib.files import exists
from io import BytesIO
from fabric.api import get
from qlib.data import Cache, dbobj
from qlib.log import L
from functools import partial
from fabric.colors import red, green, blue
from base64 import b64encode
from seed.mrpackage.test import Test
from seed.mrpackage.config import SEED_HOME
from seed.mrpackage.config import DB_PATH, LOCAL_PUB_KEY
from seed.mrpackage.config import Host, Cache
local_pub = open(LOCAL_PUB_KEY).read()
PY3_ENV = 'export PATH="$PATH:/usr/local/python3/bin" && '
srun = run
hosts_db = Cache(DB_PATH)

def add_host(host, port=22, user='root'):
    passwd = getpass.getpass()
    h = Host(host=host, passwd=passwd, port=port, user=user)
    h.save(hosts_db)


@parallel
def ssh_key():
    fd = BytesIO()
    if not exists('/root/.ssh/'):
        run("mkdir -p /root/.ssh/ && ssh-keygen -t rsa -P '' -f /root/.ssh/id_rsa")
    if not exists('/root/.ssh/id_rsa.pub'):
        run("ssh-keygen -t rsa -P '' -f '/root/.ssh/id_rsa'")
    get('/root/.ssh/id_rsa.pub', fd)
    content = fd.getvalue()
    return content.decode()


@parallel
def upload_pub_key(key_bytes):
    if not exists('/root/.ssh/authorized_keys'):
        run('touch /root/.ssh/authorized_keys')
    put((BytesIO(key_bytes)), '/root/.ssh/authorized_keys.bak', mode='0644')
    run('cat /root/.ssh/authorized_keys >> /root/.ssh/authorized_keys.bak')
    run('sort /root/.ssh/authorized_keys.bak | uniq  > /root/.ssh/authorized_keys')


@parallel
def ex(cmd):
    res = run((PY3_ENV + cmd), quiet=True)
    print(green('[+]'), blue(env.host), cmd)
    print(blue('[{}]'.format(env.host)), res)


def upload_local_pub():
    put(BytesIO(local_pub.encode()), '/root/.ssh/authorized_keys.bak')
    run('cat /root/.ssh/authorized_keys.bak >> /root/.ssh/authorized_keys')


@parallel
def change_log(log):
    if not exists('/root/.config/seed'):
        run("mkdir /root/.config/seed/ && echo 'INFO' >> /root/.config/seed/log_config")
    run(("echo '{}' >> /root/.config/seed/log_config".format(log)), quiet=True)
    run('cat /root/.config/seed/log_config')


def exchange_ssh_key(*servers):
    env.hosts += servers
    ssh = execute(ssh_key)
    authorized_keys = '\n'.join(list(ssh.values()) + [local_pub]).encode('utf8')
    execute(upload_pub_key, authorized_keys)


@parallel
def shadowsocks_start(*args):
    if not run("pip3 list 2>/dev/null | grep shadowsocks | grep -v 'grep' | xargs", quiet=True):
        ex('pip3 install shadowsocks ')
    else:
        if not exists('/etc/shadowsocks.json'):
            ss_json = '{\n    "server":"0.0.0.0",\n    "port_password": {\n        "13001": "thefoolish1",\n        "13002": "thefoolish2",\n        "13003": "thefoolish3",\n        "13004": "thefoolish4",\n        "13005": "thefoolish5",\n        "13006": "thefoolish6",\n        "13007": "thefoolish7",\n        "13008": "thefoolish8",\n        "13009": "thefoolish9",\n        "13010": "thefoolish10",\n        "13011": "thefoolish11",\n        "13012": "thefoolish12",\n        "13013": "thefoolish13"\n    },\n    "workers": 15,\n    "method":"aes-256-cfb"\n}'
            with open('/tmp/sss.json', 'w') as (fp):
                fp.write(ss_json)
            put('/tmp/sss.json', '/etc/shadowsocks.json')
        else:
            if_start = run("ps aux | grep ssserver | grep json | grep -v 'grep' | awk '{print $2}' | xargs", quiet=True)
            if not if_start.strip():
                ex(PY3_ENV + 'ssserver -c /etc/shadowsocks.json -d start')
            else:
                ex(PY3_ENV + 'ssserver -c /etc/shadowsocks.json -d restart')
        if not exists('/tmp/pids'):
            ex('mkdir /tmp/pids', quiet=True)
    run("ps aux | grep ssserver | grep json | grep -v 'grep' | awk '{print $2}' | xargs > /tmp/pids/shadowsocks_server.pid", quiet=True)


def shadowsocks_pids():
    status = run('cat /tmp/pids/shadowsocks_server.pid')
    print(red(env.host), status)


def download(file):
    if exists(file):
        if not os.path.exists('/tmp/downloads'):
            os.mkdir('/tmp/downloads')
        filename = os.path.basename(file)
        get(file, '/tmp/downloads/' + filename)


def check_python_module(module):
    res = run("pip3 list 2>/dev/null | grep {m} | grep -v 'grep' | xargs".format(m=module), quiet=True)
    if res:
        return True
    else:
        return False


@parallel
def Update(file=None):
    if file:
        if os.path.exists(file):
            put(file, '/tmp/install.zip')
            if not exists('/tmp/install.zip'):
                print('upload failed', env.host)
            if check_python_module('x-mroy-1046'):
                run('pip3 uninstall -y x-mroy-1046 2>/dev/null', quiet=True)
                L('[rm] x-mroy-1046', (env.host), color='green')
            r = run('pip3 install /tmp/install.zip 1>/dev/null 2>/dev/null  && echo 1', quiet=True)
            if r.strip() == '1':
                L('[update from local]', (env.host), color='green')
            else:
                L('[failed update]', (env.host), color='green')
            return
    run((PY3_ENV + 'pip3 uninstall -y x-mroy-1046'), quiet=True)
    run((PY3_ENV + 'pip3 install x-mroy-1046 --no-cache-dir '), quiet=True)
    r = run('pip3 list 2>/dev/null | grep x-mroy-1046 2>/dev/null', quiet=True)
    L('[ok]', r, (env.host), color='green')


@parallel
def initenv():
    sh = '\n#!/bin/bash\n#install python\n\nhash apt 2>/dev/null\nif [ $? -eq 0 ];then\n    echo "apt is existed install apt-lib"\n    apt-get install -y libc6-dev gcc\n    apt-get install -y make build-essential libssl-dev zlib1g-dev libreadline-dev libsqlite3-dev wget curl llvm\nelse\n    hash yum 2>/dev/null\n    if [ $? -eq 0 ];then\n        echo "yum is existed install yum-lib"\n        yum -y install wget gcc make epel-release\n        yum update -y\n        yum -y install zlib1g-dev bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel\n    fi\nfi\n\n\nhash python3 2>/dev/null\n    if  [ $? -eq 0 ];then\n    res=$(python3 -V 2>&1 | awk \'{print $1}\')\n    version=$(python3 -V 2>&1 | awk \'{print $2}\')\n    #echo "check command(python) available resutls are: $res"\n    if [ "$res" == "Python" ];then\n        if   [ "${version:0:3}" == "3.6" ];then\n            echo "Command python3 could be used already."\n            exit 0\n        fi\n    fi\nfi\n\necho "command python can\'t be used.start installing python3.6."\ncd /tmp\n    if [ -f /tmp/Python-3.6.1.tgz ];then\n      rm /tmp/Python-3.6.1.tgz;\n    fi\nwget https://www.python.org/ftp/python/3.6.1/Python-3.6.1.tgz\ntar -zxvf Python-3.6.1.tgz\ncd Python-3.6.1\nmkdir /usr/local/python3\n./configure --prefix=/usr/local/python3\nmake\nmake install\nif [ -f /usr/bin/python3 ];then\n   rm /usr/bin/python3;\n   rm /usr/bin/pip3;\nfi\n\nif [ -f /usr/bin/lsb_release ];then\n  rm /usr/bin/lsb_release;\nfi\n\nln -s /usr/local/python3/bin/python3 /usr/bin/python3\nln -s /usr/local/python3/bin/pip3 /usr/bin/pip3\necho \'export PATH="$PATH:/usr/local/python3/bin"\' >> ~/.bashrc'
    with open('/tmp/ini.sh', 'w') as (fp):
        fp.write(sh)
    put('/tmp/ini.sh', '/tmp/init.sh')
    run('bash /tmp/init.sh')
    print('[base]', env.host, ' --- build [ok]')
    res = run("pip3 list 2>/dev/null | grep x-mroy-1046 | grep -v 'grep' |xargs", quiet=True)
    print('[Build]', env.host, res)
    if not res:
        run(PY3_ENV + 'pip3 install x-mroy-1046 --no-cache-dir 1>/dev/null ')
    res = run("pip3 list 2>/dev/null | grep shadowsocks |grep -v 'grep' | xargs ", quiet=True)
    if not res:
        run('pip3 install shadowsocks --no-cache-dir ', quiet=True)
        print('[shadowsocks]', env.host, '  --- ok')
    if run('hash iptables-restore 1>/dev/null 2>/dev/null && echo 0', quiet=True):
        fi = '\n# Generated by iptables-save v1.4.21 on Sat Apr 28 10:24:41 2018\n*nat\n:PREROUTING ACCEPT [1:40]\n:INPUT ACCEPT [0:0]\n:OUTPUT ACCEPT [1:76]\n:POSTROUTING ACCEPT [1:76]\n:OUTPUT_direct - [0:0]\n:POSTROUTING_ZONES - [0:0]\n:POSTROUTING_ZONES_SOURCE - [0:0]\n:POSTROUTING_direct - [0:0]\n:POST_public - [0:0]\n:POST_public_allow - [0:0]\n:POST_public_deny - [0:0]\n:POST_public_log - [0:0]\n:PREROUTING_ZONES - [0:0]\n:PREROUTING_ZONES_SOURCE - [0:0]\n:PREROUTING_direct - [0:0]\n:PRE_public - [0:0]\n:PRE_public_allow - [0:0]\n:PRE_public_deny - [0:0]\n:PRE_public_log - [0:0]\n-A PREROUTING -j PREROUTING_direct\n-A PREROUTING -j PREROUTING_ZONES_SOURCE\n-A PREROUTING -j PREROUTING_ZONES\n-A OUTPUT -j OUTPUT_direct\n-A POSTROUTING -j POSTROUTING_direct\n-A POSTROUTING -j POSTROUTING_ZONES_SOURCE\n-A POSTROUTING -j POSTROUTING_ZONES\n-A POSTROUTING_ZONES -o eth0 -g POST_public\n-A POSTROUTING_ZONES -g POST_public\n-A POST_public -j POST_public_log\n-A POST_public -j POST_public_deny\n-A POST_public -j POST_public_allow\n-A PREROUTING_ZONES -i eth0 -g PRE_public\n-A PREROUTING_ZONES -g PRE_public\n-A PRE_public -j PRE_public_log\n-A PRE_public -j PRE_public_deny\n-A PRE_public -j PRE_public_allow\nCOMMIT\n# Completed on Sat Apr 28 10:24:41 2018\n# Generated by iptables-save v1.4.21 on Sat Apr 28 10:24:41 2018\n*mangle\n:PREROUTING ACCEPT [254:19298]\n:INPUT ACCEPT [254:19298]\n:FORWARD ACCEPT [0:0]\n:OUTPUT ACCEPT [151:15843]\n:POSTROUTING ACCEPT [151:15843]\n:FORWARD_direct - [0:0]\n:INPUT_direct - [0:0]\n:OUTPUT_direct - [0:0]\n:POSTROUTING_direct - [0:0]\n:PREROUTING_ZONES - [0:0]\n:PREROUTING_ZONES_SOURCE - [0:0]\n:PREROUTING_direct - [0:0]\n:PRE_public - [0:0]\n:PRE_public_allow - [0:0]\n:PRE_public_deny - [0:0]\n:PRE_public_log - [0:0]\n-A PREROUTING -j PREROUTING_direct\n-A PREROUTING -j PREROUTING_ZONES_SOURCE\n-A PREROUTING -j PREROUTING_ZONES\n-A INPUT -j INPUT_direct\n-A FORWARD -j FORWARD_direct\n-A OUTPUT -j OUTPUT_direct\n-A POSTROUTING -j POSTROUTING_direct\n-A PREROUTING_ZONES -i eth0 -g PRE_public\n-A PREROUTING_ZONES -g PRE_public\n-A PRE_public -j PRE_public_log\n-A PRE_public -j PRE_public_deny\n-A PRE_public -j PRE_public_allow\nCOMMIT\n# Completed on Sat Apr 28 10:24:41 2018\n# Generated by iptables-save v1.4.21 on Sat Apr 28 10:24:41 2018\n*security\n:INPUT ACCEPT [253:19258]\n:FORWARD ACCEPT [0:0]\n:OUTPUT ACCEPT [151:15843]\n:FORWARD_direct - [0:0]\n:INPUT_direct - [0:0]\n:OUTPUT_direct - [0:0]\n-A INPUT -j INPUT_direct\n-A FORWARD -j FORWARD_direct\n-A OUTPUT -j OUTPUT_direct\nCOMMIT\n# Completed on Sat Apr 28 10:24:41 2018\n# Generated by iptables-save v1.4.21 on Sat Apr 28 10:24:41 2018\n*raw\n:PREROUTING ACCEPT [254:19298]\n:OUTPUT ACCEPT [151:15843]\n:OUTPUT_direct - [0:0]\n:PREROUTING_ZONES - [0:0]\n:PREROUTING_ZONES_SOURCE - [0:0]\n:PREROUTING_direct - [0:0]\n:PRE_public - [0:0]\n:PRE_public_allow - [0:0]\n:PRE_public_deny - [0:0]\n:PRE_public_log - [0:0]\n-A PREROUTING -j PREROUTING_direct\n-A PREROUTING -j PREROUTING_ZONES_SOURCE\n-A PREROUTING -j PREROUTING_ZONES\n-A OUTPUT -j OUTPUT_direct\n-A PREROUTING_ZONES -i eth0 -g PRE_public\n-A PREROUTING_ZONES -g PRE_public\n-A PRE_public -j PRE_public_log\n-A PRE_public -j PRE_public_deny\n-A PRE_public -j PRE_public_allow\nCOMMIT\n# Completed on Sat Apr 28 10:24:41 2018\n# Generated by iptables-save v1.4.21 on Sat Apr 28 10:24:41 2018\n*filter\n:INPUT ACCEPT [0:0]\n:FORWARD ACCEPT [0:0]\n:OUTPUT ACCEPT [2310:506649]\n:FORWARD_IN_ZONES - [0:0]\n:FORWARD_IN_ZONES_SOURCE - [0:0]\n:FORWARD_OUT_ZONES - [0:0]\n:FORWARD_OUT_ZONES_SOURCE - [0:0]\n:FORWARD_direct - [0:0]\n:FWDI_public - [0:0]\n:FWDI_public_allow - [0:0]\n:FWDI_public_deny - [0:0]\n:FWDI_public_log - [0:0]\n:FWDO_public - [0:0]\n:FWDO_public_allow - [0:0]\n:FWDO_public_deny - [0:0]\n:FWDO_public_log - [0:0]\n:INPUT_ZONES - [0:0]\n:INPUT_ZONES_SOURCE - [0:0]\n:INPUT_direct - [0:0]\n:IN_public - [0:0]\n:IN_public_allow - [0:0]\n:IN_public_deny - [0:0]\n:IN_public_log - [0:0]\n:OUTPUT_direct - [0:0]\n-A INPUT -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT\n-A INPUT -i lo -j ACCEPT\n-A INPUT -j INPUT_direct\n-A INPUT -j INPUT_ZONES_SOURCE\n-A INPUT -j INPUT_ZONES\n-A INPUT -m conntrack --ctstate INVALID -j DROP\n-A INPUT -j REJECT --reject-with icmp-host-prohibited\n-A FORWARD -m conntrack --ctstate RELATED,ESTABLISHED -j ACCEPT\n-A FORWARD -i lo -j ACCEPT\n-A FORWARD -j FORWARD_direct\n-A FORWARD -j FORWARD_IN_ZONES_SOURCE\n-A FORWARD -j FORWARD_IN_ZONES\n-A FORWARD -j FORWARD_OUT_ZONES_SOURCE\n-A FORWARD -j FORWARD_OUT_ZONES\n-A FORWARD -m conntrack --ctstate INVALID -j DROP\n-A FORWARD -j REJECT --reject-with icmp-host-prohibited\n-A OUTPUT -j OUTPUT_direct\n-A FORWARD_IN_ZONES -i eth0 -g FWDI_public\n-A FORWARD_IN_ZONES -g FWDI_public\n-A FORWARD_OUT_ZONES -o eth0 -g FWDO_public\n-A FORWARD_OUT_ZONES -g FWDO_public\n-A FWDI_public -j FWDI_public_log\n-A FWDI_public -j FWDI_public_deny\n-A FWDI_public -j FWDI_public_allow\n-A FWDI_public -p icmp -j ACCEPT\n-A FWDO_public -j FWDO_public_log\n-A FWDO_public -j FWDO_public_deny\n-A FWDO_public -j FWDO_public_allow\n-A INPUT_ZONES -i eth0 -g IN_public\n-A INPUT_ZONES -g IN_public\n-A IN_public -j IN_public_log\n-A IN_public -j IN_public_deny\n-A IN_public -j IN_public_allow\n-A IN_public -p icmp -j ACCEPT\n-A IN_public_allow -p tcp -m tcp --dport 22 -m conntrack --ctstate NEW -j ACCEPT\n-A IN_public_allow -p tcp -m tcp --dport 13001:13011 -j ACCEPT\n-A IN_public_allow -p udp -m udp --dport 13001:13011 -j ACCEPT\n-A IN_public_allow -p tcp -m tcp --dport 60000:61000 -j ACCEPT\n-A IN_public_allow -p udp -m udp --dport 60000:61000 -j ACCEPT\nCOMMIT\n# Completed on Sat Apr 28 10:24:41 2018\n'
        with open('/tmp/fi', 'w') as (fp):
            fp.write(fi)
        put('/tmp/fi', '/tmp/fi')
        run('hash iptables-restore && iptables-restore < /tmp/fi')


def Generate_Qr(dirs, host):
    if not os.path.exists(dirs):
        return
    code = 'ss://' + b64encode('aes-256-cfb:thefoolish2@{host}:13002'.format(host=host).encode('utf8')).decode('utf8')
    cmd = 'echo "' + code + '" | qr >  ' + dirs + '/' + host.strip() + '.png'
    print(cmd)
    os.popen(cmd)


@parallel
def Startup(arg):
    if arg == 'start':
        run(PY3_ENV + 'x-relay start')
        run(PY3_ENV + 'x-bak start')
    else:
        if arg == 'stop':
            run(PY3_ENV + 'x-relay stop')
            run(PY3_ENV + 'x-bak stop')
        elif arg == 'restart':
            run(PY3_ENV + 'x-relay stop && x-relay start')
            run(PY3_ENV + 'x-bak stop && x-bak start')


@parallel
def sync(target, files):
    if not exists(target):
        print('not found ', target, 'in serer')
        return
    for file in files:
        put(file, os.path.join(target, os.path.basename(file)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add-host', default=False, action='store_true', help='add a host to db')
    parser.add_argument('-s', '--search', default=None, help="search local's db ")
    parser.add_argument('-d', '--delete', default=False, action='store_true', help='if -s xxx -d will delete content')
    parser.add_argument('-I', '--init-env', default=False, action='store_true', help='if true, will exchange_ssh_key and check then build some base env')
    parser.add_argument('-e', '--execute', nargs='*', default=None, help='run some command in server')
    parser.add_argument('-S', '--startup', default=None, help='start | restart | stop')
    parser.add_argument('-U', '--update', default=False, action='store_true', help='update x-mroy-1046 remote work with -s xxx or update all')
    parser.add_argument('--shadowsocks', default=False, action='store_true', help='if set, will deploy shadowsocks')
    parser.add_argument('--export-qr', default=None, type=str, help='export servers to qr img ')
    parser.add_argument('-D', '--download', default=None, type=str, help='download from remote server')
    parser.add_argument('--sync', nargs='+', default=None, help='sync file to remote server : --sync local_file1 local_file2 remote_dir')
    parser.add_argument('--ifup', default=False, action='store_true', help=' check if all hosts up')
    parser.add_argument('-P', '--path', default=None, help='set file path, use for other option like : -U ')
    parser.add_argument('--sync-ssh', default=False, action='store_true', help='if true will sync ssh_pub_key . you can use -s to select part of hosts')
    parser.add_argument('--log', default=None, help=' [info / error / debug / warrn] ')
    args = parser.parse_args()
    if args.log:
        if not os.path.exists(os.getenv('HOME') + '/.config/seed'):
            os.mkdir(os.getenv('HOME') + '/.config/seed')
        with open(os.getenv('HOME') + '/.config/seed/log_config', 'w') as (fp):
            fp.write(args.log.upper())
    if args.add_host:
        host = prompt('host=', default=None)
        if not host:
            print('must be a valid host')
            sys.exit(0)
        port = prompt('port=', default='22')
        user = prompt('user=', default='root')
        add_host(host, port=port, user=user)
        sys.exit(0)
    if args.ifup:
        tester = Test()
        tester.check_hosts()
    if args.search:
        hs = []
        for host in hosts_db.query(Host):
            if args.search in host.host:
                host.display()
                hs.append(host)

        if args.execute:
            [h.patch() for h in hs]
            execute(ex, ' '.join(args.execute))
            sys.exit(0)
        if args.sync:
            if len(args.sync) > 1:
                [h.patch() for h in hs]
                target = args.sync.pop()
                files = args.sync
                execute(sync, target, files)
                sys.exit(0)
        if args.download:
            [h.patch() for h in hs]
            execute(download, args.download)
            sys.exit(0)
        if args.delete:
            for h in hs:
                hosts_db.delete(h)

        else:
            if args.startup:
                for h in hs:
                    h.patch()

                execute(Startup, args.startup)
            else:
                if args.update:
                    [h.patch() for h in hs]
                    if args.path:
                        if os.path.exists(args.path):
                            print('Deal local file : ', args.path)
                            with zipfile.ZipFile('/tmp/install.zip', 'w') as (zip):
                                for root, dirs, files in os.walk(args.path):
                                    for file in files:
                                        f = os.path.join(root, file)
                                        zip.write(f)

                            print('[pre deal] ')
                    execute(Update, file='/tmp/install.zip')
                else:
                    if args.shadowsocks:
                        for h in hs:
                            h.patch()

                        execute(shadowsocks_start)
                        execute(shadowsocks_pids)
                    else:
                        if args.sync_ssh:
                            [h.patch() for h in hs]
                            exchange_ssh_key()
                            sys.exit(0)
                        else:
                            if args.init_env:
                                [h.patch() for h in hs]
                                execute(initenv)
                                exchange_ssh_key()
                                sys.exit(0)
                            else:
                                if args.log:
                                    [h.patch() for h in hs]
                                    execute(change_log, args.log)
        sys.exit(0)
    if args.update:
        [h.patch() for h in hosts_db.query(Host)]
        if args.path:
            if os.path.exists(args.path):
                print('Deal local file : ', args.path)
                with zipfile.ZipFile('/tmp/install.zip', 'w') as (zip):
                    for root, dirs, files in os.walk(args.path):
                        for file in files:
                            f = os.path.join(root, file)
                            zip.write(f)

                print('[pre deal] ')
        execute(Update, file='/tmp/install.zip')
        sys.exit(0)
    if args.export_qr:
        ips = [h.host for h in hosts_db.query(Host)]
        for ip in ips:
            Generate_Qr(args.export_qr, ip)

    if args.sync_ssh:
        [h.patch() for h in hosts_db.query(Host)]
        exchange_ssh_key()
        sys.exit(0)
    if args.init_env:
        [h.patch() for h in hosts_db.query(Host)]
        execute(initenv)
        exchange_ssh_key()
        sys.exit(0)
    if args.startup:
        w = prompt(('startup op: {} all?[y/n]'.format(args.startup)), default='n')
        if w != 'y':
            return
        [h.patch() for h in hosts_db.query(Host)]
        execute(Startup, args.startup)
    if args.shadowsocks:
        [h.patch() for h in hosts_db.query(Host)]
        execute(shadowsocks)
    if args.execute:
        [h.patch() for h in hosts_db.query(Host)]
        execute(ex, ' '.join(args.execute))