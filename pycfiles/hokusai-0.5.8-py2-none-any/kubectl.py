# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: hokusai/services/kubectl.py
# Compiled at: 2018-08-08 18:48:16
import json, yaml
from hokusai.lib.common import shout

class Kubectl(object):

    def __init__(self, context, namespace=None):
        self.context = context
        self.namespace = namespace

    def command(self, cmd):
        if self.namespace is None:
            return 'kubectl --context %s %s' % (self.context, cmd)
        else:
            return 'kubectl --context %s --namespace %s %s' % (self.context, self.namespace, cmd)

    def get_object(self, obj):
        cmd = self.command('get %s -o json' % obj)
        try:
            return json.loads(shout(cmd))
        except ValueError:
            return

        return

    def get_objects(self, obj, selector=None):
        if selector is not None:
            cmd = self.command('get %s --selector %s -o json' % (obj, selector))
        else:
            cmd = self.command('get %s -o json' % obj)
        try:
            return json.loads(shout(cmd))['items']
        except ValueError:
            return []

        return

    def contexts(self):
        return [ context['name'] for context in yaml.load(shout('kubectl config view'))['contexts'] ]