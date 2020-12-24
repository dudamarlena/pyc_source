# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pycrunchbase/resource/product.py
# Compiled at: 2017-01-13 23:45:16
import six
from .node import Node
from .utils import parse_date

@six.python_2_unicode_compatible
class Product(Node):
    """Represents a Product on CrunchBase"""
    KNOWN_PROPERTIES = [
     'permalink',
     'api_path',
     'web_path',
     'name',
     'also_known_as',
     'lifecycle_stage',
     'profile_image_url',
     'launched_on',
     'launched_on_trust_code',
     'closed_on',
     'closed_on_trust_code',
     'homepage_url',
     'short_description',
     'description',
     'created_at',
     'updated_at']
    KNOWN_RELATIONSHIPS = [
     'owner',
     'categories',
     'primary_image',
     'competitors',
     'customers',
     'websites',
     'images',
     'videos',
     'news']

    def _coerce_values(self):
        for attr in ['launched_on']:
            if getattr(self, attr, None):
                setattr(self, attr, parse_date(getattr(self, attr)))

        return

    def __str__(self):
        return ('{name} by {owner}').format(name=self.name, owner=self.owner_name)

    def __repr__(self):
        return self.__str__()