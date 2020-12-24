# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/interop/sync/tasks.py
# Compiled at: 2015-03-25 13:06:56
from celery import task
from django.utils.module_loading import import_by_path
from django.core import management

@task
def synchronize_external_layers(*args, **kwargs):
    """
    runs "python manage.py synchronize"
    """
    management.call_command('sync', *args, **kwargs)


@task
def push_changes_to_external_layers(node, external_layer, operation):
    """
    Sync other applications through their APIs by performing updates, adds or deletes.
    This method is designed to be performed asynchronously, avoiding blocking the user
    when he changes data on the local DB.

    :param node: the node which should be updated on the external layer.
    :type node: Node model instance
    :param operation: the operation to perform (add, change, delete)
    :type operation: string
    """
    from nodeshot.core.nodes.models import Node
    if not isinstance(node, basestring):
        node = Node.objects.get(pk=node.pk)
    Synchronizer = import_by_path(external_layer.synchronizer_path)
    instance = Synchronizer(external_layer.layer)
    if hasattr(instance, operation):
        getattr(instance, operation)(node)