# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/interop/sync/models/node_external.py
# Compiled at: 2014-10-01 11:23:05
from django.db import models
from django.utils.translation import ugettext_lazy as _
from nodeshot.core.nodes.models import Node

class NodeExternal(models.Model):
    """
    External Node info, extend 'Node' with additional data
    """
    node = models.OneToOneField(Node, verbose_name=_('node'), parent_link=True, related_name='external')
    external_id = models.CharField(_('external id'), blank=True, max_length=255, help_text=_('ID of this node on the external layer, might be a hash or an integer\n                                               or whatever other format the external application uses to store IDs'))

    class Meta:
        app_label = 'sync'
        db_table = 'nodes_external'
        verbose_name = _('external node')
        verbose_name_plural = _('external node info')

    def __unicode__(self):
        return '%s additional data' % self.node.name


from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save
from ..tasks import push_changes_to_external_layers

@receiver(post_save, sender=Node)
def save_external_nodes(sender, **kwargs):
    """ sync by creating nodes in external layers when needed """
    node = kwargs['instance']
    operation = 'add' if kwargs['created'] is True else 'change'
    if node.layer.is_external is False or not hasattr(node.layer, 'external') or node.layer.external.synchronizer_path is None:
        return False
    push_changes_to_external_layers.delay(node=node, external_layer=node.layer.external, operation=operation)
    return


@receiver(pre_delete, sender=Node)
def delete_external_nodes(sender, **kwargs):
    """ sync by deleting nodes from external layers when needed """
    node = kwargs['instance']
    if node.layer.is_external is False or not hasattr(node.layer, 'external') or node.layer.external.synchronizer_path is None:
        return False
    if hasattr(node, 'external') and node.external.external_id:
        push_changes_to_external_layers.delay(node=node.external.external_id, external_layer=node.layer.external, operation='delete')
    return