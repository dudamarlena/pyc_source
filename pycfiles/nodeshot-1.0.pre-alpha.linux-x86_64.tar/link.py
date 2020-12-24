# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/networking/links/models/link.py
# Compiled at: 2015-03-02 10:21:03
from django.contrib.gis.db import models
from django.contrib.gis.geos import LineString
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django_hstore.fields import DictionaryField, ReferencesField
from nodeshot.core.base.managers import HStoreGeoAccessLevelManager as LinkManager
from nodeshot.core.base.models import BaseAccessLevel
from nodeshot.core.base.utils import choicify
from nodeshot.core.nodes.models import Node
from nodeshot.core.layers.models import Layer
from nodeshot.networking.net.models import Interface
from nodeshot.networking.net.models.choices import INTERFACE_TYPES
from .choices import METRIC_TYPES, LINK_STATUS, LINK_TYPES

class Link(BaseAccessLevel):
    """
    Link Model
    Designed for both wireless and wired links
    """
    type = models.SmallIntegerField(_('type'), max_length=10, null=True, blank=True, choices=choicify(LINK_TYPES), default=LINK_TYPES.get('radio'))
    interface_a = models.ForeignKey(Interface, verbose_name=_('from interface'), related_name='link_interface_from', blank=True, null=True, help_text=_('mandatory except for "planned" links (in planned links you might not have any device installed yet)'))
    interface_b = models.ForeignKey(Interface, verbose_name=_('to interface'), related_name='link_interface_to', blank=True, null=True, help_text=_('mandatory except for "planned" links (in planned links you might not have any device installed yet)'))
    node_a = models.ForeignKey(Node, verbose_name=_('from node'), related_name='link_node_from', blank=True, null=True, help_text=_('leave blank (except for planned nodes) as it will be filled in automatically'))
    node_b = models.ForeignKey(Node, verbose_name=_('to node'), related_name='link_node_to', blank=True, null=True, help_text=_('leave blank (except for planned nodes) as it will be filled in automatically'))
    layer = models.ForeignKey(Layer, verbose_name=_('layer'), blank=True, null=True, help_text=_('leave blank - it will be filled in automatically'))
    line = models.LineStringField(blank=True, null=True, help_text=_('leave blank and the line will be drawn automatically'))
    status = models.SmallIntegerField(_('status'), choices=choicify(LINK_STATUS), default=LINK_STATUS.get('planned'))
    first_seen = models.DateTimeField(_('first time seen on'), blank=True, null=True, default=None)
    last_seen = models.DateTimeField(_('last time seen on'), blank=True, null=True, default=None)
    metric_type = models.CharField(_('metric type'), max_length=6, choices=choicify(METRIC_TYPES), blank=True, null=True)
    metric_value = models.FloatField(_('metric value'), blank=True, null=True)
    max_rate = models.IntegerField(_('Maximum BPS'), null=True, default=None, blank=True)
    min_rate = models.IntegerField(_('Minimum BPS'), null=True, default=None, blank=True)
    dbm = models.IntegerField(_('dBm average'), null=True, default=None, blank=True)
    noise = models.IntegerField(_('noise average'), null=True, default=None, blank=True)
    data = DictionaryField(_('extra data'), null=True, blank=True, help_text=_('store extra attributes in JSON string'))
    shortcuts = ReferencesField(null=True, blank=True)
    objects = LinkManager()

    class Meta:
        app_label = 'links'

    def __unicode__(self):
        return _('%s <> %s') % (self.node_a_name, self.node_b_name)

    def clean(self, *args, **kwargs):
        """
        Custom validation
            1. interface_a and interface_b mandatory except for planned links
            2. planned links should have at least node_a and node_b filled in
            3. dbm and noise fields can be filled only for radio links
            4. interface_a and interface_b must differ
            5. interface a and b type must match
        """
        if self.status != LINK_STATUS.get('planned') and (self.interface_a is None or self.interface_b is None):
            raise ValidationError(_('fields "from interface" and "to interface" are mandatory in this case'))
        if self.status == LINK_STATUS.get('planned') and (self.node_a is None or self.node_b is None):
            raise ValidationError(_('fields "from node" and "to node" are mandatory for planned links'))
        if self.type != LINK_TYPES.get('radio') and (self.dbm is not None or self.noise is not None):
            raise ValidationError(_('Only links of type "radio" can contain "dbm" and "noise" information'))
        if self.interface_a_id == self.interface_b_id or self.interface_a == self.interface_b:
            raise ValidationError(_('link cannot have same "from interface" and "to interface"'))
        if self.interface_a and self.interface_b and self.interface_a.type != self.interface_b.type:
            format_tuple = (
             self.interface_a.get_type_display(), self.interface_b.get_type_display())
            raise ValidationError(_('link cannot be between of interfaces of different types:                                    interface a is "%s" while b is "%s"') % format_tuple)
        return

    def save(self, *args, **kwargs):
        """
        Custom save does the following:
            * determine link type if not specified
            * automatically fill 'node_a' and 'node_b' fields if necessary
            * draw line between two nodes
            * fill shortcut properties node_a_name and node_b_name
        """
        if not self.type:
            if self.interface_a.type == INTERFACE_TYPES.get('wireless'):
                self.type = LINK_TYPES.get('radio')
            elif self.interface_a.type == INTERFACE_TYPES.get('ethernet'):
                self.type = LINK_TYPES.get('ethernet')
            else:
                self.type = LINK_TYPES.get('virtual')
        if self.interface_a_id:
            self.interface_a = Interface.objects.get(pk=self.interface_a_id)
        if self.interface_b_id:
            self.interface_b = Interface.objects.get(pk=self.interface_b_id)
        if self.node_a is None and self.interface_a is not None:
            self.node_a = self.interface_a.node
        if self.node_b is None and self.interface_b is not None:
            self.node_b = self.interface_b.node
        if self.layer is None:
            self.layer = self.node_a.layer
        if not self.line:
            self.line = LineString(self.node_a.point, self.node_b.point)
        if self.data is None or self.data.get('node_a_name', None) is None:
            self.data = self.data or {}
            self.data['node_a_name'] = self.node_a.name
            self.data['node_b_name'] = self.node_b.name
        if self.data.get('node_a_slug', None) is None or self.data.get('node_b_slug', None) is None:
            self.data['node_a_slug'] = self.node_a.slug
            self.data['node_b_slug'] = self.node_b.slug
        if self.data.get('interface_a_mac', None) is None or self.data.get('interface_b_mac', None) is None:
            self.data['interface_a_mac'] = self.interface_a.mac
            self.data['interface_b_mac'] = self.interface_b.mac
        if self.data.get('layer_slug') != self.layer.slug:
            self.data['layer_slug'] = self.layer.slug
        super(Link, self).save(*args, **kwargs)
        return

    @property
    def node_a_name(self):
        self.data = self.data or {}
        return self.data.get('node_a_name', None)

    @property
    def node_b_name(self):
        self.data = self.data or {}
        return self.data.get('node_b_name', None)

    @property
    def node_a_slug(self):
        self.data = self.data or {}
        return self.data.get('node_a_slug', None)

    @property
    def node_b_slug(self):
        self.data = self.data or {}
        return self.data.get('node_b_slug', None)

    @property
    def interface_a_mac(self):
        self.data = self.data or {}
        return self.data.get('interface_a_mac', None)

    @property
    def interface_b_mac(self):
        self.data = self.data or {}
        return self.data.get('interface_b_mac', None)

    @property
    def layer_slug(self):
        self.data = self.data or {}
        return self.data.get('layer_slug', None)

    @property
    def quality(self):
        """
        Quality is a number between 1 and 6 that rates the quality of the link.
        The way quality is calculated might be overridden by settings.
        0 means unknown
        """
        if self.metric_value is None:
            return 0
        else:
            return 6