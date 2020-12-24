# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/toughcli/service/wlan.py
# Compiled at: 2016-04-11 21:00:30
import os, sys, click, shutil, platform
from toughcli.settings import *
docker_compose_fmt = ('redis:\n    image: "index.alauda.cn/tutum/redis"\n    expose:\n        - "6379"\n    environment:\n        - REDIS_MAXMEMORY=512mb\n        - REDIS_PASS=wlanredis\n    restart: always \nwlanpd:\n    command: pypy /opt/toughwlan/wlanctl portald\n    image: "index.alauda.cn/toughstruct/toughwlan"\n    ports:\n        - "{portal_listen_port}:50100/udp"\n    links:\n        - redis:redis\n    environment:\n        - REDIS_URL=redis\n        - REDIS_PORT=6379\n        - REDIS_PWD=wlanredis\n        - DB_TYPE=mysql\n        - DB_URL=mysql://{mysql_user}:{mysql_pwd}@{mysql_host}:{mysql_port}/{mysql_db}?charset=utf8\n    restart: always\n    volumes:\n        - {rundir}/{instance}:/var/toughwlan\nwlan:\n    command: pypy /opt/toughwlan/wlanctl httpd\n    image: "index.alauda.cn/toughstruct/toughwlan"\n    privileged: true\n    expose:\n        - "1818"\n    links:\n        - redis:redis\n    environment:\n        - REDIS_URL=redis\n        - REDIS_PORT=6379\n        - REDIS_PWD=wlanredis\n        - EXCLUDE_PORTS=50100\n        - DB_TYPE=mysql\n        - DB_URL=mysql://{mysql_user}:{mysql_pwd}@{mysql_host}:{mysql_port}/{mysql_db}?charset=utf8\n    restart: always\n    ulimits:\n        nproc: 65535\n        nofile:\n          soft: 20000\n          hard: 40000    \n    volumes:\n        - {rundir}/{instance}:/var/toughwlan\nhaproxy:\n    image: "index.alauda.cn/tutum/haproxy"\n    privileged: true\n    ports:\n        - "{web_port}:80"\n    links:\n        - wlan:wlan\n    restart: always\n    environment:\n        - MAXCONN=40000\n    ulimits:\n        nproc: 65535\n        nofile:\n          soft: 20000\n          hard: 40000    \n').format
docker_compose_fmt2 = ('redis:\n    image: "index.alauda.cn/tutum/redis"\n    expose:\n        - "6379"\n    environment:\n        - REDIS_MAXMEMORY=256mb\n        - REDIS_PASS=wlanredis\n    restart: always         \nwlan:\n    container_name: wlan_{instance}\n    command: pypy /opt/toughwlan/wlanctl standalone\n    image: "index.alauda.cn/toughstruct/toughwlan"\n    privileged: true\n    ports:\n        - "{web_port}:1818"\n        - "{portal_listen_port}:50100"\n    links:\n        - redis:redis\n    environment:\n        - REDIS_URL=redis\n        - REDIS_PORT=6379\n        - REDIS_PWD=wlanredis\n    restart: always  \n    volumes:\n        - {rundir}/{instance}:/var/toughwlan\n').format

