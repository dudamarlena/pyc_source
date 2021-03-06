# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/paicli/ssh.py
# Compiled at: 2019-07-22 01:15:24
# Size of source mod 2**32: 2874 bytes
"""paicli: A CLI tool for PAI (Platform for AI).

Author: Sotetsu KOYAMADA
"""
from __future__ import print_function
import os, requests, subprocess, codecs, json
from .utils import to_str
from .intereactive import select_choices_interactively

def run_ssh(api, username, jobname, task_name, task_index, config, content, command='', dryrun=False):
    sshkey = _download_sshkey(content)
    path_to_sshkey = os.path.join(config.path_to_configdir, '.tmpkey')
    host = ''
    port = -1
    if len(content['containers']) == 1:
        host = content['containers'][0]['sshIp']
        port = content['containers'][0]['sshPort']
    else:
        choices = []
        ret = api.get_user_username_jobs_jobname(username, jobname)
        tasks = json.loads(ret)['taskRoles']
        for k, v in tasks.items():
            _task_name = k
            if task_name:
                if _task_name != task_name:
                    continue
            tasks_statuses = v['taskStatuses']
            for task_status in tasks_statuses:
                _task_index = task_status['taskIndex']
                if task_index != -1:
                    if task_index != _task_index:
                        continue
                container_id = task_status['containerId']
                container_ip = task_status['containerIp']
                choices.append((
                 to_str('{} [{}] {}'.format(_task_name, _task_index, container_ip)), container_id))

        if not choices:
            raise KeyError
        elif len(choices) == 1:
            _id = choices[0][1]
        else:
            selected = select_choices_interactively([c[0] for c in choices])
            _id = dict(choices)[selected]
        for c in content['containers']:
            if c['id'] == _id:
                host = c['sshIp']
                port = c['sshPort']
                break

    if os.path.exists(path_to_sshkey):
        os.remove(path_to_sshkey)
    else:
        with codecs.open(path_to_sshkey, 'w', 'utf-8') as (f):
            f.writelines(sshkey)
        os.chmod(path_to_sshkey, 384)
        cmd = [
         'ssh', '-i', path_to_sshkey, '-p', port, '-oStrictHostKeyChecking=no', 'root@{}'.format(host)]
        if command:
            cmd.append(command)
        if dryrun:
            print(' '.join(cmd))
        else:
            try:
                subprocess.call(cmd)
            finally:
                if os.path.exists(path_to_sshkey):
                    os.remove(path_to_sshkey)


def _download_sshkey(content):
    res = requests.get(content['keyPair']['privateKeyDirectDownloadLink'])
    sshkey = res.content
    return to_str(sshkey)