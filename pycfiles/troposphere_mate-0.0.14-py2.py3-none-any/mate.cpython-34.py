# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/troposphere_mate-project/troposphere_mate/core/mate.py
# Compiled at: 2019-07-09 11:24:01
# Size of source mod 2**32: 888 bytes
from .sentiel import NOTHING, REQUIRED
from .tagger import tag_property_name_mapper, update_tags_for_resource, update_tags_for_template
import troposphere

def preprocess_init_kwargs(**kwargs):
    processed_kwargs = dict()
    for key, value in kwargs.items():
        if value is not NOTHING:
            processed_kwargs[key] = value
            continue

    return processed_kwargs


class Mixin(object):

    @classmethod
    def get_tags_attr(cls):
        return tag_property_name_mapper.get(cls.resource_type)

    def update_tags(self, tags_dct, overwrite=False):
        update_tags_for_resource(self, tags_dct, overwrite=overwrite)


class Template(troposphere.Template):

    def update_tags(self, tags_dct, overwrite=False):
        update_tags_for_template(self, tags_dct, overwrite=overwrite)

    def pprint(self):
        print(self.to_json(indent=4))