# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/src/helpers.py
# Compiled at: 2019-12-17 12:12:56
# Size of source mod 2**32: 1280 bytes
import json, shutil, logging
from subprocess import CalledProcessError
from .executors import Executor, cmd_command
logger = logging.getLogger(__name__)

def create_service_from_template(template, **settings) -> bool:
    print(f'New service:\n+ Template "{template}"\n+ Settings:\n  {json.dumps(settings, indent=4)}\n    ')
    return True


def django_service(**pre_settings) -> bool:
    pre_settings.update({'repo': ''})
    return create_service_from_template(*('django', ), **pre_settings)


def flask_service(**pre_settings) -> bool:
    pre_settings.update({'repo': ''})
    return create_service_from_template(*('flask', ), **pre_settings)


def start_super_jopi_infra():
    logger.info('Cleaning previous executions data ...')
    shutil.rmtree('src/playbooks/big-bang/src/')
    playbook = 'src/playbooks/big-bang/sj-infra.yml'
    play_infra_on_local_host = f"ansible-playbook -c=local --inventory 127.0.0.1, --limit 127.0.0.1 {playbook} -i ansible_hosts"
    run_ansible_playbook = Executor(callback=cmd_command, 
     args=[
 play_infra_on_local_host], 
     known_exceptions=[
 CalledProcessError])
    run_ansible_playbook.run()