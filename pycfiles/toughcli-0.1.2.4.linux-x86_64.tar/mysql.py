# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/toughcli/service/mysql.py
# Compiled at: 2016-04-11 21:00:30
import os, sys, click, shutil
from toughcli.settings import *
docker_compose_fmt = ('dbmysql:\n    container_name: mysql_{instance}\n    image: "index.alauda.cn/toughstruct/mysql"\n    privileged: true\n    net: "host"\n    environment:\n        - SERVERID={serverid}\n        - AI_INCREMENT={ai_increment}\n        - AI_OFFSET={ai_offset}\n        - MYSQL_MAX_MEM={max_mem}\n        - MYSQL_USER={username}\n        - MYSQL_PASSWORD={password}\n        - MYSQL_DATABASE={dbname}\n        - MYSQL_ROOT_PASSWORD={root_password}\n        - MYSQL_REPL_PASSWORD={mysql_repl_password}\n    restart: always\n    ulimits:\n        nproc: 65535\n        nofile:\n          soft: 20000\n          hard: 40000    \n    volumes:\n        - {rundir}/{instance}/data:/var/lib/mysql\n        - {rundir}/{instance}/backup:/var/backup\n').format

def docker_install(rundir, instance):
    params_cfg = dict(rundir=rundir, instance=instance, username=click.prompt('Please enter mysql user', default='mydb'), password=click.prompt('Please enter mysql password', default='mypwd'), root_password=click.prompt('Please enter mysql root password ', default=''), dbname=click.prompt('Please enter mysql database', default='mydb'), max_mem=click.prompt('Please enter mysql max_mem (512M,1G,4G) ', default='', type=click.Choice(['', '512M', '1G', '4G'])), mysql_repl_password='', serverid='', ai_increment='', ai_offset='')
    if click.confirm('Do you want to use mysql replication?'):
        params_cfg['mysql_repl_password'] = click.prompt('Please enter mysql replication password', default='replication')
        params_cfg['serverid'] = click.prompt('Please enter mysql server id', default='1', type=click.Choice(['1', '2']))
        params_cfg['ai_increment'] = click.prompt('Please enter mysql auto-increment-increment', default='1', type=click.Choice(['1', '2']))
        params_cfg['ai_offset'] = click.prompt('Please enter mysql auto-increment-offset', default='1', type=click.Choice(['1', '2']))
    target_dir = ('{0}/{1}').format(rundir, instance)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    click.echo(click.style('\nMySQL config:\n', fg='cyan'))
    for k, v in params_cfg.iteritems():
        click.echo(click.style(('{0}: {1}').format(k, v), fg='green'))

    click.echo(click.style('\nMySQL docker-compose.yml:\n', fg='cyan'))
    with open(('{0}/docker-compose.yml').format(target_dir), 'wb') as (dcfile):
        yml_content = docker_compose_fmt(**params_cfg)
        dcfile.write(yml_content)
        click.echo(click.style(yml_content, fg='green'))
    os.system(('cd {0} && docker-compose up -d').format(target_dir))
    os.system(('cd {0} && docker-compose ps').format(target_dir))


def docker_op(rundir, instance, op):
    target_dir = ('{0}/{1}').format(rundir, instance)
    if not os.path.exists(target_dir):
        click.echo(click.style(('instance {0} not exist').format(instance), fg='red'))
    if op in DOCKER_OPS:
        os.system(('cd {0} && docker-compose {1}').format(target_dir, op))
        if op in ('rm', 'down') and click.confirm(('Do you want to remove mysql data ({0})?').format(target_dir)):
            shutil.rmtree(target_dir)
    elif op == 'backup':
        os.system(('docker exec -it mysql_{0} sh -c "dbutils backup" ').format(instance))
    elif op == 'makedb':
        os.system(('docker exec -it mysql_{0} sh -c "dbutils makedb" ').format(instance))
    elif op == 'showdbs':
        os.system(('docker exec -it mysql_{0} sh -c "dbutils showdbs" ').format(instance))
    else:
        click.echo(click.style(('unsupported operation {0}').format(op), fg='red'))