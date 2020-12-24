# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/community/participation/models/node_rating_count.py
# Compiled at: 2013-09-08 06:03:46
from django.db import models
from nodeshot.core.nodes.models import Node

class NodeRatingCount(models.Model):
    """
    Node Rating Count
    Keep track of participation counts of nodes.
    """
    node = models.OneToOneField(Node)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    rating_count = models.IntegerField(default=0)
    rating_avg = models.FloatField(default=0.0)
    comment_count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.node.name

    class Meta:
        app_label = 'participation'
        db_table = 'participation_node_counts'