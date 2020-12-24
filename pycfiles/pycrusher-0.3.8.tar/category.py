# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pycrunchbase/resource/category.py
# Compiled at: 2017-01-13 23:45:16
import six
from .node import Node

@six.python_2_unicode_compatible
class Category(Node):
    """Represents a Category on CrunchBase"""
    KNOWN_PROPERTIES = [
     'path',
     'name',
     'organizations_in_category',
     'products_in_category',
     'created_at',
     'updated_at']

    def __str__(self):
        return ('{name} {orgs} organizations {prods} products').format(name=self.name, orgs=self.organizations_in_category, prods=self.products_in_category)

    def __repr__(self):
        return self.__str__()