def docker_install(rundir, instance, work_num):
    yaml_cfg = docker_compose_fmt
    params_cfg = dict(rundir=rundir, instance=instance, portal_listen_port=click.prompt('Please enter portal listen port', default='50100'), web_port=click.prompt('Please enter web port', default='1818'))
    dbtype = click.prompt('database type [sqlite,mysql]', default='sqlite', type=click.Choice(['sqlite', 'mysql']))
    if dbtype == 'sqlite':
        yaml_cfg = docker_compose_fmt2
    else:
        params_cfg.update(mysql_port=click.prompt('Please enter mysql port', default='3306'), mysql_host=click.prompt('Please enter mysql host', default='localhost'), mysql_user=click.prompt('Please enter mysql user', default='myuser'), mysql_pwd=click.prompt('Please enter mysql password', default='mypwd'), mysql_db=click.prompt('Please enter mysql database', default='mydb'))
    target_dir = ('{0}/{1}').format(rundir, instance)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    click.echo(click.style('\nToughwlan config:\n', fg='cyan'))
    for k, v in params_cfg.iteritems():
        click.echo(click.style(('{0}: {1}').format(k, v), fg='green'))

    click.echo(click.style('\nToughwlan docker-compose.yml:\n', fg='cyan'))
    with open(('{0}/docker-compose.yml').format(target_dir), 'wb') as (dcfile):
        yml_content = yaml_cfg(**params_cfg)
        dcfile.write(yml_content)
        click.echo(click.style(yml_content, fg='green'))
    os.system(('cd {0} && docker-compose up -d').format(target_dir))
    os.system(('cd {0} && docker-compose ps').format(target_dir))
    if dbtype == 'mysql':
        docker_scale(rundir, instance, work_num)


def docker_op(rundir, instance, op):
    target_dir = ('{0}/{1}').format(rundir, instance)
    if not os.path.exists(target_dir):
        click.echo(click.style(('instance {0} not exist').format(instance), fg='red'))
    if op in DOCKER_OPS:
        os.system(('cd {0} && docker-compose {1}').format(target_dir, op))
        if op == 'rm' and click.confirm(('Do you want to remove toughwlan data ({0})?').format(target_dir)):
            shutil.rmtree(target_dir)
    elif op == 'upgrade':
        os.system(('cd {0} && docker-compose pull && docker-compose kill &&             docker-compose rm && docker-compose up -d && docker-compose ps').format(target_dir))
    else:
        click.echo(click.style(('unsupported operation {0}').format(op), fg='red'))


def docker_scale(rundir, instance, num):
    target_dir = ('{0}/{1}').format(rundir, instance)
    os.system(('cd {0} && docker-compose scale wlan={1}').format(target_dir, num))
    os.system(('cd {0} && docker-compose kill haproxy').format(target_dir))
    os.system(('cd {0} && docker-compose rm haproxy').format(target_dir))
    os.system(('cd {0} && docker-compose up -d haproxy').format(target_dir))


done_str = "\n\n----------------------------------------------------------------------------------------------\n- Toughradius has been installed on  /opt/toughwlan, please edit /etc/toughwlan.json\n- You may need to modify the database cofiguration options\n- Please execute cd /opt/toughwlan && make initdb' to initialize the database, \n  and do not forget to back up data\n- If you want to start radius server, please excute 'service toughwlan start'\n- If you want to stop radius server, please excute 'service toughwlan stop'\n- If you want to check its status, please excute 'service toughwlan status'\n- All data and all log  are on /var/toughwlan:\n- Sqlite data: /var/toughwlan/toughwlan.sqlite3\n- Toughwlan backup dir: /var/toughwlan/data \n- Toughwlan console log: /var/toughwlan/wlan-httpd.log\n- For example,  the last 100-line log : tail -n 100 /var/toughwlan/wlan-httpd.log\n----------------------------------------------------------------------------------------------\n\n"

def native_initdb():
    os.system('python /opt/toughwlan/wlanctl initdb -f -c /etc/toughwlan.json')


def native_upgrade(release):
    os.system('cd /opt/toughwlan && git pull --rebase --stat origin release-%s' % release)


def native_install(release, gitrepo):
    _gitrepo = 'https://github.com/talkincode/toughwlan.git'
    if gitrepo and gitrepo not in 'official':
        _gitrepo = gitrepo
    if os.path.exists('/opt/toughwlan'):
        native_upgrade(release)
    else:
        os.system('cd /opt && git clone -b release-%s %s /opt/toughwlan' % (release, _gitrepo))
    _linux = platform.dist()[0]
    if _linux == 'centos':
        os.system('cd /opt/toughwlan && make all')
        click.echo(click.style(done_str, fg='green'))
    else:
        click.echo(click.style('setup not support', fg='green'))