# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/isacpetruzzi/Code/artsy/hokusai/hokusai/commands/logs.py
# Compiled at: 2019-10-09 12:07:43
from hokusai.lib.command import command
from hokusai.lib.config import config
from hokusai.lib.common import shout, shout_concurrent
from hokusai.services.kubectl import Kubectl
from hokusai.lib.exceptions import HokusaiError

@command()
def logs(context, timestamps, follow, tail, previous, labels, namespace=None):
    kctl = Kubectl(context, namespace=namespace)
    opts = ''
    if timestamps:
        opts += ' --timestamps'
    if previous:
        opts += ' --previous'
    if follow or config.follow_logs:
        opts += ' --follow'
    if tail or config.tail_logs:
        num_tail = tail if tail else config.tail_logs
        opts += ' --tail=%s' % num_tail
    selectors = ['app=%s' % config.project_name, 'layer=application']
    for l in labels:
        if '=' not in l:
            raise HokusaiError("Error: label selectors of the form 'key=value'")
        selectors.append(l)

    pods = kctl.get_objects('pod', selector=(',').join(selectors))
    pods = filter(lambda pod: pod['status']['phase'] == 'Running', pods)
    containers = []
    for pod in pods:
        for container in pod['spec']['containers']:
            containers.append({'pod': pod['metadata']['name'], 'name': container['name']})

    commands = [ kctl.command('logs %s %s%s' % (container['pod'], container['name'], opts)) for container in containers ]
    shout_concurrent(commands, print_output=True)