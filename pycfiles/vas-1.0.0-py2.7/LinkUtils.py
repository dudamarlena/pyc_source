# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/util/LinkUtils.py
# Compiled at: 2012-11-01 11:35:36
from vas.VFabricAdministrationServerError import VFabricAdministrationServerError

class LinkUtils:

    @classmethod
    def get_link_hrefs(cls, json, rel):
        return [ link['href'] for link in json['links'] if link['rel'] == rel ]

    @classmethod
    def get_link_href(cls, json, rel):
        hrefs = cls.get_link_hrefs(json, rel)
        if len(hrefs) == 1:
            return hrefs[0]
        raise VFabricAdministrationServerError(("There are {} links for rel '{}'").format(len(hrefs), rel))

    @classmethod
    def get_self_link_href(cls, json):
        return cls.get_link_href(json, 'self')

    def __repr__(self):
        return ('{}()').format(self.__class__.__name__)