# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Pycharm\PycharmProjects\locationfield\mapbox_location_field\spatial\models.py
# Compiled at: 2019-11-03 11:02:14
# Size of source mod 2**32: 927 bytes
from django.contrib.gis.db.models import PointField
from django.utils.translation import ugettext_lazy as _
from .forms import SpatialLocationField as SpatialLocationFormField

class SpatialLocationField(PointField):
    __doc__ = 'custom model field for storing location in spatial databases'
    description = _('Location field for spatial databases, stores Points.')

    def __init__(self, *args, **kwargs):
        self.map_attrs = kwargs.pop('map_attrs', {})
        (super().__init__)(*args, **kwargs)

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        kwargs['map_attrs'] = self.map_attrs
        return (name, path, args, kwargs)

    def formfield(self, **kwargs):
        defaults = {'form_class': SpatialLocationFormField}
        defaults.update(kwargs)
        defaults.update({'map_attrs': self.map_attrs})
        return (super().formfield)(**defaults)