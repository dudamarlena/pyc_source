# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/toughcli/service/radius.py
# Compiled at: 2016-04-11 21:15:13
import os, sys, click, shutil, platform
from toughcli.settings import *
docker_compose_fmt = ('radius:\n    container_name: radius_{instance}\n    image: "index.alauda.cn/toughstruct/toughradius:{release}"\n    net: "host"\n    environment:\n        - DB_TYPE=mysql\n        - DB_URL=mysql://{mysql_user}:{mysql_pwd}@{mysql_host}:{mysql_port}/{mysql_db}?charset=utf8\n    restart: always\n    volumes:\n        - {rundir}/{instance}:/var/toughradius\n').format
docker_compose_fmt2 = ('radius:\n    container_name: radius_{instance}\n    image: "index.alauda.cn/toughstruct/toughradius:{release}"\n    net: "host"\n    restart: always\n    volumes:\n        - {rundir}/{instance}:/var/toughradius\n').format

def get_docker_compose_fmt(dbtype='sqlite'):
    if dbtype == 'mysql':
        return docker_compose_fmt
    else:
        return docker_compose_fmt2


def docker_install(rundir, instance, work_num, release):
    params_cfg = {}
    dbtype = click.prompt('database type [sqlite,mysql]', default='sqlite', type=click.Choice(['sqlite', 'mysql']))
    yaml_cfg = get_docker_compose_fmt(dbtype)
    if dbtype == 'mysql':
        params_cfg.update(mysql_port=click.prompt('Please enter mysql port', default='3306'), mysql_host=click.prompt('Please enter mysql host', default='localhost'), mysql_user=click.prompt('Please enter mysql user', default='myuser'), mysql_pwd=click.prompt('Please enter mysql password', default='mypwd'), mysql_db=click.prompt('Please enter mysql database', default='mydb'))
    target_dir = ('{0}/{1}').format(rundir, instance)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    params = dict(rundir=rundir, instance=instance, worker_num=work_num, release=release)
    params_cfg.update(params)
    click.echo(click.style('\nRadius config:\n', fg='cyan'))
    for k, v in params_cfg.iteritems():
        click.echo(click.style(('{0}: {1}').format(k, v), fg='green'))

    click.echo(click.style('\nRadius docker-compose.yml:\n', fg='cyan'))
    with open(('{0}/docker-compose.yml').format(target_dir), 'wb') as (dcfile):
        yml_content = yaml_cfg(**params_cfg)
        dcfile.write(yml_content)
        click.echo(click.style(yml_content, fg='green'))
    os.system(('cd {0} && docker-compose pull').format(target_dir))
    os.system(('cd {0} && docker-compose up -d').format(target_dir))
    os.system(('cd {0} && docker-compose ps').format(target_dir))


def docker_op(rundir, instance, op):
    target_dir = ('{0}/{1}').format(rundir, instance)
    if not os.path.exists(target_dir):
        click.echo(click.style(('instance {0} not exist').format(instance), fg='red'))
    if op in DOCKER_OPS:
        os.system(('cd {0} && docker-compose {1}').format(target_dir, op))
        if op == 'rm' and click.confirm(('Do you want to remove radius data ({0})?').format(target_dir)):
            shutil.rmtree(target_dir)
    elif op == 'upgrade':
        os.system(('cd {0} && docker-compose pull && docker-compose kill &&             docker-compose rm && docker-compose up -d && docker-compose ps').format(target_dir))
    else:
        click.echo(click.style(('unsupported operation {0}').format(op), fg='red'))


done_str = "\n\n----------------------------------------------------------------------------------------------\n- Toughradius has been installed on  /opt/toughradius, please edit /etc/toughradius.json\n- You may need to modify the database cofiguration options\n- Please execute cd /opt/toughradius && make initdb' to initialize the database, \n  and do not forget to back up data\n- If you want to start radius server, please excute 'service toughradius start'\n- If you want to stop radius server, please excute 'service toughradius stop'\n- If you want to check its status, please excute 'service toughradius status'\n- All data and all log  are on /var/toughradius:\n- Sqlite data: /var/toughradius/toughradius.sqlite3\n- Toughradius backup dir: /var/toughradius/data \n- Toughradius admin console log: /var/toughradius/radius-manage.log \n- Toughradius radius console log: /var/toughradius/radius-worker.log\n- For example,  the last 100-line log : tail -n 100 /var/toughradius/radius-worker.log\n----------------------------------------------------------------------------------------------\n\n"

def native_initdb():
    os.system('python /opt/toughradius/radiusctl initdb -f -c /etc/toughradius.json')


def native_upgrade(release):
    os.system('cd /opt/toughradius && git pull --rebase --stat origin release-%s' % release)


def native_install(release, gitrepo):
    _gitrepo = 'https://github.com/talkincode/ToughRADIUS.git'
    if gitrepo and gitrepo not in 'official':
        _gitrepo = gitrepo
    if os.path.exists('/opt/toughradius'):
        native_upgrade(release)
    else:
        os.system('cd /opt && git clone -b release-%s %s /opt/toughradius' % (release, _gitrepo))
    _linux = platform.dist()[0]
    if _linux == 'centos':
        os.system('cd /opt/toughradius && make all')
        if click.confirm('Do you want to init database?'):
            os.system('cd /opt/toughradius && make initdb')
        click.echo(click.style(done_str, fg='green'))
    else:
        click.echo(click.style('setup not support', fg='green'))