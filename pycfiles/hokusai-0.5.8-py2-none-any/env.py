# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/isacpetruzzi/Code/artsy/hokusai/hokusai/commands/env.py
# Compiled at: 2019-10-09 12:07:43
from hokusai.lib.config import config
from hokusai.lib.command import command
from hokusai.services.configmap import ConfigMap
from hokusai.lib.common import print_green, print_smart
from hokusai.lib.exceptions import HokusaiError

@command()
def delete_env(context, namespace=None):
    configmap = ConfigMap(context, namespace=namespace)
    configmap.destroy()
    print_green('Deleted configmap %s-environment' % config.project_name)


@command()
def get_env(context, environment, namespace=None):
    configmap = ConfigMap(context, namespace=namespace)
    configmap.load()
    for k, v in sorted(configmap.all().items()):
        if not environment or environment and k in environment:
            print_smart('%s=%s' % (k, v))


@command()
def set_env(context, environment, namespace=None):
    configmap = ConfigMap(context, namespace=namespace)
    configmap.load()
    for s in environment:
        if '=' not in s:
            raise HokusaiError("Error: environment variables must be of the form 'KEY=VALUE'")
        split = s.split('=', 1)
        configmap.update(split[0], split[1])

    configmap.save()


@command()
def unset_env(context, environment, namespace=None):
    configmap = ConfigMap(context, namespace=namespace)
    configmap.load()
    for s in environment:
        configmap.delete(s)

    configmap.save()