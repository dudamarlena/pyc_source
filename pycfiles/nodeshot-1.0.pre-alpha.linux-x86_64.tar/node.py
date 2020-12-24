# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/core/nodes/models/node.py
# Compiled at: 2015-03-02 13:37:41
from django.contrib.gis.db import models
from django.contrib.gis.geos.collections import GeometryCollection
from django.contrib.gis.geos import GEOSException
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify
from nodeshot.core.base.models import BaseAccessLevel
from nodeshot.core.base.managers import HStoreGeoAccessLevelPublishedManager as NodeManager
from django_hstore.fields import DictionaryField
from ..settings import settings, PUBLISHED_DEFAULT, HSTORE_SCHEMA
from ..signals import node_status_changed
from .status import Status

class Node(BaseAccessLevel):
    """
    Nodes are generic geo-referenced records
    Can be assigned to 'Layers' if nodeshot.core.layers is installed
    Can belong to 'Users'
    """
    name = models.CharField(_('name'), max_length=75, unique=True)
    slug = models.SlugField(max_length=75, db_index=True, unique=True, blank=True)
    status = models.ForeignKey(Status, blank=True, null=True)
    is_published = models.BooleanField(default=PUBLISHED_DEFAULT)
    if 'nodeshot.core.layers' in settings.INSTALLED_APPS:
        layer = models.ForeignKey('layers.Layer')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True)
    geometry = models.GeometryField(_('geometry'), help_text=_('geometry of the node (point, polygon, line)'))
    elev = models.FloatField(_('elevation'), blank=True, null=True)
    address = models.CharField(_('address'), max_length=150, blank=True, null=True)
    description = models.TextField(_('description'), max_length=255, blank=True, null=True)
    notes = models.TextField(_('notes'), blank=True, null=True, help_text=_('for internal use only'))
    data = DictionaryField(_('extra data'), null=True, blank=True, editable=False, schema=HSTORE_SCHEMA)
    objects = NodeManager()
    _current_status = None
    _additional_validation = []

    class Meta:
        db_table = 'nodes_node'
        app_label = 'nodes'

    def __unicode__(self):
        return '%s' % self.name

    def __init__(self, *args, **kwargs):
        """ Fill __current_status """
        super(Node, self).__init__(*args, **kwargs)
        if self.pk:
            self._current_status = self.status_id

    def _autofill_slug(self):
        slugified_name = slugify(self.name)
        if not self.slug or self.slug != slugified_name:
            self.slug = slugified_name

    def clean(self, *args, **kwargs):
        """ call extensible validation """
        self._autofill_slug()
        self.extensible_validation()

    def save(self, *args, **kwargs):
        """
        Custom save method does the following things:
            * converts geometry collections of just 1 item to that item (eg: a collection of 1 Point becomes a Point)
            * intercepts changes to status and fires node_status_changed signal
            * set default status
        """
        if isinstance(self.geometry, GeometryCollection) and 0 < len(self.geometry) < 2:
            self.geometry = self.geometry[0]
        if not self.status and not self.status_id:
            try:
                self.status = Status.objects.filter(is_default=True)[0]
            except IndexError:
                pass

        super(Node, self).save(*args, **kwargs)
        if self.status and self._current_status and self.status.id != self._current_status or self.status_id and self._current_status and self.status_id != self._current_status:
            node_status_changed.send(sender=self.__class__, instance=self, old_status=Status.objects.get(pk=self._current_status), new_status=self.status)
        self._current_status = self.status_id

    def extensible_validation(self):
        """
        Execute additional validation that might be defined elsewhere in the code.
        Additional validation is introduced through the class method Node.add_validation_method()
        """
        for validation_method in self._additional_validation:
            getattr(self, validation_method)()

    @classmethod
    def add_validation_method(class_, method):
        """
        Extend validation of Node by adding a function to the _additional_validation list.
        The additional validation function will be called by the clean method

        :method function: function to be added to _additional_validation
        """
        method_name = method.func_name
        class_._additional_validation.append(method_name)
        setattr(class_, method_name, method)

    @property
    def owner(self):
        return self.user

    @property
    def point(self):
        """ returns location of node. If node geometry is not a point a center  point will be returned """
        if not self.geometry:
            raise ValueError('geometry attribute must be set before trying to get point property')
        if self.geometry.geom_type == 'Point':
            return self.geometry
        try:
            return self.geometry.point_on_surface
        except GEOSException:
            return self.geometry.centroid

    if 'grappelli' in settings.INSTALLED_APPS:

        @staticmethod
        def autocomplete_search_fields():
            return ('name__icontains', 'slug__icontains', 'address__icontains')